# CodeFlash — Developer Flashcards That Stick

> **82 interactive flashcard packs for developers and cybersecurity
> professionals. HTML + PDF. No app needed.**

CodeFlash is spaced-repetition learning that fits in a browser tab.
Every pack is a single self-contained HTML file: interactive quiz
mode, category filters, progress tracking, keyword search. No
install, no account, no telemetry — just open and study.

Made in Austria.

---

## Table of Contents

1. [Try a Free Sample](#try-a-free-sample)
2. [What Makes CodeFlash Different](#what-makes-codeflash-different)
3. [How Each Pack Works](#how-each-pack-works)
4. [Pack Catalog](#pack-catalog)
5. [Vertical Coverage](#vertical-coverage)
6. [This Repo vs. the Product Repo](#this-repo-vs-the-product-repo)
7. [Repo Structure](#repo-structure)
8. [Local Preview](#local-preview)
9. [Design System](#design-system)
10. [Accessibility & Performance](#accessibility--performance)
11. [Ecosystem Context](#ecosystem-context)
12. [Hard Rules](#hard-rules)
13. [Contributing](#contributing)

---

## Try a Free Sample

Download [HTML Foundations](packs/html/html_foundations_pack1.html) —
20 interactive flashcards covering tags, layout, semantic HTML, and
accessibility. Includes quiz mode, category filters, and progress
tracking. Works offline.

Two more free samples live in [`packs/`](packs/):
[Python Core Concepts](packs/python/python_core_concepts.html) and
[Web Security: OWASP Top 10](packs/security/web_security_owasp.html).

---

## What Makes CodeFlash Different

| Most flashcard apps           | CodeFlash                                  |
| ----------------------------- | ------------------------------------------ |
| Require an account            | No account, no login, no tracking          |
| Native iOS/Android app        | Any browser, any OS — even offline         |
| Community-generated cards     | Editorially curated, 20 cards per pack     |
| Ad-supported or freemium      | One-time purchase per pack                 |
| Feature-gated quiz mode       | Every pack ships with the full experience  |
| Generic topics                | Programming + security depth from day one  |

---

## How Each Pack Works

Every pack is a single HTML file with:

- **20 cards** across **5 categories** (4 cards per category)
- **Flip-to-reveal** with optional hint
- **Syntax-highlighted code** where relevant
- **Quiz mode** with scoring
- **Category filter pills**
- **Keyword search**
- **Progress tracking** via `localStorage` (never leaves your device)
- **Responsive layout** — phone, tablet, desktop
- **Dark-theme default**
- **Fully offline** once loaded

Open the file in any modern browser. That's it.

---

## Pack Catalog

The full catalog lives on the [public site](https://codeflash.lechner-studios.at)
and pack bundles are in [`bundles/`](bundles/). Categories include:

- **Web fundamentals** — HTML, CSS, JavaScript, accessibility
- **Backend** — Node.js, Python, databases, APIs
- **DevOps** — Docker, Kubernetes, Linux, shell scripting
- **Cybersecurity** — OWASP Top 10, nmap, Burp, network security, hashing
- **Version control** — Git workflows and recovery
- **Frameworks** — React, Vue, Next.js
- **Tools** — VS Code shortcuts, curl, jq, tmux

Free samples live under [`packs/`](packs/).

---

## Vertical Coverage

Programming and security are the **current** verticals. The
underlying engine is vertical-agnostic and designed to expand:

- Languages (German → English, Spanish, Japanese)
- Medical (USMLE-style recall, pharmacology)
- Legal (statute recall, case briefs)
- Finance (certifications, valuation concepts)

See the engine in the product repo:
[flashcards-programming-app / engine/gen_pack.py](https://github.com/blaquekaktus/flashcards-programming-app/blob/main/engine/gen_pack.py).

---

## This Repo vs. the Product Repo

This is the **public marketing / landing site** for CodeFlash. The
actual pack engine, storefront, and Supabase/Stripe backend live in
[flashcards-programming-app](https://github.com/blaquekaktus/flashcards-programming-app).

Every CTA on this site lands there.

| Repo                                                                                 | Role                                          |
| ------------------------------------------------------------------------------------ | --------------------------------------------- |
| **codeflash** (this repo)                                                            | Public marketing, landing page, free samples  |
| [flashcards-programming-app](https://github.com/blaquekaktus/flashcards-programming-app) | Product — engine, web app, storefront, auth   |

Pack HTML is **authored in the product repo** (at
`public/packs/**`) and copied into this repo's `packs/` as
marketing samples — never re-author pack content here.

---

## Repo Structure

```
codeflash/
├── index.html          # Landing page
├── packs/              # Free-sample pack HTML (copied from product repo)
│   ├── html/html_foundations_pack1.html
│   ├── python/python_core_concepts.html
│   └── security/web_security_owasp.html
├── bundles/            # Bundle preview HTML pages (authored here)
├── legal/              # Impressum + Datenschutz (AT, draft with noindex)
├── assets/             # Images, fonts, stylesheets
├── scripts/            # Layer 0 pre-commit hook
├── CLAUDE.md           # Agent instructions (Layer 0 + ecosystem + project rules)
├── GAPS.md             # Known gaps vs. canonical brief
└── .layer0-allow       # Paths exempt from UID/unit Layer 0 scan
```

No build step required — the site is static-deployable. Canonical
host: **Netlify**, served at `https://codeflash.lechner-studios.at`
(per ai-brain ADR-0008 + ecosystem hosting map, decided 2026-04-20).

---

## Local Preview

```bash
git clone https://github.com/blaquekaktus/codeflash.git
cd codeflash

# Any static server works. Examples:
python3 -m http.server 8080        # Python stdlib
npx serve .                        # Node
```

Open http://localhost:8080 in your browser.

Hot-reload is not required since there's no build step. Edit
`index.html` or a pack under `packs/` and refresh.

---

## Design System

Canonical tokens (as implemented in `index.html`):

| Token             | Value                       |
| ----------------- | --------------------------- |
| `--ink`           | `#1A1812`                   |
| `--cream`         | `#F6F1EB`                   |
| `--warm-white`    | `#FDFBF8`                   |
| `--stone`         | `#8B8578`                   |
| `--pillar-steel`  | `#B6C5D2` (accent)          |
| `--gold`          | `#C8A96E`                   |
| `--sand-dot`      | `#A19578`                   |
| `--blush`         | `#E8DDD3`                   |
| `--moss`          | `#3D4A3A`                   |
| Font Display      | Cormorant                   |
| Font UI           | Manrope                     |
| Font Code         | JetBrains Mono              |

The canonical spec lives in `ai-brain/design-system/` — this table
mirrors what ships in `index.html`. If the spec and the shipped CSS
ever disagree, update the spec first, then propagate per
`CLAUDE.md` §Design system.

Voice: insider / no-BS / evidence-first. Shared with
[The AI Shortcut](https://github.com/blaquekaktus/automatedcontentcreator).
Never use hype language like "game-changer", "revolutionary",
"mind-blowing".

---

## Accessibility & Performance

- **Accessibility baseline:** WCAG 2.1 AA
- **Performance baseline:** Lighthouse mobile score ≥ 90 for the
  landing page before any release
- Touch targets ≥ 44px
- Keyboard focus rings everywhere
- ARIA labels on interactive controls
- No pop-ups, no intrusive modals, no ads

---

## Ecosystem Context

CodeFlash is part of a multi-repo portfolio:

- **[flashcards-programming-app](https://github.com/blaquekaktus/flashcards-programming-app)** — Product engine + storefront (canonical pack content)
- **[automatedcontentcreator](https://github.com/blaquekaktus/automatedcontentcreator)** (The AI Shortcut) — Content pipeline. Programming/AI content refers CodeFlash.
- **[vistera](https://github.com/blaquekaktus/vistera)** — PropTech VR platform. CodeFlash teaches the tech behind it (4K, VR, spatial).
- **[websites](https://github.com/blaquekaktus/websites)** — KMU web-build service. Footer cross-link.
- **[ai-brain](https://github.com/blaquekaktus/ai-brain)** — Shared knowledge layer.

Cross-pollination is subtle and genuine. Footer links and contextual
references only — no pop-ups, no ads.

---

## Hard Rules

1. **No visitor/client PII in commits.** Names, emails, phones,
   addresses live only in `~/.claude-private/`.
2. **No secrets in commits.** Analytics / payment / mailing keys live
   in `.env` and are `.gitignore`d.
3. **Pack content is downstream of product.** Never edit pack HTML
   here — edit in `flashcards-programming-app` (`public/packs/**`)
   and re-publish.
4. **Accessibility is not optional.** WCAG 2.1 AA is the floor, not
   the target.
5. **No hype language.** Enforced in the shared brand voice.
6. **Messaging stays in sync with the product repo.** Pricing,
   feature claims, and pack counts must match
   [flashcards-programming-app](https://github.com/blaquekaktus/flashcards-programming-app).

---

## Contributing

This is a commercial project — external PRs aren't solicited today.
If you spot a rendering bug, typo, or accessibility issue, open an
issue with:

- URL or file path
- Browser + OS
- Screenshot or recording
- Expected vs. actual behaviour

For pack content bugs, open the issue in
[flashcards-programming-app](https://github.com/blaquekaktus/flashcards-programming-app) instead.

---

## License

Proprietary — all rights reserved. Landing page source may be
referenced for educational purposes; pack content and brand assets
may not be redistributed.
