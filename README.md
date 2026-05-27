# Multiworks Construction LLC — multiworksconstruction.com

Static marketing site for **Multiworks Construction LLC**, a Utah design-build
general contractor. Built as plain HTML/CSS/JS and deployed to Cloudflare Pages
from this repo.

- **Live**: https://multiworksconstruction.com (post-DNS cutover)
- **Phone**: +1 (385) 271-6688
- **Service area**: Salt Lake County, Utah County, Summit County, Davis County

## Stack

- Static HTML/CSS/JS — no build step required for Cloudflare Pages
- Design language inspired by Utah landscape-architecture editorial sites
  (Cormorant Garamond display serif + Inter UI; bone background, terracotta
  accent; full-bleed hero with 1.8 s rotating photography)
- Hero photography and service imagery generated via Higgsfield
  (`nano_banana_pro`) — URLs referenced from
  `assets/img/manifest.json`; no local image binaries committed

## Pages

| Path                              | Description                                  |
| --------------------------------- | -------------------------------------------- |
| `/`                               | Home with 10-image hero rotation             |
| `/services.html`                  | All 10 services grid                         |
| `/about.html`                     | About + principles                           |
| `/portfolio.html`                 | Project mosaic                               |
| `/contact.html`                   | Contact form + business info                 |
| `/custom-home-building.html`      | Service page                                 |
| `/whole-home-remodeling.html`     | Service page                                 |
| `/kitchen-remodeling.html`        | Service page                                 |
| `/bathroom-remodeling.html`       | Service page                                 |
| `/basement-finishing.html`        | Service page                                 |
| `/home-additions.html`            | Service page                                 |
| `/outdoor-living.html`            | Service page                                 |
| `/commercial-construction.html`   | Service page                                 |
| `/design-build.html`              | Service page                                 |
| `/teardown-rebuild.html`          | Service page                                 |

Each page ships with `LocalBusiness`, `Service` and `FAQPage` JSON-LD
structured data, OG/Twitter meta tags, and Utah-localized SEO copy.

## Regenerating

```bash
python3 build.py
```

Reads `assets/img/manifest.json` and rewrites every HTML page. Edit the
`SERVICES`, `SERVICE_AREAS`, `PROCESS`, brand or contact constants at the top
of `build.py` and re-run.

## Deploy

Cloudflare Pages auto-builds on push to `main`. No build command — pure static
HTML served from repo root.

1. Push the chosen branch to GitHub (`misterho1/elitespautah`)
2. In Cloudflare → Pages, connect this repo to a new project named
   `multiworks` (or similar)
3. Add the custom domain `multiworksconstruction.com` and `www.multiworksconstruction.com`
4. DNS A/CNAME records to Cloudflare nameservers
