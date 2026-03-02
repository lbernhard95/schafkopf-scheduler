import type { WASocket } from '@whiskeysockets/baileys';
import { Logger } from '../core/logger';
import { WhatsAppError } from './errors';

/**
 * Information about a recipient (group or contact)
 */
export interface RecipientInfo {
  jid: string;
  name: string;
  type: 'group' | 'contact';
  participants?: number; // for groups only
}

/**
 * Removes emojis and extra whitespace from a string for comparison
 * @param str - String to normalize
 * @returns Normalized string without emojis
 */
function normalizeForComparison(str: string): string {
  return str
    // Remove emojis (Unicode ranges for most common emojis)
    .replace(/[\u{1F600}-\u{1F64F}]/gu, '') // Emoticons
    .replace(/[\u{1F300}-\u{1F5FF}]/gu, '') // Misc Symbols and Pictographs
    .replace(/[\u{1F680}-\u{1F6FF}]/gu, '') // Transport and Map
    .replace(/[\u{1F1E0}-\u{1F1FF}]/gu, '') // Flags
    .replace(/[\u{2600}-\u{26FF}]/gu, '')   // Misc symbols
    .replace(/[\u{2700}-\u{27BF}]/gu, '')   // Dingbats
    .replace(/[\u{FE00}-\u{FE0F}]/gu, '')   // Variation Selectors
    .replace(/[\u{1F900}-\u{1F9FF}]/gu, '') // Supplemental Symbols and Pictographs
    .replace(/[\u{1FA00}-\u{1FA6F}]/gu, '') // Chess Symbols
    .replace(/[\u{1FA70}-\u{1FAFF}]/gu, '') // Symbols and Pictographs Extended-A
    // Trim whitespace
    .trim()
    // Normalize multiple spaces to single space
    .replace(/\s+/g, ' ');
}

/**
 * Fetches all groups the user is participating in
 * @param sock - Baileys socket instance
 * @param logger - Logger instance
 * @returns Array of recipient info for groups
 */
async function fetchGroups(
  sock: WASocket,
  logger: Logger
): Promise<RecipientInfo[]> {
  try {
    logger.debug('Fetching all participating groups...');
    const groups = await sock.groupFetchAllParticipating();

    const recipients: RecipientInfo[] = Object.entries(groups).map(([jid, group]) => ({
      jid,
      name: group.subject || 'Unnamed Group',
      type: 'group' as const,
      participants: group.participants?.length || 0,
    }));

    logger.debug(`Found ${recipients.length} groups`);
    return recipients;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    logger.error(`Failed to fetch groups: ${errorMessage}`);
    throw new WhatsAppError(`Failed to fetch groups: ${errorMessage}`);
  }
}

/**
 * Fetches all contacts from the WhatsApp store
 * Note: Baileys doesn't provide a direct API to fetch all contacts,
 * so this returns an empty array for now. Individual contacts can still
 * be messaged by phone number.
 * @param sock - Baileys socket instance
 * @param logger - Logger instance
 * @returns Array of recipient info for contacts
 */
async function fetchContacts(
  sock: WASocket,
  logger: Logger
): Promise<RecipientInfo[]> {
  try {
    logger.debug('Fetching contacts...');

    // Baileys doesn't expose a direct contacts API in the same way as groups
    // Contacts are typically stored in sock.store but require additional setup
    // For now, we'll return an empty array and rely on phone numbers for individuals

    // TODO: Implement contact fetching if store is properly configured
    // const contacts = sock.store?.contacts || {};
    // const recipients: RecipientInfo[] = Object.entries(contacts).map(([jid, contact]) => ({
    //   jid,
    //   name: contact.name || contact.notify || 'Unknown',
    //   type: 'contact' as const,
    // }));

    logger.debug('Contact fetching not yet implemented, use phone numbers for individual chats');
    return [];
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    logger.warn(`Failed to fetch contacts: ${errorMessage}`);
    return [];
  }
}

/**
 * Fetches all available recipients (groups and contacts)
 * @param sock - Baileys socket instance
 * @param logger - Logger instance
 * @returns Array of all recipient info
 */
async function fetchAllRecipients(
  sock: WASocket,
  logger: Logger
): Promise<RecipientInfo[]> {
  const groups = await fetchGroups(sock, logger);
  const contacts = await fetchContacts(sock, logger);
  return [...groups, ...contacts];
}

/**
 * Resolves a recipient name to a JID
 * Matches on exact name (case-insensitive, emoji-independent)
 * @param sock - Baileys socket instance
 * @param name - Recipient name to resolve
 * @param logger - Logger instance
 * @returns JID of the matched recipient
 * @throws WhatsAppError if no match or multiple matches found
 */
export async function resolveRecipientName(
  sock: WASocket,
  name: string,
  logger: Logger
): Promise<string> {
  logger.debug(`Resolving recipient name: "${name}"`);

  // Fetch all recipients
  const recipients = await fetchAllRecipients(sock, logger);

  if (recipients.length === 0) {
    throw new WhatsAppError('No groups or contacts available. Please ensure you are a member of at least one group.');
  }

  // Normalize the search name
  const normalizedSearchName = normalizeForComparison(name).toLowerCase();
  logger.debug(`Normalized search name: "${normalizedSearchName}"`);

  // Find exact matches (case-insensitive, emoji-independent)
  const matches = recipients.filter(recipient => {
    const normalizedRecipientName = normalizeForComparison(recipient.name).toLowerCase();
    return normalizedRecipientName === normalizedSearchName;
  });

  // Handle no matches
  if (matches.length === 0) {
    throw new WhatsAppError(
      `No recipient found matching "${name}".`
    );
  }

  // Handle multiple matches (shouldn't happen with exact match, but be safe)
  if (matches.length > 1) {
    const matchNames = matches
      .map(r => `  - ${r.name} (${r.type}, JID: ${r.jid})`)
      .join('\n');

    throw new WhatsAppError(
      `Multiple recipients match "${name}":\n${matchNames}\n\nThis should not happen with exact matching. Please report this issue.`
    );
  }

  // Single match found
  const match = matches[0];
  logger.info(`Resolved "${name}" to ${match.type} "${match.name}" (${match.jid})`);
  if (match.type === 'group' && match.participants !== undefined) {
    logger.info(`  Group has ${match.participants} participants`);
  }

  return match.jid;
}
