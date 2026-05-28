import { defineConfig } from 'astro/config';
import AstroPWA from '@vite-pwa/astro';
import cloudflare from '@astrojs/cloudflare';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  adapter: cloudflare({
    imageService: 'cloudflare'
  }),
  integrations: [
    AstroPWA({
      registerType: 'autoUpdate',
      workbox: {
        globDirectory: 'dist',
        globPatterns: ['**/*.{js,css,svg,png,jpg,jpeg,gif,json,html,ico,txt,woff2}'],
        globIgnores: ['**/data/search-index.json'],
        navigateFallback: null,
        maximumFileSizeToCacheInBytes: 6 * 1024 * 1024 // 6 MB to support large index files
      },
      manifest: {
        name: 'Pelita - Alkitab Online',
        short_name: 'Pelita',
        description: 'Aplikasi Alkitab online yang cepat dan ringan.',
        theme_color: '#ffffff',
        icons: [
          {
            src: '/favicon.svg',
            sizes: '192x192',
            type: 'image/svg+xml'
          }
        ]
      }
    })
  ]
});
