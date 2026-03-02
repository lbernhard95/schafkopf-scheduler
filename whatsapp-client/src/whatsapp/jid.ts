import { InvalidJidError } from './errors';

/**
 * Converts a phone number to WhatsApp JID format
 * @param phoneNumber - Phone number with country code (e.g., "4917657753775")
 * @returns JID in format "4917657753775@s.whatsapp.net"
 */
export function toJid(phoneNumber: string): string {
  // Remove common formatting characters
  const cleaned = phoneNumber.replace(/[\s\-\(\)]/g, '');

  // If already a JID, return as-is
  if (cleaned.includes('@')) {
    return cleaned;
  }

  // Convert to JID format
  return `${cleaned}@s.whatsapp.net`;
}

/**
 * Extracts phone number from JID
 * @param jid - WhatsApp JID
 * @returns Phone number without JID suffix
 */
export function fromJid(jid: string): string {
  return jid.split('@')[0]?.split(':')[0] || '';
}

/**
 * Normalizes JID by removing device ID
 * Useful for sending messages to yourself
 * @param jid - JID that may contain device ID (e.g., "123:24@s.whatsapp.net")
 * @returns Normalized JID without device ID (e.g., "123@s.whatsapp.net")
 */
export function normalizeJid(jid: string): string {
  const [number, domain] = jid.split('@');
  const baseNumber = number?.split(':')[0];
  return `${baseNumber}@${domain}`;
}

/**
 * Validates if a string is a valid WhatsApp JID
 * @param jid - String to validate
 * @returns true if valid JID format
 */
export function isValidJid(jid: string): boolean {
  // Basic validation: should contain @ and end with .net
  return /^[^@]+@[^@]+\.net$/.test(jid);
}

/**
 * Checks if JID represents a group
 * @param jid - WhatsApp JID
 * @returns true if group JID (ends with @g.us)
 */
export function isGroupJid(jid: string): boolean {
  return jid.endsWith('@g.us');
}

/**
 * Validates and normalizes JID, throwing error if invalid
 * @param jid - JID to validate
 * @returns Normalized JID
 * @throws InvalidJidError if JID format is invalid
 */
export function ensureValidJid(jid: string): string {
  const normalized = normalizeJid(jid);
  if (!isValidJid(normalized)) {
    throw new InvalidJidError(jid);
  }
  return normalized;
}
