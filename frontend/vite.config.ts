import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3466,
    host: true, // Allows access from external devices if needed
  },
  css: {
    postcss: './postcss.config.js',
  },
});
