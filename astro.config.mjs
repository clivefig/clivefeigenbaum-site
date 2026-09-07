import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'

// https://astro.build/config
export default defineConfig({
  // Update this to your live domain before deploying
  site: 'https://clivefeigenbaum.com',

  integrations: [
    sitemap(),
  ],

  // Static output — perfect for Netlify via GitHub push
  // Switch to output: 'server' + netlify adapter if SSR is ever needed
  output: 'static',
})
