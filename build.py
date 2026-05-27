#!/usr/bin/env python3
"""Multiworks Construction LLC — static site generator.

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
SITE_DESC_SHORT = "Utah's design-build general contractor — custom homes, whole-home remodels, kitchens, baths and commercial construction. Licensed. Insured. On time. On budget."

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
        "slug": "custom-home-building",
        "num": "01",
        "title": "Custom Home Building",
        "tag": "Ground-up custom residential",
        "blurb": "Ground-up custom homes built to your land, your lifestyle and your standards — from foundation to final walk-through.",
        "hero_img": "custom-home-01",
        "imgs": ["custom-home-01", "custom-home-02", "custom-home-03"],
        "intro": "Building a custom home is the single largest project most families ever undertake. We treat it that way. Multiworks Construction is a full-service Utah custom home builder serving Salt Lake City, Park City, Holladay, Draper, Sandy and the surrounding Wasatch Front. Every home we build is engineered for the site, the climate and the people who'll live in it — not pulled from a stock catalog.",
        "what_we_do": [
            "Lot evaluation, feasibility and site planning",
            "Architectural design and structural engineering",
            "Permitting and code compliance with city and county jurisdictions",
            "Foundation, framing, mechanical, electrical and plumbing rough-in",
            "Custom millwork, cabinetry and interior finish carpentry",
            "Smart-home pre-wire, lighting design and integrated AV",
            "Final landscape, hardscape and exterior detailing",
        ],
        "faq": [
            ("How long does it take to build a custom home in Utah?",
             "From the day permits are issued, most of our custom homes take 10–14 months to complete. Permitting, design and selections typically add another 3–6 months on the front end. We give you a written, milestone-based schedule before construction begins and update it every two weeks."),
            ("Do you work from an architect we already hired, or do you have your own?",
             "Both. We work seamlessly with outside architects you already love, and we also have a design-build team in-house for clients who want a single point of accountability from concept through move-in."),
            ("How is pricing structured — fixed bid or cost-plus?",
             "We default to a transparent fixed-fee model: we lock construction cost upfront after selections, with a clear allowance schedule and itemized line items. Cost-plus is available on highly custom or unique projects when fixed bid would unfairly penalize you with risk premiums."),
            ("What areas of Utah do you build in?",
             "Salt Lake County, Utah County, Summit County and Davis County — including Salt Lake City, Park City, Deer Valley, Holladay, Draper, Sandy, Lehi, Provo, Bountiful and Cottonwood Heights."),
        ],
    },
    {
        "slug": "whole-home-remodeling",
        "num": "02",
        "title": "Whole-Home Remodeling",
        "tag": "Floor-to-ceiling transformations",
        "blurb": "Reimagine the home you already own. Whole-home remodels, additions and structural reworks that respect the bones and elevate the experience.",
        "hero_img": "whole-home-01",
        "imgs": ["whole-home-01", "whole-home-02", "whole-home-03"],
        "intro": "Sometimes the right move isn't a new build — it's reinventing the home you're already in. Whole-home remodels are our craft. We open walls, raise ceilings, replan flow, modernize systems, and bring older Utah homes up to the standard of new construction — without losing the character that made you love the place to begin with.",
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
             "Often, yes — we plan in phases so one side of the home stays habitable while the other is under construction. For larger or more invasive renovations, we'll be honest if temporary housing is the smarter call."),
            ("How is a whole-home remodel priced?",
             "We provide a fixed-fee proposal after a site walk and a clear scope conversation. The price covers labor, materials, subcontractors and a defined allowance schedule for selections like tile, plumbing fixtures and lighting."),
            ("Will the remodel match the original architecture?",
             "That's the goal whenever you want it to be. We have craftspeople who specialize in seamless additions and historically appropriate finishes — and we're equally happy to take a mid-century or 90s home in a fully modern direction."),
        ],
    },
    {
        "slug": "kitchen-remodeling",
        "num": "03",
        "title": "Kitchen Remodeling",
        "tag": "The most-used room, done right",
        "blurb": "Custom kitchens engineered around how you actually cook, host and live — not a stock layout pulled from a showroom.",
        "hero_img": "kitchen-01",
        "imgs": ["kitchen-01", "kitchen-02", "kitchen-03"],
        "intro": "A kitchen remodel is a high-stakes investment in your daily life and your home's resale value. We approach kitchens as a craft: layout first, then cabinetry, then appliances and finishes. Whether you want a transitional white-and-brass classic, a moody English cottage kitchen or a fully modern chef's space, our team plans, builds and installs every component.",
        "what_we_do": [
            "Layout redesign, island reconfiguration, wall removal",
            "Fully custom cabinetry — paint-grade, stain-grade or quarter-sawn hardwood",
            "Stone, quartz and porcelain countertops, full-height backsplashes",
            "Built-in appliance packages (Wolf, Sub-Zero, Miele, Thermador)",
            "Plumbing, electrical, gas and HVAC reworks to support new layouts",
            "Hood vents, pantry build-outs, butler's pantries, beverage stations",
            "Lighting design — recessed, under-cabinet, decorative pendants",
        ],
        "faq": [
            ("How long does a luxury kitchen remodel take?",
             "Most full kitchen remodels take 10–16 weeks from demo to final punch. Cabinetry lead times drive the schedule — we order early and stage delivery to minimize the time you're without a kitchen."),
            ("What's a typical budget range?",
             "Most of our kitchen projects in Salt Lake City and Park City fall between $80K and $250K, depending on size, custom cabinetry, appliance package and stone selections. We're happy to give you a realistic range during the first conversation."),
            ("Do you handle the design or do I need a separate kitchen designer?",
             "Either works. We have an in-house kitchen designer who handles layout, cabinetry detailing, elevations and selections. We also collaborate often with outside interior designers."),
        ],
    },
    {
        "slug": "bathroom-remodeling",
        "num": "04",
        "title": "Bathroom Remodeling",
        "tag": "Master suites, baths, powder rooms",
        "blurb": "Spa-grade primary baths, guest baths, powder rooms and full master suite remodels — built waterproof, on time, on budget.",
        "hero_img": "bathroom-01",
        "imgs": ["bathroom-01", "bathroom-02", "bathroom-03"],
        "intro": "Bathrooms are unforgiving — every joint has to be waterproof, every fixture has to be right the first time, every tile cut has to line up. Multiworks builds bathrooms the way a yacht is built: methodically, with experienced trades, and zero shortcuts behind the walls. Our master suites, primary baths, guest baths and powder rooms are the most-photographed rooms we finish.",
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
             "A primary bath suite usually takes 6–10 weeks. Guest baths and powder rooms typically finish in 4–6 weeks. We sequence selections and trades to keep momentum without compromise."),
            ("What's a realistic budget for a master bathroom in Utah?",
             "A high-end primary bath in Salt Lake or Park City typically runs $60K–$150K depending on size, stone, tile, fixtures and whether structural changes are involved."),
            ("Will my bathroom be torn up for the whole project?",
             "Demo is just the first week. We protect adjacent floors and finishes, contain dust, and stage trades efficiently so the disruption is concentrated rather than open-ended."),
        ],
    },
    {
        "slug": "basement-finishing",
        "num": "05",
        "title": "Basement Finishing",
        "tag": "Add usable square footage downstairs",
        "blurb": "Unlock thousands of sq ft below grade — theaters, gyms, wine rooms, guest suites, full apartments, and the playroom the kids actually use.",
        "hero_img": "basement-01",
        "imgs": ["basement-01", "basement-02", "basement-03"],
        "intro": "A finished basement is the single highest-ROI square footage you can add to a Utah home. Most of our clients walk in expecting a finished rec room and walk out with a guest suite, a home theater, a wine cellar, a gym, a wet bar, and a place the family actually wants to spend time. We handle egress, framing, mechanical, electrical, plumbing, drywall, finish — and the permits.",
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
             "Most finished basements in our catalog take 8–14 weeks once permits are issued. Larger basements with bathrooms, wet bars and wine rooms run toward the longer end."),
            ("Do I need a permit to finish my basement?",
             "Yes — every Utah municipality requires a permit for adding bedrooms, bathrooms, kitchens or any structural and electrical work. We pull all permits and schedule inspections."),
            ("Can I add a rental unit (ADU) in my basement?",
             "Often, yes. Many Salt Lake County cities now allow internal accessory dwelling units. We'll check zoning, walkout/egress requirements and utility separation during the initial consultation."),
        ],
    },
    {
        "slug": "home-additions",
        "num": "06",
        "title": "Home Additions & ADUs",
        "tag": "Add space, value and function",
        "blurb": "Second-story additions, primary suite additions, sunrooms, in-law suites and detached ADUs (casitas) — built to look like they were always there.",
        "hero_img": "additions-01",
        "imgs": ["additions-01", "additions-02", "additions-03"],
        "intro": "Outgrew the floor plan but love the neighborhood? We add rooms, stories, suites and detached accessory dwelling units (ADUs / casitas) onto Utah homes every year. Additions are tricky — roofline tie-ins, structural reinforcement, utility runs — and we handle every piece of it so the finished result looks original.",
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
             "Almost always cheaper to add on — and you keep the lot, the neighborhood, the schools, the trees. We can give you a realistic cost-vs-move analysis in our first meeting."),
            ("Can you add a second story to a 1950s or 60s home?",
             "Yes. Older Utah homes usually require structural reinforcement of the foundation and existing walls, and we'll evaluate that before quoting. We've added second stories to ramblers and bungalows across the Wasatch Front."),
            ("Are ADUs legal in Utah?",
             "Utah state law now broadly allows internal ADUs, and most cities allow detached ADUs with conditions on lot size and parking. We help you navigate local zoning."),
        ],
    },
    {
        "slug": "outdoor-living",
        "num": "07",
        "title": "Outdoor Living",
        "tag": "Patios, pergolas, kitchens, pools",
        "blurb": "Outdoor kitchens, covered patios, pergolas, pools, fire features and mountain-view living rooms designed for Utah's seasons.",
        "hero_img": "outdoor-01",
        "imgs": ["outdoor-01", "outdoor-02", "outdoor-03"],
        "intro": "Utah outdoors is the reason most of us live here. We design and build outdoor living spaces that work nine months of the year — covered patios with heaters and motorized screens, outdoor kitchens, fire pits, fireplaces, pergolas, infinity pools and hardscape that integrates seamlessly with the home and the mountains.",
        "what_we_do": [
            "Covered patios and pavilions with structural roof systems",
            "Outdoor kitchens — built-in grills, pizza ovens, refrigeration, sinks",
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
             "Most permanent structures require permits — we handle them. Detached pergolas under a certain size and with no electrical sometimes don't, but we always confirm with the AHJ first."),
        ],
    },
    {
        "slug": "commercial-construction",
        "num": "08",
        "title": "Commercial & TI",
        "tag": "Tenant improvements, ground-up, retail",
        "blurb": "Commercial ground-up construction, tenant improvements, restaurant buildouts and retail finish-outs along the Wasatch Front.",
        "hero_img": "commercial-01",
        "imgs": ["commercial-01", "commercial-02", "commercial-03"],
        "intro": "Commercial work demands a different operating tempo: tighter deadlines, lease-driven schedules, landlord coordination and inspector relationships. Multiworks runs a dedicated commercial division for tenant improvements (TI), ground-up commercial, restaurant and bar buildouts, retail finish-outs and small office/mixed-use projects.",
        "what_we_do": [
            "Tenant improvements for office, medical, dental and professional space",
            "Restaurant and bar buildouts: kitchen, hood, grease, finish",
            "Retail storefront finish-outs and fit-outs",
            "Small ground-up commercial: mixed-use, flex, light industrial",
            "ADA compliance retrofits and accessibility upgrades",
            "Mechanical, electrical and plumbing rework for new use",
            "Landlord coordination, lease milestone management",
        ],
        "faq": [
            ("Do you work with landlords and property managers?",
             "Yes — much of our commercial work is initiated by property owners and managers for TI buildouts. We handle landlord work-letter compliance, scope reconciliation and final lien releases."),
            ("How fast can you turn around a TI buildout?",
             "A simple office TI can finish in 6–10 weeks. Restaurants and medical buildouts run 12–24 weeks depending on permitting and equipment lead times. We give you a written milestone schedule before lease commencement."),
        ],
    },
    {
        "slug": "design-build",
        "num": "09",
        "title": "Design-Build Services",
        "tag": "One team, one contract",
        "blurb": "Architecture, interior design and construction under one roof — fewer handoffs, faster decisions, no finger-pointing.",
        "hero_img": "design-build-01",
        "imgs": ["design-build-01", "design-build-02", "design-build-03"],
        "intro": "Design-build is the most efficient way to plan and execute a major construction project. Architecture, engineering, interior design and construction live on the same team and the same contract. Decisions get made faster, change orders shrink, and there's never a finger-point between architect and contractor when something needs solving.",
        "what_we_do": [
            "Full architectural design (custom homes, remodels, ADUs, commercial)",
            "Interior design, material selections and FF&E specification",
            "Structural and MEP engineering coordination",
            "3D renderings, virtual walk-throughs, sample boards",
            "Single fixed-fee contract spanning design through construction",
            "Permitting, plan check and jurisdictional coordination",
            "Single point of accountability from first sketch to final walk-through",
        ],
        "faq": [
            ("How is design-build different from design-bid-build?",
             "Design-bid-build splits the project across an architect and a contractor with two separate contracts. Design-build keeps them on one team with one contract — which usually means faster timelines, fewer change orders and aligned incentives."),
            ("Will design-build cost more?",
             "Almost always less, when you account for the full project. Construction-aware design avoids the expensive change orders that happen when an architect designs without contractor input."),
        ],
    },
    {
        "slug": "teardown-rebuild",
        "num": "10",
        "title": "Teardown & Rebuild",
        "tag": "Right neighborhood, wrong house",
        "blurb": "When the lot is worth more than the house — full teardown, new foundation, and a custom home that fits the neighborhood and your life.",
        "hero_img": "teardown-01",
        "imgs": ["teardown-01", "teardown-02", "teardown-03"],
        "intro": "Sometimes the best home for a lot doesn't exist yet. Teardown-and-rebuild lets you keep the address, the schools, the mature trees, the neighborhood — and replace a dated or undersized home with one designed for how you actually live today. We handle demo, abatement, permits, foundation, and full custom build.",
        "what_we_do": [
            "Pre-purchase teardown feasibility and zoning analysis",
            "Asbestos and hazardous material abatement",
            "Selective demolition or full razing with site clearing",
            "Survey, soils, geotech and engineering coordination",
            "New foundation engineered for the lot's conditions",
            "Full custom home build to your program and budget",
            "Landscape, hardscape, driveway and final exterior",
        ],
        "faq": [
            ("How much does it cost to tear down a house in Utah?",
             "Typical residential demo runs $15K–$40K depending on size, abatement and disposal. Larger or older homes with hazardous materials cost more. We give you a fixed demo number up front."),
            ("How long does the full teardown-rebuild process take?",
             "From closing on the property to keys in hand, most teardown projects run 15–22 months — including design, permitting, demo and construction."),
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
    ("Consult", "We meet at your property or our office, walk the project, listen carefully, and put a realistic budget and timeline on the table — usually inside a week."),
    ("Design", "Plans, elevations, 3D renderings and a written specification. You see exactly what you're getting before a single dollar of construction is spent."),
    ("Build", "One project manager, one schedule, dedicated trades. Bi-weekly updates with photos, milestones and any change orders signed before work proceeds."),
    ("Hand-off", "Final walk-through, punch list completion, warranty package, and a homeowner's manual for every system, finish and serial number in your home."),
]

# ----------------------------------------------------------------
# Page template
# ----------------------------------------------------------------

def esc(s):
    return html.escape(s, quote=True)

def common_head(title, description, canonical_path, og_image_name, extra_jsonld=None):
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
<link rel="stylesheet" href="/assets/styles.css">
{scripts}
</head>
<body>"""

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

