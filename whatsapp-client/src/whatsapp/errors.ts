/**
 * Base error class for all WhatsApp-related errors
 */
export class WhatsAppError extends Error {
  constructor(message: string, public readonly cause?: Error) {
    super(message);
    this.name = 'WhatsAppError';
    if (cause) {
      this.stack = `${this.stack}\nCaused by: ${cause.stack}`;
    }
  }
}

/**
 * Thrown when authentication fails or credentials are invalid
 */
export class AuthenticationError extends WhatsAppError {
  constructor(message: string, cause?: Error) {
    super(message, cause);
    this.name = 'AuthenticationError';
  }
}

/**
 * Thrown when connection to WhatsApp fails
 */
export class ConnectionError extends WhatsAppError {
  constructor(message: string, cause?: Error) {
    super(message, cause);
    this.name = 'ConnectionError';
  }
}

/**
 * Thrown when sending a message fails
 */
export class MessageSendError extends WhatsAppError {
  constructor(message: string, public readonly recipient?: string, cause?: Error) {
    super(message, cause);
    this.name = 'MessageSendError';
  }
}

/**
 * Thrown when JID format is invalid
 */
export class InvalidJidError extends WhatsAppError {
  constructor(jid: string) {
    super(`Invalid JID format: ${jid}`);
    this.name = 'InvalidJidError';
  }
}
