#!/usr/bin/env python3
"""Multiworks Construction LLC, static site generator.

Emits every HTML page from a shared template and content data.
Image URLs come from assets/img/manifest.json (Higgsfield CDN).
"""
import json, os, html, datetime, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "assets", "img", "manifest.json")

# ----------------------------------------------------------------
# Brand / contact
# ----------------------------------------------------------------
BRAND = "Multiworks Construction"
BRAND_FULL = "Multiworks Construction LLC"
BRAND_TAG = "Utah · General Contractor"
PHONE = "+1 (385) 271-6688"
PHONE_TEL = "+13852716688"
EMAIL = "build@multiworksconstruction.com"
ADDRESS_REGION = "Salt Lake County, Utah"
ADDRESS_LOCALITY = "Salt Lake City"
ADDRESS_STATE = "UT"
ADDRESS_POSTAL = "84101"
DOMAIN = "https://multiworksconstruction.com"
SITE_DESC_SHORT = "Utah high-end remodeling and design-build contractor. Whole-home transformations, kitchens, baths, additions and commercial buildouts. Licensed, insured, locally owned."

# Hero strategy: three photos on an 8s crossfade.
# Five was still too many — most visitors see 1-2 slides max, so the extra preloads were waste.
# Each carries real descriptive alt text (WCAG 1.1.1).
HERO = [
    ("hero-01", "White oak shaker kitchen with brass pulls and a waterfall quartz island, finished by Multiworks on a Holladay remodel."),
    ("hero-05", "Holladay primary bath with a curbless walk-in shower, freestanding tub and warmed limestone floor."),
    ("hero-09", "Salt Lake City home addition with mountain-view picture windows and white oak floors."),
]

# Proof scaffolding for the home page trust strip. Marketing-site convention: state the
# specifics, no big numerals. Replaces the deleted hero-metric stats block.
TRUST_POINTS = [
    "Utah Licensed GC #12345678",
    "Commercial general liability + workers' comp insured",
    "24-month workmanship warranty",
    "BBB accredited",
]

# Per-image alt text for service triptychs. Falls back to a generic per-service template
# if a specific entry isn't present. Used by page_service().
IMAGE_ALTS = {
    "custom-home-01": "Custom Utah home exterior with stone and timber detail",
    "whole-home-01": "Open-plan whole-home remodel with vaulted ceiling and oak floors",
    "whole-home-02": "Living room remodel with new fireplace surround and built-ins",
    "whole-home-03": "Reworked staircase and foyer with curated lighting",
    "kitchen-01": "Custom kitchen with shaker cabinets, brass pulls and quartz waterfall island",
    "kitchen-02": "Range wall with hood vent and hand-glazed backsplash",
    "kitchen-03": "Walk-in pantry build-out with marble counters and integrated storage",
    "bathroom-01": "Primary bathroom with curbless walk-in shower and stone floor",
    "bathroom-02": "Freestanding soaking tub against a fluted-stone feature wall",
    "bathroom-03": "Double-vanity bathroom with integrated lighted mirrors",
    "basement-01": "Basement home theater with riser seating and acoustic paneling",
    "basement-02": "Basement wet bar with backlit glass shelving and walnut cabinetry",
    "basement-03": "Finished basement guest suite with custom millwork",
    "additions-01": "Second-story home addition tied into an existing roofline",
    "additions-02": "Primary suite addition with corner picture windows",
    "additions-03": "Detached ADU casita with covered entry porch",
    "outdoor-01": "Covered patio with outdoor kitchen and fire feature",
    "outdoor-02": "Pergola over a paver patio with integrated lighting",
    "outdoor-03": "Pool deck with stone hardscape and mountain view",
    "commercial-01": "Restaurant build-out with exposed beams and open kitchen pass",
    "commercial-02": "Tenant-improvement office buildout with glass partition walls",
    "commercial-03": "Retail storefront finish-out with custom millwork display",
    "design-build-01": "Architectural plan review with project manager and client",
    "design-build-02": "Interior selections board with stone, wood and tile samples",
    "design-build-03": "On-site walkthrough with framer and superintendent",
    "teardown-01": "Lot prep for a teardown rebuild project",
    "teardown-02": "New foundation pour on a previously tear-down lot",
    "teardown-03": "Completed rebuild home in a mature neighborhood",
}

def alt_for(name):
    """Return descriptive alt text for an image, or a sane fallback."""
    return IMAGE_ALTS.get(name, f"Multiworks Construction project photograph: {name}")

def service_card_html(s):
    """Render a single service card. Numeric prefix removed per /impeccable critique
    (numbered section markers were a load-bearing AI-template tic across cards + process)."""
    return (
        f'<a class="service-card" href="/{s["slug"]}.html">\n'
        f'  <h3 class="service-card__title">{esc(s["title"])}</h3>\n'
        f'  <p class="service-card__desc">{esc(s["blurb"])}</p>\n'
        f'  <span class="service-card__link">Explore <span class="arrow">&rarr;</span></span>\n'
        f'</a>'
    )

with open(MANIFEST) as f:
    IMG = json.load(f)

def img(name):
    """Return the manifest URL for a named image (relative or absolute)."""
    return IMG.get(name, "")

def absolute_url(path):
    """Promote a possibly-relative path to a fully-qualified URL.

    Open Graph and JSON-LD require absolute image URLs for social previews
    and structured data to validate. In-page CSS/HTML can keep relative paths.
    """
    if not path:
        return ""
    if path.startswith(("http://", "https://")):
        return path
    return f"{DOMAIN}{path}"

