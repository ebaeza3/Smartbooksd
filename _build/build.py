#!/usr/bin/env python3
"""
Smart Book SD — static site generator.

Edit the SETTINGS block below, then run:   python3 _build/build.py
All .html pages, sitemap.xml and robots.txt in the site root are regenerated.
(GitHub Pages ignores this _build folder.)
"""
import datetime as dt
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================== SETTINGS ==============================
SITE_URL = "https://ebaeza3.github.io/Smartbooksd"   # change when you add a custom domain (no trailing slash)
BUSINESS = "Smart Book SD"
PHONE = "619-764-8026"
PHONE_E164 = "+16197648026"
EMAIL = "Smartbooksd@gmail.com"

# Form delivery. FormSubmit forwards submissions to EMAIL with no account needed.
# IMPORTANT: the first submission sends an activation email to EMAIL — click "Activate" once.
# Set to "" to fall back to opening the visitor's email app instead.
FORM_ENDPOINT = "https://formsubmit.co/ajax/" + EMAIL

# Optional: an online scheduling link (Calendly, Google Calendar booking page, etc.).
# When set, "Book a Free Consultation" buttons go straight to it.
BOOKING_URL = ""

# How fast you reply to new inquiries (shown on the site). Use "" to hide.
RESPONSE_TIME = "1 business day"

# Credentials shown in the footer/About page, e.g.
# "CTEC Registered Tax Preparer (A123456) · IRS PTIN holder"  or  "Enrolled Agent"
# Leave "" until you have the exact wording/numbers.
CREDENTIALS = ""
OWNER_NAME = ""          # e.g. "Maria Lopez" — adds a personal intro on the About page

# Real client reviews ONLY (FTC rules prohibit fake or edited reviews). Get permission first.
# Example: {"quote": "...", "name": "Jordan P.", "detail": "LLC owner, San Diego", "stars": 5}
TESTIMONIALS = []

# Social / review profiles, e.g. {"Google": "https://g.page/...", "Yelp": "https://yelp.com/biz/..."}
SOCIAL = {}

ANNOUNCEMENT = "<strong>2027 tax season:</strong> now booking free consultations. <a href=\"contact.html\">Reserve your spot →</a>"
LEGAL_EFFECTIVE = "November 18, 2026"
# =====================================================================

BOOK_HREF = BOOKING_URL or "contact.html"
BOOK_ATTR = ' target="_blank" rel="noopener"' if BOOKING_URL else ""
e = html.escape


def svg(p):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{p}</svg>')


I = {
    "person": svg('<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>'),
    "briefcase": svg('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>'),
    "book": svg('<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7M8 11h7"/>'),
    "pay": svg('<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/>'),
    "broom": svg('<path d="M3 21l7-7M14 4l6 6-6 6-6-6z"/><path d="M8 14l2 2"/>'),
    "phone": svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    "mail": svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'),
    "lock": svg('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'),
    "laptop": svg('<rect x="4" y="4" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>'),
    "map": svg('<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>'),
    "chat": svg('<path d="M21 12a8 8 0 0 1-11.8 7L3 21l2-6A8 8 0 1 1 21 12z"/>'),
    "calendar": svg('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
    "shield": svg('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>'),
    "clock": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "check": svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    "upload": svg('<path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>'),
    "doc": svg('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>'),
    "home": svg('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/>'),
    "users": svg('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.5 3-5.5 6.5-5.5s6.5 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.6c2 .6 3.5 2.3 3.5 5.4"/>'),
    "chart": svg('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'),
    "star": svg('<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>'),
    "list": svg('<path d="M9 6h12M9 12h12M9 18h12"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>'),
    "heart": svg('<path d="M12 20s-7-4.4-9-9a5 5 0 0 1 9-3 5 5 0 0 1 9 3c-2 4.6-9 9-9 9z"/>'),
    "up": svg('<path d="M12 19V5M5 12l7-7 7 7"/>'),
    "ext": svg('<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
}

# ------------------------------ SERVICES ------------------------------
SERVICES = [
    dict(
        slug="tax-preparation", key="individual", icon="person",
        name="Individual Tax Returns",
        nav="Individual Tax Returns",
        title="Online Individual Tax Preparation in San Diego & California",
        short="Federal and California returns for W-2 earners, families, retirees and side-income earners.",
        lead="Accurate federal and California tax returns prepared by a real person and handled entirely online. Upload your documents, review your return with us, and we e-file it for you.",
        ideal=["W-2 employees", "Families with dependents", "Retirees", "Investors", "Rental property owners", "Side hustles & 1099 income"],
        includes=["Federal Form 1040 and California Form 540", "W-2, 1099, interest, dividend and capital gains income",
                  "Standard vs. itemized deduction review", "Child, dependent and education credit review",
                  "Rental property income (Schedule E)", "E-filing with refund direct deposit",
                  "Prior-year and amended returns", "Help responding to IRS and FTB letters about returns we prepare"],
        body="<p>Your return deserves more than a software questionnaire. We review your full picture, including income, family changes, homeownership, investments and retirement, so the deductions and credits you're entitled to are claimed, and nothing is reported incorrectly.</p><p>Everything happens online. We'll send you a personalized document list, you upload securely, and we walk you through the finished return before anything is filed.</p>",
        faqs=[("What do I need to send you?", "After your consultation we'll send a personalized list. Most people need their W-2s and 1099s, last year's return, and records for deductions like mortgage interest, property tax, charitable gifts and childcare. Our <a href=\"document-checklist.html\">tax document checklist</a> is a good place to start."),
              ("Can you file prior-year or amended returns?", "Yes. We can prepare returns for past years you haven't filed and amend returns that need corrections."),
              ("When will I get my refund?", "Refund timing is controlled by the IRS and the California Franchise Tax Board. E-filed returns with direct deposit are typically the fastest. You can track federal refunds on IRS.gov with “Where's My Refund?”.")],
    ),
    dict(
        slug="small-business-tax", key="business", icon="briefcase",
        name="Small Business Taxes",
        nav="Small Business Taxes",
        title="Small Business & LLC Tax Preparation for California",
        short="LLCs, sole proprietors, freelancers and Schedule C filers.",
        lead="Business tax preparation for California LLCs, sole proprietors and freelancers, with careful attention to the deductions that help you keep more of what you earn.",
        ideal=["Sole proprietors", "Freelancers & consultants", "Single-member LLCs", "Multi-member LLCs", "Gig & rideshare workers", "Real estate agents"],
        includes=["Schedule C for sole proprietors and single-member LLCs", "Multi-member LLC partnership returns",
                  "California LLC annual tax and fee filings", "Quarterly estimated tax calculations (federal & CA)",
                  "1099-NEC preparation for your contractors", "Home office, vehicle and equipment deduction review",
                  "Self-employment tax planning", "Year-round answers to your tax questions"],
        body="<p>Running a business means more forms, more deadlines and more chances to overpay. We prepare your business return accurately and help you plan ahead, including setting estimated payments so April holds no surprises.</p><p>If we also keep your books, your tax return flows straight from clean, reconciled numbers. That's faster for you, more accurate, and easier to support if a tax agency ever asks questions.</p>",
        faqs=[("Do California LLCs have extra filing requirements?", "Yes. Most California LLCs owe an annual LLC tax to the Franchise Tax Board and may owe an additional fee based on gross receipts, in addition to federal filings. We'll make sure your LLC's filings and payments are on our calendar."),
              ("Should I be making quarterly estimated payments?", "If you're self-employed and expect to owe tax, you generally need to make estimated payments during the year. We'll calculate recommended amounts and remind you of the due dates."),
              ("I'm thinking about forming an LLC or S-corp. Can you help?", "We can walk through the tax side of the decision with you on a consultation. For legal formation questions, we recommend also speaking with a business attorney.")],
    ),
    dict(
        slug="bookkeeping", key="bookkeeping", icon="book",
        name="Monthly Bookkeeping (QuickBooks)",
        nav="Monthly Bookkeeping",
        title="Online QuickBooks Bookkeeping Services for Small Businesses",
        short="Clean, reconciled books every month in QuickBooks Online.",
        lead="We keep your QuickBooks Online books accurate and up to date every month, so you always know where your business stands and tax time is easy.",
        ideal=["Service businesses", "E-commerce sellers", "Contractors & trades", "Restaurants & retail", "Agencies & studios", "Any business using QuickBooks Online"],
        includes=["Monthly transaction categorization", "Bank and credit card reconciliations",
                  "Monthly profit & loss and balance sheet", "QuickBooks Online setup and chart of accounts",
                  "Bank feed rules to automate the routine", "Receipt and document organization",
                  "Accounts receivable and payable tracking", "Year-end package ready for your tax return"],
        body="<p>Good bookkeeping is the foundation for everything else: smarter decisions, easier loans, and a smooth tax season. Each month we categorize every transaction, reconcile your accounts and send you clear reports you can actually use.</p><p>Already using QuickBooks Online? We'll pick up right where you are. New to it? We'll set it up properly from day one.</p>",
        faqs=[("Do I need QuickBooks Online?", "We work in QuickBooks Online. If you're not using it yet, we'll help you get set up. If you're on another system, let's talk on your consultation."),
              ("What do I need to do each month?", "Very little. Once your bank feeds are connected, we handle the categorizing and reconciling. We'll occasionally send a short list of questions about transactions we can't identify."),
              ("When will I get my monthly reports?", "Timing depends on when your statements close. We'll agree on a monthly schedule during onboarding.")],
    ),
    dict(
        slug="payroll", key="payroll", icon="pay",
        name="Payroll Setup & Processing",
        nav="Payroll",
        title="Online Payroll Services for California Small Businesses",
        short="Pay your team on time with taxes and filings handled.",
        lead="From your first hire to a growing team, we set up payroll the right way and run it on schedule, with federal and California payroll filings handled.",
        ideal=["First-time employers", "Small teams", "S-corp owners paying themselves", "Businesses with contractors", "Seasonal employers"],
        includes=["Payroll setup and new-hire onboarding", "Weekly, biweekly, semi-monthly or monthly pay runs",
                  "Direct deposit for employees", "Federal payroll tax deposits and quarterly Form 941",
                  "California EDD registration and quarterly DE 9 / DE 9C", "Year-end W-2s and 1099-NECs",
                  "Owner / S-corp officer payroll", "Payroll records that tie to your books"],
        body="<p>California payroll comes with its own rules, agencies and deadlines. We take payroll off your plate by setting it up correctly, running each pay period on time and handling the federal and state filings that go with it.</p><p>Because payroll connects directly to your bookkeeping, your labor costs are always recorded accurately, with no year-end surprises.</p>",
        faqs=[("I'm hiring my first employee. Where do I start?", "Book a consultation. We'll walk you through the registrations you'll need with the IRS and California EDD, the new-hire paperwork, and choosing a pay schedule, then set it all up for you."),
              ("Can you pay independent contractors too?", "Yes. We can handle contractor payments and prepare 1099-NEC forms at year end."),
              ("What if I've already been running payroll myself?", "No problem. We'll review what's been filed so far and take over going forward, making sure the year's totals line up.")],
    ),
    dict(
        slug="catch-up-bookkeeping", key="catchup", icon="broom",
        name="Catch-Up & Cleanup Bookkeeping",
        nav="Catch-Up & Cleanup",
        title="Catch-Up & Cleanup Bookkeeping: Get Your Books Current",
        short="Behind on your books? We'll get you current, fast.",
        lead="Months, or even years, behind? No judgment. We'll organize your records, clean up QuickBooks and get your books accurate and current so you can file with confidence.",
        ideal=["Behind on bookkeeping", "Messy QuickBooks files", "Unfiled tax returns", "Switching bookkeepers", "Preparing for a loan or sale"],
        includes=["Catch-up bookkeeping for months or years", "Cleanup of miscategorized and duplicate transactions",
                  "Reconciliation of past bank and card statements", "Opening balance and equity corrections",
                  "Preparation of past-due tax returns", "Clear plan to stay current going forward",
                  "Smooth handoff into monthly bookkeeping", "Financial statements you can trust"],
        body="<p>Falling behind happens, especially when you're busy running the business. The longer it waits, the harder tax season gets. We'll gather your bank and card statements, rebuild your records and reconcile everything so your numbers are finally right.</p><p>Once you're caught up, we can keep you current every month so you never fall behind again.</p>",
        faqs=[("How far back can you go?", "As far as you need. We regularly help clients who are a year or more behind. We'll scope the project during your free consultation."),
              ("What if I don't have all my receipts?", "Bank and credit card statements are the starting point and can usually be downloaded from your bank. We'll work with what you have and help you fill in the gaps."),
              ("I also have unfiled tax returns. Can you help?", "Yes. Once the books are caught up, we can prepare your past-due returns as well.")],
    ),
]
SVC = {s["key"]: s for s in SERVICES}

NAV = [("services.html", "Services"), ("resources.html", "Resources"), ("about.html", "About"), ("faq.html", "FAQ"), ("contact.html", "Contact")]

ORG_LD = {
    "@context": "https://schema.org", "@type": "AccountingService", "@id": SITE_URL + "/#business",
    "name": BUSINESS, "url": SITE_URL + "/", "telephone": PHONE_E164, "email": EMAIL,
    "logo": SITE_URL + "/assets/logo.png", "image": SITE_URL + "/assets/og-image.png",
    "description": "100% online tax preparation, QuickBooks bookkeeping and payroll services for individuals and small businesses in San Diego and throughout California.",
    "areaServed": [{"@type": "City", "name": "San Diego"}, {"@type": "State", "name": "California"}],
    "knowsAbout": ["Tax preparation", "Small business taxes", "Bookkeeping", "QuickBooks Online", "Payroll"],
    "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_E164, "email": EMAIL, "contactType": "customer service", "areaServed": "US-CA", "availableLanguage": "English"},
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{SITE_URL}/{s['slug']}.html"}} for s in SERVICES]},
}
if SOCIAL:
    ORG_LD["sameAs"] = list(SOCIAL.values())


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE_URL}/{h}"} for i, (h, n) in enumerate(items)]}


def faq_ld(pairs):
    import re
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in pairs]}


