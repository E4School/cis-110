/**
 * Centralized resource cache to prevent duplicate fetches
 * Implements in-memory caching with Promise deduplication
 */

import { getCacheBuster } from '../utils/cacheBuster';

class ResourceCache {
  constructor() {
    // Cache for completed requests (url -> response data)
    this.cache = new Map();
    
    // Cache for in-flight requests (url -> Promise)
    this.pendingRequests = new Map();
    
    // Optional: Set up cache expiration (5 minutes default)
    this.cacheExpiration = 5 * 60 * 1000; // 5 minutes in milliseconds
    this.expirationTimes = new Map();
  }

  /**
   * Get a resource with caching and deduplication
   * @param {string} url - The URL to fetch
   * @param {Object} options - Fetch options
   * @returns {Promise<string>} - The response text
   */
  async getText(url, options = {}) {
    const cacheKey = this.getCacheKey(url);
    
    // Check if we have a valid cached response
    if (this.hasValidCache(cacheKey)) {
      console.log('ResourceCache: Cache hit for', url);
      return this.cache.get(cacheKey);
    }

    // Check if there's already a pending request for this resource
    if (this.pendingRequests.has(cacheKey)) {
      console.log('ResourceCache: Deduplicating request for', url);
      return this.pendingRequests.get(cacheKey);
    }

    // Create new request
    console.log('ResourceCache: New request for', url);
    const cacheBuster = getCacheBuster();
    const requestUrl = `${url}${cacheBuster}`;
    
    const requestPromise = this.performFetch(requestUrl, options)
      .then(response => {
        // Cache the successful response
        this.cache.set(cacheKey, response);
        this.expirationTimes.set(cacheKey, Date.now() + this.cacheExpiration);
        
        // Remove from pending requests
        this.pendingRequests.delete(cacheKey);
        
        return response;
      })
      .catch(error => {
        // Remove from pending requests on error
        this.pendingRequests.delete(cacheKey);
        throw error;
      });

    // Store the promise to deduplicate concurrent requests
    this.pendingRequests.set(cacheKey, requestPromise);
    
    return requestPromise;
  }

  /**
   * Get JSON data with caching
   * @param {string} url - The URL to fetch
   * @param {Object} options - Fetch options
   * @returns {Promise<Object>} - Parsed JSON response
   */
  async getJSON(url, options = {}) {
    const text = await this.getText(url, options);
    try {
      return JSON.parse(text);
    } catch (error) {
      throw new Error(`Failed to parse JSON from ${url}: ${error.message}`);
    }
  }

  /**
   * Perform the actual fetch request
   * @param {string} url - URL with cache buster
   * @param {Object} options - Fetch options
   * @returns {Promise<string>} - Response text
   */
  async performFetch(url, options) {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: Failed to fetch ${url}`);
    }
    
    return await response.text();
  }

  /**
   * Generate cache key from URL (removes cache buster for consistent keys)
   * @param {string} url - Original URL without cache buster
   * @returns {string} - Cache key
   */
  getCacheKey(url) {
    // Remove any existing cache busters to create consistent cache keys
    return url.replace(/[?&]_cb=[^&]*/, '').replace(/[?&]v=[^&]*/, '');
  }

  /**
   * Check if we have a valid (non-expired) cache entry
   * @param {string} cacheKey - Cache key to check
   * @returns {boolean} - True if cache is valid
   */
  hasValidCache(cacheKey) {
    if (!this.cache.has(cacheKey)) {
      return false;
    }

    const expiration = this.expirationTimes.get(cacheKey);
    if (expiration && Date.now() > expiration) {
      // Cache expired, remove it
      this.cache.delete(cacheKey);
      this.expirationTimes.delete(cacheKey);
      return false;
    }

    return true;
  }

  /**
   * Clear the entire cache
   */
  clearCache() {
    console.log('ResourceCache: Clearing cache');
    this.cache.clear();
    this.pendingRequests.clear();
    this.expirationTimes.clear();
  }

  /**
   * Clear cache for a specific URL pattern
   * @param {RegExp|string} pattern - Pattern to match URLs to clear
   */
  clearPattern(pattern) {
    const regex = typeof pattern === 'string' ? new RegExp(pattern) : pattern;
    
    for (const [key] of this.cache) {
      if (regex.test(key)) {
        this.cache.delete(key);
        this.expirationTimes.delete(key);
      }
    }
    
    console.log('ResourceCache: Cleared cache entries matching pattern:', pattern);
  }

  /**
   * Try multiple URLs until one works (for fallback scenarios)
   * @param {string[]} urls - Array of URLs to try in order
   * @param {Object} options - Fetch options
   * @returns {Promise<{text: string, url: string}>} - Response text and successful URL
   */
  async getTextFromMultipleUrls(urls, options = {}) {
    let lastError;
    const attemptedUrls = [];

    for (const url of urls) {
      try {
        attemptedUrls.push(url);
        console.log(`ResourceCache: Trying URL: ${url}`);
        
        const text = await this.getText(url, options);
        
        // Check if we got HTML instead of markdown (happens when file doesn't exist)
        if (text.trim().startsWith('<!doctype html>') || text.trim().startsWith('<html')) {
          console.log(`ResourceCache: Got HTML response for ${url}, trying next URL...`);
          continue;
        }
        
        console.log(`ResourceCache: Successfully found content at: ${url}`);
        return { text, url };
        
      } catch (error) {
        console.log(`ResourceCache: Failed to fetch ${url}:`, error.message);
        lastError = error;
        continue;
      }
    }

    // If we get here, all URLs failed
    const errorMessage = `Failed to fetch from any of ${urls.length} URLs. Attempted: ${attemptedUrls.join(', ')}. Last error: ${lastError?.message}`;
    throw new Error(errorMessage);
  }

  /**
   * Get cache statistics for debugging
   * @returns {Object} - Cache stats
   */
  getStats() {
    return {
      cacheSize: this.cache.size,
      pendingRequests: this.pendingRequests.size,
      cacheKeys: Array.from(this.cache.keys())
    };
  }
}

// Create singleton instance
const resourceCache = new ResourceCache();

// Export both the instance and the class for testing
export default resourceCache;
export { ResourceCache };