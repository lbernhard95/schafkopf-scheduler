import type { WASocket } from '@whiskeysockets/baileys';
import { MessageSendError } from './errors';
import type { PollConfig } from './types';
import { Logger } from '../core/logger';

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

    const result = await sock.sendMessage(jid, { text });

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

    const result = await sock.sendMessage(jid, {
      poll: {
        name: config.name,
        values: config.values,
        selectableCount: config.selectableCount,
      },
    });

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
