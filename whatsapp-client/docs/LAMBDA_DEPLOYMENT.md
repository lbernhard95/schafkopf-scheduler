# AWS Lambda Deployment Guide

This guide explains how to deploy the WhatsApp Scheduler with S3-based authentication storage that works both locally and on AWS Lambda.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [IAM Permissions](#iam-permissions)
- [Troubleshooting](#troubleshooting)

---

## Overview

The WhatsApp client **always uses S3** to persist authentication credentials, both locally and on Lambda. This ensures consistent behavior across all environments and eliminates the need for local `./auth/` directory storage.

**Key Features:**
- **S3-first design**: All auth storage goes through S3 (no local-only mode)
- **Environment-aware paths**: Uses `./tmp/auth` locally, `/tmp/auth` on Lambda
- **Automatic .env loading**: Loads AWS credentials from monorepo root `.env` file
- **Bidirectional sync**: Auth downloaded on start, uploaded after execution
- **Fail-fast**: Application fails immediately if auth cannot be downloaded from S3

---

## Architecture

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ Local Development OR Lambda Execution                       │
│                                                             │
│  1. Application starts                                      │
│     ↓                                                       │
│  2. Loads .env from monorepo root (schafkopf-scheduler/.env)│
│     ↓                                                       │
│  3. Detects environment (Lambda: /tmp/auth, Local: ./tmp/auth) │
│     ↓                                                       │
│  4. Downloads auth.zip from S3                              │
│     ↓                                                       │
│  5. Extracts to temp auth directory                         │
│     ↓                                                       │
│  6. Connects to WhatsApp using credentials                  │
│     ↓                                                       │
│  7. Executes scheduler logic (sends poll)                   │
│     ↓                                                       │
│  8. Closes WhatsApp connection                              │
│     ↓                                                       │
│  9. Zips temp auth directory                                │
│     ↓                                                       │
│  10. Uploads auth.zip back to S3                            │
│     ↓                                                       │
│  11. Execution completes                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ S3 Bucket: whatsapp-scheduler-082113759242                  │
│                                                             │
│  └── auth.zip (WhatsApp credentials)                        │
│      - ~3.5MB compressed                                    │
│      - 892 files (creds, keys, state)                       │
│      - Updated after each execution (local or Lambda)       │
└─────────────────────────────────────────────────────────────┘
```

### S3 Storage Structure

- **Bucket**: `whatsapp-scheduler-082113759242` (hardcoded)
- **Object key**: `auth.zip`
- **Format**: Zip archive containing entire auth directory
- **Size**: ~3.5MB compressed
- **Contents**: 892 files including credentials, pre-keys, app state

---

## Prerequisites

### 1. AWS Credentials

Create a `.env` file in the **monorepo root** (`schafkopf-scheduler/.env`):

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=eu-central-1
```

The application automatically loads this file on startup to authenticate with AWS S3.

### 2. Initial WhatsApp Authentication

You must authenticate WhatsApp locally first and upload to S3:

```bash
# Authenticate locally (one-time setup)
bun run scheduler
# Scan QR code with WhatsApp mobile app
# Wait for successful connection and poll sent

# Auth is automatically uploaded to S3 after first run
```

After the first successful run, auth is stored in S3 and all future executions (local or Lambda) will use it.

### 3. AWS Account

- AWS Account with appropriate permissions
- S3 bucket created: `whatsapp-scheduler-082113759242`
- IAM permissions for S3 access (see [IAM Permissions](#iam-permissions))

**Create S3 bucket:**
```bash
aws s3 mb s3://whatsapp-scheduler-082113759242
```

---

## Setup Instructions

### Step 1: Configure AWS Credentials

Create `.env` file in monorepo root (`schafkopf-scheduler/.env`):

```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=eu-central-1
```

### Step 2: Bootstrap S3 (Optional - First Time Only)

If you have existing auth in `./auth/` directory from before the S3-always change, upload it manually:

```bash
bun run upload-auth
```

**Otherwise, skip to Step 3** - the first run of `bun run scheduler` will automatically handle authentication and upload to S3.

### Step 3: Run Scheduler Locally

First execution (if no auth in S3 yet):

```bash
bun run scheduler
```

**Expected flow:**
1. Attempts to download auth from S3
2. If S3 auth doesn't exist, will fail with error - this is expected for first run
3. For first-time setup, use the upload-auth script after authenticating locally OR manually upload your existing `./auth/` to S3

**Subsequent executions:**
1. Downloads auth from S3 to `./tmp/auth`
2. Connects to WhatsApp
3. Sends poll
4. Uploads updated auth back to S3

**Expected output:**
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
==================================================

📋 Next Steps:

1. Deploy your Lambda function
   → Ensure Lambda has IAM permissions:
     - s3:GetObject on arn:aws:s3:::whatsapp-scheduler-082113759242/auth.zip
     - s3:PutObject on arn:aws:s3:::whatsapp-scheduler-082113759242/auth.zip

2. Test Lambda execution
   → Lambda will automatically download auth from S3

3. Monitor CloudWatch Logs for:
   ✓ "Lambda environment detected, downloading auth from S3..."
   ✓ "Connected to WhatsApp successfully"
   ✓ "Uploading updated auth to S3..."
```

**Troubleshooting bootstrap errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Local auth directory not found` | Haven't authenticated locally | Run `bun run scheduler` first |
| `Failed to upload to S3: AccessDenied` | Missing AWS permissions | Run `aws configure` or check IAM policy |
| `Failed to upload to S3: NoSuchBucket` | S3 bucket doesn't exist | Create bucket: `aws s3 mb s3://whatsapp-scheduler-082113759242` |

### Step 2: Package Lambda Function

Create a deployment package with all dependencies:

```bash
# Install production dependencies
bun install --production

# Create deployment package
zip -r lambda-deployment.zip \
  src/ \
  config/ \
  node_modules/ \
  package.json \
  bun.lock \
  tsconfig.json
```

**Note**: The `auth/` directory is **not** included in the deployment package since Lambda downloads it from S3.

### Step 3: Create Lambda Function

#### Option A: AWS Console

1. Go to AWS Lambda Console
2. Click "Create function"
3. Configure:
   - **Name**: `whatsapp-schafkopf-scheduler`
   - **Runtime**: Node.js 20.x
   - **Architecture**: x86_64 or arm64
   - **Handler**: `src/apps/schafkopf-scheduler/index.ts` (if using custom runtime) or bundle with `bun build`
4. Upload `lambda-deployment.zip`
5. Set **Memory**: 512 MB (minimum recommended)
6. Set **Timeout**: 30 seconds
7. Set **Ephemeral storage**: 512 MB (default is sufficient)

#### Option B: AWS CLI

```bash
# Create Lambda function
aws lambda create-function \
  --function-name whatsapp-schafkopf-scheduler \
  --runtime nodejs20.x \
  --role arn:aws:iam::082113759242:role/lambda-whatsapp-scheduler-role \
  --handler index.handler \
  --zip-file fileb://lambda-deployment.zip \
  --timeout 30 \
  --memory-size 512
```

### Step 4: Configure IAM Role

Attach the IAM policy to your Lambda execution role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "WhatsAppAuthS3Access",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::whatsapp-scheduler-082113759242/auth.zip"
    },
    {
      "Sid": "CloudWatchLogs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:082113759242:log-group:/aws/lambda/whatsapp-schafkopf-scheduler:*"
    }
  ]
}
```

**Apply via AWS CLI:**

```bash
# Create IAM policy
aws iam create-policy \
  --policy-name WhatsAppSchedulerLambdaPolicy \
  --policy-document file://iam-policy.json

# Attach to Lambda role
aws iam attach-role-policy \
  --role-name lambda-whatsapp-scheduler-role \
  --policy-arn arn:aws:iam::082113759242:policy/WhatsAppSchedulerLambdaPolicy
```

### Step 5: Test Lambda Function

Invoke Lambda manually to test:

```bash
aws lambda invoke \
  --function-name whatsapp-schafkopf-scheduler \
  --log-type Tail \
  --query 'LogResult' \
  --output text \
  response.json | base64 --decode
```

**Expected CloudWatch Logs:**

```
[INFO] Initializing WhatsApp client...
[INFO] Lambda environment detected, downloading auth from S3...
[INFO] Downloading auth from S3 bucket: whatsapp-scheduler-082113759242
[INFO] Auth successfully extracted to /tmp/auth
[INFO] Initializing WhatsApp connection...
[INFO] Connected to WhatsApp successfully
[INFO] Starting Schafkopf Scheduler...
[INFO] Generated 10 poll options: Mo 09.03, Di 10.03, ...
[INFO] Sending poll to 4917657753775...
[INFO] Poll sent successfully (Message ID: 3EB0983CC915213CC5A495)
[INFO] Disconnecting WhatsApp client...
[INFO] Uploading updated auth to S3...
[INFO] Uploading auth to S3 bucket: whatsapp-scheduler-082113759242
[INFO] Auth successfully uploaded to S3
[INFO] WhatsApp client disconnected successfully
✓ Success! Poll sent (Message ID: 3EB0983CC915213CC5A495)
```

### Step 6: Set Up Scheduled Execution (Optional)

Create an EventBridge rule to run the scheduler periodically:

```bash
# Create CloudWatch Events rule (runs every Monday at 9 AM UTC)
aws events put-rule \
  --name whatsapp-scheduler-weekly \
  --schedule-expression "cron(0 9 ? * MON *)" \
  --state ENABLED

# Add Lambda as target
aws events put-targets \
  --rule whatsapp-scheduler-weekly \
  --targets "Id"="1","Arn"="arn:aws:lambda:eu-central-1:082113759242:function:whatsapp-schafkopf-scheduler"

# Grant EventBridge permission to invoke Lambda
aws lambda add-permission \
  --function-name whatsapp-schafkopf-scheduler \
  --statement-id AllowEventBridgeInvoke \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:eu-central-1:082113759242:rule/whatsapp-scheduler-weekly
```

---

## IAM Permissions

### Minimum Required Permissions

#### Lambda Execution Role

The Lambda function's execution role needs:

1. **S3 Access** (for auth storage)
   ```json
   {
     "Effect": "Allow",
     "Action": ["s3:GetObject", "s3:PutObject"],
     "Resource": "arn:aws:s3:::whatsapp-scheduler-082113759242/auth.zip"
   }
   ```

2. **CloudWatch Logs** (for logging)
   ```json
   {
     "Effect": "Allow",
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Resource": "arn:aws:logs:*:082113759242:log-group:/aws/lambda/*"
   }
   ```

#### Developer/CI/CD Permissions

For uploading auth and deploying Lambda:

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:PutObject",
    "lambda:CreateFunction",
    "lambda:UpdateFunctionCode",
    "lambda:UpdateFunctionConfiguration",
    "iam:PassRole"
  ],
  "Resource": [
    "arn:aws:s3:::whatsapp-scheduler-082113759242/auth.zip",
    "arn:aws:lambda:*:082113759242:function:whatsapp-schafkopf-scheduler",
    "arn:aws:iam::082113759242:role/lambda-whatsapp-scheduler-role"
  ]
}
```

---

## Troubleshooting

### Common Issues

#### 1. Lambda fails with "Failed to download auth from S3"

**Symptoms:**
```
[ERROR] Failed to download auth from S3: Access Denied
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Missing IAM permissions | Add `s3:GetObject` permission to Lambda role |
| Auth not uploaded to S3 | Run `bun run upload-auth` first |
| Wrong S3 bucket name | Verify bucket exists: `aws s3 ls s3://whatsapp-scheduler-082113759242` |
| S3 bucket in different region | Ensure Lambda and S3 are in same region or update S3 client config |

#### 2. Lambda fails with "Unable to retrieve user JID"

**Symptoms:**
```
[ERROR] Unable to retrieve user JID
```

**Causes:**
- Auth credentials expired or corrupted
- Auth.zip in S3 is invalid

**Solution:**
1. Re-authenticate locally: `bun run scheduler`
2. Re-upload auth: `bun run upload-auth`
3. Test Lambda again

#### 3. Lambda succeeds but auth updates not saved

**Symptoms:**
- Lambda completes successfully
- Next invocation requires re-authentication
- Logs show: "Failed to upload auth to S3"

**Causes:**
- Missing `s3:PutObject` permission

**Solution:**
Add `s3:PutObject` to Lambda IAM role:
```bash
aws iam attach-role-policy \
  --role-name lambda-whatsapp-scheduler-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

#### 4. Lambda timeout errors

**Symptoms:**
```
Task timed out after 3.00 seconds
```

**Causes:**
- WhatsApp connection takes longer than timeout
- Network latency

**Solution:**
Increase Lambda timeout:
```bash
aws lambda update-function-configuration \
  --function-name whatsapp-schafkopf-scheduler \
  --timeout 30
```

#### 5. Out of memory errors

**Symptoms:**
```
Runtime exited with error: signal: killed
Runtime.ExitError
```

**Causes:**
- Auth extraction uses too much memory
- WhatsApp client memory usage

**Solution:**
Increase Lambda memory:
```bash
aws lambda update-function-configuration \
  --function-name whatsapp-schafkopf-scheduler \
  --memory-size 512
```

### Debugging Tips

#### Enable Debug Logging

Update `config/schafkopf-scheduler.yaml`:
```yaml
whatsapp:
  logLevel: "debug"
```

Redeploy Lambda and check CloudWatch Logs for detailed output.

#### Check S3 Object Metadata

Verify auth.zip was uploaded correctly:
```bash
aws s3api head-object \
  --bucket whatsapp-scheduler-082113759242 \
  --key auth.zip
```

Expected output:
```json
{
  "LastModified": "2026-03-02T14:30:00Z",
  "ContentLength": 3670016,
  "ContentType": "application/zip"
}
```

#### Download and Inspect Auth.zip

Download auth from S3 to verify contents:
```bash
aws s3 cp s3://whatsapp-scheduler-082113759242/auth.zip ./auth-from-s3.zip
unzip -l auth-from-s3.zip | head -20
```

Should show ~892 files including:
- `creds.json`
- `app-state-sync-key-*.json`
- `pre-key-*.json`

#### Test Lambda Locally with Docker

Simulate Lambda environment locally:
```bash
# Set Lambda environment variables
export AWS_EXECUTION_ENV=AWS_Lambda_nodejs20.x
export AWS_LAMBDA_FUNCTION_NAME=whatsapp-schafkopf-scheduler

# Run scheduler
bun run scheduler
```

This should trigger S3 download/upload even though running locally.

---

## Environment Variables

The Lambda function automatically detects Lambda environment via these variables (set by AWS):

- `AWS_EXECUTION_ENV` - e.g., "AWS_Lambda_nodejs20.x"
- `AWS_LAMBDA_FUNCTION_NAME` - Function name
- `LAMBDA_TASK_ROOT` - Lambda runtime directory

**No manual configuration needed!** The WhatsApp client automatically checks for these variables.

---

## Cost Estimates

### S3 Storage

- **Storage**: ~3.5 MB = **$0.000083/month** (Standard tier)
- **Requests**: 2 per invocation (GET + PUT) = **$0.00001/invocation**

### Lambda

- **Compute**: 512 MB, 5-10 seconds = **~$0.000167/invocation**
- **Requests**: **$0.0000002/invocation**

### Total Cost Example

Weekly invocations (52/year):
- S3: $0.000083 + ($0.00001 × 52) = **$0.000603/month**
- Lambda: ($0.000167 × 52) = **$0.00869/month**
- **Total: ~$0.01/month** (essentially free tier)

---

## Security Best Practices

### 1. Least Privilege IAM

Grant only minimum required permissions:
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::whatsapp-scheduler-082113759242/auth.zip"
}
```

### 2. S3 Bucket Encryption

Enable default encryption on S3 bucket:
```bash
aws s3api put-bucket-encryption \
  --bucket whatsapp-scheduler-082113759242 \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

### 3. S3 Bucket Versioning

Enable versioning to prevent accidental deletion:
```bash
aws s3api put-bucket-versioning \
  --bucket whatsapp-scheduler-082113759242 \
  --versioning-configuration Status=Enabled
```

### 4. VPC Configuration (Optional)

For enhanced security, run Lambda inside VPC:
```bash
aws lambda update-function-configuration \
  --function-name whatsapp-schafkopf-scheduler \
  --vpc-config SubnetIds=subnet-xxx,SecurityGroupIds=sg-xxx
```

**Note**: Requires VPC endpoint for S3 or NAT Gateway for internet access.

---

## Monitoring & Alerts

### CloudWatch Alarms

Create alarms for Lambda failures:

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name whatsapp-scheduler-failures \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --period 300 \
  --statistic Sum \
  --threshold 1 \
  --dimensions Name=FunctionName,Value=whatsapp-schafkopf-scheduler \
  --alarm-actions arn:aws:sns:eu-central-1:082113759242:lambda-alerts
```

### CloudWatch Insights Queries

Query logs for successful polls:
```
fields @timestamp, @message
| filter @message like /Poll sent successfully/
| sort @timestamp desc
```

Query logs for S3 sync operations:
```
fields @timestamp, @message
| filter @message like /S3/ or @message like /Lambda environment detected/
| sort @timestamp desc
```

---

## FAQ

**Q: Does the scheduler work without Lambda?**
A: Yes! Local execution uses `./auth/` directory and never touches S3.

**Q: What happens if auth expires on Lambda?**
A: Lambda will fail with authentication error. You'll need to re-authenticate locally and re-upload: `bun run upload-auth`

**Q: Can I use a different S3 bucket?**
A: The bucket name `whatsapp-scheduler-082113759242` is hardcoded in `src/core/s3-auth-manager.ts`. To change it, update the constant and redeploy.

**Q: Does Lambda execution refresh WhatsApp credentials?**
A: Yes! Every Lambda execution refreshes credentials and uploads updated auth back to S3.

**Q: Can I run multiple Lambda functions with same auth?**
A: Not recommended. Concurrent Lambda invocations may cause auth conflicts. Use a single Lambda with scheduled execution.

**Q: How long do WhatsApp credentials last?**
A: WhatsApp credentials typically last several weeks without activity. Regular Lambda executions keep them fresh.

---

## Next Steps

1. ✅ Authenticate locally: `bun run scheduler`
2. ✅ Upload auth to S3: `bun run upload-auth`
3. ✅ Create Lambda function
4. ✅ Configure IAM permissions
5. ✅ Test Lambda invocation
6. ⚙️ Set up scheduled execution (optional)
7. 📊 Configure monitoring & alerts (recommended)

For support or questions, check the main [README.md](../../README.md) or contact the development team.
