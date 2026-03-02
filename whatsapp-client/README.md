# whatsapp-client (Bun + Baileys)

This is a standalone WhatsApp client for sending messages and polls, built with Bun & TypeScript using the Baileys library. Designed for multi-project repos and runnable in AWS Lambda or locally.

## Features
- Authenticate/log in only once, then persist session to /auth
- Send messages to user or group by specifying JID
- Send polls (question + options to any group or user)
- TypeScript & Bun native (fast, deployable)

## Usage

### 1. Install dependencies
```bash
bun install
```

### 2. Set up authentication
On first run, a QR code appears: scan with WhatsApp for login. Session is saved to `/auth`. Subsequent runs reuse that session.

### 3. JID is automatically detected after login for sending messages to yourself.
- To send to other users or groups, set JID in your code or via environment variable (see `.env.example`)
- Format: `123456789@s.whatsapp.net` (user) or `<group_id>@g.us` (group)

### 4. Run client demo
```bash
bun run src/index.ts
```
(Default: sends a text message and a poll to the configured JID)

## AWS Lambda Notes
- Persist `/auth` contents (session files) somewhere durable (e.g., S3) across invocations
- Use environment variables for dynamic JID selection

## Customization
- Edit `src/index.ts` to suit your workflow, add more features, or connect to other apps/scripts

---
Refer to the Baileys [Wiki](https://baileys.wiki/) for advanced features and troubleshooting.
