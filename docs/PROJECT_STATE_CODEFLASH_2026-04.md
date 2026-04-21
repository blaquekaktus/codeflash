# CodeFlash Project State — 2026-04

Cross-repo archaeology of `blaquekaktus/codeflash` (this repo) and `blaquekaktus/flashcards-programming-app`. Investigation date: 2026-04-21. Default branches: both `main`. Latest commits: `codeflash` `310269d` 2026-04-19, `flashcards-programming-app` `8a296fb` 2026-04-20.

The report is split across a folder of per-section files because a single document repeatedly hit stream timeouts. Read this index for the verdict and critical questions; drill into the sections for evidence.

## TL;DR verdict

**Consolidation recommendation: YES, with a narrow scope** — fold `codeflash` into `flashcards-programming-app` as a private monorepo, and publish only the built landing page (plus free-sample packs) to GitHub Pages from CI. See `07-consolidation.md`.

The stated reason for the split ("public frontend, hidden backend") is **not what the split actually delivers today**. The product repo (`flashcards-programming-app`) is itself a public repo containing the full storefront, Supabase schema, edge functions, and all pack content — nothing is hidden. The only thing the split buys is a separate public GitHub URL that can host a static marketing page; a single-repo setup with a built-artifact deploy achieves the same goal with far less drift.

## Three questions I'd need answered before moving

1. **Is `codeflash.at` live and pointing where?** `README.md` claims `https://codeflash.at` but `index.html`'s Open Graph URL still points at the old GitHub Pages URL for the product repo (`https://blaquekaktus.github.io/flashcards-programming-app/`). Which one is the real public surface today — and where is DNS actually pointed?
2. **Is the React app at `flashcards-programming-app` meant to be the public front door, or a private operator tool?** `Landing.jsx` exists and is deployed on Vercel; `docs/NEXT_SESSION.md` calls the other repo "legacy static marketing/content site (untouched)". If the Vercel app is the public front door, `codeflash/index.html` is redundant. If `codeflash/index.html` is the public front door, why does the React app serve its own landing?
3. **What was the original "hide the backend" concern — the source code, or the secrets?** If source code: the current split does not hide it (product repo is public). If secrets: `.env` + Vercel env vars already solve that and the split adds nothing. Naming the threat model makes the consolidation call trivial.

## Sections

1. [Identity of each repo](./PROJECT_STATE_CODEFLASH_2026-04/01-identity.md)
2. [Relationship between them](./PROJECT_STATE_CODEFLASH_2026-04/02-relationship.md)
3. [The split decision itself](./PROJECT_STATE_CODEFLASH_2026-04/03-split-decision.md)
4. [Structure (per repo)](./PROJECT_STATE_CODEFLASH_2026-04/04-structure.md)
5. [Decisions already made](./PROJECT_STATE_CODEFLASH_2026-04/05-decisions.md)
6. [What's still open (table)](./PROJECT_STATE_CODEFLASH_2026-04/06-open-items.md)
7. [Consolidation assessment](./PROJECT_STATE_CODEFLASH_2026-04/07-consolidation.md)

## Method & caveats

All paths in backticks are GitHub paths. Evidence is commit SHA, PR number, or file path — not inference. Aspirational README copy is flagged as such where the code doesn't back it up. "Unclear" means "not documented and not visible in code I read" — not "I skipped it."
