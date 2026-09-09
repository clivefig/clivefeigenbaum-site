import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { test } from 'node:test'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')

function read(rel) {
  return readFileSync(join(root, rel), 'utf8')
}

const ROBOTS_DIRECTIVES = [
  'noindex',
  'nofollow',
  'noarchive',
  'nosnippet',
  'noimageindex',
  'nocache',
  'noai',
  'noimageai',
]

test('/career 302s to the CV subdomain with noindex headers', () => {
  const netlify = read('netlify.toml')

  assert.match(netlify, /from\s+=\s+"\/career"/)
  assert.match(netlify, /from\s+=\s+"\/career\/\*"/)
  assert.match(netlify, /to\s+=\s+"https:\/\/cv\.clivefeigenbaum\.com\/"/)
  assert.match(netlify, /status\s+=\s+302/)

  for (const directive of ROBOTS_DIRECTIVES) {
    assert.match(
      netlify,
      new RegExp(`X-Robots-Tag\\s+=\\s+"[^"]*\\b${directive}\\b`),
      `netlify.toml X-Robots-Tag must include ${directive}`,
    )
  }
})

test('/career is disallowed for crawlers and AI scrapers in robots.txt', () => {
  const robots = read('public/robots.txt')

  assert.match(robots, /Disallow:\s*\/career(?:\s|$)/m)
  assert.match(robots, /Disallow:\s*\/career\//)

  for (const bot of ['GPTBot', 'ClaudeBot', 'CCBot', 'Googlebot', 'Bytespider', 'PerplexityBot']) {
    const block = robots.split(/User-agent:\s*/i).find((part) => part.startsWith(bot))
    assert.ok(block, `robots.txt must have a User-agent: ${bot} block`)
    assert.match(block, /Disallow:\s*\/career/)
  }
})

test('/career HTML fallback is noindex and is not linked from the public site', () => {
  const page = read('src/pages/career.astro')
  const nav = read('src/components/Nav.astro')
  const footer = read('src/components/Footer.astro')
  const index = read('src/pages/index.astro')

  assert.match(page, /name="robots"/)
  for (const directive of ['noindex', 'nofollow', 'noarchive', 'noai']) {
    assert.match(page, new RegExp(directive))
  }
  assert.match(page, /cv\.clivefeigenbaum\.com/)

  for (const [name, src] of [
    ['Nav', nav],
    ['Footer', footer],
    ['index', index],
  ]) {
    assert.equal(/href=["']\/career/i.test(src), false, `${name} must not link to /career`)
  }
})
