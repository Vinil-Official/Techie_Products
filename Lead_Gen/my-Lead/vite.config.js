import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/process-leads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/run-agent': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/leads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/qualified-leads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
