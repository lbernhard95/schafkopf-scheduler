import yaml from 'js-yaml';
import path from 'node:path';
import { readFileSync, existsSync } from 'node:fs';

/**
 * Configuration interface for Schafkopf Scheduler
 */
export interface SchedulerConfig {
  whatsapp: {
    authDir: string;
    logLevel: 'silent' | 'error' | 'warn' | 'info' | 'debug';
  };
  scheduler: {
    pollTitle: string;
    recipient: string;
    timezone: string;
    weekdaysCount: number;
  };
}

/**
 * Default configuration values
 */
const DEFAULT_CONFIG: SchedulerConfig = {
  whatsapp: {
    authDir: './tmp/auth',
    logLevel: 'info',
  },
  scheduler: {
    pollTitle: 'Next Schafkopf Event Poll',
    recipient: '',
    timezone: 'Europe/Berlin',
    weekdaysCount: 10,
  },
};

/**
 * Loads configuration from YAML file
 * @param configPath - Path to the YAML configuration file
 * @returns Parsed and validated configuration
 * @throws Error if config file doesn't exist or is invalid
 */
export function loadConfig(configPath: string): SchedulerConfig {
  // Check if file exists
  if (!existsSync(configPath)) {
    throw new Error(`Configuration file not found: ${configPath}`);
  }

  // Read and parse YAML
  let rawConfig: any;
  try {
    const fileContents = readFileSync(configPath, 'utf8');
    rawConfig = yaml.load(fileContents);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to parse YAML configuration: ${message}`);
  }

  // Validate and merge with defaults
  const config: SchedulerConfig = {
    whatsapp: {
      authDir: rawConfig?.whatsapp?.authDir || DEFAULT_CONFIG.whatsapp.authDir,
      logLevel: rawConfig?.whatsapp?.logLevel || DEFAULT_CONFIG.whatsapp.logLevel,
    },
    scheduler: {
      pollTitle: rawConfig?.scheduler?.pollTitle || DEFAULT_CONFIG.scheduler.pollTitle,
      recipient: rawConfig?.scheduler?.recipient || DEFAULT_CONFIG.scheduler.recipient,
      timezone: rawConfig?.scheduler?.timezone || DEFAULT_CONFIG.scheduler.timezone,
      weekdaysCount: rawConfig?.scheduler?.weekdaysCount || DEFAULT_CONFIG.scheduler.weekdaysCount,
    },
  };

  // Validate required fields
  validateConfig(config);

  return config;
}

/**
 * Validates that all required configuration fields are present and valid
 * @param config - Configuration to validate
 * @throws Error if validation fails
 */
function validateConfig(config: SchedulerConfig): void {
  const errors: string[] = [];

  // Validate recipient
  if (!config.scheduler.recipient || config.scheduler.recipient.trim() === '') {
    errors.push('scheduler.recipient is required');
  }

  // Validate weekdays count
  if (config.scheduler.weekdaysCount < 1) {
    errors.push('scheduler.weekdaysCount must be at least 1');
  }

  if (config.scheduler.weekdaysCount > 20) {
    errors.push('scheduler.weekdaysCount cannot exceed 20 (4 weeks)');
  }

  // Validate log level
  const validLogLevels = ['silent', 'error', 'warn', 'info', 'debug'];
  if (!validLogLevels.includes(config.whatsapp.logLevel)) {
    errors.push(`whatsapp.logLevel must be one of: ${validLogLevels.join(', ')}`);
  }

  // Validate timezone (basic check - just ensure it's not empty)
  if (!config.scheduler.timezone || config.scheduler.timezone.trim() === '') {
    errors.push('scheduler.timezone is required');
  }

  // Throw if any validation errors
  if (errors.length > 0) {
    throw new Error(`Configuration validation failed:\n${errors.map(e => `  - ${e}`).join('\n')}`);
  }
}

/**
 * Gets the default config file path
 */
export function getDefaultConfigPath(): string {
  return path.join(import.meta.dir || '.', '../../../config/schafkopf-scheduler.yaml');
}