# ----------------------------------------------------------------
# Service catalog (merged from competitor scans)
# ----------------------------------------------------------------
SERVICES = [
    {
        "slug": "whole-home-remodeling",
        "num": "01",
        "title": "Whole-Home Remodeling",
        "tag": "Floor-to-ceiling transformations",
        "blurb": "Reimagine the home you already own. Whole-home remodels, additions and structural reworks that respect the bones and elevate the experience.",
        "hero_img": "whole-home-01",
        "imgs": ["whole-home-01", "whole-home-02", "whole-home-03"],
        "intro": "Sometimes the right move isn't a new build, it's reinventing the home you're already in. Whole-home remodels are our craft. We open walls, raise ceilings, replan flow, modernize systems, and bring older Utah homes up to the standard of new construction, without losing the character that made you love the place to begin with.",
        "what_we_do": [
            "Structural reworks, load-bearing wall removal, beam install",
            "Full mechanical, electrical and plumbing rework to code",
            "Floor plan redesign and circulation improvements",
            "New windows, doors, insulation envelope and energy upgrades",
            "Full interior finish-out: floors, ceilings, millwork, paint",
            "Exterior refresh: siding, stone, roofline, landscape",
            "Phase planning for live-in remodels with minimal disruption",
        ],
        "faq": [
            ("Can we live in the house during a whole-home remodel?",
             "Often, yes, we plan in phases so one side of the home stays habitable while the other is under construction. For larger or more invasive renovations, we'll be honest if temporary housing is the smarter call."),
            ("How is a whole-home remodel priced?",
             "We provide a fixed-fee proposal after a site walk and a clear scope conversation. The price covers labor, materials, subcontractors and a defined allowance schedule for selections like tile, plumbing fixtures and lighting."),
            ("Will the remodel match the original architecture?",
             "That's the goal whenever you want it to be. We have craftspeople who specialize in seamless additions and historically appropriate finishes, and we're equally happy to take a mid-century or 90s home in a fully modern direction."),
        ],
    },
    {
        "slug": "kitchen-remodeling",
        "num": "02",
        "title": "Kitchen Remodeling",
        "tag": "The most-used room in the house",
        "blurb": "Custom kitchens engineered around how you actually cook, host and live, not a stock layout pulled from a showroom.",
        "hero_img": "kitchen-01",
        "imgs": ["kitchen-01", "kitchen-02", "kitchen-03"],
        "intro": "A kitchen remodel is a high-stakes investment in your daily life and your home's resale value. We approach kitchens as a craft: layout first, then cabinetry, then appliances and finishes. Whether you want a transitional white-and-brass classic, a moody English cottage kitchen or a fully modern chef's space, our team plans, builds and installs every component.",
        "what_we_do": [
            "Layout redesign, island reconfiguration, wall removal",
            "Fully custom cabinetry, paint-grade, stain-grade or quarter-sawn hardwood",
            "Stone, quartz and porcelain countertops, full-height backsplashes",
            "Built-in appliance packages (Wolf, Sub-Zero, Miele, Thermador)",
            "Plumbing, electrical, gas and HVAC reworks to support new layouts",
            "Hood vents, pantry build-outs, butler's pantries, beverage stations",
            "Lighting design, recessed, under-cabinet, decorative pendants",
        ],
        "faq": [
            ("How long does a luxury kitchen remodel take?",
             "Most full kitchen remodels take 10 to 16 weeks from demo to final punch. Cabinetry lead times drive the schedule, we order early and stage delivery to minimize the time you're without a kitchen."),
            ("What's a typical budget range?",
             "Most of our kitchen projects in Salt Lake City and Park City fall between $80K and $250K, depending on size, custom cabinetry, appliance package and stone selections. We're happy to give you a realistic range during the first conversation."),
            ("Do you handle the design or do I need a separate kitchen designer?",
             "Either works. We have an in-house kitchen designer who handles layout, cabinetry detailing, elevations and selections. We also collaborate often with outside interior designers."),
        ],
    },
    {
        "slug": "bathroom-remodeling",
        "num": "03",
        "title": "Bathroom Remodeling",
        "tag": "Master suites, baths, powder rooms",
        "blurb": "Spa-grade primary baths, guest baths, powder rooms and full master suite remodels, built waterproof, on time, on budget.",
        "hero_img": "bathroom-01",
        "imgs": ["bathroom-01", "bathroom-02", "bathroom-03"],
        "intro": "Bathrooms are unforgiving, every joint has to be waterproof, every fixture has to be right the first time, every tile cut has to line up. Multiworks builds bathrooms the way a yacht is built: methodically, with experienced trades, and zero shortcuts behind the walls. Our master suites, primary baths, guest baths and powder rooms are the most-photographed rooms we finish.",
        "what_we_do": [
            "Master bath suite buildouts with separate water closets, dressing rooms, dual vanities",
            "Curbless walk-in showers, steam showers, body-spray systems",
            "Freestanding tubs, drop-ins, and built-in soaking tubs",
            "Full waterproofing systems (Schluter, hot-mop, sheet membrane)",
            "Heated floors, heated towel racks, programmable lighting",
            "Custom vanities, integrated lighting mirrors, stone counters",
            "Powder rooms with statement walls, tile, fixtures and millwork",
        ],
        "faq": [
            ("How long does a bathroom remodel take?",
             "A primary bath suite usually takes 6 to 10 weeks. Guest baths and powder rooms typically finish in 4 to 6 weeks. We sequence selections and trades to keep momentum without compromise."),
            ("What's a realistic budget for a master bathroom in Utah?",
             "A high-end primary bath in Salt Lake or Park City typically runs $60K–$150K depending on size, stone, tile, fixtures and whether structural changes are involved."),
            ("Will my bathroom be torn up for the whole project?",
             "Demo is just the first week. We protect adjacent floors and finishes, contain dust, and stage trades efficiently so the disruption is concentrated rather than open-ended."),
        ],
    },
    {
        "slug": "basement-finishing",
        "num": "04",
        "title": "Basement Finishing",
        "tag": "Add usable square footage downstairs",
        "blurb": "Unlock thousands of sq ft below grade, theaters, gyms, wine rooms, guest suites, full apartments, and the playroom the kids actually use.",
        "hero_img": "basement-01",
        "imgs": ["basement-01", "basement-02", "basement-03"],
        "intro": "A finished basement is the single highest-ROI square footage you can add to a Utah home. Most of our clients walk in expecting a finished rec room and walk out with a guest suite, a home theater, a wine cellar, a gym, a wet bar, and a place the family actually wants to spend time. We handle egress, framing, mechanical, electrical, plumbing, drywall, finish, and the permits.",
        "what_we_do": [
            "Egress window install and full code compliance",
            "Home theaters with riser platforms, acoustic panels, smart AV pre-wire",
            "Full wet bars and second kitchens with appliance packages",
            "Conditioned wine rooms with cooling and custom racking",
            "Home gyms with rubber flooring, mirror walls, ventilation",
            "Bedroom + bath guest suites and rentable basement apartments / ADUs",
            "Smart-home integration, lighting scenes, motorized shades",
        ],
        "faq": [
            ("How long does it take to finish a basement?",
             "Most finished basements in our catalog take 8 to 14 weeks once permits are issued. Larger basements with bathrooms, wet bars and wine rooms run toward the longer end."),
            ("Do I need a permit to finish my basement?",
             "Yes. every Utah municipality requires a permit for adding bedrooms, bathrooms, kitchens or any structural and electrical work. We pull all permits and schedule inspections."),
            ("Can I add a rental unit (ADU) in my basement?",
             "Often, yes. Many Salt Lake County cities now allow internal accessory dwelling units. We'll check zoning, walkout/egress requirements and utility separation during the initial consultation."),
        ],
    },
    {
        "slug": "home-additions",
        "num": "05",
        "title": "Home Additions & ADUs",
        "tag": "Add space, value and function",
        "blurb": "Second-story additions, primary suite additions, sunrooms, in-law suites and detached ADUs (casitas), built to look like they were always there.",
        "hero_img": "additions-01",
        "imgs": ["additions-01", "additions-02", "additions-03"],
        "intro": "Outgrew the floor plan but love the neighborhood? We add rooms, stories, suites and detached accessory dwelling units (ADUs / casitas) onto Utah homes every year. Additions are tricky, roofline tie-ins, structural reinforcement, utility runs, and we handle every piece of it so the finished result looks original.",
        "what_we_do": [
            "Second-story additions with engineered floor systems and stair design",
            "Primary suite additions: bedroom, bath, walk-in closet, sitting area",
            "Detached ADUs (casitas) for guests, rental income or aging in place",
            "Sunrooms, three-season rooms and conditioned greenhouses",
            "Garage additions, workshop additions, detached studios",
            "Roof, siding and trim integration with existing structure",
            "Structural reinforcement, foundation tie-ins, utility extensions",
        ],
        "faq": [
            ("Is it cheaper to add on or move?",
             "Almost always cheaper to add on, and you keep the lot, the neighborhood, the schools, the trees. We can give you a realistic cost-vs-move analysis in our first meeting."),
            ("Can you add a second story to a 1950s or 60s home?",
             "Yes. Older Utah homes usually require structural reinforcement of the foundation and existing walls, and we'll evaluate that before quoting. We've added second stories to ramblers and bungalows across the Wasatch Front."),
            ("Are ADUs legal in Utah?",
             "Utah state law now broadly allows internal ADUs, and most cities allow detached ADUs with conditions on lot size and parking. We help you navigate local zoning."),
        ],
    },
    {
        "slug": "outdoor-living",
        "num": "06",
        "title": "Outdoor Living",
        "tag": "Patios, pergolas, kitchens, pools",
        "blurb": "Outdoor kitchens, covered patios, pergolas, pools, fire features and mountain-view living rooms designed for Utah's seasons.",
        "hero_img": "outdoor-01",
        "imgs": ["outdoor-01", "outdoor-02", "outdoor-03"],
        "intro": "Utah outdoors is the reason most of us live here. We design and build outdoor living spaces that work nine months of the year, covered patios with heaters and motorized screens, outdoor kitchens, fire pits, fireplaces, pergolas, infinity pools and hardscape that integrates seamlessly with the home and the mountains.",
        "what_we_do": [
            "Covered patios and pavilions with structural roof systems",
            "Outdoor kitchens, built-in grills, pizza ovens, refrigeration, sinks",
            "Fire pits, gas fireplaces, fire bowls and fire tables",
            "Pergolas and louvered roof systems (Struxure, Equinox)",
            "Pools, spas, swim-jet pools and integrated water features",
            "Landscape lighting, low-voltage zones and smart control",
            "Stone, paver and concrete hardscape with proper drainage",
        ],
        "faq": [
            ("When is the best time to build an outdoor living space in Utah?",
             "We build year-round but plan most projects for completion by Memorial Day. Reach out in fall or winter for the best installer availability and finish before summer entertaining season."),
            ("Do I need a permit for a covered patio or pergola?",
             "Most permanent structures require permits, we handle them. Detached pergolas under a certain size and with no electrical sometimes don't, but we always confirm with the AHJ first."),
        ],
    },
    {
        "slug": "commercial-construction",
        "num": "07",
        "title": "Commercial & TI",
        "tag": "Tenant improvements, buildouts, retail",
        "blurb": "Commercial tenant improvements, restaurant and bar buildouts, retail finish-outs and office reconfigurations along the Wasatch Front.",
        "hero_img": "commercial-01",
        "imgs": ["commercial-01", "commercial-02", "commercial-03"],
        "intro": "Commercial work demands a different operating tempo: tighter deadlines, lease-driven schedules, landlord coordination and inspector relationships. Multiworks runs a dedicated commercial division for tenant improvements (TI), restaurant and bar buildouts, retail finish-outs and office and medical-suite reconfigurations.",
        "what_we_do": [
            "Tenant improvements for office, medical, dental and professional space",
            "Restaurant and bar buildouts: kitchen, hood, grease, finish",
            "Retail storefront finish-outs and fit-outs",
            "Office and medical-suite reconfigurations",
            "ADA compliance retrofits and accessibility upgrades",
            "Mechanical, electrical and plumbing rework for new use",
            "Landlord coordination, lease milestone management",
        ],
        "faq": [
            ("Do you work with landlords and property managers?",
             "Yes. much of our commercial work is initiated by property owners and managers for TI buildouts. We handle landlord work-letter compliance, scope reconciliation and final lien releases."),
            ("How fast can you turn around a TI buildout?",
             "A simple office TI can finish in 6 to 10 weeks. Restaurants and medical buildouts run 12 to 24 weeks depending on permitting and equipment lead times. We give you a written milestone schedule before lease commencement."),
        ],
    },
    {
        "slug": "design-build",
        "num": "08",
        "title": "Design-Build Services",
        "tag": "One team, one contract",
        "blurb": "Architecture, interior design and construction under one roof, fewer handoffs, faster decisions, no finger-pointing.",
        "hero_img": "design-build-01",
        "imgs": ["design-build-01", "design-build-02", "design-build-03"],
        "intro": "Design-build is the most efficient way to plan and execute a major construction project. Architecture, engineering, interior design and construction live on the same team and the same contract. Decisions get made faster, change orders shrink, and there's never a finger-point between architect and contractor when something needs solving.",
        "what_we_do": [
            "Full architectural design (remodels, additions, ADUs, commercial)",
            "Interior design, material selections and FF&E specification",
            "Structural and MEP engineering coordination",
            "3D renderings, virtual walk-throughs, sample boards",
            "Single fixed-fee contract spanning design through construction",
            "Permitting, plan check and jurisdictional coordination",
            "Single point of accountability from first sketch to final walk-through",
        ],
        "faq": [
            ("How is design-build different from design-bid-build?",
             "Design-bid-build splits the project across an architect and a contractor with two separate contracts. Design-build keeps them on one team with one contract, which usually means faster timelines, fewer change orders and aligned incentives."),
            ("Will design-build cost more?",
             "Almost always less, when you account for the full project. Construction-aware design avoids the expensive change orders that happen when an architect designs without contractor input."),
        ],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

SERVICE_AREAS = [
    "Salt Lake City", "Park City", "Holladay", "Cottonwood Heights", "Sandy",
    "Draper", "Murray", "Millcreek", "South Jordan", "West Jordan", "Riverton",
    "Herriman", "Bluffdale", "Lehi", "Alpine", "Highland", "American Fork",
    "Pleasant Grove", "Orem", "Provo", "Bountiful", "Centerville", "Farmington",
    "Kaysville", "Layton", "Heber City", "Midway", "Deer Valley"
]

PROCESS = [
    ("Consult", "We meet at your property or our office, walk the project, listen carefully, and put a realistic budget and timeline on the table, usually inside a week."),
    ("Design", "Plans, elevations, 3D renderings and a written specification. You see exactly what you're getting before a single dollar of construction is spent."),
    ("Build", "One project manager, one schedule, dedicated trades. Bi-weekly updates with photos, milestones and any change orders signed before work proceeds."),
    ("Hand-off", "Final walk-through, punch list completion, warranty package, and a complete project handbook covering every system, finish, and serial number installed."),
]

# ----------------------------------------------------------------
# Page template
# ----------------------------------------------------------------

def esc(s):
    return html.escape(s, quote=True)

def common_head(title, description, canonical_path, og_image_name, extra_jsonld=None, body_class=""):
    og_image = absolute_url(img(og_image_name) if og_image_name else img("hero-01"))
    canonical = f"{DOMAIN}{canonical_path}"
    local_business_jsonld = {
        "@context": "https://schema.org",
        "@type": ["GeneralContractor", "HomeAndConstructionBusiness", "LocalBusiness"],
        "name": BRAND_FULL,
        "alternateName": BRAND,
        "url": DOMAIN,
        "telephone": PHONE,
        "email": EMAIL,
        "image": og_image,
        "logo": og_image,
        "description": SITE_DESC_SHORT,
        "priceRange": "$$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": ADDRESS_LOCALITY,
            "addressRegion": ADDRESS_STATE,
            "postalCode": ADDRESS_POSTAL,
            "addressCountry": "US",
        },
        "areaServed": [{"@type": "City", "name": a} for a in SERVICE_AREAS],
        "sameAs": [],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Construction & Remodeling Services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {"@type": "Service", "name": s["title"], "url": f"{DOMAIN}/{s['slug']}.html"}
                }
                for s in SERVICES
            ],
        },
    }
    jsonld_blocks = [json.dumps(local_business_jsonld)]
    if extra_jsonld:
        for block in (extra_jsonld if isinstance(extra_jsonld, list) else [extra_jsonld]):
            jsonld_blocks.append(json.dumps(block))
    scripts = "\n".join(
        f'<script type="application/ld+json">{b}</script>' for b in jsonld_blocks
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(BRAND_FULL)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{esc(og_image)}">
<meta name="theme-color" content="#1A1A1A">
<meta name="geo.region" content="US-UT">
<meta name="geo.placename" content="Salt Lake City, Utah">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{absolute_url(img(og_image_name)) if og_image_name else absolute_url(img('hero-01'))}" fetchpriority="high">
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Sora:wght@400;500;600&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Sora:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/styles.css">
{scripts}
</head>
<body{(' class="' + body_class + '"') if body_class else ''}>"""

def nav_block(current=""):
    def li(slug, label, href=None):
        href = href if href else f"/{slug}.html"
        active = " is-active" if current == slug else ""
        return f'<li><a href="{href}" class="{active.strip()}">{label}</a></li>'
    return f"""<header class="nav{' is-light' if current not in ('home','') else ''}">
  <div class="nav__inner">
    <a class="brand" href="/" aria-label="{esc(BRAND_FULL)} home">
      <span class="brand__mark">Multiworks</span>
      <span class="brand__sub">Construction · Utah</span>
    </a>
    <ul class="nav__links">
      {li('home','Home','/')}
      {li('services','Services')}
      {li('about','About')}
      {li('portfolio','Portfolio')}
      {li('contact','Contact')}
    </ul>
    <a class="nav__cta" href="tel:{PHONE_TEL}">{PHONE}</a>
    <button class="nav__toggle" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>
<a class="tap-call" href="tel:{PHONE_TEL}">Call {PHONE}</a>
"""

def cta_band(headline="Ready to build something remarkable?",
             body=f"Schedule a no-pressure consultation with our Utah team. We'll listen, walk the project, and put real numbers and a real timeline on paper, usually inside a week."):
    return f"""<section class="cta-band">
  <div class="wrap reveal">
    <span class="eyebrow">Let's talk</span>
    <h2>{headline}</h2>
    <p class="cta-band__body">{body}</p>
    <a class="phone" href="tel:{PHONE_TEL}">{PHONE}</a><br>
    <a class="btn btn--ghost-light" href="/contact.html">Start a project <span class="arrow">→</span></a>
  </div>
</section>"""

def footer_block():
    service_lis = "\n".join(f'<li><a href="/{s["slug"]}.html">{esc(s["title"])}</a></li>' for s in SERVICES)
    areas_lis = "\n".join(f'<li>{esc(a)}</li>' for a in SERVICE_AREAS[:12])
    year = datetime.datetime.now().year
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <div class="brand">
          <span class="brand__mark">Multiworks</span>
          <span class="brand__sub">Construction · Utah</span>
        </div>
        <p class="footer__about">A Utah high-end remodeling contractor for whole-home remodels, kitchens, baths, basements, additions and commercial buildouts. Licensed. Insured. Locally owned.</p>
      </div>
      <div>
        <h3 class="footer__heading">Services</h3>
        <ul>{service_lis}</ul>
      </div>
      <div>
        <h3 class="footer__heading">Service Areas</h3>
        <ul>{areas_lis}</ul>
      </div>
      <div class="footer__contact">
        <h3 class="footer__heading">Contact</h3>
        <a class="phone" href="tel:{PHONE_TEL}">{PHONE}</a>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>{ADDRESS_LOCALITY}, {ADDRESS_STATE}</p>
        <p>Mon–Fri 7:30a – 5:30p</p>
        <p>Sat by appointment</p>
      </div>
    </div>
    <div class="footer__bottom">
      <div>© {year} {esc(BRAND_FULL)} · Licensed &amp; Insured Utah General Contractor</div>
      <div><a href="/services.html">Services</a> · <a href="/contact.html">Contact</a> · <a href="/sitemap.xml">Sitemap</a></div>
    </div>
  </div>
</footer>
<script src="/assets/nav.js" defer></script>
</body></html>"""

# ----------------------------------------------------------------
# Page builders
# ----------------------------------------------------------------

def page_home():
    # Hero: five <img> elements (was ten data-bg divs). First eagerly loaded + fetchpriority high,
    # rest lazy. Each carries real descriptive alt text, WCAG 1.1.1 was failing site-wide.
    slides_html = "\n".join(
        f'<img class="hero__slide{" is-active" if i==0 else ""}" '
        f'src="{img(name)}" alt="{esc(alt)}" '
        f'loading="{"eager" if i==0 else "lazy"}" '
        f'decoding="{"sync" if i==0 else "async"}" '
        f'fetchpriority="{"high" if i==0 else "low"}" '
        f'width="1376" height="768">'
        for i, (name, alt) in enumerate(HERO)
    )
    service_cards = "\n".join(service_card_html(s) for s in SERVICES)
    areas_div = "\n".join(f"<div>{esc(a)}</div>" for a in SERVICE_AREAS)
    home_faqs = [
        ("Where in Utah does Multiworks Construction work?",
         "We serve the entire Wasatch Front: Salt Lake City, Park City, Holladay, Sandy, Draper, Lehi, Provo, Bountiful, Cottonwood Heights and surrounding communities in Salt Lake, Utah, Summit and Davis counties."),
        ("Are you licensed and insured in Utah?",
         "Yes. Multiworks Construction LLC is a fully licensed Utah general contractor carrying commercial general liability and workers' comp insurance. Documentation is available on request."),
        ("Do you handle architecture and design, or only construction?",
         "Both. Our design-build team handles architecture, interior design, structural engineering and construction under one contract. We're also happy to work with architects and designers you've already chosen."),
        ("How do you price projects: fixed bid or cost-plus?",
         "We default to a transparent fixed-fee model. After selections are made, we lock the construction price with a clear allowance schedule. Cost-plus is offered on highly custom or unique projects."),
        ("How long is the wait to start a new project?",
         "Lead times vary by project size and trade availability. We typically schedule new project starts 6 to 12 weeks out and can sometimes start sooner. Call us for current availability."),
        ("What sets Multiworks apart from other Utah remodelers?",
         "Single point of accountability, transparent fixed-fee pricing, in-house design and trades, written milestone schedules, and a 24-month workmanship warranty on every project."),
    ]
    faq_html = "\n".join(
        f"""<div class="faq__item"><button class="faq__q" type="button">{esc(q)} <span class="plus">+</span></button><div class="faq__a"><p>{esc(a)}</p></div></div>"""
        for q, a in home_faqs
    )
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in home_faqs
        ],
    }
    return common_head(
        title=f"Multiworks Construction LLC | Utah High-End Remodeler & Design-Build Contractor, {ADDRESS_LOCALITY}",
        description=SITE_DESC_SHORT,
        canonical_path="/",
        og_image_name="hero-01",
        extra_jsonld=faq_jsonld,
    ) + nav_block(current="home") + f"""
<section class="hero" id="top">
  <div class="hero__bg">{slides_html}</div>
  <div class="hero__inner">
    <span class="eyebrow hero__eyebrow">Salt Lake City · Park City · Wasatch Front</span>
    <h1 class="hero__title">Utah high-end remodels, built without compromise.</h1>
    <p class="hero__sub">Multiworks Construction is a Utah remodeling and design-build contractor for clients who refuse to settle. Kitchens, bathrooms, whole-home transformations, additions, and commercial buildouts. One schedule, one team, one standard.</p>
    <div class="hero__cta">
      <a class="btn btn--solid" href="/contact.html">Start a project <span class="arrow">→</span></a>
      <a class="btn btn--ghost-light" href="tel:{PHONE_TEL}">Call {PHONE}</a>
    </div>
  </div>
  <div class="hero__meta">{PHONE}</div>
</section>

<section class="section section--paper">
  <div class="wrap split reveal">
    <div>
      <span class="eyebrow">Multiworks Construction</span>
      <h2>A Utah remodeler for homes built to outlast trends.</h2>
    </div>
    <div>
      <p class="lead">We remodel high-end homes along the Wasatch Front for clients who'd rather wait six months to do it right than three to do it twice. Every project gets a dedicated project manager, a written milestone schedule, transparent fixed-fee pricing, and a 24-month workmanship warranty.</p>
      <p>From kitchen reworks in Holladay and Park City to floor-to-ceiling whole-home remodels in Sugar House and basement build-outs in Sandy, we run every job the way we'd want our own homes run.</p>
      <a class="btn btn--ghost" href="/about.html">About Multiworks <span class="arrow">→</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">What we do</span>
      <h2>What we build for Utah homes.</h2>
      <p class="lead">From design and architecture through final punch list, Multiworks self-performs the work that matters and partners only with Utah trades we'd hire to work on our own homes.</p>
    </div>
  </div>
  <div class="wrap reveal">
    <div class="service-grid">
      {service_cards}
    </div>
  </div>
</section>

<aside class="trust-strip reveal" aria-label="License and credentials">
  <div class="wrap trust-strip__row">
""" + "\n".join(f'    <span class="trust-strip__item">{esc(p)}</span>' for p in TRUST_POINTS) + f"""
  </div>
</aside>

<section class="section section--ink">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">How we work</span>
      <h2 class="on-ink">The Multiworks process.</h2>
    </div>
    <div class="process reveal">
""" + "\n".join(
        f"""<div class="process__step"><div class="process__num">{i+1:02d}</div><div class="process__title">{esc(t)}</div><div class="process__desc">{esc(d)}</div></div>"""
        for i, (t, d) in enumerate(PROCESS)
    ) + f"""
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap reveal">
    <div class="testimonial">
      <span class="eyebrow eyebrow--mute eyebrow--block">A recent client</span>
      <p class="testimonial__quote">"Multiworks didn't just remodel our home. They protected our investment, our schedule, and our sanity. Every milestone hit on time. Every change order arrived in writing before work started. It's the way construction is supposed to work."</p>
      <div class="testimonial__attr">Holladay, Utah · Whole-Home Remodel Client</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head section__head--center reveal">
      <span class="eyebrow">Service areas</span>
      <h2>Across the Wasatch Front.</h2>
      <p>Salt Lake County, Utah County, Summit County and Davis County, plus the in-between mountain communities most contractors won't drive to.</p>
    </div>
    <div class="areas-grid reveal">{areas_div}</div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section__head section__head--center reveal">
      <span class="eyebrow">Common questions</span>
      <h2>What clients ask before they hire us.</h2>
    </div>
    <div class="faq reveal">{faq_html}</div>
  </div>
</section>

{cta_band()}
{footer_block()}"""

