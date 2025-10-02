// Cache buster utility for markdown files
// This helps prevent browser caching issues when content is updated

// In production, this should be set at build time to avoid excessive cache misses
// For now, we'll use a simple approach that resets daily
const getBuildTimestamp = () => {
  // Use environment variable if available (for build-time setting)
  if (import.meta.env.VITE_BUILD_TIMESTAMP) {
    return import.meta.env.VITE_BUILD_TIMESTAMP;
  }
  
  // Fallback: Use current timestamp (less efficient but ensures fresh content)
  return Date.now();
};

// Cache buster that changes based on build time or current time
export const getCacheBuster = () => {
  return `?v=${getBuildTimestamp()}`;
};

// Alternative: Reset cache daily (more efficient than every request)
export const getDailyCacheBuster = () => {
  const now = new Date();
  const dayKey = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`;
  return `?v=${dayKey}`;
};

// For immediate cache busting (use sparingly)
export const getTimestampCacheBuster = () => {
  return `?t=${Date.now()}`;
};