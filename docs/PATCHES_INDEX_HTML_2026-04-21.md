# Pending edits to `index.html` — 2026-04-21

These edits are drift fixes and pricing / positioning updates for
`codeflash/index.html`. Not applied in the investigation branch
because the file is large enough to hit stream-timeout limits on a
single MCP tool-call rewrite (per `ai-brain/patterns/mcp-commit-sizing.md`).
Apply locally or in a fresh session.

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

Canonical URL is `https://codeflash.lechner-studios.at/` per `ai-brain/open-items.md` §"Ecosystem Hosting Map" (decided 2026-04-20). `codeflash.at` in prior drafts is treated as stale.

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

## 5. Netlify Forms scaffolding (Path 2 follow-up)

When the Netlify migration lands:

- Wrap the hero `free-cta` block in `<form name="lead-capture" method="POST" data-netlify="true" netlify-honeypot="bot-field">` and swap the download CTAs for an email field + subscribe button.
- Add hidden `<input name="bot-field">` + `<input type="hidden" name="form-name" value="lead-capture">`.
- Double-opt-in language (TKG § 174 / DSGVO Art 6 Abs 1 lit a) required — link `legal/datenschutz.html` from the consent copy.
- Notification email → `hallo@lechner-studios.at`.
- Downstream: `ai-brain/compliance/sub-processors.md` needs a Netlify row (ADR-0008 downstream impact).

## 6. Pricing grid — bundle reshuffle + subscription replaces lifetime

Per decision-ledger entry `2026-04-21T06:45`.

### Replace the top All-Access block (two-column "1 Year / Lifetime")

Current:

```
All-Access — 1 Year · $99 /year · [Store Opening Soon]
All-Access — Lifetime (BEST VALUE) · $129 one-time · [Store Opening Soon]
```

New:

```
All-Access Subscription · €9 /month · stream the full catalog
All-Access Subscription (BEST VALUE) · €99 /year · €8.25 / month equivalent · 1 month free
```

Both cards carry copy: *"Access every pack across every topic and every vertical. Non-downloadable, streaming-only. Cancel anytime."*

### Replace the "Individual Pack" card

Current: *"Individual Pack · $7 each"*.

New layout — three tiers, not one:

```
Individual Pack · €7 · one pack, 20 cards · downloadable license + 12 months updates
Topic · €15 · 2–4 packs in one language or tool · downloadable license bundle + 12 months updates
Specialisation Bundle · €24–€49 (varies) · career-track · downloadable licenses + 12 months updates
```

### Revised specialisation-bundle prices (ordered)

Replace the `.bundle-grid` contents with the grid below. Bundle counts
reflect the extensions decided in the same ledger entry (Mobile goes
3 → 6 packs, Game Dev 2 → 5 packs, Interview Prep 3 → 6 packs — all
before launch via PackForge).

| Bundle | Packs | Price |
|---|---|---|
| Frontend Engineer | 23 | **€49** |
| Back End Engineer | 12 | **€39** |
| Security Engineer | 15 | **€39** |
| DevOps Engineer | 12 | **€39** |
| Cloud / AWS Architect | 8 | **€29** |
| Mobile Developer | 6 | **€29** |
| Game Developer | 5 | **€29** |
| Interview Prep | 6 | **€29** |
| Data Engineer | 6 | **€24** |

All currency symbols: `€`, not `$`. All numbers whole-euro (no `.99`).

## 7. License-language pass (EULA alignment)

Per `ai-brain/business-planning/lechner-studios/01-codeflash-eula-template.md`
implementation notes: keep *"License Fee / license to use / subscribe"*
everywhere; avoid *"purchase / buy / Kaufpreis / product"*.

Find-and-replace targets inside `index.html`:

| Find | Replace with |
|---|---|
| `Buy Once` / `Buy once` | `Own it` |
| `one-time purchase per pack` | `one-time license per pack` |
| `Buy only what you need` | `License only what you need` |
| `Get Started` (nav CTA) | `Get a license` |
| "What's your refund policy?" (FAQ) | Keep question; update answer to reference the § 11 FAGG/Widerrufsverzicht pattern once the three-checkbox flow ships |
| Button labels `Store Opening Soon` | Keep during pre-launch; swap to real CTAs (`Get license` / `Subscribe`) post-LS-approval |
| "Buy" anywhere | `License` or `Subscribe` (context-dependent) |
| Pricing copy tagline `One purchase, study forever` | `One license, study forever` |

Add a single line under the pricing heading clarifying the two paths:

> *License a pack you want to own (downloadable, works offline). Or
> subscribe to explore the full catalog (streaming, non-downloadable).*

This is the copy most likely to affect Lemon Squeezy reviewer
perception of the product category (license + service = software-service
vs purchase = Handel). Worth getting right before sending the
onboarding reply.

## 8. Remove the Game Dev €10 / Interview Prep €14 / Mobile €14 thin-bundle copy

These prices in the current landing copy don't match the new ladder.
Covered by the replacement grid in §6; listed here as a targeted
find-and-delete so nothing stale slips through:

- Delete: *"Interview Prep · $14 · 3 packs / 60 cards"*
- Delete: *"Mobile Developer · $14 · 3 packs / 60 cards"*
- Delete: *"Game Developer · $10 · 2 packs / 40 cards"*

(All replaced by the new €29 / 5–6 pack versions in §6.)