def cta_band(headline="Ready to <em>build something</em> remarkable?",
             body=f"Schedule a no-pressure consultation with our Utah team. We'll listen, walk the project, and put real numbers and a real timeline on paper — usually inside a week."):
    return f"""<section class="cta-band">
  <div class="wrap reveal">
    <span class="eyebrow" style="color:var(--accent)">Let's talk</span>
    <h2 style="margin-top:1rem">{headline}</h2>
    <p style="max-width:55ch">{body}</p>
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
        <p class="footer__about">A Utah design-build general contractor for custom homes, whole-home remodels, kitchens, baths, basements, additions and commercial buildouts. Licensed. Insured. Locally owned.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>{service_lis}</ul>
      </div>
      <div>
        <h4>Service Areas</h4>
        <ul>{areas_lis}</ul>
      </div>
      <div class="footer__contact">
        <h4>Contact</h4>
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
    slides_html = "\n".join(
        f'<div class="hero__slide{" is-active" if i==0 else ""}" data-bg="{img(f"hero-{i+1:02d}")}" aria-hidden="true"></div>'
        for i in range(10)
    )
    service_cards = "\n".join(
        f"""<a class="service-card" href="/{s['slug']}.html">
  <span class="service-card__num">{s['num']}</span>
  <h3 class="service-card__title">{esc(s['title'])}</h3>
  <p class="service-card__desc">{esc(s['blurb'])}</p>
  <span class="service-card__link">Explore <span class="arrow">→</span></span>
