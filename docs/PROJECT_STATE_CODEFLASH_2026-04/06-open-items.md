# 6. What's still open

No committed `TODO` / `FIXME` / `HACK` / `XXX` markers were found in either repo via GitHub code search. No `.skip` / `.todo` tests (no test suite in either repo). The open work captured below comes from `GAPS.md`, session handoffs, open issues, PR descriptions, and verifiable drift I found while reading.

Severity key: 🔴 blocker (breaks what's claimed / shipped) · 🟠 drift or known debt · 🟡 parked work · 🟢 hygiene

| Repo | Area | Item | Location | Severity |
| --- | --- | --- | --- | --- |
| codeflash | Landing copy | Hero stats read `80 / 1,600 / 30` but OG meta + subhead + footer + pricing read `82 / 1,640 / 32` — same file, inconsistent | `index.html` (hero stats block vs `<meta property="og:…">` + footer) | 🔴 |
| codeflash | Landing meta | `og:url` = `https://blaquekaktus.github.io/flashcards-programming-app/` (URL of the other repo, possibly not live) | `index.html` head | 🔴 |
| codeflash | Landing assets | `assets/logos/codeflash_favicon_64.png` referenced but never generated → 404 on every page load | `index.html` `<link rel="icon" sizes="64x64">` | 🔴 |
| codeflash | Pack sync | Manual HTML copy from `flashcards-programming-app/public/packs/` — still blocked on mapping | `GAPS.md` §1 (also flashcards `GAPS.md` §2) | 🔴 |
| codeflash | Legal pages | Impressum + Datenschutz rendered with `{{token}}` placeholders still unfilled; owner task | `legal/impressum.html`, `legal/datenschutz.html` | 🔴 |
| codeflash | Footer | Impressum + Datenschutz links not wired into `index.html` footer | `index.html` `<footer>` | 🔴 |
| codeflash | Checkout | All "Store Opening Soon" placeholder buttons are inert — pricing section advertises 10 bundles but nothing clicks | `index.html` `#pricing` | 🟠 |
| codeflash | Design drift | README advertises `#00D4FF` + `#00FF88` accent colours; actual CSS uses `#5BF0A5` + `#3DD68C` | `README.md` §Design System vs `index.html` `:root` | 🟠 |
| codeflash | Pack path drift | `CLAUDE.md` references `flashcards-programming-app/packs/`; product repo moved to `public/packs/` in `871d4ce` | `CLAUDE.md` §Repo shape | 🟠 |
| codeflash | README claims | *"80+ interactive flashcard packs"* on the header and *"Can I try before buying? Three complete packs are free…"* — but only 3 HTML files exist in `packs/` | `README.md`, `index.html` FAQ | 🟠 |
| codeflash | Pre-commit hook | Hook script committed but install is per-clone; PR-time drift check not enforced by CI | `scripts/precommit-hook.sh` (no `.github/workflows/precommit-*`) | 🟢 |
| codeflash | CI drift check | `ai-brain/scripts/check-claudemd-drift.sh` referenced in PR #3 but no workflow runs it in this repo | `CLAUDE.md` + `.github/workflows/` | 🟢 |
| codeflash | Portfolio bridge | Blog / resources pages mentioned in `CLAUDE.md` as *"once they exist"* — CMS pipeline from `automatedcontentcreator` blocked upstream | `GAPS.md` §5 | 🟡 |
| codeflash | Open branches | `claude/claudemd-drift-propagation-lBvaw`, `claude/continue-claude-framework-S2wCF`, `claude/currency-token-cleanup-Ht1TN` and others still exist on origin post-merge | GitHub branches list | 🟢 |
| codeflash | Analytics | None installed; `CLAUDE.md` calls for GDPR-compliant analytics, deferred | implicit | 🟡 |
| codeflash | GitHub Pages deploy workflow | README claims GitHub Pages but no deploy workflow in `.github/workflows/`. Likely using repo Settings → Pages, not committed CI | `.github/workflows/` | 🟠 |
| flashcards-programming-app | Payment wiring | Lemon Squeezy store URL / variant IDs not set; no `VITE_PAYMENT_PROVIDER` in env → `isCheckoutEnabled()` returns false → Buy buttons hidden | `src/lib/payments.js`, `docs/SESSION_HANDOFF_2026-04-14_evening.md` | 🔴 |
| flashcards-programming-app | Content port | 51 Template A + 17 Template B packs without DB rows — Phase 1B not started | `GAPS.md` §2, `docs/SESSION_HANDOFF_2026-04-14_evening.md` | 🔴 |
| flashcards-programming-app | Only 8 packs seeded | DB seeds 31 pack rows but only `html-1, html-2, html-3, css-1, css-2, js-1, python-1, react-1` have real cards | `engine/pack_sources.json`, handoff doc | 🔴 |
| flashcards-programming-app | Stripe products | `packs.stripe_price_id` null for most packs; any Stripe Buy button will error | `docs/NEXT_SESSION.md` landmines | 🔴 |
| flashcards-programming-app | Secret exposure | Supabase URL + anon key committed in plain text | `docs/NEXT_SESSION.md` "State of the world" | 🟠 (anon keys are designed public, but convention-breaking) |
| flashcards-programming-app | Env var drift | `.env.example` has `VITE_STRIPE_PUBLISHABLE_KEY`; `README.md` lists `VITE_STRIPE_PUBLIC_KEY` | `.env.example` vs `README.md` §Deployment | 🟠 |
| flashcards-programming-app | Supabase kit | Extracted upstream in vistera but blocked on SSR/SPA architectural split | `GAPS.md` §4 | 🟡 |
| flashcards-programming-app | Stripe kit | Same SSR mismatch; also blocked on server-side Stripe surface | `GAPS.md` §5 | 🟡 |
| flashcards-programming-app | CI | No test / lint / build CI; only file-size guard | `.github/workflows/` | 🟠 |
| flashcards-programming-app | Drift checker | Not installed; waiting on `ai-brain#28` | `GAPS.md` §6 | 🟢 |
| flashcards-programming-app | Revenue emit | Helper shipped (`engine/revenue_emit.py`) but zero call sites | `GAPS.md` §8 | 🟡 |
| flashcards-programming-app | Playwright tests | Standalone scripts, not wired into CI | `scripts/verify_flip*.py`, commit `975d619` | 🟢 |
| flashcards-programming-app | Tests in general | Zero unit tests, zero integration tests. No `.skip` / `.todo`, no test framework configured | whole repo | 🟠 |
| flashcards-programming-app | Two landing surfaces | `src/pages/Landing.jsx` (18 KB React) + `docs/archive/legacy-landing.html` moved there in `158c44d`. Third exists in `codeflash/index.html` | repo | 🟠 |
| flashcards-programming-app | i18n keys | Bundle pages were hardcoded English before 2026-04-14 sweep; new bundle pages still risk regressing | `NEXT_SESSION.md` "Known gotchas" | 🟢 |
| flashcards-programming-app | `package-lock.json` | Committed, and `simple-icons` v13.21.0 added to lockfile manually | commit `c317549` | 🟢 |
| flashcards-programming-app | Committed binaries | `public/bundles/all_access_bundle.zip` 2.3 MB, `frontend_engineer_bundle.zip` 498 KB, etc. — under the 10 MB guard but still bloating git | `public/bundles/*.zip` | 🟠 |
| flashcards-programming-app | Branches | 11 unmerged `claude/*` and `fix/*` branches on origin post-merge | GitHub branches list | 🟢 |
| flashcards-programming-app | Roadmap page | `src/pages/Roadmap.jsx` exists (13 KB) but **no route wires it up** in `App.jsx` — dead page | `src/App.jsx` (routes), `src/pages/Roadmap.jsx` | 🟠 |
| flashcards-programming-app | Supabase Edge Functions | `create-checkout` + `stripe-webhook` exist but app switched payment abstraction to Lemon Squeezy (no matching edge fn) | `supabase/functions/` | 🟠 |
| flashcards-programming-app | Pre-commit hook | Same propagation story as codeflash — install is per-clone | `scripts/precommit-hook.sh` | 🟢 |
| both | CLAUDE.md drift across repos | Manual propagation via paired PRs; automated drift check still not in CI | each repo's `.github/workflows/` | 🟠 |

## Open GitHub issues

- codeflash #5 *"Layer 0 hook v2 — phase 2"* — **closed** (resolved by PR #8, 2026-04-15)
- flashcards-programming-app #11 *"Layer 0 hook v2 — phase 2"* — **closed** (resolved by PR #16, 2026-04-15)

No other open issues in either repo. All recent PRs are closed + merged.