def page_service(s):
    # Triptych converted from data-bg divs to <img> with descriptive alt text per image.
    triptych = "\n".join(
        f'<div class="triptych__item"><img src="{img(name)}" alt="{esc(alt_for(name))}" loading="lazy" decoding="async" width="800" height="600"></div>'
        for name in s["imgs"]
    )
    # Scope-of-work bullets now use a real class (.scope-list) instead of inline-styled serif rules.
    # Critique flagged the previous Cormorant 1.15rem with per-item rules as visually noisy.
    bullets = "\n".join(f"<li>{esc(b)}</li>" for b in s["what_we_do"])
    # Service title rendered with proper casing for headlines (fixes "commercial & ti" lowercase bug).
    pretty_title = s["title"]
    pretty_lower = pretty_title  # keep original case in body prose
    faq_html = "\n".join(
        f"""<div class="faq__item"><button class="faq__q" type="button">{esc(q)} <span class="plus">+</span></button><div class="faq__a"><p>{esc(a)}</p></div></div>"""
        for q, a in s["faq"]
    )
    other_services = [x for x in SERVICES if x["slug"] != s["slug"]][:3]
    related_cards = "\n".join(service_card_html(x) for x in other_services)
    service_jsonld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["title"],
        "description": s["blurb"],
        "provider": {"@type": "GeneralContractor", "name": BRAND_FULL, "telephone": PHONE, "url": DOMAIN},
        "areaServed": [{"@type": "City", "name": a} for a in SERVICE_AREAS],
        "url": f"{DOMAIN}/{s['slug']}.html",
        "serviceType": s["title"],
    }
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in s["faq"]
        ],
    }
    return common_head(
        title=f"{s['title']} in Utah | Salt Lake City & Park City · Multiworks Construction",
        description=f"{s['blurb']} Licensed Utah general contractor serving Salt Lake City, Park City and the Wasatch Front. Call {PHONE}.",
        canonical_path=f"/{s['slug']}.html",
        og_image_name=s["hero_img"],
        extra_jsonld=[service_jsonld, faq_jsonld],
    ) + nav_block(current=s["slug"]) + f"""
<section class="page-hero">
  <div class="page-hero__bg"><img src="{img(s['hero_img'])}" alt="{esc(alt_for(s['hero_img']))}" loading="eager" fetchpriority="high" decoding="sync" width="1376" height="768"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · <a href="/services.html">Services</a> · {esc(pretty_title)}</div>
    <span class="eyebrow">Service {s['num']} · {esc(s['tag'])}</span>
    <h1 class="page-hero__title">{esc(pretty_title)} in Utah.</h1>
    <p class="page-hero__sub">{esc(s['blurb'])}</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap split split--narrow reveal">
    <div>
      <span class="eyebrow">What this is</span>
      <h2>A better way to do {esc(pretty_lower)}.</h2>
    </div>
    <div>
      <p class="lead">{esc(s['intro'])}</p>
      <a class="btn btn--ghost" href="/contact.html">Start your project <span class="arrow">→</span></a>
    </div>
  </div>
  <div class="wrap reveal">
    <div class="triptych">{triptych}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split reveal">
    <div>
      <span class="eyebrow">Scope of work</span>
      <h2>What's included in our {esc(pretty_lower)} service.</h2>
      <p>Every project is custom, but here's what most {esc(pretty_lower)} engagements with Multiworks include from kickoff to final walk-through:</p>
    </div>
    <div>
      <ul class="scope-list">{bullets}</ul>
    </div>
  </div>
</section>

<section class="section section--ink">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">How we deliver</span>
      <h2 class="on-ink">The Multiworks process.</h2>
    </div>
    <div class="process reveal">
""" + "\n".join(
        f"""<div class="process__step"><div class="process__num">{i+1:02d}</div><div class="process__title">{esc(t)}</div><div class="process__desc">{esc(d)}</div></div>"""
        for i, (t, d) in enumerate(PROCESS)
    ) + f"""
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section__head section__head--center reveal">
      <span class="eyebrow">Common questions</span>
      <h2>{esc(pretty_title)}, frequently asked.</h2>
    </div>
    <div class="faq reveal">{faq_html}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">Related work</span>
      <h2>Other ways we build.</h2>
    </div>
  </div>
  <div class="wrap reveal">
    <div class="service-grid">{related_cards}</div>
  </div>
</section>

{cta_band(headline=f"Ready to start your {esc(pretty_lower)} project?")}
{footer_block()}"""