def crumbs(items):
    parts = ['<a href="index.html">Home</a>'] + [f'<a href="{h}">{e(n)}</a>' for h, n in items[:-1]] + [f'<span aria-current="page" style="margin:0">{e(items[-1][1])}</span>']
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(parts) + "</nav>"


def book_btn(cls="btn btn-primary", text="Book a Free Consultation"):
    return f'<a class="{cls}" href="{BOOK_HREF}"{BOOK_ATTR}>{text}</a>'


def page(fname, title, desc, body, schema=(), noindex=False, active=None):
    active = active or fname
    navlinks = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    canonical = f"{SITE_URL}/" if fname == "index.html" else f"{SITE_URL}/{fname}"
    cfg = {"phone": PHONE, "email": EMAIL, "formEndpoint": FORM_ENDPOINT, "responseTime": RESPONSE_TIME,
           "services": {s["key"]: {"name": s["name"], "short": s["short"], "url": s["slug"] + ".html", "icon": I[s["icon"]]} for s in SERVICES}}
    schemas = "\n".join(ld(s) for s in schema)
    cred = f'<p class="cred">{e(CREDENTIALS)}</p>' if CREDENTIALS else ""
    social = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a></li>' for n, u in SOCIAL.items())
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{canonical}">'}
<meta name="theme-color" content="#0b2239">
<meta property="og:site_name" content="{BUSINESS}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/logo.png">
<link rel="preload" href="assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/jakarta.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css">
{schemas}
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
{f'<div class="announce" role="region" aria-label="Announcement">{ANNOUNCEMENT}</div>' if ANNOUNCEMENT else ''}
<header class="site-header">
  <nav class="container nav" aria-label="Main">
    <a class="logo" href="index.html" aria-label="{BUSINESS} home"><span class="logo-mark" aria-hidden="true">SB</span><span>Smart Book SD<small>Tax · Books · Payroll</small></span></a>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav-menu"><span></span><span></span><span></span></button>
    <div class="nav-menu" id="nav-menu">
      <ul class="nav-links">{navlinks}</ul>
      <div class="nav-cta">
        <a class="nav-phone" href="tel:{PHONE_E164}">{I["phone"]}{PHONE}</a>
        {book_btn()}
      </div>
    </div>
  </nav>
</header>
<main id="main" tabindex="-1">
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="logo" href="index.html"><span class="logo-mark" aria-hidden="true">SB</span><span>Smart Book SD<small>Tax · Books · Payroll</small></span></a>
        <p>100% online tax preparation, bookkeeping and payroll for individuals and small businesses in San Diego and throughout California.</p>
        {cred}
      </div>
      <div>
        <h2>Services</h2>
        <ul>{"".join(f'<li><a href="{s["slug"]}.html">{s["nav"]}</a></li>' for s in SERVICES)}</ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="tax-deadlines.html">Tax Deadlines</a></li>
          <li><a href="document-checklist.html">Document Checklist</a></li>
          <li><a href="contact.html">Contact</a></li>
          {social}
        </ul>
      </div>
      <div>
        <h2>Get in touch</h2>
        <ul>
          <li><a href="tel:{PHONE_E164}">{PHONE}</a> (call or text)</li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Online &amp; by appointment. No office visits needed.</li>
          <li>Serving San Diego &amp; all of California</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="legal-links"><span>&copy; <span data-year>{dt.date.today().year}</span> {BUSINESS}. All rights reserved.</span><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Use</a><a href="accessibility.html">Accessibility</a><a href="sitemap.xml">Sitemap</a></div>
      <p style="margin:0">Content on this website is general information, not tax, legal or financial advice. Contacting us or using this site does not create a client relationship; services begin only after a signed engagement letter. {BUSINESS} is not affiliated with the IRS, the California Franchise Tax Board, the EDD or Intuit Inc. QuickBooks is a registered trademark of Intuit Inc.</p>
    </div>
  </div>
</footer>
<div class="mobile-cta" aria-label="Quick contact">
  <a class="btn btn-ghost" href="tel:{PHONE_E164}">{I["phone"]} Call</a>
  {book_btn(text="Free Consultation")}