</a>"""
        for s in SERVICES
    )
    areas_div = "\n".join(f"<div>{esc(a)}</div>" for a in SERVICE_AREAS)
    home_faqs = [
        ("Where in Utah does Multiworks Construction build?",
         "We serve the entire Wasatch Front: Salt Lake City, Park City, Holladay, Sandy, Draper, Lehi, Provo, Bountiful, Cottonwood Heights and surrounding communities in Salt Lake, Utah, Summit and Davis counties."),
        ("Are you licensed and insured in Utah?",
         "Yes — Multiworks Construction LLC is a fully licensed Utah general contractor carrying commercial general liability and workers' comp insurance. Documentation is available on request."),
        ("Do you handle architecture and design, or only construction?",
         "Both. Our design-build team handles architecture, interior design, structural engineering and construction under one contract. We're also happy to work with architects and designers you've already chosen."),
        ("How do you price projects — fixed bid or cost-plus?",
         "We default to a transparent fixed-fee model. After selections are made, we lock the construction price with a clear allowance schedule. Cost-plus is offered on highly custom or unique projects."),
        ("How long is the wait to start a new project?",
         "Lead times vary by project size and trade availability. We typically schedule new project starts 6–12 weeks out and can sometimes start sooner. Call us for current availability."),
        ("What sets Multiworks apart from other Utah general contractors?",
         "Single point of accountability, transparent fixed-fee pricing, in-house design and trades, written milestone schedules, and a 24-month workmanship warranty on every home we build."),
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
        title=f"Multiworks Construction LLC | Utah Custom Home Builder & Remodeler — {ADDRESS_LOCALITY}",
        description=SITE_DESC_SHORT,
        canonical_path="/",
        og_image_name="hero-01",
        extra_jsonld=faq_jsonld,
    ) + nav_block(current="home") + f"""
