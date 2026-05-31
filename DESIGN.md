# Design System — Multiworks Construction LLC

This document captures the design tokens, typographic system, and component conventions in use after the polish pass. It's the contract any future change should align to, and the source of truth for `/impeccable polish` runs.

## Color palette

All values live in `assets/styles.css :root`. Use the token, never hardcode.

| Token | Value | Use |
|---|---|---|
| `--bone` | `#F5F1EA` | Page background. Warm off-white tinted toward the accent. |
| `--paper` | `#FFFFFF` | Lighter card backgrounds, alternating section banding. |
| `--ink` | `#1A1A1A` | Body text, dark sections, primary button background. Never `#000`. |
| `--ink-soft` | `#2A2A28` | Sub-body text where `--ink` is too heavy. |
| `--mute` | `#5A5A56` | Secondary text. Tightened from `#6B6B66` for stronger AA contrast. |
| `--mute-2` | `#9A9690` | Disabled / decorative gray on dark sections. |
| `--rule` | `#D8D2C7` | Hairline borders, separators. |
| `--rule-soft` | `#E8E3D9` | Even quieter rule. |
| `--accent` | `#8B5A3C` | Terracotta accent: process numerals, eyebrow text, link hovers, principle marks. |
| `--accent-hover` | `#6F4530` | Darker accent on interactive states. |
| `--forest` | `#2E3A2C` | Form success state. Used sparingly. |

