// Export main client class
export { WhatsAppClient } from './whatsapp/client';

// Export types
export type {
  WhatsAppClientOptions,
  ConnectionState,
  PollConfig,
} from './whatsapp/types';

// Export error classes
export {
  WhatsAppError,
  AuthenticationError,
  ConnectionError,
  MessageSendError,
  InvalidJidError,
} from './whatsapp/errors';

// Export utility functions
export {
  toJid,
  fromJid,
  normalizeJid,
  isValidJid,
  isGroupJid,
} from './whatsapp/jid';

// Export logger for advanced usage
export { Logger } from './core/logger';