<section class="hero" id="top">
  <div class="hero__bg">{slides_html}</div>
  <div class="hero__inner">
    <span class="eyebrow hero__eyebrow">Salt Lake City · Park City · Wasatch Front</span>
    <h1 class="hero__title">Utah custom homes &amp; remodels, built <em>without compromise</em>.</h1>
    <p class="hero__sub">Multiworks Construction is a design-build general contractor for clients who refuse to settle. From ground-up custom homes to floor-to-ceiling remodels, we build with one schedule, one team, and one standard: on time, on budget, no excuses.</p>
    <div class="hero__cta">
      <a class="btn btn--solid" href="/contact.html">Start a project <span class="arrow">→</span></a>
      <a class="btn btn--ghost-light" href="/services.html">Our services</a>
    </div>
  </div>
  <div class="hero__meta">{PHONE}</div>
</section>

<section class="section section--paper">
  <div class="wrap split reveal">
    <div>
      <span class="eyebrow">Multiworks Construction</span>
      <h2 style="margin-top:1rem">A Utah general contractor for homes built to <em>outlast trends</em>.</h2>
    </div>
    <div>
      <p class="lead">We build and remodel homes along the Wasatch Front for clients who'd rather wait six months to do it right than three to do it twice. Every project gets a dedicated project manager, a written milestone schedule, transparent fixed-fee pricing, and a 24-month workmanship warranty.</p>
      <p>From ground-up custom homes in Holladay and Park City to floor-to-ceiling remodels in Sugar House and basement build-outs in Sandy, we run every job the way we'd want our own homes run.</p>
      <a class="btn btn--ghost" href="/about.html">About Multiworks <span class="arrow">→</span></a>
    </div>
  </div>
