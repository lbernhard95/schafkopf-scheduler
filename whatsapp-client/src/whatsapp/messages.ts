import type { WASocket } from '@whiskeysockets/baileys';
import { MessageSendError } from './errors';
import type { PollConfig } from './types';
import { Logger } from '../core/logger';
import { isGroupJid } from './jid';

/**
 * Creates a promise that rejects after a timeout
 * @param ms - Timeout in milliseconds
 * @param message - Error message
 * @returns Promise that rejects after timeout
 */
function timeoutPromise(ms: number, message: string): Promise<never> {
  return new Promise((_, reject) => {
    setTimeout(() => reject(new MessageSendError(message)), ms);
  });
}

/**
 * Ensures group metadata is available before sending a message
 * This is required for group messages in Baileys to work properly
 * @param sock - The Baileys socket instance
 * @param jid - The recipient JID
 * @param logger - Logger instance
 */
async function ensureGroupMetadata(
  sock: WASocket,
  jid: string,
  logger: Logger
): Promise<void> {
  if (!isGroupJid(jid)) {
    logger.debug(`JID ${jid} is not a group, skipping metadata fetch`);
    return;
  }

  // Skip explicit metadata fetch since we're already fetching all groups on connection
  // The metadata should be cached by Baileys after groupFetchAllParticipating()
  logger.debug(`Group JID detected: ${jid}, metadata should be cached from groupFetchAllParticipating()`);
}

/**
 * Sends a text message to a JID
 * @param sock - The Baileys socket instance
 * @param jid - The recipient JID (already validated and normalized)
 * @param text - The message text
 * @param logger - Logger instance
 * @returns The message ID
 * @throws MessageSendError if sending fails
 */
export async function sendText(
  sock: WASocket,
  jid: string,
  text: string,
  logger: Logger
): Promise<string> {
  try {
    logger.debug(`Sending text message to ${jid}`);

    // Ensure group metadata is available for group chats
    await ensureGroupMetadata(sock, jid, logger);

    // Send message with timeout protection (15 seconds)
    logger.debug(`Calling sock.sendMessage for text to ${jid}...`);
    const startTime = Date.now();

    const result = await Promise.race([
      sock.sendMessage(jid, { text }),
      timeoutPromise(15000, `Message send timeout after 15 seconds for ${jid}`)
    ]);

    const duration = Date.now() - startTime;
    logger.debug(`sock.sendMessage completed in ${duration}ms`);

    if (!result?.key?.id) {
      throw new MessageSendError('Failed to send message: no message ID returned');
    }

    logger.info(`Text message sent successfully to ${jid} (ID: ${result.key.id})`);
    return result.key.id;
  } catch (error) {
    if (error instanceof MessageSendError) {
      throw error;
    }

    const errorMessage = error instanceof Error ? error.message : String(error);
    logger.error(`Failed to send text message to ${jid}: ${errorMessage}`);
    throw new MessageSendError(`Failed to send text message: ${errorMessage}`, error);
  }
}

/**
 * Sends a poll message to a JID
 * @param sock - The Baileys socket instance
 * @param jid - The recipient JID (already validated and normalized)
 * @param config - Poll configuration
 * @param logger - Logger instance
 * @returns The message ID
 * @throws MessageSendError if sending fails
 */
export async function sendPoll(
  sock: WASocket,
  jid: string,
  config: PollConfig,
  logger: Logger
): Promise<string> {
  try {
    logger.debug(`Sending poll to ${jid}: "${config.name}"`);

    // Validate poll options
    if (config.values.length < 2) {
      throw new MessageSendError('Poll must have at least 2 options');
    }

    if (config.values.length > 12) {
      throw new MessageSendError('Poll cannot have more than 12 options');
    }

    if (config.selectableCount < 1 || config.selectableCount > config.values.length) {
      throw new MessageSendError(
        `selectableCount must be between 1 and ${config.values.length}`
      );
    }

    // Ensure group metadata is available for group chats
    await ensureGroupMetadata(sock, jid, logger);

    // Send poll with timeout protection (30 seconds for polls as they're larger)
    logger.debug(`Calling sock.sendMessage for poll to ${jid}...`);
    const startTime = Date.now();

    const result = await Promise.race([
      sock.sendMessage(jid, {
        poll: {
          name: config.name,
          values: config.values,
          selectableCount: config.selectableCount,
        },
      }),
      timeoutPromise(30000, `Poll send timeout after 30 seconds for ${jid}`)
    ]);

    const duration = Date.now() - startTime;
    logger.debug(`sock.sendMessage completed in ${duration}ms`);

    if (!result?.key?.id) {
      throw new MessageSendError('Failed to send poll: no message ID returned');
    }

    logger.info(`Poll sent successfully to ${jid} (ID: ${result.key.id})`);
    return result.key.id;
  } catch (error) {
    if (error instanceof MessageSendError) {
      throw error;
    }

    const errorMessage = error instanceof Error ? error.message : String(error);
    logger.error(`Failed to send poll to ${jid}: ${errorMessage}`);
    throw new MessageSendError(`Failed to send poll: ${errorMessage}`, error);
  }
}
