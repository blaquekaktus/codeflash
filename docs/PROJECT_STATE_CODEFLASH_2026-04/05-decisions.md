# 5. Decisions already made

No formal ADR directory exists in either repo. Decisions live in `CLAUDE.md`, `README.md`, `GAPS.md`, PR descriptions, and commit messages. The items below are the ones that are **committed in writing** — not inferred.

## `codeflash`

| Decision | Chosen | Rejected / alternative | Why (as documented) | Source |
| --- | --- | --- | --- | --- |
| Static site, no build step | Pure HTML/CSS/JS | Any bundler / SSG / React | *"Keep the repo static-deployable (no build step required) until a real reason to add one appears."* | `CLAUDE.md` §Repo shape |
| Pack content ownership | Authored in `flashcards-programming-app`, published here as samples | Authoring locally | *"Pack content is downstream of product. Never edit pack HTML here — edit in `flashcards-programming-app` and re-publish."* | `CLAUDE.md` §Hard rules #3 |
| Body font: Inter (not Outfit) | Inter | Outfit | *"Outfit reads as a learning-app/student typeface. Inter is the neutral sans of serious developer products (Stripe, Linear, Vercel) and signals the site's actual audience — working engineers brushing up, not newcomers."* | Commit `6358106` / PR #11 |
| Code font kept | JetBrains Mono | — | *"JetBrains Mono kept for code and numeric accents."* | Same PR |
| Design tokens are ecosystem-wide, not per-repo | `ai-brain/design-system/` | Per-repo tokens | *"single source of truth… never branch the tokens in this repo."* | `CLAUDE.md` §Design system |
| Accessibility baseline | WCAG 2.1 AA | Lower / AAA | *"WCAG 2.1 AA is the floor, not the target."* | `CLAUDE.md` §Hard rules #4 |
| Performance baseline | Lighthouse mobile ≥ 90 | — | *"before any release"* | `CLAUDE.md` §Build + deploy |
| AT legal pages (Impressum + Datenschutz) | Rendered as drafts with `noindex` + visible `{{token}}` placeholders | Leaving ai-brain template unrendered | *"match the CodeFlash landing page theme… placeholders visibly flagged so they can't be missed on pre-launch review."* | PR #9 / commit `6306ba2` |
| Currency check in hook | `[€£¥]\|\$[0-9]` (only fires on `$` immediately followed by digit) | Bare `[€$£¥]` | *"Prevents false positives on JS template literals and shell variable syntax."* | Commit `310269d` |
| Anti-scope | No build step, no AI/LLM deps | Adding either | *"Adding a build step — repo is intentionally static-deployable"* + *"AI/LLM dependencies — explicitly scoped out by CLAUDE.md"* | `GAPS.md` §Anti-scope |

## `flashcards-programming-app`

| Decision | Chosen | Rejected / alternative | Why (as documented) | Source |
| --- | --- | --- | --- | --- |
| Framework | Vite + React 18 SPA | Next.js | *"Migrate flashcards to Next.js. Out of scope — would be a rewrite of the storefront."* | `GAPS.md` §4 path 2 |
| Auth | Supabase Auth (email + GitHub + Google OAuth) | Building own auth | Implicit — all three enabled in PR #20's successor work | `docs/SESSION_HANDOFF_2026-04-13_deploy.md` |
| Payment provider abstraction | `src/lib/payments.js` with `VITE_PAYMENT_PROVIDER` switch | Hardcoded Stripe only | *"Supports: Stripe (default), Gumroad, LemonSqueezy"* | `src/lib/payments.js` header |
| Active payment provider today | Lemon Squeezy (planned) | Stripe (initial), Gumroad | *"Sonja has a pending Lemon Squeezy onboarding email"* — post-LS approval: `VITE_PAYMENT_PROVIDER=lemonsqueezy` | `docs/NEXT_SESSION.md`, `docs/SESSION_HANDOFF_2026-04-14_evening.md` |
| Pack engine | Python 3 stdlib only | Any Python deps | *"Never recreate `engine/gen_pack.py`. Import from it."* | `CLAUDE.md` §Hard rules #1 |
| Pack format invariant | Exactly 20 cards / 5 categories / 4 per category | Variable | *"No exceptions — validation fails otherwise."* | `CLAUDE.md` §Hard rules #2 |
| Supabase kit (shared across portfolio) | **Not adopted here.** Vendoring blocked on kit architectural split. | Next.js-shaped `@blaquekaktus/supabase-kit` | *"The kit is Next.js-specific… This repo is Vite + React SPA… The two surfaces share no compatible API."* | `GAPS.md` §4 (corrected in PR #17) |
| Stripe kit (shared across portfolio) | **Not adopted.** Same SSR/SPA mismatch + no server runtime yet. | `@blaquekaktus/stripe-kit` | Same architectural mismatch | `GAPS.md` §5 |
| Pack directory location | `public/packs/**` (Vite convention, served as static assets) | Root-level `packs/` | Moved via commit `871d4ce` | Commit + PR #19 fixed `build_bundles.sh` accordingly |
| Repo rename | `package.json.name = "flashcards-programming-app"` | `"codeflash"` | *"the sibling repo `blaquekaktus/codeflash` is the CodeFlash marketing site… creates a collision any time tooling references 'codeflash' by name"* | PR #12 |
| Forest-green palette + DM Sans | Unified palette across all packs | Per-vertical palette colours | *"codeflash.app is one product; it should have one palette."* | PR #22 / commit `326dc2e` |
| Content port strategy | Phase 1A (seed 8 packs) → Phase 1B (51 Template A + 17 Template B without DB rows) | All-at-once dump | Incremental + audit-first via `engine/audit_packs.py` | `docs/SESSION_HANDOFF_2026-04-14_evening.md` |
| Revenue event schema | `~/.claude-private/events/flashcards-programming-app.ndjson` via `emit_revenue_event()` | Centralised event bus | Follows ADR-0004 in ai-brain | PR #14 |
| CI | File-size guard only; **no test / lint / build CI** | Full CI | *"No test CI, no lint CI, no build check. Still pre-Phase-1 compared to vistera."* | `GAPS.md` §7 |
| Legal page | AT Impressum only so far (in-app, not scaffolded like codeflash) | Full AT stack | *"AGB… DSGVO/Datenschutz… deferred"* | Commit `4d0041c` |
