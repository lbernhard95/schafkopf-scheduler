import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

/**
 * Loads environment variables from .env file in monorepo root
 * This is called automatically by s3-auth-manager to ensure AWS credentials are available
 */
export function loadMonorepoEnv(): void {
  // Bun auto-loads .env from CWD, but we want monorepo root
  // Path from whatsapp-client/ to schafkopf-scheduler/
  const monorepoRoot = resolve(import.meta.dir, '../../../');
  const envPath = resolve(monorepoRoot, '.env');

  if (existsSync(envPath)) {
    // Read .env file synchronously
    const content = readFileSync(envPath, 'utf-8');
    const lines = content.split('\n');

    for (const line of lines) {
      // Skip comments and empty lines
      if (!line || line.trim().startsWith('#') || line.trim() === '') {
        continue;
      }

      // Parse KEY=VALUE format
      const match = line.match(/^([^=]+)=(.*)$/);
      if (match) {
        const key = match[1].trim();
        const value = match[2].trim();

        // Remove quotes if present
        const cleanValue = value.replace(/^["']|["']$/g, '');

        // Set environment variable if not already set
        if (!process.env[key]) {
          process.env[key] = cleanValue;
        }
      }
    }
  }
}
