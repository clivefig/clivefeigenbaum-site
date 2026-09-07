import { defineConfig } from 'astro/config'

// https://astro.build/config
export default defineConfig({
  site: 'https://clivefeigenbaum.com',

  // Static output — perfect for Netlify via GitHub push
  // Switch to output: 'server' + netlify adapter if SSR is ever needed
  output: 'static',

  // @astrojs/sitemap will be re-added when the full site has multiple pages
})
