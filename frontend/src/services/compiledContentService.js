/**
 * Compiled content service - replacement for resourceCache
 * Uses build-time compiled content instead of runtime fetching
 */

import { compiledFiles, stats } from '../compiled';

class CompiledContentService {
  constructor() {
    console.log('📚 CompiledContentService initialized with:', stats);
  }

  /**
   * Get content for a path (replaces resourceCache.getText)
   * @param {string} path - Path relative to textbook root (e.g., 'content/overviews/01-one-computer/concept-map.yml')
   * @returns {Promise<string>} - Content as string
   */
  async getText(path) {
    try {
      // Remove any cache busters or query parameters
      const cleanPath = this.cleanPath(path);
      
      console.log(`CompiledContentService: Getting text for path: ${cleanPath}`);
      
      const fileKey = this.pathToKey(cleanPath);
      const compiled = compiledFiles[fileKey];
      
      if (!compiled) {
        throw new Error(`File not found in compiled content: ${cleanPath}`);
      }
      
      const content = compiled.module;
      
      // If it's already a string (markdown), return it
      if (typeof content === 'string') {
        return content;
      }
      
      // If it's an object (parsed YAML), stringify it
      return JSON.stringify(content, null, 2);
      
    } catch (error) {
      console.error(`CompiledContentService: File not found: ${path}`, error);
      throw new Error(`Compiled file not found: ${path}`);
    }
  }

  /**
   * Get parsed YAML content
   * @param {string} path - Path to YAML file
   * @returns {Promise<Object>} - Parsed YAML data
   */
  async getYaml(path) {
    try {
      const cleanPath = this.cleanPath(path);
      console.log(`CompiledContentService: Getting YAML for path: ${cleanPath}`);
      
      const fileKey = this.pathToKey(cleanPath);
      const compiled = compiledFiles[fileKey];
      
      if (!compiled) {
        throw new Error(`File not found in compiled content: ${cleanPath}`);
      }
      
      const content = compiled.module;
      
      // If it's already an object (parsed YAML), return it
      if (typeof content === 'object') {
        return content;
      }
      
      // If it's a string, try to parse it as YAML
      const yaml = await import('js-yaml');
      return yaml.load(content);
      
    } catch (error) {
      console.error(`CompiledContentService: YAML file not found: ${path}`, error);
      throw new Error(`Compiled YAML file not found: ${path}`);
    }
  }

  /**
   * Try multiple URLs until one works (for fallback scenarios)
   * @param {string[]} paths - Array of paths to try
   * @returns {Promise<{text: string, path: string}>} - First successful content and path
   */
  async getTextFromMultiplePaths(paths) {
    let lastError;

    for (const path of paths) {
      try {
        console.log(`CompiledContentService: Trying path: ${path}`);
        const text = await this.getText(path);
        
        // Check if we got HTML (shouldn't happen with compiled content, but just in case)
        if (text.trim().startsWith('<!doctype html>') || text.trim().startsWith('<html')) {
          console.log(`CompiledContentService: Got HTML response for ${path}, trying next...`);
          continue;
        }
        
        console.log(`CompiledContentService: Successfully found content at: ${path}`);
        return { text, path };
        
      } catch (error) {
        console.log(`CompiledContentService: Path ${path} not found:`, error.message);
        lastError = error;
        continue;
      }
    }

    // If we get here, all paths failed
    const errorMessage = `Failed to find compiled content at any of ${paths.length} paths: ${paths.join(', ')}`;
    console.error(errorMessage);
    throw new Error(errorMessage);
  }

  /**
   * List all available compiled files
   * @param {string} type - Filter by type ('yaml' or 'markdown')
   * @returns {string[]} - Array of available file paths
   */
  listFiles(type = null) {
    return listCompiledFiles(type);
  }

  /**
   * Get compilation statistics
   * @returns {Object} - Compilation stats
   */
  getStats() {
    return stats;
  }

  /**
   * Clean path by removing cache busters and normalizing
   * @param {string} path - Original path
   * @returns {string} - Cleaned path
   */
  cleanPath(path) {
    // Remove any base URLs or prefixes
    let cleanPath = path.replace(/^.*\/textbook\//, '');
    
    // Remove cache busters
    cleanPath = cleanPath.replace(/[?&]_cb=[^&]*/, '').replace(/[?&]v=[^&]*/, '');
    
    // Remove query parameters
    cleanPath = cleanPath.split('?')[0];
    
    return cleanPath;
  }

  /**
   * Convert a file path to the key used in compiledFiles
   * @param {string} path - Clean file path
   * @returns {string} - Key for compiledFiles lookup
   */
  pathToKey(path) {
    // The keys in compiledFiles are the original file paths without /textbook/ prefix
    // So we just return the cleaned path as-is
    return path;
  }

  /**
   * Check if a file exists in compiled content
   * @param {string} path - Path to check
   * @returns {boolean} - True if file exists
   */
  hasFile(path) {
    try {
      const cleanPath = this.cleanPath(path);
      const fileKey = this.pathToKey(cleanPath);
      return compiledFiles.hasOwnProperty(fileKey);
    } catch {
      return false;
    }
  }
}

// Create singleton instance
const compiledContentService = new CompiledContentService();

// Export both the instance and the class
export default compiledContentService;
export { CompiledContentService };