# Product Context — Multiworks Construction LLC marketing site

## Register

**Brand.** This is a marketing surface. The deliverable is the *impression itself*: a visitor's read of the brand in the first 5 seconds, before they call. Conversion goes through the phone CTA and the contact form; there is no e-commerce, no account creation, no logged-in surface.

## Users

Two real personas, named for the previous critique pass:

1. **Karen — Holladay / Park City homeowner.** Late 30s to 50s. Researching a kitchen, bath, or whole-home remodel for an existing property worth $1M–$5M. Skims on her iPhone during lunch. Budget bands: $80K–$1M. Wants to know **price**, **timeline**, and **what real Holladay/Park City projects look like** before she calls. Hates wasting time and hates being upsold. Trusts referrals; the website is the second-opinion check.

2. **Mark — Park City furniture maker / Salt Lake commercial owner.** 40s. Looking for a general contractor for a tenant-improvement build-out, a workshop expansion, or a small ground-up commercial project. Wants to confirm Multiworks is a *real* commercial shop, not a residential GC moonlighting. Cares about lease milestones, landlord coordination, and the contractor's ability to finish on a fixed deadline.

Both audiences are sophisticated. Both will sniff out an AI-generated brand site instantly and treat that as a credibility issue.

## Brand voice

Three physical-object words: **quiet · precise · unhurried**.

Not "luxury" (overused). Not "professional" (empty). Not "trusted" (claim, not voice).

The model is a museum caption: declarative, calm, leaves space around the facts. Sentence rhythm prefers periods over em-dashes. Vocabulary is real-contractor (allowance schedule, punch list, change order, TI, cost-plus, fixed-fee) rather than marketing-speak. The brand respects the reader's intelligence.

## Strategic principles

These are the things every page should make obvious within one scroll:

1. **Single point of accountability.** One contract, one project manager, one number to call.
2. **Transparent fixed-fee pricing** (with cost-plus as an exception, not the default).
3. **Written milestone schedule** updated every two weeks.
4. **24-month workmanship warranty** on every project.
5. **Locally rooted.** Utah-owned. Works with Utah trades they'd hire for their own home.

## Positioning

**High-end residential remodels + select commercial.** Not a custom home builder. Not a teardown-and-rebuild shop. Not a handyman, not a flipper, not a track-home builder. The recent typeset pass explicitly removed the "custom home" service to make this lane clear.

Geographic: Salt Lake County, Utah County, Summit County, Davis County. Heavy concentration in Holladay, Park City, Sandy, Cottonwood Heights, Lehi.

## Anti-references

We are explicitly **not** trying to look like:

- Generic AI-generated brand sites (Cormorant + Inter + tracked-uppercase eyebrows + italic accent words + em dashes + 01/02/03 numerals). This is the Stripe-adjacent editorial-typographic lane and it has saturated.
- SaaS landing pages with hero-metric stats (`100+` / `$50M+` / `5.0★`).
- Webflow agency templates with identical 3-up card grids and "Consult / Design / Build / Hand-off" timelines.
- Foxterra/Studio-clone construction sites with full-bleed Cormorant headlines.

We *are* trying to look like a careful Utah museum's annual-report page or a Klim-style catalog of a real builder's work — slightly architectural, slightly carved-stone, deeply unfussy.

## Tone constraints

- No exclamation points anywhere.
- No emojis anywhere.
- Em dashes are banned (replace with periods, commas, colons, semicolons, parentheses).
- Use "we" and "you" — not "our company" or "the homeowner".
- Short sentences. Verbs do work. Adjectives earn their place.
- Stats are sourceable or they're cut. No "100+" without an audited source.

## Conversion targets

In rank order:

1. Phone call to **+1 (385) 271-6688** — the highest-value action because it ends with a scheduled site walk in under a week.
2. Form submission via `/api/contact` (Pages Function, Resend-backed).
3. Email to `build@multiworksconstruction.com` (the cold-skip-form fallback).

Vanity metrics (page views, time on site, social shares) are not goals.

## Open questions

- **Real testimonials.** Currently using placeholder anonymous quotes from "Holladay client" and "Park City client". Need actual names + photos + project specifics, with client permission.
- **Real project addresses.** Portfolio captions currently show a city per image from a placeholder rotation. Should be a real project address per real project photo when those become available.
- **Real GC license number.** Trust strip uses placeholder `#12345678`; need the actual Utah license number from Andrew/Geoff.
- **DNS cutover plan.** Site is on `multiworksconstruction.pages.dev` with canonical pointing at `multiworksconstruction.com` (not yet DNS-live).
