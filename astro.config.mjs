import { defineConfig } from 'astro/config'

// https://astro.build/config
export default defineConfig({
  site: 'https://clivefeigenbaum.com',

  // Static output — perfect for Netlify via GitHub push
  // Switch to output: 'server' + netlify adapter if SSR is ever needed
  output: 'static',

  // /career is an unlisted noindex trampoline (src/pages/career.astro).
  // Production 302 is in netlify.toml — do not add Astro redirects here;
  // external URL redirects are unsupported and /career/** breaks the build.

  // @astrojs/sitemap will be re-added when the full site has multiple pages
  // Filter: never include /career in a sitemap.
})
