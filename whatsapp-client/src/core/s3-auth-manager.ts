import { S3Client, GetObjectCommand, PutObjectCommand } from '@aws-sdk/client-s3';
import { existsSync, unlinkSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { Logger } from './logger';
import { zipDirectory, unzipFile } from './zip-utils';
import { loadMonorepoEnv } from './env-loader';

// Load .env from monorepo root on module import
loadMonorepoEnv();

// Hardcoded S3 bucket name for WhatsApp Scheduler
const S3_BUCKET_NAME = 'whatsapp-scheduler-082113759242';
const AUTH_ZIP_KEY = 'auth.zip';

/**
 * Detects if code is running in AWS Lambda environment
 * @returns true if running on Lambda, false otherwise
 */
export function isLambdaEnvironment(): boolean {
  return !!(
    process.env.AWS_EXECUTION_ENV ||
    process.env.AWS_LAMBDA_FUNCTION_NAME ||
    process.env.LAMBDA_TASK_ROOT
  );
}

/**
 * Downloads auth.zip from S3 and extracts to auth directory
 * @param authDir - Directory to extract auth files to (/tmp/auth on Lambda, ./tmp/auth locally)
 * @param logger - Logger instance for progress messages
 * @throws Error if download or extraction fails
 */
export async function downloadAuthFromS3(authDir: string, logger: Logger): Promise<void> {
  const s3Client = new S3Client({});

  // Use /tmp for Lambda, ./tmp for local
  const isLambda = isLambdaEnvironment();
  const tempZipPath = isLambda ? '/tmp/auth.zip' : './tmp/auth.zip';

  try {
    logger.info(`Downloading auth from S3 bucket: ${S3_BUCKET_NAME}`);

    // Download auth.zip from S3
    const command = new GetObjectCommand({
      Bucket: S3_BUCKET_NAME,
      Key: AUTH_ZIP_KEY,
    });

    const response = await s3Client.send(command);

    if (!response.Body) {
      throw new Error('S3 response body is empty');
    }

    // Ensure temp directory exists (for local dev)
    const tempDir = path.dirname(tempZipPath);
    if (!existsSync(tempDir)) {
      mkdirSync(tempDir, { recursive: true });
    }

    // Convert stream to buffer and write to file
    const bodyBytes = await response.Body.transformToByteArray();
    await Bun.write(tempZipPath, bodyBytes);

    logger.debug(`Auth zip downloaded to ${tempZipPath}`);

    // Extract zip to auth directory
    logger.debug(`Extracting auth to ${authDir}`);
    await unzipFile(tempZipPath, authDir);

    logger.info(`Auth successfully extracted to ${authDir}`);

    // Clean up temp zip file
    if (existsSync(tempZipPath)) {
      unlinkSync(tempZipPath);
    }
  } catch (error) {
    // Clean up temp file on error
    if (existsSync(tempZipPath)) {
      try {
        unlinkSync(tempZipPath);
      } catch {
        // Ignore cleanup errors
      }
    }

    const message = error instanceof Error ? error.message : String(error);
    console.log(`Failed to download auth from S3: ${message}`);
  }
}

/**
 * Zips auth directory and uploads to S3
 * @param authDir - Directory containing auth files to upload
 * @param logger - Logger instance for progress messages
 * @throws Error if zip creation or upload fails
 */
export async function uploadAuthToS3(authDir: string, logger: Logger): Promise<void> {
  const s3Client = new S3Client({});

  // Use /tmp for Lambda, ./tmp for local
  const isLambda = isLambdaEnvironment();
  const tempZipPath = isLambda ? '/tmp/auth-upload.zip' : './tmp/auth-upload.zip';

  try {
    // Verify auth directory exists
    if (!existsSync(authDir)) {
      throw new Error(`Auth directory not found: ${authDir}`);
    }

    logger.info(`Uploading auth to S3 bucket: ${S3_BUCKET_NAME}`);

    // Ensure temp directory exists (for local dev)
    const tempDir = path.dirname(tempZipPath);
    if (!existsSync(tempDir)) {
      mkdirSync(tempDir, { recursive: true });
    }

    // Create zip from auth directory
    logger.debug(`Creating zip archive from ${authDir}`);
    await zipDirectory(authDir, tempZipPath);

    logger.debug(`Reading zip file for upload`);
    const zipBuffer = await Bun.file(tempZipPath).arrayBuffer();

    // Upload to S3
    const command = new PutObjectCommand({
      Bucket: S3_BUCKET_NAME,
      Key: AUTH_ZIP_KEY,
      Body: new Uint8Array(zipBuffer),
      ContentType: 'application/zip',
    });

    await s3Client.send(command);

    logger.info('Auth successfully uploaded to S3');

    // Clean up temp zip file
    if (existsSync(tempZipPath)) {
      unlinkSync(tempZipPath);
    }
  } catch (error) {
    // Clean up temp file on error
    if (existsSync(tempZipPath)) {
      try {
        unlinkSync(tempZipPath);
      } catch {
        // Ignore cleanup errors
      }
    }

    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to upload auth to S3: ${message}`);
  }
}
