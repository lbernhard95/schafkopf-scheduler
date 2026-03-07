import {
  useMultiFileAuthState,
  makeWASocket,
  fetchLatestBaileysVersion,
  DisconnectReason
} from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import { existsSync, mkdirSync, rmSync } from 'node:fs';
import { Logger } from '../core/logger';
import { AuthenticationError, ConnectionError } from './errors';
import type { WASocket } from '@whiskeysockets/baileys';
import { isLambdaEnvironment, downloadAuthFromS3, uploadAuthToS3 } from '../core/s3-auth-manager';

export interface CreateConnectionOptions {
  authDir: string;
  logger: Logger;
  onQR?: (qr: string) => void;
  forceReauth?: boolean;
  downloadFromS3?: boolean;
}

export interface CreateConnectionResult {
  sock: WASocket;
  myJid: string;
}

function resolveAuthDir(authDir: string): string {
  const isLambda = isLambdaEnvironment();
  if (!isLambda) {
    return authDir;
  }

  if (authDir.startsWith('/tmp/')) {
    return authDir;
  }

  return '/tmp/auth';
}

/**
 * Creates a new WhatsApp connection
 */
export async function createConnection(options: CreateConnectionOptions): Promise<CreateConnectionResult> {
    const { authDir, logger, onQR, forceReauth, downloadFromS3 = true } = options;

    const effectiveAuthDir = resolveAuthDir(authDir);

    if (forceReauth) {
      logger.info('Forcing re-authentication, clearing local auth directory...');
      if (existsSync(effectiveAuthDir)) {
        rmSync(effectiveAuthDir, { recursive: true, force: true });
      }
    } else if (downloadFromS3) {
      logger.info(`Downloading auth from S3...`);
      await downloadAuthFromS3(effectiveAuthDir, logger);
    } else {
      logger.info('Skipping auth download from S3, using local auth directory...');
      if (!existsSync(effectiveAuthDir)) {
        mkdirSync(effectiveAuthDir, { recursive: true });
      }
    }

    logger.info('Initializing WhatsApp connection...');

    const { state, saveCreds } = await useMultiFileAuthState(effectiveAuthDir);
    const { version } = await fetchLatestBaileysVersion();

    const sock = makeWASocket({
      version,
      auth: state,
      syncFullHistory: false,
      printQRInTerminal: false, // We handle QR ourselves
      // getMessage: async (key) => {
      //   // This is needed for proper group message handling
      //   return { conversation: '' }
      // },
      logger: {
        level: 'silent',
        fatal: () => {},
        error: () => {},
        warn: () => {},
        info: () => {},
        debug: () => {},
        trace: () => {},
        child: () => ({
          level: 'silent',
          fatal: () => {},
          error: () => {},
          warn: () => {},
          info: () => {},
          debug: () => {},
          trace: () => {},
        } as any),
      } as any,
    });

    // Save credentials on update
    sock.ev.on('creds.update', saveCreds);

    logger.debug('Waiting for connection updates...');
    // Wait for connection to open
    await new Promise<void>((resolve, reject) => {
      let resolved = false;

      sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;
        if (logger) {
          logger.debug(
            `connection.update: connection=${connection || 'n/a'} hasQr=${!!qr} lastDisconnect=${
              lastDisconnect ? JSON.stringify({
                errorMessage: (lastDisconnect.error as any)?.message,
                statusCode: (lastDisconnect.error as any)?.output?.statusCode,
              }) : 'n/a'
            }`
          );
        }

        // Handle QR code for new authentication
        if (qr) {
          logger.info('QR code received, scan with WhatsApp');
          if (onQR) {
            onQR(qr);
          } else {
            // Default: display in terminal
            qrcode.generate(qr, { small: true });
          }
        }

        // Connection opened successfully
        if (connection === 'open' && !resolved) {
          logger.info('Connected to WhatsApp successfully');

          // Fetch all participating groups to ensure group metadata is synced
          try {
            logger.debug('Fetching participating groups...');
            await sock.groupFetchAllParticipating();
            logger.debug('Groups fetched successfully');
          } catch (error) {
            logger.warn(`Failed to fetch groups: ${error instanceof Error ? error.message : String(error)}`);
            // Don't fail connection if group fetch fails
          }

          resolved = true;
          resolve();
        }

        // Connection closed
        if (connection === 'close' && !resolved) {
          resolved = true;
          const reason = (lastDisconnect?.error as any)?.output?.statusCode;

          if (reason === DisconnectReason.loggedOut) {
            reject(new AuthenticationError('Logged out, please re-authenticate'));
          } else {
            reject(new ConnectionError(`Connection closed: ${reason || 'unknown reason'}`));
          }
        }
      });
    });

    const myJid = sock.authState?.creds.me?.id;
    if (!myJid) {
      throw new AuthenticationError('Unable to retrieve user JID');
    }

    return { sock, myJid };
}

/**
 * Gets the current user's JID from the socket
 */
export function getMyJid(sock: WASocket): string {
    const jid = sock.authState?.creds.me?.id;
    if (!jid) {
      throw new AuthenticationError('Unable to retrieve user JID');
    }
    return jid;
}

/**
 * Closes the connection gracefully
 * Waits 2 seconds to allow pending messages to be delivered
 */
export async function closeConnection(
  sock: WASocket,
  logger: Logger,
  options?: { authDir?: string }
): Promise<void> {
    logger.debug('Waiting for messages to be delivered...');
    await new Promise(resolve => setTimeout(resolve, 2000));

    logger.debug('Closing WhatsApp connection...');
    await sock.end();
    logger.debug('Connection closed');

    const effectiveAuthDir = resolveAuthDir(options?.authDir || './tmp/auth');

    logger.info('Uploading updated auth to S3...');
    try {
      await uploadAuthToS3(effectiveAuthDir, logger);
    } catch (error) {
      // Log but don't throw - we're in cleanup phase
      const message = error instanceof Error ? error.message : String(error);
      logger.error(`Failed to upload auth to S3: ${message}`);
    }
}
