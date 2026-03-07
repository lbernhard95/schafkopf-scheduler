#!/usr/bin/env bun
/**
 * Re-authenticate WhatsApp and Upload Auth to S3
 *
 * Usage: bun run reauth-upload
 *
 * Flow:
 * 1. Clears local auth directory to force QR login
 * 2. Connects and waits for QR scan
 * 3. Uploads the fresh auth state to S3
 */

import { existsSync, rmSync } from 'node:fs';
import { Logger } from '../core/logger';
import { isLambdaEnvironment } from '../core/s3-auth-manager';
import { createConnection, closeConnection } from '../whatsapp/connection';

async function reauthAndUpload(): Promise<void> {
  console.log('🔐 WhatsApp Re-authentication + S3 Upload');
  console.log('='.repeat(50));
  console.log();

  const logger = new Logger('debug');
  const isLambda = isLambdaEnvironment();
  const authDir = isLambda ? '/tmp/auth' : './tmp/auth';

  console.log(`📁 Using auth directory: ${authDir}`);
  if (existsSync(authDir)) {
    console.log('🧹 Clearing existing auth directory to force QR login...');
    rmSync(authDir, { recursive: true, force: true });
    console.log('✓ Local auth cleared');
  }
  console.log();

  console.log('📱 Waiting for QR scan...');
  const maxAttempts = 3;
  let lastError: unknown;
  let connection: { sock: any; myJid: string } | null = null;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      connection = await createConnection({
        authDir,
        logger,
        forceReauth: attempt === 1,
        downloadFromS3: false,
      });
      break;
    } catch (error) {
      lastError = error;
      const message = error instanceof Error ? error.message : String(error);
      if (message.includes('Connection closed: 515')) {
        console.log(`⚠️  Restart required from WhatsApp (attempt ${attempt}/${maxAttempts}). Retrying...`);
        await new Promise(resolve => setTimeout(resolve, 2000));
        continue;
      }
      throw error;
    }
  }

  if (!connection) {
    throw lastError instanceof Error ? lastError : new Error(String(lastError));
  }

  const { sock, myJid } = connection;

  console.log(`✓ Authenticated as: ${myJid}`);
  console.log();

  console.log('☁️  Uploading updated auth to S3...');
  await closeConnection(sock, logger, { authDir });
  console.log('✓ Re-auth complete and uploaded to S3');
}

reauthAndUpload().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error('❌ Re-auth failed:', message);
  process.exit(1);
});