</section>

<div class="stats wrap reveal">
  <div class="stats__item"><div class="stats__num">100<sup>+</sup></div><div class="stats__label">Utah projects delivered</div></div>
  <div class="stats__item"><div class="stats__num">$50M<sup>+</sup></div><div class="stats__label">Construction value built</div></div>
  <div class="stats__item"><div class="stats__num">24<sub style="font-size:0.4em;color:var(--mute)">mo</sub></div><div class="stats__label">Workmanship warranty</div></div>
  <div class="stats__item"><div class="stats__num">5.0<sup>★</sup></div><div class="stats__label">Average client rating</div></div>
</div>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">What we do</span>
      <h2 style="margin-top:1rem">Ten services. <em>One team.</em></h2>
      <p class="lead">From design and architecture through final punch list, Multiworks self-performs the work that matters and partners only with Utah trades we'd hire to work on our own homes.</p>
    </div>
  </div>
  <div class="wrap reveal">
    <div class="service-grid">
      {service_cards}
    </div>
  </div>
</section>

<section class="section section--ink">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">How we work</span>
      <h2 style="color:var(--bone);margin-top:1rem">The Multiworks <em>process</em>.</h2>
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
      <span class="eyebrow eyebrow--mute" style="display:block;margin-bottom:1.5rem">A recent client</span>
      <p class="testimonial__quote">"Multiworks didn't just build our home — they protected our investment, our schedule and our sanity. Every milestone hit on time. Every change order arrived in writing before work started. It's the way construction is supposed to work."</p>
      <div class="testimonial__attr">Holladay, Utah · Custom Home Client</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head section__head--center reveal">
      <span class="eyebrow">Service areas</span>
      <h2 style="margin-top:1rem">Building across the <em>Wasatch Front</em>.</h2>
      <p>Salt Lake County, Utah County, Summit County and Davis County — and the in-between mountain communities most contractors won't drive to.</p>
    </div>
    <div class="areas-grid reveal">{areas_div}</div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section__head section__head--center reveal">
      <span class="eyebrow">Common questions</span>
      <h2 style="margin-top:1rem">What clients ask <em>before</em> they hire us.</h2>
    </div>
    <div class="faq reveal">{faq_html}</div>
  </div>
</section>