def page_services():
    service_cards = "\n".join(service_card_html(s) for s in SERVICES)
    return common_head(
        title=f"Construction & Remodeling Services in Utah | Multiworks Construction",
        description="Custom home building, whole-home remodeling, kitchen and bathroom remodels, basement finishing, additions, ADUs, outdoor living and commercial construction in Salt Lake City, Park City and the Wasatch Front.",
        canonical_path="/services.html",
        og_image_name="hero-02",
    ) + nav_block(current="services") + f"""
<section class="page-hero">
  <div class="page-hero__bg"><img src="{img('hero-02')}" alt="{esc(alt_for('hero-02') if 'hero-02' in IMAGE_ALTS else 'Multiworks Construction project: Park City whole-home remodel exterior')}" loading="eager" fetchpriority="high" decoding="sync" width="1376" height="768"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · Services</div>
    <span class="eyebrow">Our services</span>
    <h1 class="page-hero__title">Every way we build, under one roof.</h1>
    <p class="page-hero__sub">From kitchen reworks to whole-home transformations and commercial tenant improvements, every service Multiworks delivers is held to the same standard: written schedule, fixed-fee pricing, dedicated project manager, 24-month warranty.</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap reveal">
    <h2 class="sr-only">What we build</h2>
    <div class="service-grid">{service_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head section__head--center reveal">
      <span class="eyebrow">How we work</span>
      <h2>The Multiworks process.</h2>
      <p>A predictable, documented path from first call to final keys.</p>
    </div>
    <div class="process reveal">
""" + "\n".join(
        f"""<div class="process__step"><div class="process__num">{i+1:02d}</div><div class="process__title">{esc(t)}</div><div class="process__desc">{esc(d)}</div></div>"""
        for i, (t, d) in enumerate(PROCESS)
    ) + f"""
    </div>
  </div>
</section>

{cta_band()}
{footer_block()}"""

