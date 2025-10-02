/**
 * Vite plugin for content compilation
 * Runs content compilation before each build and dev server start
 */

import { main as compileContent } from '../scripts/compile-content.js';

export default function contentCompilerPlugin() {
  return {
    name: 'content-compiler',
    
    buildStart() {
      // Run compilation at the start of each build
      console.log('🔄 Running content compilation...');
      compileContent();
    },
    
    configureServer(server) {
      // Run compilation when dev server starts
      console.log('🔄 Running content compilation for dev server...');
      compileContent();
      
      // Note: File watching could be added here with chokidar if needed
      // For now, manual recompilation on file changes
    }
  };
}