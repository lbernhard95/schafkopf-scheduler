# Scripts Directory

This directory contains utility scripts for managing the WhatsApp Scheduler.

## Available Scripts

### `upload-auth-to-s3.ts`

Bootstrap script to upload local WhatsApp authentication credentials to S3 for Lambda deployment.

#### Usage

```bash
bun run upload-auth
```

#### What It Does

1. **Validates** local auth directory exists (`./auth/`)
2. **Creates** zip archive from auth directory
3. **Uploads** `auth.zip` to S3 bucket: `whatsapp-scheduler-082113759242`
4. **Cleans up** temporary files
5. **Displays** next steps for Lambda deployment

#### Prerequisites

- WhatsApp authenticated locally (run `bun run scheduler` first)
- AWS credentials configured (`aws configure`)
- S3 bucket exists: `whatsapp-scheduler-082113759242`

#### Expected Output

```
🚀 WhatsApp Auth Bootstrap Script
==================================================

📁 Checking local auth directory...
✓ Local auth directory found

📦 Creating zip archive from local auth...
✓ Zip archive created: ./auth.zip

☁️  Uploading to S3 bucket: whatsapp-scheduler-082113759242
✓ Successfully uploaded to S3

🧹 Cleaning up temporary files...
✓ Temporary files removed

✅ SUCCESS! Auth uploaded to S3
```

#### Troubleshooting

| Error | Solution |
|-------|----------|
| `Local auth directory not found` | Run `bun run scheduler` to authenticate first |
| `Failed to upload to S3: AccessDenied` | Configure AWS credentials: `aws configure` |
| `Failed to upload to S3: NoSuchBucket` | Create bucket: `aws s3 mb s3://whatsapp-scheduler-082113759242` |

#### Configuration

The script uses hardcoded configuration:

```typescript
const S3_BUCKET_NAME = 'whatsapp-scheduler-082113759242';
const AUTH_ZIP_KEY = 'auth.zip';
const LOCAL_AUTH_DIR = './auth';
```

To use a different S3 bucket, modify `S3_BUCKET_NAME` in the script and update `src/core/s3-auth-manager.ts`.

#### When to Re-run

Re-run this script when:

- WhatsApp credentials expire on Lambda
- You re-authenticate locally with a different account
- Lambda logs show authentication errors
- S3 auth.zip is corrupted or deleted

#### Related Documentation

See [Lambda Deployment Guide](../../docs/LAMBDA_DEPLOYMENT.md) for complete Lambda setup instructions.
