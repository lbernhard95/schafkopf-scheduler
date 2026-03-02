#!/usr/bin/env bun
/**
 * Bootstrap Script: Upload Local Auth to S3
 *
 * This script uploads your local WhatsApp authentication credentials
 * to S3 so they can be used by Lambda functions.
 *
 * Usage: bun run upload-auth
 *
 * Prerequisites:
 * 1. You must have authenticated WhatsApp locally first (./auth/ directory exists)
 * 2. AWS credentials must be configured (via ~/.aws/credentials or environment variables)
 * 3. S3 bucket must exist: whatsapp-scheduler-082113759242
 */

import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { zipDirectory } from '../core/zip-utils';

// Hardcoded configuration
const S3_BUCKET_NAME = 'whatsapp-scheduler-082113759242';
const AUTH_ZIP_KEY = 'auth.zip';
const LOCAL_AUTH_DIR = './auth';
const TEMP_ZIP_PATH = './auth.zip';

/**
 * Main function to upload auth to S3
 */
async function uploadAuthToS3(): Promise<void> {
  console.log('🚀 WhatsApp Auth Bootstrap Script');
  console.log('='.repeat(50));
  console.log();

  // Step 1: Check if local auth directory exists
  console.log('📁 Checking local auth directory...');
  if (!existsSync(LOCAL_AUTH_DIR)) {
    console.error('❌ Error: Local auth directory not found: ' + LOCAL_AUTH_DIR);
    console.error();
    console.error('Please authenticate WhatsApp locally first by running:');
    console.error('  bun run example');
    console.error('or');
    console.error('  bun run scheduler');
    process.exit(1);
  }
  console.log('✓ Local auth directory found');
  console.log();

  // Step 2: Create zip archive
  console.log('📦 Creating zip archive from local auth...');
  try {
    await zipDirectory(LOCAL_AUTH_DIR, TEMP_ZIP_PATH);
    console.log('✓ Zip archive created: ' + TEMP_ZIP_PATH);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error('❌ Failed to create zip archive: ' + message);
    process.exit(1);
  }
  console.log();

  // Step 3: Upload to S3
  console.log(`☁️  Uploading to S3 bucket: ${S3_BUCKET_NAME}`);
  try {
    const s3Client = new S3Client({});
    const zipBuffer = await Bun.file(TEMP_ZIP_PATH).arrayBuffer();

    const command = new PutObjectCommand({
      Bucket: S3_BUCKET_NAME,
      Key: AUTH_ZIP_KEY,
      Body: new Uint8Array(zipBuffer),
      ContentType: 'application/zip',
    });

    await s3Client.send(command);
    console.log('✓ Successfully uploaded to S3');
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error('❌ Failed to upload to S3: ' + message);
    console.error();
    console.error('Common issues:');
    console.error('  1. AWS credentials not configured');
    console.error('     → Run: aws configure');
    console.error('  2. S3 bucket does not exist');
    console.error('     → Create bucket: ' + S3_BUCKET_NAME);
    console.error('  3. Missing S3 permissions');
    console.error('     → Ensure your AWS user/role has s3:PutObject permission');

    // Clean up temp file
    if (existsSync(TEMP_ZIP_PATH)) {
      await Bun.write(TEMP_ZIP_PATH, ''); // Clear file
      await import('node:fs/promises').then(fs => fs.unlink(TEMP_ZIP_PATH));
    }

    process.exit(1);
  }
  console.log();

  // Step 4: Clean up temp file
  console.log('🧹 Cleaning up temporary files...');
  if (existsSync(TEMP_ZIP_PATH)) {
    await import('node:fs/promises').then(fs => fs.unlink(TEMP_ZIP_PATH));
    console.log('✓ Temporary files removed');
  }
  console.log();

  // Step 5: Success message with next steps
  console.log('✅ SUCCESS! Auth uploaded to S3');
}

// Run the script
uploadAuthToS3().catch((error) => {
  console.error('❌ Unexpected error:', error);
  process.exit(1);
});
