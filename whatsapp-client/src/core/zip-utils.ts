import AdmZip from 'adm-zip';
import { existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';

/**
 * Creates a zip archive from a directory
 * @param sourceDir - Source directory to zip
 * @param outputZipPath - Output path for the zip file
 * @throws Error if source directory doesn't exist
 */
export async function zipDirectory(sourceDir: string, outputZipPath: string): Promise<void> {
  if (!existsSync(sourceDir)) {
    throw new Error(`Source directory not found: ${sourceDir}`);
  }

  try {
    const zip = new AdmZip();

    // Add the entire directory to the zip
    zip.addLocalFolder(sourceDir);

    // Write the zip file
    zip.writeZip(outputZipPath);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to create zip archive: ${message}`);
  }
}

/**
 * Extracts a zip archive to a destination directory
 * @param zipPath - Path to the zip file
 * @param destDir - Destination directory for extraction
 * @throws Error if zip file doesn't exist or is corrupt
 */
export async function unzipFile(zipPath: string, destDir: string): Promise<void> {
  if (!existsSync(zipPath)) {
    throw new Error(`Zip file not found: ${zipPath}`);
  }

  try {
    // Create destination directory if it doesn't exist
    if (!existsSync(destDir)) {
      mkdirSync(destDir, { recursive: true });
    }

    const zip = new AdmZip(zipPath);

    // Extract all files to destination
    zip.extractAllTo(destDir, true);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to extract zip archive: ${message}`);
  }
}
