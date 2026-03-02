import type { WASocket } from '@whiskeysockets/baileys';
import { Logger } from '../core/logger';
import { createConnection, closeConnection, getMyJid } from './connection';
import { sendText as sendTextMessage, sendPoll as sendPollMessage } from './messages';
import { normalizeJid, ensureValidJid, toJid, fromJid, isGroupJid } from './jid';
import type { WhatsAppClientOptions, PollConfig, ConnectionState } from './types';
import { WhatsAppError } from './errors';

/**
 * Main WhatsApp client class that provides a clean API for sending messages
 */
export class WhatsAppClient {
  private sock: WASocket | null = null;
  private logger: Logger;
  private authDir: string;
  private onQR?: (qr: string) => void;
  private connectionPromise: Promise<void> | null = null;
  private myJid: string | null = null;

  constructor(options: WhatsAppClientOptions = {}) {
    this.authDir = options.authDir || './auth';
    this.onQR = options.onQR;

    // Initialize logger
    const logLevel = options.logLevel || 'info';
    this.logger = new Logger(logLevel);

    // Suppress Baileys logs if not in debug mode
    if (logLevel !== 'debug') {
      Logger.muteBaileysLogs();
    }

    // Auto-connect on instantiation
    this.connectionPromise = this.connect();
  }

  /**
   * Establishes connection to WhatsApp
   * This is called automatically on instantiation
   */
  private async connect(): Promise<void> {
    try {
      this.logger.info('Initializing WhatsApp client...');

      const { sock, myJid } = await createConnection({
        authDir: this.authDir,
        onQR: this.onQR,
        logger: this.logger,
      });

      this.sock = sock;
      this.myJid = myJid;

      this.logger.info(`WhatsApp client connected successfully (${fromJid(myJid)})`);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      this.logger.error(`Failed to connect: ${errorMessage}`);
      throw error;
    }
  }

  /**
   * Ensures the client is connected before performing operations
   */
  private async ensureConnected(): Promise<WASocket> {
    if (this.connectionPromise) {
      await this.connectionPromise;
    }

    if (!this.sock) {
      throw new WhatsAppError('Client is not connected');
    }

    return this.sock;
  }

  /**
   * Gets the client's own JID (phone number)
   * @returns The client's JID
   */
  async getMyJid(): Promise<string> {
    await this.ensureConnected();

    if (!this.myJid) {
      throw new WhatsAppError('Unable to determine own JID');
    }

    return this.myJid;
  }

  /**
   * Gets the client's own phone number
   * @returns The client's phone number (without @s.whatsapp.net)
   */
  async getMyPhoneNumber(): Promise<string> {
    const jid = await this.getMyJid();
    return fromJid(jid);
  }

  /**
   * Sends a text message
   * @param recipient - Phone number (e.g., "1234567890"), individual JID (e.g., "1234567890@s.whatsapp.net"), or group JID (e.g., "GROUP_ID@g.us")
   * @param text - The message text
   * @returns The message ID
   * @throws WhatsAppError if sending fails
   */
  async sendText(recipient: string, text: string): Promise<string> {
    const sock = await this.ensureConnected();

    // Convert to JID and validate
    let jid = recipient.includes('@') ? recipient : toJid(recipient);

    // Normalize JID (remove device ID if present)
    jid = normalizeJid(jid);

    // Validate JID format
    ensureValidJid(jid);

    return await sendTextMessage(sock, jid, text, this.logger);
  }

  /**
   * Sends a poll message
   * @param recipient - Phone number (e.g., "1234567890"), individual JID (e.g., "1234567890@s.whatsapp.net"), or group JID (e.g., "GROUP_ID@g.us")
   * @param question - The poll question
   * @param options - Array of poll options (2-12 options)
   * @param selectableCount - Number of options users can select (default: 1)
   * @returns The message ID
   * @throws WhatsAppError if sending fails
   */
  async sendPoll(
    recipient: string,
    question: string,
    options: string[],
    selectableCount: number = 1
  ): Promise<string> {
    const sock = await this.ensureConnected();

    // Convert to JID and validate
    let jid = recipient.includes('@') ? recipient : toJid(recipient);

    // Normalize JID (remove device ID if present)
    jid = normalizeJid(jid);

    // Validate JID format
    ensureValidJid(jid);

    const pollConfig: PollConfig = {
      name: question,
      values: options,
      selectableCount,
    };

    return await sendPollMessage(sock, jid, pollConfig, this.logger);
  }

  /**
   * Disconnects the client gracefully
   * Waits 2 seconds to allow pending messages to be delivered
   */
  async disconnect(): Promise<void> {
    if (!this.sock) {
      this.logger.warn('Client is already disconnected');
      return;
    }

    this.logger.info('Disconnecting WhatsApp client...');

    try {
      await closeConnection(this.sock, this.logger, { authDir: this.authDir });
      this.sock = null;
      this.myJid = null;
      this.logger.info('WhatsApp client disconnected successfully');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      this.logger.error(`Error during disconnect: ${errorMessage}`);
      throw error;
    }
  }

  /**
   * Utility: Converts a phone number to a JID
   */
  static toJid(phoneNumber: string): string {
    return toJid(phoneNumber);
  }

  /**
   * Utility: Extracts phone number from a JID
   */
  static fromJid(jid: string): string {
    return fromJid(jid);
  }

  /**
   * Utility: Checks if a JID is a group
   */
  static isGroupJid(jid: string): boolean {
    return isGroupJid(jid);
  }
}