{cta_band()}
{footer_block()}"""

def page_service(s):
    triptych = "\n".join(
        f'<div class="triptych__item" data-bg="{img(name)}" role="img" aria-label="{esc(s["title"])} example"></div>'
        for name in s["imgs"]
    )
    bullets = "\n".join(f"<li style='padding:0.5rem 0;border-bottom:1px solid var(--rule);font-family:var(--serif);font-size:1.15rem'>{esc(b)}</li>" for b in s["what_we_do"])
    faq_html = "\n".join(
        f"""<div class="faq__item"><button class="faq__q" type="button">{esc(q)} <span class="plus">+</span></button><div class="faq__a"><p>{esc(a)}</p></div></div>"""
        for q, a in s["faq"]
    )
    other_services = [x for x in SERVICES if x["slug"] != s["slug"]][:3]
    related_cards = "\n".join(
        f"""<a class="service-card" href="/{x['slug']}.html">
  <span class="service-card__num">{x['num']}</span>
  <h3 class="service-card__title">{esc(x['title'])}</h3>
  <p class="service-card__desc">{esc(x['blurb'])}</p>
  <span class="service-card__link">Explore <span class="arrow">→</span></span>
</a>"""
        for x in other_services
    )
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
  <div class="page-hero__bg" data-bg="{img(s['hero_img'])}"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · <a href="/services.html">Services</a> · {esc(s['title'])}</div>
    <span class="eyebrow" style="color:var(--accent)">Service {s['num']} · {esc(s['tag'])}</span>
    <h1 class="page-hero__title" style="margin-top:1rem">{esc(s['title'])} in Utah.</h1>
    <p class="page-hero__sub">{esc(s['blurb'])}</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap split split--narrow reveal">
    <div>
      <span class="eyebrow">What this is</span>
      <h2 style="margin-top:1rem">A <em>better</em> way to do {esc(s['title'].lower())}.</h2>
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
      <h2 style="margin-top:1rem">What's included in our <em>{esc(s['title'].lower())}</em> service.</h2>
      <p>Every project is custom, but here's what most {esc(s['title'].lower())} engagements with Multiworks include from kickoff to final walk-through:</p>
    </div>
    <div>
      <ul style="list-style:none;padding:0;margin:0">{bullets}</ul>
    </div>
  </div>
</section>

<section class="section section--ink">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">How we deliver</span>
      <h2 style="color:var(--bone);margin-top:1rem">The Multiworks <em>process</em>.</h2>
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
      <h2 style="margin-top:1rem">{esc(s['title'])} — <em>frequently asked</em>.</h2>
    </div>
    <div class="faq reveal">{faq_html}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">Related work</span>
      <h2 style="margin-top:1rem">Other ways we <em>build</em>.</h2>
    </div>
  </div>
  <div class="wrap reveal">
    <div class="service-grid">{related_cards}</div>
  </div>
</section>

{cta_band(headline=f"Ready to start your <em>{esc(s['title'].lower())}</em> project?")}
{footer_block()}"""

def page_services():
    service_cards = "\n".join(
        f"""<a class="service-card" href="/{s['slug']}.html">
  <span class="service-card__num">{s['num']}</span>
  <h3 class="service-card__title">{esc(s['title'])}</h3>
  <p class="service-card__desc">{esc(s['blurb'])}</p>
  <span class="service-card__link">Explore <span class="arrow">→</span></span>
</a>"""
        for s in SERVICES
    )
    return common_head(
        title=f"Construction & Remodeling Services in Utah | Multiworks Construction",
        description="Custom home building, whole-home remodeling, kitchen and bathroom remodels, basement finishing, additions, ADUs, outdoor living and commercial construction in Salt Lake City, Park City and the Wasatch Front.",
        canonical_path="/services.html",
        og_image_name="hero-02",
    ) + nav_block(current="services") + f"""
<section class="page-hero">
  <div class="page-hero__bg" data-bg="{img('hero-02')}"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · Services</div>
    <span class="eyebrow" style="color:var(--accent)">Our services</span>
    <h1 class="page-hero__title" style="margin-top:1rem">Ten services. <em>One Utah team.</em></h1>
    <p class="page-hero__sub">From ground-up custom homes to commercial tenant improvements — every service Multiworks delivers is held to the same standard: written schedule, fixed-fee pricing, dedicated project manager, 24-month warranty.</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap reveal">
    <div class="service-grid">{service_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head section__head--center reveal">
      <span class="eyebrow">How we work</span>
      <h2 style="margin-top:1rem">The Multiworks <em>process</em>.</h2>
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
        title="About Multiworks Construction | Utah Custom Home Builder & Remodeler",
        description="Multiworks Construction LLC is a Utah-owned design-build general contractor serving Salt Lake City, Park City and the Wasatch Front. Licensed, insured, locally rooted.",
        canonical_path="/about.html",
        og_image_name="hero-05",
    ) + nav_block(current="about") + f"""
