# 2. Relationship between the two repos

## Direction of dependency

**`codeflash` depends on `flashcards-programming-app`, by manual copy.** No npm package link, no git submodule, no CI sync. Pack HTML is authored in `flashcards-programming-app/public/packs/` (~80 files) and hand-copied into `codeflash/packs/` (only 3 files currently: `html/html_foundations_pack1.html`, `python/python_core_concepts.html`, `security/web_security_owasp.html`).

Evidence: commit `a9c728c` (2026-04-17) "Copy python_core_concepts.html and web_security_owasp.html from flashcards-programming-app/public/packs/ into codeflash/packs/ (per CLAUDE.md convention)". Note the commit predates the product repo's move to `public/packs/` in some of the script references — `CLAUDE.md` in this repo still says *"pack HTML is produced by the `flashcards-programming-app` generator"* and points at the old `flashcards-programming-app/packs/` path (pre-`871d4ce`).

**No runtime dependency.** `codeflash/index.html` makes zero network calls to the product (verified — no `fetch`, no cross-origin `<script>`, no API URL references). Users click "Store Opening Soon" placeholders; pricing buttons are inert.

## API contracts — shared or duplicated?

**Neither — they don't share API contracts because there's no runtime cross-call.**

- `codeflash` has no API client. Bundle prices and pack counts are **hardcoded** into `index.html` (e.g. *"Security Engineer $39 / 15 packs / 300 cards"*).
- `flashcards-programming-app` has a Supabase schema (`db/schema.sql`) used only internally by `src/lib/supabase.js`. Tables: `profiles`, `packs`, `cards`, `progress`, `quiz_results`, `streaks`, `purchases`, `pack_reviews`, `bundles`, `topics`, `bundle_topics`, `bundle_purchases`, plus a `leaderboard_view`. Card-id columns use `text` primary keys (`'html-1'`, `'ts-1'`). None of these IDs are referenced in `codeflash`.

**Drift is guaranteed** because the numbers are duplicated and denormalized. Concrete drift right now:

- `codeflash/index.html` hero: *"80 packs / 1,600 cards / 30 topics"*.
- `codeflash/index.html` OG meta + subhead + footer: *"82 packs / 1,640 cards / 32 topics"*. **Same file, inconsistent claims.**
- `README.md` says *"80+ interactive flashcard packs"*.
- Reality in product repo: `db/schema.sql` seeds **31** `packs` rows; `public/packs/**` has ~80 HTML files; only **8** packs have real cards in Supabase per `docs/SESSION_HANDOFF_2026-04-14_evening.md`.

## Shared config, tokens, env vars

- **Design tokens: duplicated & drifted.** `codeflash/README.md` lists `--accent` as electric blue `#00D4FF` and electric green `#00FF88`. Actual `codeflash/index.html` uses forest green `#5BF0A5` + `#3DD68C`. Product repo moved to forest green + DM Sans in commit `ec1489a` (2026-04-19). Neither repo pulls from `ai-brain/design-system/` at runtime; `CLAUDE.md` claims that's the single source of truth, but no tooling enforces it.
- **Framework-level CLAUDE.md: near-identical Layer 0 + Ecosystem preamble.** Divergent below the divider (each repo has its own engineering rules). Propagation is manual — commit `12f81f7` (2026-04-19) had to sync "no-sign-off" and PR-discipline rules across repos.
- **Shared hook + allow-list.** `scripts/precommit-hook.sh` is identical in both repos (SHA `d6e0eb9`), so is `.github/workflows/file-size-guard.yml` (SHA `3047914d`), so is `.github/pull_request_template.md` (SHA `955cd467`). Copied via portfolio-hygiene PRs (`#6` here, `#13` there).
- **Env vars.** No env-var overlap today. `codeflash` has no `.env`. `flashcards-programming-app/.env.example` has `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_STRIPE_PUBLISHABLE_KEY`. README there says `VITE_STRIPE_PUBLIC_KEY` — **drift between `.env.example` and `README.md`**.
- **Secret exposure.** `flashcards-programming-app/docs/NEXT_SESSION.md` commits the Supabase project URL and anon key. Anon keys are designed to be public + RLS-gated, so this isn't a vulnerability, but it does mean the "hidden backend" narrative doesn't hold.

## CORS / auth / proxy setup between them

**None.** There is no CORS setup because there is no cross-origin traffic today. The React app at Vercel talks to Supabase directly from the browser (Supabase handles CORS on its side). `codeflash` has no auth at all; the React app uses Supabase Auth with GitHub + Google OAuth configured through Supabase's dashboard (per `docs/SESSION_HANDOFF_2026-04-13_deploy.md`).

The implicit plan is that visitors land on `codeflash` (marketing), click "Browse Packs", and get redirected to the Vercel URL (product) — but **the redirect target is not wired up today**. `codeflash/index.html` "Store Opening Soon" placeholders don't point anywhere. When wired, this will be cross-origin: `codeflash.at` → `*.vercel.app`. No shared domain, no session transfer mechanism planned in code.
