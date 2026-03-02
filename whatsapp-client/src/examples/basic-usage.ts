/**
 * Basic usage example for WhatsApp Client
 *
 * This demonstrates:
 * - Creating a client instance (auto-connects)
 * - Sending text messages
 * - Sending polls
 * - Graceful disconnection
 */

import { WhatsAppClient } from '../index';
import path from 'node:path';

const AUTH_DIR = path.join(import.meta.dir || '.', '../../auth');

async function main() {
  console.log('=== WhatsApp Client Basic Usage Example ===\n');

  // Create client - it will auto-connect
  const client = new WhatsAppClient({
    authDir: AUTH_DIR,
    logLevel: 'info', // 'silent' | 'error' | 'warn' | 'info' | 'debug'
  });

  try {
    // Get own phone number
    const myPhoneNumber = await client.getMyPhoneNumber();
    console.log(`✓ Connected as: ${myPhoneNumber}\n`);

    // Send a text message to yourself
    console.log('Sending text message...');
    const messageId = await client.sendText(myPhoneNumber, 'Hello from the new WhatsApp Client API! 🚀');
    console.log(`✓ Text message sent (ID: ${messageId})\n`);

    // Send a poll to yourself
    console.log('Sending poll...');
    const pollId = await client.sendPoll(
      myPhoneNumber,
      'Which feature do you want next?',
      ['More examples', 'Send images', 'Schedule messages', 'Contact management'],
      1 // Allow selecting 1 option
    );
    console.log(`✓ Poll sent (ID: ${pollId})\n`);

    // You can also use JID format directly
    const myJid = await client.getMyJid();
    console.log('Sending another message using JID format...');
    const messageId2 = await client.sendText(myJid, 'This message was sent using JID format!');
    console.log(`✓ Message sent (ID: ${messageId2})\n`);

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  } finally {
    // Always disconnect gracefully
    console.log('\nDisconnecting...');
    await client.disconnect();
    console.log('✓ Disconnected successfully');
  }
}

// Run the example
main().catch(console.error);
