# Pending edits to `index.html` — 2026-04-21

These edits are drift fixes per `docs/PROJECT_STATE_CODEFLASH_2026-04/06-open-items.md`.
Not applied in the investigation branch because the file is large enough to hit stream-timeout limits on a single tool-call rewrite. Apply locally or in a fresh session.

## 1. Stats reconciliation (82 / 1,640 / 32 everywhere)

- Line: `<meta name="description" content="80 interactive flashcard packs with real code examples. Open in your browser, study offline, print for your desk. No app needed.">`
  → replace `80 interactive` with `82 interactive`.
- Line in hero: `<p class="sub">80 interactive flashcard packs with real code examples. …`
  → replace `80 interactive` with `82 interactive`.
- Hero stats block:
  - `<div class="stat-val">80</div><div class="stat-label">Packs</div>` → `82`
  - `<div class="stat-val">1,600</div><div class="stat-label">Cards</div>` → `1,640`
  - `<div class="stat-val">30</div><div class="stat-label">Topics</div>` → `32`
- Persona card "Security professionals":
  - Paragraph starts `14 packs covering OWASP, pentesting, …` → `15 packs covering …`
  - Highlight pill `14 PACKS / 280 CARDS` → `15 PACKS / 300 CARDS`

All other `82 / 1,640 / 32` references (OG description, Twitter description, footer, All-Access bundle card, FAQ code-examples line) are already correct.

## 2. Fix stale Open-Graph / Twitter URLs

Replace every occurrence of `https://blaquekaktus.github.io/flashcards-programming-app/` with `https://codeflash.lechner-studios.at/` in these three lines:

- `<meta property="og:image" content="…assets/banners/codeflash_banner_1600x300.png">`
- `<meta property="og:url" content="…">`
- `<meta name="twitter:image" content="…assets/banners/codeflash_banner_1600x300.png">`

Canonical URL is `https://codeflash.lechner-studios.at/` per `ai-brain/open-items.md` §"Ecosystem Hosting Map" (decided 2026-04-20). `codeflash.at` in the README is treated as stale; will be corrected in a separate commit.

## 3. Footer — add legal links, correct brand domain

Current footer:

```html
<footer>CodeFlash — Developer Flashcards That Stick<br>
<span style="margin-top:.5rem;display:inline-block;">Made in Austria. 82 packs. 1,640 cards. Zero tracking.</span><br>
<span style="margin-top:.75rem;display:inline-block;font-size:.7rem;color:var(--dim);">Built by <a href="https://lechnerstudios.at" target="_blank" rel="noopener" style="color:var(--muted);text-decoration:none;border-bottom:1px solid var(--border);">Websites by Lechner Studios</a></span></footer>
```

Changes:

- `https://lechnerstudios.at` → `https://lechner-studios.at` (actual registered domain per ai-brain).
- Insert, before the "Built by" line, a legal-links span:

```html
<br><span style="margin-top:.5rem;display:inline-block;font-size:.75rem;">
<a href="legal/impressum.html" style="color:var(--muted);text-decoration:none;border-bottom:1px solid var(--border);">Impressum</a>
 · <a href="legal/datenschutz.html" style="color:var(--muted);text-decoration:none;border-bottom:1px solid var(--border);">Datenschutz</a>
</span>
```

Closes `codeflash/GAPS.md` item #6 follow-up.

## 4. Favicon — no change needed

Report §6 row *"favicon 64px never generated"* was a false positive. `assets/logos/codeflash_favicon_64.png` exists (3,870 bytes). The corresponding drift only exists in the product repo and was fixed by its own PR #23. Leave `codeflash/index.html` as-is.

## 5. Netlify Forms scaffolding (Path 2 follow-up — NOT in this patch set)

When the Netlify migration lands:

- Wrap the hero `free-cta` block in `<form name="lead-capture" method="POST" data-netlify="true" netlify-honeypot="bot-field">` and swap the download CTAs for an email field + subscribe button.
- Add hidden `<input name="bot-field">` + `<input type="hidden" name="form-name" value="lead-capture">`.
- Double-opt-in language (TKG § 174 / DSGVO Art 6 Abs 1 lit a) required — link `legal/datenschutz.html` from the consent copy.
- Netlify Site Settings → Forms → notification webhook → `hallo@lechner-studios.at` (Zoho Mail box already live per ai-brain 2026-04-19 closed item).
- Downstream: `ai-brain/compliance/sub-processors.md` needs a Netlify row (ADR-0008 downstream impact, already flagged).