<section class="page-hero">
  <div class="page-hero__bg" data-bg="{img('hero-05')}"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · About</div>
    <span class="eyebrow" style="color:var(--accent)">About Multiworks</span>
    <h1 class="page-hero__title" style="margin-top:1rem">Utah-built. <em>Client-aligned.</em> No drama.</h1>
    <p class="page-hero__sub">Multiworks Construction LLC is a Utah-owned design-build general contractor. We build custom homes, remodel existing ones, and finish out commercial spaces along the Wasatch Front — for clients who'd rather hire one team than coordinate five.</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap split reveal">
    <div class="split__image" data-bg="{img('design-build-02')}"></div>
    <div>
      <span class="eyebrow">Our story</span>
      <h2 style="margin-top:1rem">A general contractor that <em>actually</em> answers the phone.</h2>
      <p class="lead">Multiworks Construction was founded on a simple frustration: too many Utah construction projects start with a smile and a promise, then drift into missed milestones, mystery change orders and silent project managers.</p>
      <p>We built Multiworks to be the contractor we wish we'd hired. Single point of accountability. Written milestone schedules. Fixed-fee pricing. Change orders signed before work starts, never after. And the people who answer your call on Tuesday are the same people swinging hammers on your job Wednesday.</p>
      <a class="btn btn--ghost" href="/contact.html">Start a project <span class="arrow">→</span></a>
    </div>
  </div>
</section>

<div class="stats wrap reveal">
  <div class="stats__item"><div class="stats__num">100<sup>+</sup></div><div class="stats__label">Utah projects delivered</div></div>
  <div class="stats__item"><div class="stats__num">$50M<sup>+</sup></div><div class="stats__label">Construction value built</div></div>
  <div class="stats__item"><div class="stats__num">24<sub style="font-size:0.4em;color:var(--mute)">mo</sub></div><div class="stats__label">Workmanship warranty</div></div>
  <div class="stats__item"><div class="stats__num">5.0<sup>★</sup></div><div class="stats__label">Average client rating</div></div>
</div>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">What we believe</span>
      <h2 style="margin-top:1rem">Five principles we won't <em>compromise</em> on.</h2>
    </div>
    <div class="process reveal">
      <div class="process__step"><div class="process__num">01</div><div class="process__title">Single accountability</div><div class="process__desc">One contract, one project manager, one number to call. Never "that's the architect's problem" or "talk to the subcontractor".</div></div>
      <div class="process__step"><div class="process__num">02</div><div class="process__title">Transparent pricing</div><div class="process__desc">Fixed-fee proposals with itemized line items and a clear allowance schedule. No mystery markups. No silent change orders.</div></div>
      <div class="process__step"><div class="process__num">03</div><div class="process__title">Written schedule</div><div class="process__desc">A milestone-based schedule before work begins, updated every two weeks with photos and progress against the plan.</div></div>
      <div class="process__step"><div class="process__num">04</div><div class="process__title">Local trades, local pride</div><div class="process__desc">We work with Utah's most skilled trades and treat them well. That's how you keep talent on your job instead of someone else's.</div></div>
    </div>
  </div>
</section>

<section class="section section--ink">
  <div class="wrap reveal">
    <div class="testimonial">
      <span class="eyebrow" style="display:block;margin-bottom:1.5rem">A recent client</span>
      <p class="testimonial__quote" style="color:var(--bone)">"You don't realize how rare honest construction is until you've experienced it. Multiworks ran our build like a Swiss watch — and made it look easy."</p>
      <div class="testimonial__attr" style="color:var(--mute-2)">Park City · Custom Home Client</div>
    </div>
  </div>
</section>

{cta_band()}
{footer_block()}"""

def page_portfolio():
    # Mosaic from all service images
    all_imgs = []
    for s in SERVICES:
        all_imgs.extend([(name, s["title"]) for name in s["imgs"]])
    # Plus hero shots
    for i in range(1, 11):
        all_imgs.append((f"hero-{i:02d}", "Multiworks Construction"))
    mosaic = "\n".join(
        f"""<a class="portfolio__item" href="#" style="background-image:url('{img(n)}')" aria-label="{esc(t)}">
  <span class="portfolio__caption">{esc(t)}</span>
</a>"""
        for n, t in all_imgs
    )
    return common_head(
        title="Portfolio | Utah Custom Homes, Remodels & Commercial — Multiworks Construction",
        description="A selection of Multiworks Construction's recent Utah projects — custom homes, kitchens, baths, basements, additions, outdoor living and commercial buildouts in Salt Lake City and Park City.",
        canonical_path="/portfolio.html",
        og_image_name="hero-06",
    ) + nav_block(current="portfolio") + f"""
