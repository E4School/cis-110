import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  base: mode === 'production' ? '/cis-110/' : '/',
  define: {
    // Optional: Set build timestamp for cache busting
    'import.meta.env.VITE_BUILD_TIMESTAMP': JSON.stringify(Date.now().toString())
  }
}))