**Pure black and pure white are banned.** Every neutral is tinted toward the bone/terracotta palette. The accent is restricted to one role per surface (don't paint multiple things terracotta).

## Typography

Two families. Both are off the impeccable reflex-reject list.

**`--serif: 'Marcellus'`** (Google Fonts, weight 400 only). Trajan-influenced inscriptional serif. Carries every H1, H2, H3, the `.brand__mark`, `.testimonial__quote`, `.contact-card__value`, and `.service-card__title`. Marcellus is single-weight, so hierarchy comes from scale + letter-spacing, not weight contrast.

**`--sans: 'Sora'`** (Google Fonts, weights 400/500/600). Contemporary humanist sans, 2022 release. Carries body copy, `.eyebrow`, `.process__num` (small caps), buttons, form labels, footer text.

### Scale

| Element | clamp() | Notes |
|---|---|---|
| `h1` | `clamp(2.5rem, 6vw, 5.5rem)` | letter-spacing `-0.02em`, line-height `1.04`. |
| `h2` | `clamp(2rem, 4.6vw, 4rem)` | letter-spacing `-0.012em`, line-height `1.1`. |
| `h3` | `clamp(1.25rem, 2.2vw, 2.2rem)` | letter-spacing `-0.005em`, line-height `1.18`. |
| body | `1rem` | line-height `1.65`, `var(--sans)`. |
| `.lead` | `1.15rem` | line-height `1.7`, `var(--ink-soft)`. |
| `.eyebrow` | `0.75rem` | Sora 500, letter-spacing `0.18em`, uppercase, `var(--accent)`. |
| `.btn` | `0.78rem` | Sora 500, letter-spacing `0.16em`, uppercase. |

Body line length is capped at `65ch`. Headlines may exceed.

### Banned typography patterns

- Italic accent words inside H1/H2 via `<em>` — the previous AI tic.
- 01/02/03 italic Marcellus mini-numerals on cards or sections (kept only for the ordinal `.process` steps and styled as Sora small caps, not serif italic).
- Tracked-uppercase eyebrow + serif italic H2 on every section — this is the editorial-magazine cliche.
- Em dashes anywhere in prose. Use periods, commas, colons, semicolons.

## Spacing

`--gutter: clamp(1.25rem, 4vw, 3rem)` — horizontal page gutter, used on `.wrap` and most section padding.

Section vertical padding: `clamp(4rem, 9vw, 8rem)` via `.section`. Tightened headers use `1rem` margin-top on `.section__head h1/h2` (CSS-only — never inline `style="margin-top:1rem"` on individual elements).

## Components

### `.service-card`

Anchor element with `:hover { background: var(--paper) }`. **No leading numeral** — the H3 title carries the card. Title + blurb + Explore arrow. Used in the home service grid, the services hub, and the related-work section of each service detail page.

### `.scope-list`

Replaces the previous inline-styled Cormorant 1.15rem bullet list. Sans body, 0.98rem, `2px` accent dash bullet to the left of each item. No per-item rule (was visually noisy).

### `.trust-strip`

Horizontal banner between the home service grid and the process section. List of facts (license, insurance, warranty, BBB) in Sora 0.72rem caps, separated by middots. **Never** uses big numerals — that's the hero-metric trap.

### `.process` and `.process__num`

Numbered ordered sequence (Consult / Design / Build / Hand-off). Numerals are **Sora 500 caps with `0.22em` letter-spacing** — explicitly NOT italic Marcellus mini-numerals. This is the only place numbered section markers are allowed.

### `.principle`

Used on the about page for the four guiding principles. Replaces the previous `.process__num` 01-04 numerals with a 2rem × 2px accent rule (`.principle__mark`). Principles aren't ordinal so they shouldn't be numbered.

### `.faq__item` + `.faq__q` + `.faq__a`

Click-toggle accordion. Refactored from `max-height:500px` to `grid-template-rows: 0fr → 1fr` so any length of answer animates correctly. `aria-expanded` and `aria-controls` wired in `nav.js`.

### `.hero` and `.hero__slide`

5 images was tightened to **3 images on an 8s crossfade**. Each is a real `<img>` element with descriptive alt text. First eager + `fetchpriority="high"`, rest lazy. Rotation pauses on hover, focus, and `visibilitychange`. Honors `prefers-reduced-motion`.

### `.portfolio-group`

Per-service group with a visible `<h2>` divider, a count badge, and the project tiles below. Captions are **visible by default beneath each figure**, not hover-only (broken on touch).

### `.tap-call`

Mobile-only sticky bottom CTA. Hidden site-wide on `body.page-contact` so it doesn't overlap the form submit button.

### Form

Action `/api/contact` → Cloudflare Pages Function (`functions/api/contact.js`). Validates required fields, runs honeypot check, posts to Resend if `RESEND_API_KEY` env var is set (else logs). Client JS at `assets/nav.js` handles submit, status display, button state.

## Motion

- **Hero crossfade**: 1.2s opacity transition, 8s interval.
- **`.reveal`**: 0.8s opacity + 20px translateY-in on `IntersectionObserver` enter.
- **FAQ accordion**: 0.4s `grid-template-rows` transition.
- **All transitions ease-out-ish.** No bounce, no elastic, no spring.

Global `@media (prefers-reduced-motion: reduce)` strips every animation to 0.01ms. JS guards the hero `setInterval` with a `matchMedia` check.

## Accessibility floor

- All photographic content uses `<img>` with descriptive alt text. `data-bg` divs are banned for content imagery.
- `:focus-visible` outline is `2px solid var(--accent)` with `3px` offset, applied globally with per-component nudges.
- FAQ buttons carry `aria-expanded` + `aria-controls` + `role="region"` on the panel.
- Touch targets meet 44 × 44 minimum where they matter (sticky tap-call CTA, buttons).
- Heading hierarchy: H1 → H2 → H3 with no skips. `.sr-only` utility available for invisible H2 anchors where the visual design doesn't want a heading.
- Color contrast: `--mute` on `--bone` is ~5.7:1 (passes AA, borderline AAA).

## Security baseline (`_headers`)

- HSTS, X-Frame, X-Content-Type, Permissions-Policy, Referrer-Policy: all set.
- CSP: `default-src 'self'` with explicit allowances for Google Fonts. **No `'unsafe-inline'`** on `style-src` — all inline `<style>` blocks were moved into `styles.css` during the polish pass.
- `img-src` includes the production domain and the pages.dev preview domain.
- WebP files get `Cache-Control: public, max-age=31536000, immutable`.

## File layout

- `build.py` — single-file site generator. Top of file declares `SERVICES`, `HERO`, `TRUST_POINTS`, `IMAGE_ALTS`, `PROCESS`, brand constants.
- `assets/styles.css` — design system. Tokens at top, components below, accessibility/motion preference at bottom.
- `assets/nav.js` — interaction layer. Nav, hero rotation, reveal observer, FAQ accordion, form AJAX.
- `assets/img/*.webp` — 34 self-hosted WebP images. Filename matches `IMAGE_ALTS` keys.
- `assets/img/manifest.json` — relative-path lookup map. Single source of truth for image paths.
- `functions/api/contact.js` — Cloudflare Pages Function for the contact form.
- `_headers` — security + cache config.
- `_redirects` — apex/www enforcement.
- `rehost_images.py` — one-off script for image rehost (kept for future re-encode runs).

## Open work

Tracked in PRODUCT.md "Open questions" plus the next round of `/impeccable critique`.