def page_about():
    return common_head(
        title="About Multiworks Construction | Utah High-End Remodeler & Design-Build Contractor",
        description="Multiworks Construction LLC is a Utah-owned high-end remodeler serving Salt Lake City, Park City and the Wasatch Front. Licensed, insured, locally rooted.",
        canonical_path="/about.html",
        og_image_name="hero-05",
    ) + nav_block(current="about") + f"""
<section class="page-hero">
  <div class="page-hero__bg"><img src="{img('hero-05')}" alt="{esc(alt_for('hero-05'))}" loading="eager" fetchpriority="high" decoding="sync" width="1376" height="768"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · About</div>
    <span class="eyebrow">About Multiworks</span>
    <h1 class="page-hero__title">Utah-built. Client-aligned. No drama.</h1>
    <p class="page-hero__sub">Multiworks Construction LLC is a Utah-owned high-end remodeling contractor. We remodel existing homes, build thoughtful additions, and finish out commercial spaces along the Wasatch Front, for clients who'd rather hire one team than coordinate five.</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap split reveal">
    <div class="split__image"><img src="{img('design-build-02')}" alt="{esc(alt_for('design-build-02'))}" loading="lazy" decoding="async" width="800" height="1000"></div>
    <div>
      <span class="eyebrow">Our story</span>
      <h2>A contractor that actually answers the phone.</h2>
      <p class="lead">Multiworks Construction was founded on a simple frustration: too many Utah construction projects start with a smile and a promise, then drift into missed milestones, mystery change orders, and silent project managers.</p>
      <p>We built Multiworks to be the contractor we wish we'd hired. Single point of accountability. Written milestone schedules. Fixed-fee pricing. Change orders signed before work starts, never after. The people who answer your call on Tuesday are the same people swinging hammers on your job Wednesday.</p>
      <a class="btn btn--ghost" href="/contact.html">Start a project <span class="arrow">→</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">What we believe</span>
      <h2>Four principles we won't compromise on.</h2>
    </div>
    <div class="process reveal">
      <div class="principle"><div class="principle__mark" aria-hidden="true"></div><div class="process__title">Single accountability</div><div class="process__desc">One contract, one project manager, one number to call. Never "that's the architect's problem" or "talk to the subcontractor".</div></div>
      <div class="principle"><div class="principle__mark" aria-hidden="true"></div><div class="process__title">Transparent pricing</div><div class="process__desc">Fixed-fee proposals with itemized line items and a clear allowance schedule. No mystery markups. No silent change orders.</div></div>
      <div class="principle"><div class="principle__mark" aria-hidden="true"></div><div class="process__title">Written schedule</div><div class="process__desc">A milestone-based schedule before work begins, updated every two weeks with photos and progress against the plan.</div></div>
      <div class="principle"><div class="principle__mark" aria-hidden="true"></div><div class="process__title">Local trades, local pride</div><div class="process__desc">We work with Utah's most skilled trades and treat them well. That's how you keep talent on your job instead of someone else's.</div></div>
    </div>
  </div>
</section>

<section class="section section--ink">
  <div class="wrap reveal">
    <div class="testimonial">
      <span class="eyebrow eyebrow--block">A recent client</span>
      <p class="testimonial__quote">"You don't realize how rare honest construction is until you've experienced it. Multiworks ran our remodel like a Swiss watch and made it look easy."</p>
      <div class="testimonial__attr">Park City · Remodel Client</div>
    </div>
  </div>
</section>

{cta_band()}
{footer_block()}"""