</div>
<button class="to-top" type="button" aria-label="Back to top">{I["up"]}</button>
<script>window.SBSD={json.dumps(cfg)};</script>
<script src="assets/main.js" defer></script>
</body>
</html>
'''


def cta(h="Ready to take taxes and books off your plate?",
        p="Book a free, no-obligation consultation. We'll talk through your situation and give you a clear quote before any work begins."):
    return f'''<section class="section tight"><div class="container"><div class="cta reveal">
  <div><h2>{h}</h2><p>{p}</p></div>
  <div class="btn-row">{book_btn("btn btn-light")}<a class="btn btn-outline-light" href="tel:{PHONE_E164}">{I["phone"]} {PHONE}</a></div>
</div></div></section>'''


def faq_block(pairs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in pairs) + "</div>"


# ------------------------------ HOME ------------------------------
HOME_FAQ = [
    ("Do I ever need to come into an office?", "No. Smart Book SD is 100% online. We meet by phone or video and you share documents through a secure, encrypted upload link, so you can work with us from anywhere in California."),
    ("Is the consultation really free?", "Yes. Your first consultation is free with no obligation. We'll learn about your situation and give you a clear quote before any work begins."),
    ("How do I send my documents securely?", "After your consultation we'll send you a secure upload link. Please don't email Social Security numbers, bank account numbers or tax documents as regular email attachments."),
    ("Do you only work with clients in San Diego?", "We're based in San Diego, but because everything is virtual we serve individuals and businesses throughout California."),
    ("I'm months behind on my bookkeeping. Can you help?", "Absolutely. <a href=\"catch-up-bookkeeping.html\">Catch-up and cleanup bookkeeping</a> is one of our specialties. We'll get your books current and set you up so it doesn't happen again."),
]


def svc_card(s):
    return f'''<article class="card link reveal"><div class="ico">{I[s["icon"]]}</div><h3>{s["name"]}</h3><p>{s["short"]}</p>
<a class="more stretch" href="{s["slug"]}.html">Learn more<span class="sr-only"> about {s["name"]}</span></a></article>'''


FINDER_Q = [
    ("I am a…", "who", [("W-2 employee or retiree", "individual"), ("Freelancer / self-employed", "business bookkeeping"),
                        ("LLC or small business owner", "business bookkeeping"), ("Business with employees", "payroll bookkeeping business")]),
    ("I need help with…", "need", [("My personal tax return", "individual"), ("My business taxes", "business"),
                                   ("Keeping my books organized", "bookkeeping"), ("Paying employees", "payroll"),
                                   ("Getting caught up — I'm behind", "catchup")]),
]
finder_html = ""
for legend, name, opts in FINDER_Q:
    chips = "".join(f'<label class="chip"><input type="checkbox" name="{name}" data-svc="{v}"><span>{e(t)}</span></label>' for t, v in opts)
    finder_html += f'<fieldset><legend>{legend}</legend><div class="chips">{chips}</div></fieldset>'

testimonials = ""
if TESTIMONIALS:
    cards = "".join(f'''<figure class="card quote reveal"><div class="stars" aria-label="{t.get("stars",5)} out of 5 stars">{"★"*int(t.get("stars",5))}</div>
<blockquote>“{e(t["quote"])}”</blockquote><figcaption><strong>{e(t["name"])}</strong>{e(t.get("detail",""))}</figcaption></figure>''' for t in TESTIMONIALS)
    testimonials = f'''<section class="section soft"><div class="container"><div class="center head"><span class="eyebrow">Client Stories</span><h2>What our clients say</h2></div>
