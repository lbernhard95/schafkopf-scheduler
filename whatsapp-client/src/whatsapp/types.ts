import type { WASocket } from '@whiskeysockets/baileys';

/**
 * Configuration options for WhatsApp client
 */
export interface WhatsAppClientOptions {
  /** Directory to store authentication files (default: './auth') */
  authDir?: string;

  /** Logging level (default: 'info') */
  logLevel?: 'silent' | 'error' | 'warn' | 'info' | 'debug';

  /** Custom QR code handler, if not provided uses qrcode-terminal */
  onQR?: (qr: string) => void;
}

/**
 * Internal connection state
 */
export interface ConnectionState {
  connected: boolean;
  authenticated: boolean;
  myJid?: string;
}

/**
 * Poll configuration
 */
export interface PollConfig {
  question: string;
  options: string[];
  selectableCount?: number;
}
