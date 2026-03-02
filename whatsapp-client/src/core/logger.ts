export type LogLevel = 'silent' | 'error' | 'warn' | 'info' | 'debug';

const LOG_LEVELS: Record<LogLevel, number> = {
  silent: 0,
  error: 1,
  warn: 2,
  info: 3,
  debug: 4,
};

export class Logger {
  private level: number;

  constructor(logLevel: LogLevel = 'info') {
    this.level = LOG_LEVELS[logLevel];
  }

  setLevel(level: LogLevel): void {
    this.level = LOG_LEVELS[level];
  }

  error(message: string, ...args: any[]): void {
    if (this.level >= LOG_LEVELS.error) {
      console.error(`[ERROR] ${message}`, ...args);
    }
  }

  warn(message: string, ...args: any[]): void {
    if (this.level >= LOG_LEVELS.warn) {
      console.warn(`[WARN] ${message}`, ...args);
    }
  }

  info(message: string, ...args: any[]): void {
    if (this.level >= LOG_LEVELS.info) {
      console.log(`[INFO] ${message}`, ...args);
    }
  }

  debug(message: string, ...args: any[]): void {
    if (this.level >= LOG_LEVELS.debug) {
      console.log(`[DEBUG] ${message}`, ...args);
    }
  }

  /**
   * Silences Baileys verbose logging
   * Sets logging libraries to silent mode
   */
  static muteBaileysLogs(): void {
    // Suppress Baileys/Pino logs
    try {
      const pino = require('pino');
      if (pino.defaultOptions) {
        pino.defaultOptions.level = 'silent';
      }
    } catch {
      // Pino not available or already configured
    }
  }
}