<style>
.portfolio-grid {{ display:grid; grid-template-columns: repeat(3, 1fr); gap:1px; background:var(--rule); border-block:1px solid var(--rule); }}
@media (max-width:900px) {{ .portfolio-grid {{ grid-template-columns: repeat(2,1fr); }} }}
@media (max-width:560px) {{ .portfolio-grid {{ grid-template-columns: 1fr; }} }}
.portfolio__item {{ aspect-ratio: 4/3; background-size: cover; background-position: center; position: relative; overflow: hidden; }}
.portfolio__item::after {{ content:''; position:absolute; inset:0; background: linear-gradient(180deg, transparent 50%, rgba(0,0,0,0.65)); opacity: 0.6; transition: opacity 0.4s ease; }}
.portfolio__item:hover::after {{ opacity: 0.85; }}
.portfolio__caption {{
  position:absolute; bottom:1.25rem; left:1.5rem; right:1.5rem;
  z-index:2; color:var(--bone);
  font-family: var(--serif); font-size:1.15rem;
  transform: translateY(8px); opacity:0;
  transition: all 0.4s ease;
}}
.portfolio__item:hover .portfolio__caption {{ transform: translateY(0); opacity:1; }}
</style>

<section class="page-hero">
  <div class="page-hero__bg" data-bg="{img('hero-06')}"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · Portfolio</div>
    <span class="eyebrow" style="color:var(--accent)">Selected work</span>
    <h1 class="page-hero__title" style="margin-top:1rem">A selection of <em>recent work</em>.</h1>
    <p class="page-hero__sub">Custom homes, whole-home remodels, kitchens, baths, basements, additions and outdoor living spaces from across Utah's Wasatch Front.</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap reveal" style="margin-bottom:3rem">
    <span class="eyebrow">Browse the work</span>
    <h2 style="margin-top:1rem;max-width:24ch">Every photo here is a <em>real project</em> — or what your project could become.</h2>
  </div>
  <div class="portfolio-grid reveal">{mosaic}</div>
</section>

{cta_band(headline="See something you <em>like</em>? Let's build yours.")}
{footer_block()}"""

def page_contact():
    return common_head(
        title="Contact Multiworks Construction | Utah General Contractor — Call or Get a Quote",
        description=f"Contact Multiworks Construction LLC for custom homes, remodels and commercial work in Utah. Call {PHONE} or request a no-pressure consultation. Serving Salt Lake City, Park City and the Wasatch Front.",
        canonical_path="/contact.html",
        og_image_name="hero-08",
    ) + nav_block(current="contact") + f"""
<section class="page-hero">
  <div class="page-hero__bg" data-bg="{img('hero-08')}"></div>
  <div class="page-hero__inner">
    <div class="crumbs"><a href="/">Home</a> · Contact</div>
    <span class="eyebrow" style="color:var(--accent)">Let's talk</span>
    <h1 class="page-hero__title" style="margin-top:1rem">Start your <em>Utah project</em>.</h1>
    <p class="page-hero__sub">Call us, email us, or fill out the form. We'll respond within one business day, schedule a no-pressure site walk, and put real numbers and a real timeline on paper — usually within a week.</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap contact-grid reveal">
    <div class="contact-card">
      <h3>Get in touch.</h3>
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
      <h3>Request a consultation.</h3>
      <p style="margin-bottom:2rem;color:var(--mute)">Tell us about your project. The more detail you can share, the more useful our first conversation will be.</p>
      <form class="form" action="mailto:{EMAIL}" method="post" enctype="text/plain">
        <div class="form__row">
          <div><label for="name">Name</label><input id="name" name="name" type="text" required></div>
          <div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" required></div>
        </div>
        <div class="form__row">
          <div><label for="email">Email</label><input id="email" name="email" type="email" required></div>
          <div><label for="city">City</label><input id="city" name="city" type="text" placeholder="Salt Lake City, Park City…"></div>
        </div>
        <div>
          <label for="service">Project type</label>
          <select id="service" name="service">
            <option value="">Select a service…</option>
""" + "\n".join(f'<option value="{esc(s["title"])}">{esc(s["title"])}</option>' for s in SERVICES) + f"""
            <option value="Not sure yet">Not sure yet</option>
          </select>
        </div>
        <div>
          <label for="budget">Approximate budget</label>
          <select id="budget" name="budget">
            <option value="">Select a range…</option>
            <option>Under $100K</option>
            <option>$100K – $250K</option>
            <option>$250K – $500K</option>
            <option>$500K – $1M</option>
            <option>$1M – $3M</option>
            <option>$3M+</option>
            <option>Not sure yet</option>
          </select>
        </div>
        <div>
          <label for="msg">Project details</label>
          <textarea id="msg" name="message" rows="5" placeholder="Tell us about your project, timeline, and anything else that'd help us prepare for our first call…"></textarea>
        </div>
        <div><button class="btn btn--solid" type="submit">Send message <span class="arrow">→</span></button></div>
        <p style="font-size:0.78rem;color:var(--mute);margin-top:0.5rem">By submitting, you agree to be contacted about your project. We don't share your information.</p>
      </form>
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