<div class="grid grid-3">{cards}</div></div></section>'''

home = f'''
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="pill"><b>Now booking</b> 2027 tax season consultations</span>
      <h1>Taxes, Bookkeeping &amp; Payroll, <span class="grad-text">Done Online</span></h1>
      <p class="lead">Smart Book SD helps individuals and small businesses in San Diego and across California stay organized, compliant and stress-free, without ever stepping into an office.</p>
      <div class="btn-row">
        {book_btn()}
        <a class="btn btn-ghost" href="tel:{PHONE_E164}">{I["phone"]} Call {PHONE}</a>
      </div>
      <ul class="trust">
        <li>{I["check"]}Free consultation</li><li>{I["check"]}100% virtual</li><li>{I["check"]}QuickBooks Online</li><li>{I["check"]}Serving all of California</li>
      </ul>
    </div>
    <div class="mock" aria-hidden="true">
      <div class="mock-card">
        <div class="mock-top"><strong>Monthly Snapshot</strong><span class="tag">Books current</span></div>
        <div class="kpis">
          <div class="kpi"><small>Revenue</small><b>$48,200</b></div>
          <div class="kpi"><small>Expenses</small><b>$29,650</b></div>
          <div class="kpi"><small>Net profit</small><b>$18,550</b></div>
        </div>
        <div class="bars">{"".join(f'<span style="height:{h}%;animation-delay:{i*80}ms"></span>' for i, h in enumerate([42,55,48,66,60,78,72,90]))}</div>
        <div class="months">{"".join(f"<span>{m}</span>" for m in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"])}</div>
        <ul class="mock-list">
          <li><span class="dot">{I["check"]}</span>Bank accounts reconciled<em>Done</em></li>
          <li><span class="dot">{I["check"]}</span>Payroll processed &amp; filed<em>Done</em></li>
          <li><span class="dot">{I["check"]}</span>Q3 estimated tax reminder<em>Sent</em></li>
        </ul>
      </div>
      <p class="mock-note">Illustrative example</p>
      <div class="float f1"><span class="ico">{I["doc"]}</span><div><strong>Return e-filed</strong><small>Federal + California</small></div></div>
      <div class="float f2"><span class="ico">{I["lock"]}</span><div><strong>Docs received</strong><small>Secure upload</small></div></div>
    </div>
  </div>
</section>

<section class="band" aria-label="Highlights">
  <div class="container band-grid">
    <div class="band-item"><span class="ico">{I["laptop"]}</span><div><strong>100% Online</strong><span>No office visits, ever</span></div></div>
    <div class="band-item"><span class="ico">{I["chat"]}</span><div><strong>Free Consultation</strong><span>No obligation, clear quote</span></div></div>
    <div class="band-item"><span class="ico">{I["map"]}</span><div><strong>California-Focused</strong><span>Federal + CA filings</span></div></div>
    <div class="band-item"><span class="ico">{I["lock"]}</span><div><strong>Secure File Sharing</strong><span>Encrypted document uploads</span></div></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center head reveal">
      <span class="eyebrow">Our Services</span>
      <h2>Everything your finances need, in one place</h2>
      <p class="lead">One trusted team for your taxes, books and payroll, so nothing falls through the cracks.</p>
    </div>
    <div class="grid grid-3">{"".join(svc_card(s) for s in SERVICES)}
      <article class="card feature link reveal"><div class="ico">{I["chat"]}</div><h3>Not sure what you need?</h3><p>Tell us about your situation on a free call and we'll recommend the right mix of services.</p><a class="more stretch" href="{BOOK_HREF}"{BOOK_ATTR}>Book a free consultation</a></article>
    </div>
  </div>
</section>

<section class="section soft" id="finder-section">
  <div class="container">
    <div class="center head reveal">
      <span class="eyebrow">Find Your Fit</span>
      <h2>Which services are right for you?</h2>
      <p class="lead">Pick what describes you and we'll suggest where to start. It takes about 10 seconds.</p>
    </div>
    <div class="finder reveal">
      <form id="finder" onsubmit="return false">{finder_html}</form>
      <div class="finder-result" id="finder-out" aria-live="polite">
        <h3>Your recommended services</h3>
        <p class="finder-empty">Select an option on the left to see recommendations.</p>
        <ul hidden></ul>
        <a class="btn btn-primary" href="contact.html">Request a Free Consultation</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center head reveal">
      <span class="eyebrow">How It Works</span>
      <h2>Getting started takes 3 simple steps</h2>
      <p class="lead">No appointments to drive to and no piles of paper. Everything happens online, on your schedule.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="step-num">{I["calendar"]}</div><h3>Book a call</h3><p>Schedule a free consultation by phone or video. We'll learn about your situation and give you a clear quote.</p></div>
      <div class="step reveal"><div class="step-num">{I["upload"]}</div><h3>Send documents securely</h3><p>Upload tax forms, statements and receipts through a secure, encrypted link. No mailing and no office visits.</p></div>
      <div class="step reveal"><div class="step-num">{I["check"]}</div><h3>We handle the rest</h3><p>We prepare, review and file. You get clear updates and approve everything before it's submitted.</p></div>
    </div>
    <div class="center btn-row">{book_btn()}</div>
  </div>
</section>

<section class="section soft">
  <div class="container">
    <div class="center head reveal"><span class="eyebrow">The Smart Book Difference</span><h2>A better way to handle your finances</h2></div>
    <div class="compare">
      <div class="card old reveal"><h3>The old way</h3><ul>
        <li>Taking time off to drive to an office</li><li>Shoeboxes of paper receipts</li><li>Books months behind until tax season</li>
        <li>Guessing at quarterly payments</li><li>Different people for taxes, books and payroll</li></ul></div>
      <div class="card new reveal"><h3><span class="tag">Smart Book SD</span></h3><ul>
        <li>Meet by phone or video, wherever you are</li><li>Secure digital uploads from your phone or computer</li><li>Books reconciled every month</li>
        <li>Estimated tax amounts and reminders</li><li>Taxes, books and payroll under one roof</li></ul></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Why Smart Book SD</span>
      <h2>Professional service, without the office</h2>
      <p class="lead">Being fully online means less hassle for you and more time spent on what matters: getting your numbers right.</p>
      <ul class="feature-list">
        <li><span class="ico">{I["laptop"]}</span><div><strong>Work from anywhere</strong><span>Phone or video meetings and online file sharing. Your time is valuable.</span></div></li>
        <li><span class="ico">{I["lock"]}</span><div><strong>Privacy &amp; security first</strong><span>Encrypted document sharing and strict confidentiality for your financial information.</span></div></li>
        <li><span class="ico">{I["chat"]}</span><div><strong>Real, responsive people</strong><span>Plain-English answers from the person who actually works on your file.</span></div></li>
        <li><span class="ico">{I["map"]}</span><div><strong>California know-how</strong><span>Based in San Diego and familiar with California tax, LLC and payroll requirements.</span></div></li>
      </ul>
    </div>
    <div class="panel reveal">
      <h3>Who we help</h3>
      <div class="row"><span>Individuals &amp; families</span><b>Tax returns</b></div>
      <div class="row"><span>Freelancers &amp; gig workers</span><b>Schedule C</b></div>
      <div class="row"><span>LLCs &amp; sole proprietors</span><b>Taxes + books</b></div>
      <div class="row"><span>Growing small businesses</span><b>Payroll</b></div>
      <div class="row"><span>Behind on your books?</span><b>Catch-up</b></div>
      <div class="btn-row" style="position:relative">{book_btn("btn btn-light")}</div>
    </div>
  </div>
</section>
{testimonials}
<section class="section soft">
  <div class="container">
    <div class="center head reveal"><span class="eyebrow">Free Resources</span><h2>Tools to make tax season easier</h2></div>
    <div class="grid grid-2">
      <article class="card link reveal"><div class="ico">{I["calendar"]}</div><h3>2027 Tax Deadline Calendar</h3><p>Every key federal and California due date for individuals, the self-employed, businesses and employers, all in one place.</p><a class="more stretch" href="tax-deadlines.html">View deadlines</a></article>
      <article class="card link reveal"><div class="ico">{I["list"]}</div><h3>Interactive Tax Document Checklist</h3><p>Check off documents as you gather them. Your progress saves on your device, and you can print it.</p><a class="more stretch" href="document-checklist.html">Open checklist</a></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center head reveal"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
    {faq_block(HOME_FAQ)}
    <p class="center" style="margin-top:24px"><a href="faq.html">See all frequently asked questions →</a></p>
  </div>
</section>
{cta()}
'''

# ------------------------------ SERVICES OVERVIEW ------------------------------
bundles = [
    ("Business Essentials", "Monthly Bookkeeping + Small Business Taxes", "Clean books all year and a business return that flows straight from them.", ["bookkeeping", "business"]),
    ("Employer Package", "Bookkeeping + Payroll + Business Taxes", "Everything a business with employees needs, handled by one team.", ["bookkeeping", "payroll", "business"]),
    ("Fresh Start", "Catch-Up Bookkeeping + Monthly Bookkeeping", "Get current, then stay current. No more year-end scrambles.", ["catchup", "bookkeeping"]),
]
services_page = f'''
<section class="page-hero"><div class="container">
  {crumbs([("services.html", "Services")])}
  <span class="eyebrow">Services</span>
  <h1>Tax, bookkeeping &amp; payroll services</h1>
  <p class="lead">Practical, done-for-you financial services for individuals and small businesses, delivered 100% online to clients throughout California.</p>
  <div class="btn-row">{book_btn()}</div>
</div></section>
<section class="section" style="padding-top:24px"><div class="container">
  <div class="grid grid-3">{"".join(f"""<article class="card link reveal"><div class="ico">{I[s["icon"]]}</div><h2 style="font-size:1.25rem">{s["name"]}</h2><p>{s["short"]}</p>
<ul class="mini-list">{"".join(f"<li>{x}</li>" for x in s["includes"][:4])}</ul><a class="more stretch" href="{s["slug"]}.html">Learn more<span class="sr-only"> about {s["name"]}</span></a></article>""" for s in SERVICES)}
  <article class="card feature link reveal"><div class="ico">{I["chat"]}</div><h2 style="font-size:1.25rem;color:#fff">Not sure where to start?</h2><p>Book a free consultation and we'll recommend the right plan for your situation.</p><a class="more stretch" href="{BOOK_HREF}"{BOOK_ATTR}>Book a free consultation</a></article>
  </div>
</div></section>
<section class="section soft"><div class="container">
  <div class="center head reveal"><span class="eyebrow">Popular Combinations</span><h2>Services work better together</h2><p class="lead">Many clients combine services so their books, payroll and taxes stay perfectly in sync.</p></div>
  <div class="grid grid-3">{"".join(f"""<article class="card reveal"><span class="tag">{n}</span><h3 style="margin-top:14px">{sub}</h3><p>{d}</p><a class="btn btn-ghost" href="contact.html?service={",".join(k)}">Ask about this package</a></article>""" for n, sub, d, k in bundles)}</div>
</div></section>
{cta("Not sure which service fits?", "Every situation is different. Book a free consultation and we'll recommend the right plan for you.")}
'''


def service_page(s):
    others = "".join(f'<li><a href="{o["slug"]}.html"{" aria-current=\"page\"" if o is s else ""}>{o["nav"]}</a></li>' for o in SERVICES)
    steps = [("Free consultation", "We learn about your situation and give you a clear quote."),
             ("Secure onboarding", "You sign an engagement letter and upload documents through a secure link."),
             ("We do the work", "We prepare everything carefully and reach out if we have questions."),
             ("Review & finish", "We walk you through the results before anything is filed or finalized.")]
    body = f'''
<section class="page-hero"><div class="container">
  {crumbs([("services.html", "Services"), (s["slug"] + ".html", s["nav"])])}
  <div style="display:flex;gap:20px;align-items:center;margin-bottom:12px"><div class="ico-lg" style="margin:0">{I[s["icon"]]}</div><span class="eyebrow" style="margin:0">Online · San Diego &amp; California</span></div>
  <h1>{s["name"]}</h1>
  <p class="lead">{s["lead"]}</p>
  <div class="btn-row">{book_btn()}<a class="btn btn-ghost" href="tel:{PHONE_E164}">{I["phone"]} {PHONE}</a></div>
</div></section>
<section class="section" style="padding-top:32px"><div class="container svc-layout">
  <div class="prose">
    <h2>What's included</h2>
    <ul class="checks">{"".join(f"<li>{x}</li>" for x in s["includes"])}</ul>
    <h2>Who it's for</h2>
    <div class="ideal">{"".join(f"<span>{x}</span>" for x in s["ideal"])}</div>
    {s["body"]}
    <h2>How it works</h2>
    <ol class="process">{"".join(f"<li><strong>{a}</strong>{b}</li>" for a, b in steps)}</ol>
    <h2>Questions about {s["nav"].lower()}</h2>
    {faq_block(s["faqs"])}
  </div>
  <aside>
    <div class="aside-card">
      <h3>Get started with a free consultation</h3>
      <p>No obligation. We'll review your situation and give you a clear quote{f" — and we respond within {RESPONSE_TIME}" if RESPONSE_TIME else ""}.</p>
      <a class="btn btn-primary" href="{BOOKING_URL or "contact.html?service=" + s["key"]}"{BOOK_ATTR}>Book a Free Consultation</a>
      <a class="btn btn-ghost" href="tel:{PHONE_E164}">{I["phone"]} {PHONE}</a>
      <hr>
      <h3 style="font-size:1rem">All services</h3>
      <ul>{others}</ul>
    </div>
  </aside>
</div></section>
{cta()}
'''
    schema = [ORG_LD,
              {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
               "description": s["lead"], "provider": {"@id": SITE_URL + "/#business"},
               "areaServed": {"@type": "State", "name": "California"}, "url": f"{SITE_URL}/{s['slug']}.html"},
              crumbs_ld([("services.html", "Services"), (s["slug"] + ".html", s["nav"])]),
              faq_ld(s["faqs"])]
    return page(s["slug"] + ".html", f"{s['title']} | {BUSINESS}", s["lead"][:155], body, schema, active="services.html")


# ------------------------------ ABOUT ------------------------------
owner = f'<p>{BUSINESS} was founded by <strong>{e(OWNER_NAME)}</strong> to make professional tax and bookkeeping help simple and accessible.</p>' if OWNER_NAME else \
    f'<p>We started {BUSINESS} to make professional tax and bookkeeping help simple and accessible.</p>'
cred_row = f'<div class="row"><span>Credentials</span><b>{e(CREDENTIALS)}</b></div>' if CREDENTIALS else ""
about = f'''
<section class="page-hero"><div class="container">
  {crumbs([("about.html", "About")])}
  <span class="eyebrow">About Us</span>
  <h1>A modern, online approach to your finances</h1>
  <p class="lead">{BUSINESS} is a San Diego–based tax, bookkeeping and payroll firm that serves clients entirely online throughout California.</p>
</div></section>
<section class="section" style="padding-top:32px">
  <div class="container split">
    <div class="reveal">
      <h2>Our story</h2>
      {owner}
      <p>No office visits, no waiting rooms and no shoebox of receipts. Just clear communication, secure technology and careful, accurate work.</p>
      <p>Because we're 100% virtual, we can focus our time where it matters: getting your numbers right, keeping you compliant and helping you understand where your money is going.</p>
      <p>Whether you're filing a personal return, running an LLC, hiring your first employee or finally getting your books caught up, we'll treat your finances with the same care we'd give our own.</p>
      <div class="btn-row">{book_btn()}</div>
    </div>
    <div class="panel reveal">
      <h3>At a glance</h3>
      <div class="row"><span>Based in</span><b>San Diego, CA</b></div>
      <div class="row"><span>Service area</span><b>All of California</b></div>
      <div class="row"><span>How we work</span><b>100% online</b></div>
      <div class="row"><span>Bookkeeping software</span><b>QuickBooks Online</b></div>
      <div class="row"><span>First consultation</span><b>Free</b></div>
      {f'<div class="row"><span>Response time</span><b>Within {RESPONSE_TIME}</b></div>' if RESPONSE_TIME else ""}
      {cred_row}
    </div>
  </div>
</section>
<section class="section soft"><div class="container">
  <div class="center head reveal"><span class="eyebrow">What we value</span><h2>How we work with every client</h2></div>
  <div class="grid grid-4">
    <article class="card reveal"><div class="ico">{I["shield"]}</div><h3>Accuracy</h3><p>Careful, double-checked work that keeps you on the right side of the IRS and California agencies.</p></article>
    <article class="card reveal"><div class="ico">{I["lock"]}</div><h3>Confidentiality</h3><p>Your information is shared through encrypted channels and never sold. See our <a href="privacy.html">Privacy Policy</a>.</p></article>
    <article class="card reveal"><div class="ico">{I["chat"]}</div><h3>Clear communication</h3><p>Plain-English answers, timely updates and no surprises on deadlines or fees.</p></article>
    <article class="card reveal"><div class="ico">{I["heart"]}</div><h3>No judgment</h3><p>Behind on books or returns? We're here to help you move forward, not to lecture.</p></article>
  </div>
</div></section>
<section class="section"><div class="narrow">
  <div class="center head reveal"><span class="eyebrow">Our commitments</span><h2>What you can expect</h2></div>
  <ul class="feature-list">
    <li class="reveal"><span class="ico">{I["doc"]}</span><div><strong>A written engagement letter</strong><span>Before work begins, you'll know exactly what's included, what it costs and who is responsible for what.</span></div></li>
    <li class="reveal"><span class="ico">{I["check"]}</span><div><strong>Your review before filing</strong><span>We walk you through your return or reports, and nothing is filed without your approval.</span></div></li>
    <li class="reveal"><span class="ico">{I["lock"]}</span><div><strong>Secure document handling</strong><span>We collect sensitive documents through encrypted file sharing, never by regular email.</span></div></li>
    <li class="reveal"><span class="ico">{I["calendar"]}</span><div><strong>Deadline reminders</strong><span>We keep track of your filing and payment due dates and remind you ahead of time.</span></div></li>
  </ul>
</div></section>
{cta()}
'''

# ------------------------------ FAQ ------------------------------
FAQ_GROUPS = [
    ("Getting started", [
        ("How do I get started?", f"<a href=\"contact.html\">Request a free consultation</a> or call/text {PHONE}. We'll schedule a short phone or video call, learn about your needs and give you a quote. If you decide to move forward, we'll send an engagement letter and a secure upload link."),
        ("Is the consultation really free?", "Yes. The first consultation is free and there's no obligation to hire us."),
        ("How much do your services cost?", "Pricing depends on the complexity of your return, the volume of transactions in your books, and the size of your payroll. You'll receive a clear quote after your free consultation and before any work begins, so there are no surprises."),
        ("Do you work with clients outside San Diego?", "Yes. We're based in San Diego and work with individuals and businesses throughout California, entirely online."),
    ]),
    ("Working online & security", [
        ("Do I ever need to visit an office?", "No. We're a fully virtual firm. Meetings happen by phone or video and documents are shared electronically."),
        ("How do I send my documents?", "We'll provide a secure, encrypted upload link. You can upload photos or scans from your phone or computer. Please don't send Social Security numbers, bank account numbers or tax forms as regular email attachments or through our website contact form."),
        ("How do you protect my information?", "We limit access to client information, use encrypted file sharing, and keep tax return information confidential as required by federal law. Read our <a href=\"privacy.html\">Privacy Policy</a> for details."),
        ("Can I sign documents electronically?", "Yes. Engagement letters and e-file authorizations can be signed electronically where allowed."),
    ]),
    ("Taxes", [
        ("Do you prepare both federal and California returns?", "Yes. We prepare federal returns and California state returns for individuals and small businesses."),
        ("What if I receive a letter from the IRS or FTB?", "Don't panic, and don't ignore it. Send us a copy through your secure link. Many notices are routine and can be resolved quickly."),
        ("Can you help if I haven't filed in a few years?", "Yes. We can prepare past-due returns and help you get back on track."),
        ("Can I get an extension?", "Yes. An extension gives you more time to file, but generally not more time to pay. We can file extensions and estimate any payment due. See our <a href=\"tax-deadlines.html\">tax deadline calendar</a>."),
    ]),
    ("Bookkeeping & payroll", [
        ("What software do you use for bookkeeping?", "We work in QuickBooks Online. If you're not on it yet, we'll help you get set up."),
        ("How behind is too behind?", "There's no such thing. Our <a href=\"catch-up-bookkeeping.html\">catch-up bookkeeping</a> service is designed for businesses that are months or years behind."),
        ("Can you run payroll for just one or two employees?", "Absolutely. Many of our payroll clients are small teams, including S-corp owners paying only themselves."),
    ]),
]
all_faq = [p for _, g in FAQ_GROUPS for p in g]
faq_page = f'''
<section class="page-hero"><div class="container">
  {crumbs([("faq.html", "FAQ")])}
  <span class="eyebrow">FAQ</span>
  <h1>Frequently asked questions</h1>
  <p class="lead">Answers to the questions we hear most. Don't see yours? <a href="contact.html">Ask us directly</a>.</p>
</div></section>
<section class="section" style="padding-top:32px"><div class="narrow">
  {"".join(f'<div class="faq-group"><h2>{t}</h2>{faq_block(g)}</div>' for t, g in FAQ_GROUPS)}
</div></section>
{cta("Still have questions?", "We're happy to help. Book a free consultation or give us a call.")}
'''

# ------------------------------ RESOURCES ------------------------------
resources = f'''
<section class="page-hero"><div class="container">
  {crumbs([("resources.html", "Resources")])}
  <span class="eyebrow">Resources</span>
  <h1>Free tax &amp; bookkeeping resources</h1>
  <p class="lead">Helpful tools and official links to keep you organized and on time all year.</p>
</div></section>
<section class="section" style="padding-top:32px"><div class="container">
  <div class="grid grid-2">
    <article class="card link reveal"><div class="ico">{I["calendar"]}</div><h2 style="font-size:1.3rem">2027 Tax Deadline Calendar</h2><p>Key federal and California due dates for individuals, self-employed people, businesses and employers, with filters.</p><a class="more stretch" href="tax-deadlines.html">View deadlines</a></article>
    <article class="card link reveal"><div class="ico">{I["list"]}</div><h2 style="font-size:1.3rem">Tax Document Checklist</h2><p>An interactive, printable checklist of what to gather for your tax return. Progress saves on your device.</p><a class="more stretch" href="document-checklist.html">Open checklist</a></article>
  </div>
  <div class="head center reveal" style="margin:72px 0 32px"><span class="eyebrow">Official Links</span><h2>Helpful government websites</h2></div>
  <div class="grid grid-3">
    {"".join(f'''<article class="card link reveal"><h3>{n}</h3><p>{d}</p><a class="more stretch" href="{u}" target="_blank" rel="noopener">Visit {host}<span class="sr-only"> (opens in a new tab)</span></a></article>''' for n, d, u, host in [
        ("Where's My Refund? (IRS)", "Check the status of your federal tax refund.", "https://www.irs.gov/refunds", "IRS.gov"),
        ("IRS Direct Pay", "Make federal tax and estimated payments directly from your bank account.", "https://www.irs.gov/payments/direct-pay", "IRS.gov"),
        ("IRS Online Account", "View your federal balance, payment history and tax records.", "https://www.irs.gov/payments/your-online-account", "IRS.gov"),
        ("CA Franchise Tax Board", "California refunds, payments and MyFTB account access.", "https://www.ftb.ca.gov/", "FTB.ca.gov"),
        ("CA Employment Development Dept.", "California payroll tax registration and e-Services for Business.", "https://edd.ca.gov/en/payroll_taxes/", "EDD.ca.gov"),
        ("CA Secretary of State: bizfile", "Business entity filings and the LLC Statement of Information.", "https://bizfileonline.sos.ca.gov/", "sos.ca.gov"),
    ])}
  </div>
  <p class="form-note center" style="margin-top:24px">We are not affiliated with these agencies. Links are provided for convenience.</p>
</div></section>
{cta()}
'''

# ------------------------------ DEADLINES ------------------------------
def adj(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


D = lambda y, m, d: adj(dt.date(y, m, d))
DEADLINES = [
    (D(2027, 1, 15), "Q4 2026 estimated tax payment", ["Federal 4th-quarter estimated tax (Form 1040-ES)", "California 4th estimated payment (Form 540-ES)"], ["individual", "self"]),
    (D(2027, 1, 31), "W-2s, 1099-NECs & Q4 payroll returns", ["Furnish W-2s to employees and file with the SSA", "Furnish and file 1099-NEC for contractors", "Federal Form 941 (Q4) and Form 940 (annual FUTA)", "California EDD DE 9 and DE 9C (Q4)"], ["business", "employer"]),
    (D(2027, 3, 15), "Partnership & S-corp returns", ["Form 1065 (partnerships & multi-member LLCs)", "Form 1120-S (S corporations)", "California Form 565 / 568 / 100S as applicable", "Deadline to request a 6-month extension"], ["business"]),
    (D(2027, 4, 15), "Individual tax day + Q1 estimates", ["Federal Form 1040 and California Form 540 for 2026", "Deadline to file an extension (to October 15)", "Q1 2027 estimated tax, federal and California", "C-corporation returns (Form 1120 / CA 100) for calendar-year filers", "California LLC annual tax (Form 3522) for calendar-year LLCs", "Single-member LLC Form 568 (owned by an individual)"], ["individual", "self", "business"]),
    (D(2027, 4, 30), "Q1 payroll returns", ["Federal Form 941 (Q1)", "California EDD DE 9 and DE 9C (Q1)"], ["employer"]),
    (D(2027, 6, 15), "Q2 estimated tax payment", ["Federal Q2 estimated tax", "California Q2 estimated tax (CA has no September payment)"], ["individual", "self"]),
    (D(2027, 7, 31), "Q2 payroll returns", ["Federal Form 941 (Q2)", "California EDD DE 9 and DE 9C (Q2)"], ["employer"]),
    (D(2027, 9, 15), "Q3 estimates + extended business returns", ["Federal Q3 estimated tax", "Extended Form 1065 and Form 1120-S returns"], ["self", "business"]),
    (D(2027, 10, 15), "Extended individual returns", ["Extended 2026 Form 1040 and California Form 540", "Extended C-corporation returns (Form 1120)"], ["individual", "self", "business"]),
    (D(2027, 10, 31), "Q3 payroll returns", ["Federal Form 941 (Q3)", "California EDD DE 9 and DE 9C (Q3)"], ["employer"]),
    (D(2028, 1, 15), "Q4 2027 estimated tax payment", ["Federal 4th-quarter estimated tax", "California 4th estimated payment"], ["individual", "self"]),
]
WHO = {"individual": "Individuals", "self": "Self-employed", "business": "Businesses", "employer": "Employers"}
dl_items = "".join(f'''<li class="deadline reveal" data-date="{d.isoformat()}" data-who="{' '.join(w)}">
  <div class="date-badge"><small>{d.strftime("%b")}</small><b>{d.day}</b><small>{d.strftime("%a")} · {d.year}</small></div>
  <div><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul><div class="who">{"".join(f"<span>{WHO[x]}</span>" for x in w)}</div></div>
</li>''' for d, t, items, w in DEADLINES)
filt = '<label class="chip"><input type="radio" name="who" value="all" checked><span>All</span></label>' + "".join(
    f'<label class="chip"><input type="radio" name="who" value="{k}"><span>{v}</span></label>' for k, v in WHO.items())
deadlines_page = f'''
<section class="page-hero"><div class="container">
  {crumbs([("resources.html", "Resources"), ("tax-deadlines.html", "Tax Deadlines")])}
  <span class="eyebrow">Free Resource</span>
  <h1>2027 tax deadline calendar</h1>
  <p class="lead">Key federal and California filing and payment due dates for calendar-year taxpayers, adjusted for weekends.</p>
</div></section>
<section class="section" style="padding-top:32px"><div class="narrow">
  <div class="notice no-print" style="margin-bottom:24px"><strong>Please note:</strong> Dates shown are for calendar-year filers and move to the next business day when they fall on a weekend. Holidays, disaster relief and fiscal-year filing can change your actual due dates. Always confirm with us, <a href="https://www.irs.gov" target="_blank" rel="noopener">IRS.gov</a> or <a href="https://www.ftb.ca.gov" target="_blank" rel="noopener">FTB.ca.gov</a>.</div>
  <fieldset class="filter-bar" id="deadline-filter" style="border:0;padding:0;margin:0 0 24px"><legend class="sr-only">Filter deadlines by taxpayer type</legend><div class="chips">{filt}</div></fieldset>
  <ol class="deadlines" id="deadlines">{dl_items}</ol>
</div></section>
{cta("Never miss a deadline again", "When you work with us, we track your due dates and remind you ahead of time. Book a free consultation to get started.")}
'''

# ------------------------------ CHECKLIST ------------------------------
CHECK = [
    ("person", "Personal information", [("Last year's federal and California tax returns", ""), ("Social Security numbers and birth dates for you, your spouse and dependents", "Share these only through our secure link"), ("Bank routing and account number for direct deposit", ""), ("IRS Identity Protection PIN (if you have one)", "")]),
    ("doc", "Income", [("W-2s from every employer", ""), ("1099-NEC / 1099-K / 1099-MISC for freelance or gig income", ""), ("1099-INT, 1099-DIV and 1099-B from banks and brokerages", ""), ("1099-R for retirement distributions; SSA-1099 for Social Security", ""), ("1099-G for unemployment or state refunds", ""), ("K-1s from partnerships, S-corps or trusts", "")]),
    ("home", "Deductions & credits", [("Form 1098 mortgage interest statement", ""), ("Property tax and vehicle registration (VLF) records", ""), ("Charitable donation receipts", ""), ("Childcare provider name, tax ID and amount paid", ""), ("Form 1098-T tuition and 1098-E student loan interest", ""), ("Form 1095-A if you had Covered California health insurance", ""), ("HSA (Form 5498-SA / 1099-SA) and IRA contribution records", "")]),
    ("briefcase", "Self-employed & small business", [("Profit & loss statement or bookkeeping records", ""), ("Business bank and credit card statements", ""), ("Home office square footage and household expenses", ""), ("Vehicle mileage log", ""), ("Receipts for equipment and major purchases", ""), ("Estimated tax payments made during the year (federal & CA)", ""), ("1099s you issued to contractors", "")]),
    ("map", "Rental property", [("Rents received", ""), ("Expenses: repairs, insurance, HOA, utilities, management fees", ""), ("Purchase documents for newly acquired property", "")]),
]
cl_html = ""
n = 0
for icon, title, items in CHECK:
    rows = ""
    for t, sub in items:
        n += 1
        rows += f'<label class="check-item" for="c{n}"><input type="checkbox" id="c{n}"><span>{t}{f"<small>{sub}</small>" if sub else ""}</span></label>'
    cl_html += f'<section class="check-group reveal"><h2><span class="ico">{I[icon]}</span>{title}</h2>{rows}</section>'
checklist_page = f'''
<section class="page-hero"><div class="container">
  {crumbs([("resources.html", "Resources"), ("document-checklist.html", "Document Checklist")])}
  <span class="eyebrow">Free Resource</span>
  <h1>Tax document checklist</h1>
  <p class="lead">Check off documents as you gather them. Your progress saves privately in this browser on this device, and nothing is sent to us.</p>
</div></section>
<section class="section" style="padding-top:32px"><div class="narrow" id="checklist">
  <div class="checklist-tools">
    <div class="progress"><strong id="cl-count" aria-live="polite">0 gathered</strong><div class="progress-bar" aria-hidden="true"><span id="cl-bar"></span></div></div>
    <div style="display:flex;gap:10px"><button class="btn btn-ghost" type="button" id="cl-reset">Reset</button><button class="btn btn-primary" type="button" id="cl-print">Print</button></div>
  </div>
  {cl_html}
  <p class="notice">Not every item applies to everyone. On your free consultation, we'll send you a personalized list. <strong>Never email sensitive documents.</strong> Use the secure upload link we provide.</p>
</div></section>
{cta("Got your documents together?", "Book a free consultation and we'll take it from here.")}
'''

# ------------------------------ CONTACT ------------------------------
svc_checks = "".join(f'<label class="chip"><input type="checkbox" name="services" value="{s["key"]}"><span>{s["nav"]}</span></label>' for s in SERVICES) + \
    '<label class="chip"><input type="checkbox" name="services" value="not-sure"><span>Not sure yet</span></label>'
contact = f'''
<section class="page-hero"><div class="container">
  {crumbs([("contact.html", "Contact")])}
  <span class="eyebrow">Contact</span>
  <h1>Book your free consultation</h1>
  <p class="lead">Tell us a little about what you need and we'll reach out{f" within {RESPONSE_TIME}" if RESPONSE_TIME else ""} to schedule a phone or video call. No obligation.</p>
</div></section>
<section class="section" style="padding-top:32px">
  <div class="container contact-grid">
    <div>
      <h2 style="font-size:1.5rem">Prefer to reach us directly?</h2>
      <div class="contact-item"><span class="ico">{I["phone"]}</span><div><small>Call or text</small><a href="tel:{PHONE_E164}">{PHONE}</a></div></div>
      <div class="contact-item"><span class="ico">{I["mail"]}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
      <div class="contact-item"><span class="ico">{I["laptop"]}</span><div><small>How we meet</small><strong>Phone or video, 100% online</strong></div></div>
      <div class="contact-item"><span class="ico">{I["map"]}</span><div><small>Service area</small><strong>San Diego &amp; all of California</strong></div></div>
      {f'<div class="contact-item"><span class="ico">{I["clock"]}</span><div><small>Response time</small><strong>Within {RESPONSE_TIME}</strong></div></div>' if RESPONSE_TIME else ""}
      <p class="form-note" style="margin-top:20px">We're a fully virtual firm with no walk-in office. Consultations are by appointment.</p>
      <div class="panel" style="margin-top:28px;padding:28px">
        <h3>What happens next?</h3>
        <ol class="process" style="color:#c9d6e3;margin:0">
          <li><strong style="color:#fff">We reach out</strong>to schedule a time that works for you.</li>
          <li><strong style="color:#fff">Free consultation</strong>15–30 minutes by phone or video.</li>
          <li><strong style="color:#fff">Clear quote</strong>so you know the cost before any work begins.</li>
        </ol>
      </div>
    </div>
    <form class="form-card" id="contact-form" novalidate>
      <h2 style="font-size:1.5rem">Request a free consultation</h2>
      <input type="hidden" name="_subject" value="New consultation request: {BUSINESS} website">
      <input type="hidden" name="_template" value="table">
      <div class="hp" aria-hidden="true"><label for="hp">Leave this field empty</label><input id="hp" name="_honey" tabindex="-1" autocomplete="off"></div>
      <div class="field-row">
        <div class="field"><label for="name">Full name</label><input id="name" name="name" autocomplete="name" required aria-describedby="name-err"><span class="err" id="name-err">Please enter your name.</span></div>
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-err"><span class="err" id="email-err">Please enter a valid email address.</span></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="phone">Phone <span class="opt">(optional)</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
        <div class="field"><label for="type">I am a…</label>
          <select id="type" name="client_type" required aria-describedby="type-err"><option value="">Select one…</option><option>Individual / family</option><option>Freelancer / self-employed</option><option>LLC or small business</option><option>Business with employees</option></select><span class="err" id="type-err">Please choose one.</span></div>
      </div>
      <div class="field" id="svc-field" role="group" aria-labelledby="svc-label">
        <span class="label" id="svc-label">Services I'm interested in</span>
        <div class="chips">{svc_checks}</div>
        <span class="err">Please choose at least one.</span>
      </div>
      <div class="field-row">
        <div class="field"><label for="pref">Best way to reach you</label>
          <select id="pref" name="contact_preference"><option>Phone call</option><option>Video call</option><option>Email</option><option>Text message</option></select></div>
        <div class="field"><label for="time">Best time <span class="opt">(optional)</span></label>
          <select id="time" name="best_time"><option>Any time</option><option>Morning</option><option>Afternoon</option><option>Evening</option></select></div>
      </div>
      <div class="field"><label for="message">Tell us about your situation <span class="opt">(optional)</span></label><textarea id="message" name="message" rows="5" maxlength="2000" placeholder="e.g., I have an LLC and I'm about 6 months behind on bookkeeping…"></textarea></div>
      <div class="field" style="margin:0"><label for="source">How did you hear about us? <span class="opt">(optional)</span></label>
        <select id="source" name="referral_source"><option value="">Select…</option><option>Google search</option><option>Social media</option><option>Referral from a friend or client</option><option>Online review site</option><option>Other</option></select></div>
      <label class="consent" for="consent" style="margin-top:18px"><input type="checkbox" id="consent" name="consent" value="yes" required>
        <span>I agree that {BUSINESS} may contact me by phone, text or email about my inquiry, and I have read the <a href="privacy.html">Privacy Policy</a>. Consent is not a condition of purchase. Message &amp; data rates may apply; reply STOP to opt out of texts.</span></label>
      <button class="btn btn-primary" type="submit" style="width:100%">Request My Free Consultation</button>
      <p class="form-status" id="form-status" role="status" tabindex="-1"></p>
      <p class="form-note">{I["lock"].replace('<svg', '<svg style="display:inline;width:14px;height:14px;vertical-align:-2px;margin-right:4px"')}Please <strong>don't</strong> include Social Security numbers, account numbers or tax documents in this form. We'll send a secure upload link after we connect. Submitting this form does not create a client relationship.</p>
    </form>
  </div>
</section>
'''

# ------------------------------ LEGAL ------------------------------
privacy = f'''
<section class="page-hero"><div class="container">{crumbs([("privacy.html", "Privacy Policy")])}<h1>Privacy Policy</h1><p class="updated">Effective {LEGAL_EFFECTIVE}</p></div></section>
<section class="section legal" style="padding-top:24px"><div class="narrow">
<p>This Privacy Policy explains how {BUSINESS} (“we,” “us”) collects, uses, shares and protects personal information through this website and in providing tax preparation, bookkeeping and payroll services. It is intended to comply with the California Online Privacy Protection Act (CalOPPA) and to describe the privacy rights available to California residents.</p>

<h2>Information we collect</h2>
<h3>Information you give us through this website</h3>
<p>When you submit our contact form, we collect your name, email address, phone number (if provided), the type of client you are, the services you're interested in, your preferred contact method and time, how you heard about us, and any message you include. Please do not submit Social Security numbers, financial account numbers or tax documents through the form.</p>
<h3>Information from clients</h3>
<p>If you become a client, we collect the information needed to provide our services. This may include identification details, Social Security or taxpayer identification numbers, income and tax documents, bank and credit card statements, payroll and employee information, and business financial records. You provide this through secure file-sharing tools after you sign an engagement letter.</p>
<h3>Information collected automatically</h3>
<p>This website does <strong>not</strong> use cookies, analytics, advertising pixels or tracking scripts. Our hosting provider may automatically log technical information (such as IP address, browser type and pages requested) for security and operations. The optional document checklist saves your check-marks only in your own browser's local storage on your device; that data is never sent to us.</p>

<h2>How we use information</h2>
<ul>
<li>To respond to your inquiry and schedule consultations</li>
<li>To provide, bill for and improve our services</li>
<li>To prepare and file tax returns, maintain books and process payroll as you authorize</li>
<li>To communicate with you about your account, deadlines and services</li>
<li>To comply with legal, regulatory and professional obligations and to protect against fraud</li>
</ul>

<h2>Tax return information</h2>
<p>Information you provide for tax preparation is protected by federal law, including Internal Revenue Code Section 7216. We do not use or disclose your tax return information for any purpose other than preparing your return, unless you give specific written consent or the disclosure is otherwise permitted by law (for example, to file your return with the IRS and California agencies).</p>

<h2>How we share information</h2>
<p><strong>We do not sell your personal information, and we do not share it for cross-context behavioral advertising.</strong> We share information only:</p>
<ul>
<li>With government agencies (such as the IRS, California Franchise Tax Board and EDD) when filing on your behalf</li>
<li>With service providers that help us operate, under confidentiality obligations, such as our email provider, secure file-sharing and e-signature tools, accounting and payroll software (such as QuickBooks Online), website hosting (GitHub Pages) and our website form-forwarding service (FormSubmit), which delivers contact-form submissions to our inbox</li>
<li>When required by law, subpoena or to protect rights and safety</li>
<li>With your direction or consent</li>
</ul>

<h2>How we protect information</h2>
<p>We maintain administrative, technical and physical safeguards designed to protect client information, consistent with the FTC Safeguards Rule and IRS guidance for tax professionals. These include encrypted file sharing, limited access, strong authentication and secure disposal. No method of transmission or storage is completely secure, so please use the secure channels we provide for sensitive documents.</p>

<h2>Retention</h2>
<p>We keep inquiry information only as long as needed to respond and follow up. We retain client records for as long as needed to provide services and to meet legal and professional record-keeping requirements, then securely dispose of them.</p>

<h2>Your California privacy rights</h2>
<p>Depending on applicable law, California residents may have the right to:</p>
<ul>
<li><strong>Know</strong> what personal information we collect, use and disclose</li>
<li><strong>Access</strong> a copy of your personal information</li>
<li><strong>Correct</strong> inaccurate personal information</li>
<li><strong>Delete</strong> personal information, subject to legal exceptions (for example, records we must keep by law)</li>
<li><strong>Not be discriminated against</strong> for exercising these rights</li>
</ul>
<p>Because we do not sell or share personal information or use sensitive personal information for purposes requiring a limit, there is nothing to opt out of. To make a request, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_E164}">{PHONE}</a>. We will verify your identity before responding and respond within the time required by law. You may use an authorized agent with your written permission.</p>
<p><strong>California “Shine the Light”:</strong> We do not disclose personal information to third parties for their own direct marketing purposes.</p>

<h2>Do Not Track and Global Privacy Control</h2>
<p>Because this website does not track visitors across sites or over time, it does not change its behavior in response to Do Not Track signals. If you use Global Privacy Control, it is honored by default because we do not sell or share personal information.</p>

<h2>Text messages</h2>
<p>If you agree to receive text messages, we will text only about your inquiry or account. Message and data rates may apply. Reply STOP to opt out or HELP for help. We do not share mobile numbers or text-messaging consent with third parties for their marketing.</p>

<h2>Children</h2>
<p>This website is not directed to children under 16, and we do not knowingly collect their personal information through it. Information about minor dependents is collected only from parents or guardians as part of tax services.</p>

<h2>Links to other websites</h2>
<p>Our site links to government and other websites we don't control. Their privacy practices are governed by their own policies.</p>

<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. We'll post the new version here with a new effective date.</p>

<h2>Contact us</h2>
<p>{BUSINESS}<br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br>Phone: <a href="tel:{PHONE_E164}">{PHONE}</a></p>
</div></section>
'''

terms = f'''
<section class="page-hero"><div class="container">{crumbs([("terms.html", "Terms of Use")])}<h1>Terms of Use</h1><p class="updated">Effective {LEGAL_EFFECTIVE}</p></div></section>
<section class="section legal" style="padding-top:24px"><div class="narrow">
<p>By using this website, you agree to these Terms of Use. If you do not agree, please do not use the site.</p>
<h2>Informational purposes only</h2>
<p>Content on this website, including articles, deadline calendars and checklists, is general information. It is not tax, legal, accounting or financial advice, and it may not apply to your specific situation. Tax laws and due dates change. Do not act on website content without consulting a qualified professional about your circumstances.</p>
<h2>No client relationship</h2>
<p>Visiting this website, submitting the contact form, or communicating with us by phone, text or email does not create a client relationship. A client relationship begins only when we both sign a written engagement letter describing the scope of services and fees.</p>
<h2>No guarantees</h2>
<p>We do not guarantee any particular result, refund amount or outcome with any taxing authority. Illustrations on this website, such as sample dashboards, are examples only and do not represent actual client results.</p>
<h2>Do not send sensitive information through this website</h2>
<p>Please do not submit Social Security numbers, financial account numbers or tax documents through the website contact form or regular email. We provide secure methods after engagement.</p>
<h2>Third-party links</h2>
<p>Links to third-party websites, including government agencies, are provided for convenience. We are not responsible for their content or practices and are not affiliated with them.</p>
<h2>Intellectual property</h2>
<p>The content, design and branding of this website belong to {BUSINESS} unless otherwise noted. You may print or share pages for personal, non-commercial use. QuickBooks is a registered trademark of Intuit Inc.; other trademarks belong to their respective owners.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent permitted by law, {BUSINESS} is not liable for any damages arising from your use of, or reliance on, this website or its content. The website is provided “as is” without warranties of any kind.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the State of California. Any dispute relating to this website will be resolved in the courts located in San Diego County, California.</p>
<h2>Changes</h2>
<p>We may update these terms at any time by posting a revised version on this page.</p>
<h2>Contact</h2>
<p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_E164}">{PHONE}</a>.</p>
</div></section>
'''

accessibility = f'''
<section class="page-hero"><div class="container">{crumbs([("accessibility.html", "Accessibility")])}<h1>Accessibility Statement</h1><p class="updated">Updated {LEGAL_EFFECTIVE}</p></div></section>
<section class="section legal" style="padding-top:24px"><div class="narrow">
<p>{BUSINESS} is committed to making our website usable by everyone, including people with disabilities. We aim to conform to the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA.</p>
<h2>What we've done</h2>
<ul>
<li>Semantic headings, landmarks and a “skip to main content” link</li>
<li>Full keyboard navigation with visible focus indicators</li>
<li>Text and interface colors chosen for sufficient contrast</li>
<li>Labels and error messages on every form field</li>
<li>Layouts that adapt to phones, tablets, zoom up to 200% and larger text</li>
<li>Animations that turn off automatically if your device is set to reduce motion</li>
</ul>
<h2>Need help or found a problem?</h2>
<p>If any part of this site is difficult to use, please let us know and we'll provide the information in another way and work to fix it. Contact us at <a href="mailto:{EMAIL}">{EMAIL}</a> or <a href="tel:{PHONE_E164}">{PHONE}</a>. Because we serve clients entirely by phone, video and email, we're happy to accommodate the format that works best for you.</p>
</div></section>
'''

notfound = f'''
<section class="page-hero" style="padding:120px 0"><div class="container center">
  <span class="eyebrow">Error 404</span>
  <h1>We couldn't find that page</h1>
  <p class="lead">The page may have moved. Try one of these instead:</p>
  <div class="btn-row"><a class="btn btn-primary" href="index.html">Go to Home</a><a class="btn btn-ghost" href="services.html">View Services</a><a class="btn btn-ghost" href="contact.html">Contact Us</a></div>
