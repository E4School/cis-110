// Auto-generated TypeScript definitions for compiled content

export interface CompiledFileMetadata {
  sourceFile: string;
  compiledAt: string;
  type: 'yaml' | 'markdown';
  contentType?: 'textbook' | 'wiki';
}

export interface CompiledFile {
  module: any;
  metadata: CompiledFileMetadata;
  type: 'yaml' | 'markdown';
  contentType?: 'textbook' | 'wiki';
}

export interface CompilationStats {
  totalFiles: number;
  yamlFiles: number;
  markdownFiles: number;
  compiledAt: string;
}

export declare const compiledFiles: Record<string, CompiledFile>;
export declare const stats: CompilationStats;

export declare function getCompiledFile(path: string): any;
export declare function getFileMetadata(path: string): CompiledFileMetadata;
export declare function listCompiledFiles(type?: 'yaml' | 'markdown'): string[];