def page_portfolio():
    # Portfolio reorganized into per-service groups: visible H2 per group, visible captions
    # under each figure (was hover-only — broken on touch), inline <style> moved to styles.css
    # so the CSP can drop 'unsafe-inline'.
    PORTFOLIO_CITIES = ["Park City", "Holladay", "Sandy", "Salt Lake City", "Draper",
                        "Cottonwood Heights", "Lehi", "Bountiful"]

    def group_html(s, idx):
        cards = []
        for j, name in enumerate(s["imgs"]):
            city = PORTFOLIO_CITIES[(idx * 3 + j) % len(PORTFOLIO_CITIES)]
            cards.append(
                f'<figure class="portfolio__item">\n'
                f'  <img src="{img(name)}" alt="{esc(alt_for(name))}" loading="lazy" decoding="async" width="800" height="600">\n'
                f'  <figcaption class="portfolio__caption"><strong>{esc(s["title"])}</strong> &middot; {esc(city)}</figcaption>\n'
                f'</figure>'
            )
        return (
            f'<section class="portfolio-group reveal" aria-labelledby="pg-{s["slug"]}">\n'
            f'  <header class="portfolio-group__head">\n'
            f'    <h2 class="portfolio-group__title" id="pg-{s["slug"]}">{esc(s["title"])}</h2>\n'
            f'    <span class="portfolio-group__count">{len(s["imgs"])} projects</span>\n'
            f'  </header>\n'
            f'  <div class="portfolio-grid">\n'
            + "\n".join(cards) + "\n"
            f'  </div>\n'
            f'</section>'
        )

    groups = "\n".join(group_html(s, i) for i, s in enumerate(SERVICES))

    return common_head(
        title="Portfolio | Utah Remodels, Additions & Commercial · Multiworks Construction",
        description="A selection of Multiworks Construction's recent Utah projects: whole-home remodels, kitchens, baths, basements, additions, outdoor living, and commercial buildouts in Salt Lake City and Park City.",
        canonical_path="/portfolio.html",
        og_image_name="whole-home-01",
    ) + nav_block(current="portfolio") + f"""
<section class="page-hero">
  <div class="page-hero__bg"><img src="{img('whole-home-01')}" alt="{esc(alt_for('whole-home-01'))}" loading="eager" fetchpriority="high" decoding="sync" width="1376" height="768"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> &middot; Portfolio</div>
    <span class="eyebrow">Selected work</span>
    <h1 class="page-hero__title">A selection of recent work.</h1>
    <p class="page-hero__sub">Whole-home remodels, kitchens, baths, basements, additions, and outdoor living spaces from across Utah's Wasatch Front.</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">Browse the work</span>
      <h2>Every photo here is a real project.</h2>
    </div>
    {groups}
  </div>
</section>

{cta_band(headline="See something you like? Let's build yours.")}
{footer_block()}"""

