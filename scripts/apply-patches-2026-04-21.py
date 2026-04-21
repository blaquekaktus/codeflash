#!/usr/bin/env python3
"""
scripts/apply-patches-2026-04-21.py

Applies drift + pricing patches to index.html per
docs/PATCHES_INDEX_HTML_2026-04-21.md §§ 1, 2, 3, 6, 7, 8.

Idempotent — safe to re-run. Exits non-zero if index.html is missing
or a required anchor isn't found (indicates manual changes have
diverged the file; re-check the patch doc manually).

Usage from the codeflash repo root:

    python3 scripts/apply-patches-2026-04-21.py
    git diff index.html           # review
    git add index.html && git commit -m "apply drift + pricing patches" && git push

Netlify auto-deploys within ~60s of push.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SRC = Path("index.html")
if not SRC.exists():
    sys.stderr.write("index.html not found — run from the codeflash repo root\n")
    sys.exit(1)

html = SRC.read_text(encoding="utf-8")
original = html

# --- §1 Stats reconciliation ------------------------------------------------

html = html.replace("80 interactive flashcard packs", "82 interactive flashcard packs")
html = html.replace('<div class="stat-val">80</div>', '<div class="stat-val">82</div>')
html = html.replace('<div class="stat-val">1,600</div>', '<div class="stat-val">1,640</div>')
html = html.replace('<div class="stat-val">30</div>', '<div class="stat-val">32</div>')
html = html.replace("14 packs covering OWASP, pentesting", "15 packs covering OWASP, pentesting")
html = html.replace("14 PACKS / 280 CARDS", "15 PACKS / 300 CARDS")

# --- §2 OG / Twitter URLs ---------------------------------------------------

html = html.replace(
    "https://blaquekaktus.github.io/flashcards-programming-app/",
    "https://codeflash.lechner-studios.at/",
)

# --- §3 Footer: brand domain + legal links ----------------------------------

html = html.replace("https://lechnerstudios.at", "https://lechner-studios.at")

if 'href="legal/impressum.html"' not in html:
    html = html.replace(
        '<span style="margin-top:.75rem;display:inline-block;font-size:.7rem;color:var(--dim);">Built by',
        '<br><span style="margin-top:.5rem;display:inline-block;font-size:.75rem;">'
        '<a href="legal/impressum.html" style="color:var(--muted);text-decoration:none;'
        'border-bottom:1px solid var(--border);">Impressum</a> · '
        '<a href="legal/datenschutz.html" style="color:var(--muted);text-decoration:none;'
        'border-bottom:1px solid var(--border);">Datenschutz</a>'
        "</span>"
        '<br><span style="margin-top:.75rem;display:inline-block;font-size:.7rem;color:var(--dim);">Built by',
    )

# --- §6 Pricing: replace All-Access block -----------------------------------

ACCESS_PATTERN = re.compile(
    r'<div class="bundle-card" style="text-align:center;padding:2rem;">\s*'
    r'<div class="bundle-name"[^>]*>All-Access\s*[—-]\s*1 Year</div>.*?'
    r'<span class="bundle-btn"[^>]*>Store Opening Soon</span>\s*</div>\s*'
    r'<div class="bundle-card featured"[^>]*>\s*<div class="bundle-badge">BEST VALUE</div>\s*'
    r'<div class="bundle-name"[^>]*>All-Access\s*[—-]\s*Lifetime</div>.*?'
    r'<span class="bundle-btn"[^>]*>Store Opening Soon</span>\s*</div>',
    re.DOTALL,
)

ACCESS_NEW = '''<div class="bundle-card" style="text-align:center;padding:2rem;">
<div class="bundle-name" style="font-size:1.1rem;">All-Access · Monthly</div>
<div class="bundle-price" style="font-size:2.2rem;">€9 <small>/month</small></div>
<div class="bundle-desc">Stream the full catalog via the web app. Non-downloadable. Cancel anytime.</div>
<span class="bundle-btn" style="background:var(--surface2);color:var(--dim);cursor:default;border:1px solid var(--border)">Store Opening Soon</span>
</div>
<div class="bundle-card featured" style="text-align:center;padding:2rem;">
<div class="bundle-badge">BEST VALUE</div>
<div class="bundle-name" style="font-size:1.1rem;">All-Access · Annual</div>
<div class="bundle-price" style="font-size:2.2rem;">€99 <small>/year</small></div>
<div class="bundle-desc">€8.25 / month equivalent — 1 month free. Streaming access to the full catalog; non-downloadable.</div>
<span class="bundle-btn" style="background:var(--surface2);color:var(--dim);cursor:default;border:1px solid var(--border)">Store Opening Soon</span>
</div>'''

html_after, n = ACCESS_PATTERN.subn(ACCESS_NEW, html)
if n == 0 and "All-Access · Monthly" not in html:
    sys.stderr.write("§6 All-Access block anchor not found — index.html may have diverged\n")
    sys.exit(2)
html = html_after

# --- §6 Specialisation bundle prices ($ → € + new values) -------------------

bundle_price_fixes = [
    # (name, old $ price, new € price)
    ("Front End Engineer", "$49", "€49"),
    ("Security Engineer", "$39", "€39"),
    ("DevOps Engineer", "$29", "€39"),
    ("Back End Engineer", "$29", "€39"),
    ("Cloud / AWS Architect", "$24", "€29"),
    ("Data Engineer", "$24", "€24"),
    ("Interview Prep", "$14", "€29"),
    ("Mobile Developer", "$14", "€29"),
    ("Game Developer", "$10", "€29"),
]
for name, old_price, new_price in bundle_price_fixes:
    html = html.replace(
        f'<div class="bundle-name">{name}</div><div class="bundle-price">{old_price}</div>',
        f'<div class="bundle-name">{name}</div><div class="bundle-price">{new_price}</div>',
    )

# Individual Pack card — expand label, keep €7
html = html.replace(
    '<div class="bundle-name">Individual Pack</div><div class="bundle-price">$7 <small>each</small></div>',
    '<div class="bundle-name">Individual Pack · License</div><div class="bundle-price">€7</div>',
)

# --- §6 Bundle metadata — reflect extended pack counts + license language ---

meta_fixes = [
    ("23 packs / 460 cards / HTML + PDF", "23 packs · 460 cards · downloadable license + 12 mo updates"),
    ("15 packs / 300 cards / HTML + PDF", "15 packs · 300 cards · downloadable license + 12 mo updates"),
    ("12 packs / 240 cards / HTML + PDF", "12 packs · 240 cards · downloadable license + 12 mo updates"),
    ("8 packs / 160 cards / HTML + PDF", "8 packs · 160 cards · downloadable license + 12 mo updates"),
    ("6 packs / 120 cards / HTML + PDF", "6 packs · 120 cards · downloadable license + 12 mo updates"),
    # Thin bundles — Mobile / Interview originally 3 packs, Game 2 packs;
    # extended per decision 2026-04-21T06:45 to 6 / 6 / 5 respectively.
    # Until the extended packs ship, landing still reflects target counts.
    ("3 packs / 60 cards / HTML + PDF", "6 packs · 120 cards · downloadable license + 12 mo updates"),
    ("2 packs / 40 cards / HTML + PDF", "5 packs · 100 cards · downloadable license + 12 mo updates"),
    ("1 pack / 20 cards / HTML + PDF", "1 pack · 20 cards · downloadable license + 12 mo updates"),
]
for old, new in meta_fixes:
    html = html.replace(old, new)

# --- §7 License-language pass ---------------------------------------------

html = html.replace("One purchase, study forever", "One license, study forever")
html = html.replace(
    "No subscriptions. No recurring fees. Buy once, keep forever.",
    "License a pack you want to own (downloadable, works offline), or subscribe to explore the full catalog (streaming, non-downloadable).",
)
html = html.replace("30 TOPICS / BUY ONLY WHAT YOU NEED", "32 TOPICS / LICENSE ONLY WHAT YOU NEED")

# --- Write back + report ----------------------------------------------------

if html == original:
    print("index.html: no changes (already patched)")
    sys.exit(0)

SRC.write_text(html, encoding="utf-8")
delta = len(html) - len(original)
print(f"index.html: patches applied ({delta:+d} bytes delta)")
print()
print("Next:")
print("  git diff index.html           # review the changes")
print("  git add index.html")
print("  git commit -m 'apply drift + pricing patches per ledger 2026-04-21T06:45'")
print("  git push")
print()
print("Netlify auto-deploys within ~60s of push.")
