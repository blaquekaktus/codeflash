# 3. The split decision itself

## Timeline

- **2026-04-10** (day -1): `flashcards-programming-app` already exists; PR #1 "Organize repo into standard project structure" moves 82 root-level files into `src/`, `db/`, `content/`, splits `pages.jsx` god-file into page components.
- **2026-04-11** (split day): `codeflash` is created. First commit `07b6a64` "Add initial project files and asset packs". Followed same day by `3be9ff9` (bundle landing pages), `32791a` "Flatten site structure and remove duplicated codeflash files" — indicating the initial dump included a nested `codeflash/` subdir of duplicated files that had to be deleted.
- **2026-04-12**: PR #1 on codeflash *"Apply Universal CLAUDE.md Framework to codeflash"* introduces the official framing: *"public frontend / marketing landing site for the CodeFlash spaced-repetition product, whose engine lives in flashcards-programming-app."*
- **2026-04-13**: `flashcards-programming-app` gets its Vite + React scaffold (`73997f9` feat(build): add Vite + React scaffold). The product repo now has its own landing page (`Landing.jsx`). The old static marketing HTML gets moved to `public/legacy-landing.html` (later to `docs/archive/`).
- **2026-04-14**: `docs/NEXT_SESSION.md` in the product repo labels this repo *"legacy static marketing/content site (untouched, don't modify unless asked)"* and lists *"Repo merge (codeflash static site → flashcards-programming-app)"* among deferred items.

## Stated reason (documented)

- `codeflash/CLAUDE.md`: *"Public marketing/landing site for the CodeFlash product. Funnels discovery → product signup. Hosting: GitHub Pages or equivalent."*
- `codeflash/README.md`: explicit *"This Repo vs. the Product Repo"* section: *"This is the **public marketing / landing site** for CodeFlash. The actual pack engine, storefront, and Supabase/Stripe backend live in `flashcards-programming-app`."*

The user's recollection — *"so the frontend could be public (GitHub Pages) without exposing the backend"* — does **not** appear verbatim in any committed doc. The closest is the "funnel discovery → product signup" framing, which is a different claim (traffic-routing, not access control).

## What was considered / rejected

**Nothing documented.** No ADR, no `docs/decisions/`, no PR description with a pro/con table, no `CLAUDE.md` note on why a monorepo was rejected. The framework files (`CLAUDE.md`, `GAPS.md`) describe the *current* split as a given. The rename PR #12 ("remove codeflash collision") is the closest thing to a decision trace — it reveals that `package.json.name = "codeflash"` was originally the same string on both sides, which created tooling collisions until one was renamed. That's architectural debt from the split, not a rationale for it.

## What the split has cost

Verifiable from commits and docs:

1. **Manual pack sync** (`GAPS.md` #1 here, #2 there). Open, blocked on path mapping. As of today, `codeflash/packs/` has 3 files; `flashcards-programming-app/public/packs/` has ~80. The two will diverge on every pack edit that doesn't trigger a manual copy.
2. **Marketing-copy drift** in `codeflash/index.html` itself — hero reads "80 / 1,600 / 30" while subhead + OG + footer read "82 / 1,640 / 32". This drifts from the product repo's reality (8 fully-seeded packs per the 2026-04-14 evening handoff).
3. **Stale OG URL**: `index.html` still advertises `https://blaquekaktus.github.io/flashcards-programming-app/` as `og:url` — a URL that belongs to the *other* repo and may not even be live.
4. **Broken favicon reference**: `<link rel="icon" ... href="assets/logos/codeflash_favicon_64.png">` — product repo PR #23 fixed the same dead ref there; codeflash still has it.
5. **Duplicate CLAUDE.md propagation pain**: PRs #3, portfolio-hygiene PR #6, hook-v2 PR #8, legal-scaffold PR #9 all have paired sibling PRs in the product repo. Propagation is currently human-driven. `ai-brain/scripts/check-claudemd-drift.sh` is referenced but not wired into CI here (the workflow file doesn't exist in `.github/workflows/`).
6. **Design-token drift** (colours + fonts between README and actual CSS — see section 2).
7. **Name collision** (npm / package.json) — cost one rename PR (#12 in product repo).
8. **Two landing pages**: `codeflash/index.html` (static, hand-written) and `flashcards-programming-app/src/pages/Landing.jsx` (React, 18 KB). Both answer *"what is CodeFlash"*. The product-repo handoff treats codeflash as legacy, yet the codeflash repo is still receiving content commits.
9. **No shared build/CI for accessibility / Lighthouse / link-checking.** `CLAUDE.md` in codeflash says Lighthouse mobile ≥ 90 before release; nothing automates it.
10. **Extra secret/config surface**: `flashcards-programming-app` has `.env` + Vercel env vars. `codeflash` has no secrets today but would grow them the moment an analytics key, Stripe publishable key, or Plausible token is added. Already parked: NEXT_SESSION lists *"email capture on landing"* and *"analytics install"*.