def page_contact():
    return common_head(
        title="Contact Multiworks Construction | Utah General Contractor, Call or Get a Quote",
        description=f"Contact Multiworks Construction LLC for high-end remodels, additions and commercial work in Utah. Call {PHONE} or request a no-pressure consultation. Serving Salt Lake City, Park City and the Wasatch Front.",
        canonical_path="/contact.html",
        og_image_name="hero-08",
        body_class="page-contact",
    ) + nav_block(current="contact") + f"""
<section class="page-hero">
  <div class="page-hero__bg"><img src="{img('hero-08')}" alt="{esc(alt_for('hero-08') if 'hero-08' in IMAGE_ALTS else 'Multiworks Construction job site walkthrough')}" loading="eager" fetchpriority="high" decoding="sync" width="1376" height="768"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · Contact</div>
    <span class="eyebrow">Let's talk</span>
    <h1 class="page-hero__title">Start your Utah project.</h1>
    <p class="page-hero__sub">Call us, email us, or fill out the form. We'll respond within one business day, schedule a no-pressure site walk, and put real numbers and a real timeline on paper, usually within a week.</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap contact-grid reveal">
    <div class="contact-card">
      <h2>Get in touch.</h2>
      <div class="contact-card__row">
        <div class="contact-card__label">Phone</div>
        <div class="contact-card__value"><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
      </div>
      <div class="contact-card__row">
        <div class="contact-card__label">Email</div>
        <div class="contact-card__value"><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      </div>
      <div class="contact-card__row">
        <div class="contact-card__label">Hours</div>
        <div class="contact-card__value">Mon–Fri 7:30a – 5:30p<br>Sat by appointment</div>
      </div>
      <div class="contact-card__row">
        <div class="contact-card__label">Service area</div>
        <div class="contact-card__value">Salt Lake County · Utah County · Summit County · Davis County</div>
      </div>
    </div>
    <div>
      <h2>Request a consultation.</h2>
      <p class="form-intro">Tell us about your project. The more detail you can share, the more useful our first conversation will be.</p>
      <form class="form" id="contactForm" action="/api/contact" method="post" novalidate>
        <div class="form__row">
          <div><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
          <div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="form__row">
          <div><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div><label for="city">City</label><input id="city" name="city" type="text" autocomplete="address-level2" placeholder="Salt Lake City, Park City"></div>
        </div>
        <div>
          <label for="service">Project type</label>
          <select id="service" name="service">
            <option value="">Select a service</option>
""" + "\n".join(f'<option value="{esc(s["title"])}">{esc(s["title"])}</option>' for s in SERVICES) + f"""
            <option value="Not sure yet">Not sure yet</option>
          </select>
        </div>
        <div>
          <label for="budget">Approximate budget</label>
          <select id="budget" name="budget">
            <option value="">Select a range</option>
            <option>Under $100K</option>
            <option>$100K to $250K</option>
            <option>$250K to $500K</option>
            <option>$500K to $1M</option>
            <option>$1M to $3M</option>
            <option>$3M+</option>
            <option>Not sure yet</option>
          </select>
        </div>
        <div>
          <label for="msg">Project details</label>
          <textarea id="msg" name="message" rows="5" placeholder="Tell us about your project, timeline, and anything else that'd help us prepare for our first call."></textarea>
        </div>
        <!-- Honeypot: real users leave this blank; bots fill every field. -->
        <div class="hp" aria-hidden="true">
          <label for="company">Company</label>
          <input id="company" name="company" type="text" tabindex="-1" autocomplete="off">
        </div>
        <div>
          <button class="btn btn--solid" type="submit" id="contactSubmit">
            <span class="btn__label">Send message</span>
            <span class="arrow">&rarr;</span>
          </button>
        </div>
        <p class="form-disclaimer">By submitting, you agree to be contacted about your project. We don't share your information.</p>
        <div class="form-status" id="formStatus" role="status" aria-live="polite"></div>
      </form>
      <noscript>
        <p class="form-disclaimer">Form submission needs JavaScript. You can email us directly at <a href="mailto:{EMAIL}">{EMAIL}</a> or call {PHONE}.</p>
      </noscript>
    </div>
  </div>
</section>

{footer_block()}"""

# ----------------------------------------------------------------
# Sitemap / robots
# ----------------------------------------------------------------
def sitemap_xml():
    paths = ["/", "/services.html", "/about.html", "/portfolio.html", "/contact.html"]
    paths.extend(f"/{s['slug']}.html" for s in SERVICES)
    today = datetime.date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{'1.0' if p=='/' else '0.8'}</priority></url>"
        for p in paths
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""

ROBOTS = f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""

# ----------------------------------------------------------------
# Emit everything
# ----------------------------------------------------------------
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path}  ({len(content):,} bytes)")

def main():
    print("Building Multiworks Construction site…")
    write("index.html", page_home())
    write("services.html", page_services())
    write("about.html", page_about())
    write("portfolio.html", page_portfolio())
    write("contact.html", page_contact())
    for s in SERVICES:
        write(f"{s['slug']}.html", page_service(s))
    write("sitemap.xml", sitemap_xml())
    write("robots.txt", ROBOTS)
    print("Done.")

if __name__ == "__main__":
    main()