</div></section>
'''

# ------------------------------ WRITE ------------------------------
PAGES = [
    ("index.html", "Online Tax, Bookkeeping & Payroll in San Diego | Smart Book SD",
     "100% online tax preparation, QuickBooks bookkeeping and payroll for individuals and small businesses in San Diego and across California. Book a free consultation.",
     home, [ORG_LD, {"@context": "https://schema.org", "@type": "WebSite", "name": BUSINESS, "url": SITE_URL + "/"}, faq_ld(HOME_FAQ)], 1.0),
    ("services.html", "Tax, Bookkeeping & Payroll Services | Smart Book SD",
     "Individual and small business tax returns, QuickBooks bookkeeping, payroll and catch-up bookkeeping, all 100% online for clients across California.",
     services_page, [ORG_LD, crumbs_ld([("services.html", "Services")])], 0.9),
    ("about.html", "About Smart Book SD | Online Tax & Bookkeeping Firm",
     "Smart Book SD is a San Diego–based, 100% online tax, bookkeeping and payroll firm serving individuals and small businesses across California.",
     about, [ORG_LD, crumbs_ld([("about.html", "About")])], 0.7),
    ("faq.html", "Frequently Asked Questions | Smart Book SD",
     "Answers about working with an online tax, bookkeeping and payroll firm: getting started, pricing, security, taxes, QuickBooks and payroll.",
     faq_page, [crumbs_ld([("faq.html", "FAQ")]), faq_ld(all_faq)], 0.7),
    ("resources.html", "Free Tax & Bookkeeping Resources | Smart Book SD",
     "Free tax deadline calendar, interactive tax document checklist and official IRS and California tax links.",
     resources, [crumbs_ld([("resources.html", "Resources")])], 0.6),
    ("tax-deadlines.html", "2027 Tax Deadline Calendar: Federal & California | Smart Book SD",
     "Key 2027 federal and California tax deadlines for individuals, self-employed people, businesses and employers: estimated taxes, payroll filings and more.",
     deadlines_page, [crumbs_ld([("resources.html", "Resources"), ("tax-deadlines.html", "Tax Deadlines")])], 0.8),
    ("document-checklist.html", "Tax Document Checklist (Interactive & Printable) | Smart Book SD",
     "Free interactive checklist of the documents you need for your tax return: income, deductions, self-employment and rental property. Printable.",
     checklist_page, [crumbs_ld([("resources.html", "Resources"), ("document-checklist.html", "Document Checklist")])], 0.8),
    ("contact.html", "Book a Free Consultation | Smart Book SD",
     f"Request a free online consultation for tax, bookkeeping or payroll services. Call or text {PHONE} or email {EMAIL}.",
     contact, [ORG_LD, crumbs_ld([("contact.html", "Contact")])], 0.9),
    ("privacy.html", "Privacy Policy | Smart Book SD", "How Smart Book SD collects, uses and protects your personal information, and your California privacy rights.", privacy, [], 0.3),
    ("terms.html", "Terms of Use | Smart Book SD", "Terms of use for the Smart Book SD website.", terms, [], 0.3),
    ("accessibility.html", "Accessibility Statement | Smart Book SD", "Smart Book SD's commitment to website accessibility (WCAG 2.1 AA).", accessibility, [], 0.3),
]

today = dt.date.today().isoformat()
urls = []
for fname, title, desc, body, schema, prio in PAGES:
    with open(os.path.join(ROOT, fname), "w") as f:
        f.write(page(fname, title, desc, body, schema))
    urls.append((fname, prio))
for s in SERVICES:
    with open(os.path.join(ROOT, s["slug"] + ".html"), "w") as f:
        f.write(service_page(s))
    urls.append((s["slug"] + ".html", 0.9))
with open(os.path.join(ROOT, "404.html"), "w") as f:
    f.write(page("404.html", "Page Not Found | Smart Book SD", "Page not found.", notfound, noindex=True, active=""))

with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u, p in urls:
        loc = SITE_URL + "/" + ("" if u == "index.html" else u)
        f.write(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
print(f"Built {len(urls) + 1} pages.")
