// Utility to get the correct base URL for assets
export const getAssetUrl = (path) => {
  // Remove leading slash if present
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  
  // In development, use the path as-is
  // In production, prepend the base path
  const basePath = import.meta.env.PROD ? '/cis-110' : '';
  
  return `${basePath}/${cleanPath}`;
};

// Utility to get the base path for routing
export const getBasePath = () => {
  return import.meta.env.PROD ? '/cis-110' : '';
};