# Clive's Personal Site — Design Decisions & Iteration Log

> This document records all key decisions made during the design and build of the placeholder and eventual full personal site. Use it as a reference point when switching machines or resuming work.

---

## Project Overview

**Goal:** A single-page placeholder site that captures Clive's personality and interests while the full site is built out.  
**Tone:** Fun, upbeat, warm — not corporate, not dry.  
**Status:** Placeholder v1 live at `index.html`  
**Profile photo source:** `C:\Projects\clive_online_cv\public\profile.jpg` (copied to `assets/profile.jpg`)

---

## v1 — Placeholder Page (Sep 2026)

### Inspiration

Sourced from [Elementor's 25 Best Personal Website Examples](https://elementor.com/blog/best-personal-website-examples/). Key influences:

| Site | What we borrowed |
|------|-----------------|
| **Simone Giertz** | Fun personality-forward design, playful but purposeful |
| **Cassie Evans** | Interactive feel, the site IS the personality |
| **Sean Halpin** | Conversational tone, first-person voice |
| **Timothée Roussilhe** | Clean one-page focus, no clutter |
| **Alex Coven** | Bold first impression, clear CTA |

### Design Decisions

#### Color Palette
- **Background:** `#F9F7F4` — warm off-white (not pure white) to feel inviting, not clinical
- **Text:** `#1A1A2E` — deep navy-black for warmth over harsh pure black
- **Accent:** `#D4961F` (whisky gold) — deliberate nod to the whisky interest; warm, premium, distinctive
- **Navy:** `#1E3A5F` — used for headings and the dark Coming Soon section
- **Rationale:** The amber/gold accent gives instant personality differentiation and ties the design to one of Clive's distinctive interests

#### Typography
- **Headings:** Poppins (800 weight) — bold, modern, friendly; letter-spacing tightened for impact
- **Body:** Inter — clean, highly legible, modern without being cold
- **Rationale:** Poppins at heavy weight creates strong visual hierarchy. Inter pairs cleanly without competing.

#### Layout Structure
1. **Fixed nav** — minimal, with a pulsing "Coming Soon" pill to set expectations immediately
2. **Hero** — centered, photo-first, big name reveal with tagline. Photo has gold ring treatment + status badge
3. **Interests grid** — 6 cards (3 col desktop, 2 col tablet, 1 col mobile), each with distinct colour accent top border
4. **Coming Soon section** — dark navy block with "SOON" watermark text, progress card showing site build status
5. **Footer** — minimal, dark

#### Interest Card Colors
Each card has its own accent color (top border + icon bg) to differentiate the interests visually:

| Interest | Color | Reasoning |
|----------|-------|-----------|
| Technology | `#2563EB` (blue) | Tech = blue convention |
| Development | `#16A34A` (green) | Code = green (terminal) |
| Photography | `#DB2777` (pink) | Creative, artsy energy |
| Travel | `#EA580C` (orange) | Warmth, adventure |
| Whisky | `#9333EA` (purple) | Premium, sophisticated |
| Family | `#DC2626` (red) | Heart, love, warmth |

#### Micro-interactions
- **Scroll reveal:** `.reveal` class elements animate in on scroll (opacity + translateY). Cards stagger with 60ms delay each
- **Hover on cards:** `translateY(-6px)` lift + border colour accent match
- **Profile photo:** Gold `outline` ring with `outline-offset` gap — clean alternative to complex borders
- **Status badge:** Absolute-positioned on photo, communicates "in progress" energy
- **Decorative rings:** SVG concentric circles behind hero photo; outer ring rotates slowly with dashed stroke
- **Scroll hint:** Bouncing arrow animation at hero bottom
- **Progress fill bar:** CSS animation fills from 0% to 35% on load

#### Accessibility
- Semantic HTML throughout (`nav`, `section`, `footer`, `h1`→`h3`)
- `aria-hidden="true"` on decorative elements
- Alt text on profile image
- `prefers-reduced-motion` — *TODO for v2: wrap animations in media query*
- Footer nav has `aria-label`

---

## What's Coming (Full Site Roadmap)

| Section | Priority | Notes |
|---------|----------|-------|
| Portfolio / Projects | High | Tech & development work |
| Photography gallery | High | Lightbox, categories |
| Blog / Writing | Medium | Long-form thoughts |
| Whisky journal | Medium | Tasting notes, ratings |
| Travel log / Map | Low | Interactive world map |
| About (full) | High | Longer bio, timeline |
| Contact form | High | Replace mailto link |

---

## Tech Stack Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | Plain HTML/CSS/JS | Placeholder = zero dependencies. Fast to ship, easy to hand off to any host |
| Fonts | Google Fonts CDN | Convenience for placeholder; consider self-hosting for production |
| Icons | Inline SVG | No external library needed; full control over colour via CSS `currentColor` |
| Animations | CSS + Intersection Observer | No library overhead |
| Hosting (future) | TBD | Options: Vercel, Netlify, GitHub Pages |

---

## Iterations Log

### v1.0 — Sep 7, 2026
- Initial placeholder page created
- Profile photo sourced from `clive_online_cv` project
- 6 interest cards designed
- "Coming Soon" section with progress tracker
- Scroll reveal animations
- Mobile responsive

---

## Locked Decisions (Sep 7, 2026 update)

| Decision | Answer |
|----------|--------|
| Full name | **Clive Feigenbaum** |
| Email | `clive@clivefeigenbaum.com` |
| LinkedIn | `https://www.linkedin.com/in/clive-feigenbaum-israel/` |
| Professional title | "Customer-focused specialist. Wannabe photographer." |
| Hosting | **Netlify** (deploy from GitHub repo) |
| Version control | **GitHub** — repo to be created when ready to go live |
| Tech stack (full site) | **Astro** (preferred) with possible React islands for interactive components |

### Tech Stack Rationale — Astro

Astro is a strong fit for a personal site because:
- **Content-first:** Perfect for a site that will have a blog, photo gallery, and whisky journal
- **Zero-JS by default:** Ships static HTML; JS only where needed (React islands for interactive parts)
- **Performance:** Excellent Lighthouse scores out of the box — great for SEO
- **Netlify-native:** First-class Netlify deployment support with `@astrojs/netlify` adapter
- **File-based routing:** Simple and intuitive — `/photography`, `/blog`, `/whisky` pages are just files
- **MDX support:** Write blog posts and whisky journal entries in Markdown
- React components can be added as Astro islands for any interactive sections

### Hosting Architecture (Netlify + GitHub)

```
Local Dev  →  GitHub Repo (main branch)  →  Netlify (auto-deploy on push)
                                         →  Preview URLs on pull requests
```

**Steps when ready to go live:**
1. `git init` in `clive-personal-site/`
2. Create GitHub repo `clivefeigenbaum-site` (or similar)
3. Connect repo to Netlify via Netlify dashboard
4. Configure custom domain in Netlify (point DNS to Netlify)
5. Enable Netlify's automatic HTTPS

### Domain
- Suggested: `clivefeigenbaum.com` (matches email domain)
- Check availability and register if not already owned

---

## Pending Decisions / Open Questions

- [ ] GitHub repo name (suggestion: `clivefeigenbaum-site`)
- [ ] Instagram / other social handles to add?
- [ ] Should the whisky section be a standalone page or embedded blog?
- [ ] Photography — DSLR/mirrorless brand? (useful for "gear" page later)
- [ ] Color scheme — keep whisky gold for full Astro site or revisit?
- [ ] Will there be a separate CV/resume page, or link to existing `clive_online_cv` project?

---

## Iterations Log

### v1.0 — Sep 7, 2026
- Initial placeholder page created (plain HTML/CSS/JS)
- Profile photo sourced from `clive_online_cv` project
- 6 interest cards designed
- "Coming Soon" section with progress tracker
- Scroll reveal animations
- Mobile responsive

### v1.2 — Sep 7, 2026
- Git repo initialised (`main` branch)
- GitHub repo created: https://github.com/clivefig/clivefeigenbaum-site
- Initial commit pushed (22 files, full Astro scaffold)
- Old placeholder HTML archived to `_archive/placeholder-v1.html`
- Root `assets/` folder removed (profile photo lives in `public/assets/`)
- **Next:** Connect repo to Netlify for auto-deploy

### v1.1 — Sep 7, 2026
- Added real email: `clive@clivefeigenbaum.com`
- Added real LinkedIn URL
- Updated hero tagline to reflect professional title ("Customer-focused specialist. Wannabe photographer.")
- Updated page `<title>` and meta description with full name
- Added LinkedIn button to hero CTA group
- Locked in: Netlify hosting, GitHub source control, Astro as full-site tech stack
- Updated `DECISIONS.md` with all locked decisions

---

### v1.6 — Sep 9, 2026
- `/career` anti-index / anti-scrape stack:
  - `robots.txt` `Disallow: /career` for `*` plus Googlebot, Bingbot, GPTBot, ClaudeBot, CCBot, and other scrapers
  - `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet, noimageindex, nocache, noai, noimageai`
  - `Cache-Control: no-store` on `/career`, `/career/`, `/career/*`
  - Fallback `src/pages/career.astro` with matching meta robots (Netlify still 302s in production)
- Still unlinked from nav/footer/home. Still not access control — password the CV subdomain for real privacy
- QA: `npm test`

### v1.5 — Sep 9, 2026
- Unlisted shortcut: `clivefeigenbaum.com/career` → `https://cv.clivefeigenbaum.com/` (302)
- Not in nav, footer, homepage, or sitemap. Not listed in `robots.txt` (listing it would advertise the path)
- `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet, noimageindex` on `/career`
- This is obscurity, not access control. Anyone with the URL can open it and share it. To keep the CV private, password-protect `cv.clivefeigenbaum.com` in Netlify and add `noindex` there too
- QA: `npm test` (`scripts/qa-unlisted-routes.test.mjs`)

### v1.4 — Sep 9, 2026
- Front copy **does not** use a job title. Locked line: name + “Let’s talk.” — so the card works in any room (tech, photography, social) and does not corner Clive into SaaS onboarding
- Back word labels (PHONE / EMAIL / LINKEDIN) replaced with line icons + values
- LinkedIn printed as `clive-feigenbaum-israel` (the icon carries the network)
- Regenerated `print/business-card/output/` 10-up PDFs

### v1.3 — Sep 9, 2026
- Business card Option 1 (identity) locked: navy `#1E3A5F`, red SCAN ME `#E4453A`, Poppins + Inter
- Card size 85 × 55 mm; A4 10-up (2 × 5) with 18.5 mm side margins, 3 mm column gutter, 2 mm row gutter
- Back imposed with columns swapped for G540 long-edge flip
- Print files: `print/business-card/output/option1-front-a4.pdf` and `option1-back-a4.pdf`
- Contact on card: phone `+972 52 408 3159`, email `clive.fig@gmail.com`, LinkedIn `in/clive-feigenbaum-israel`
- QA: `python -m unittest test_layout.py` in `print/business-card/`

---

*Last updated: Sep 9, 2026 — v1.6*
