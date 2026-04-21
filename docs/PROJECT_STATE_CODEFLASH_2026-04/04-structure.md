# 4. Structure (per repo)

## `codeflash`

**High-level architecture.** Single-page static site. One HTML file, inline CSS, minimal inline JS. Plus a handful of static HTML bundle previews and legal pages. No build step.

**Top-level folders**

| Path | Purpose |
| --- | --- |
| `index.html` | Landing page (37 KB, everything inline — hero, stats, personas, topics, pricing, FAQ, footer) |
| `packs/html/`, `packs/python/`, `packs/security/` | Free-sample pack HTML (3 files), manually copied from `flashcards-programming-app/public/packs/` |
| `bundles/` | Nine static bundle preview pages (`backend.html`, `cloud.html`, `data.html`, `devops.html`, `frontend.html`, `gamedev.html`, `interview.html`, `mobile.html`, `security.html`) |
| `legal/` | `impressum.html` + `datenschutz.html` — AT legal scaffolds rendered from ai-brain templates, still contain `{{token}}` placeholders |
| `assets/banners/`, `assets/logos/` | Static image assets |
| `scripts/` | `precommit-hook.sh` (Layer 0 identity/currency/phone-number regex scanner) |
| `.github/workflows/file-size-guard.yml` | Blocks PRs with files >10 MB |
| `CLAUDE.md`, `GAPS.md`, `README.md` | Framework + governance docs |

**Key modules.** There is only one: `index.html`. Everything the landing page does — nav, hero, stats, persona cards, topic accordion (collapsible), demo cards (click-to-flip), pricing, FAQ — is in that single file.

**External services / APIs.** Exactly one runtime external call: Google Fonts (Inter + JetBrains Mono). No analytics. No API. No tracking.

**Data model.** None. Pack counts, card counts, bundle names, prices are hardcoded strings inside `index.html`.

## `flashcards-programming-app`

**High-level architecture.** Vite+React SPA storefront on top of Supabase (Postgres with RLS + Auth) and Stripe/Lemon Squeezy for payments. Python 3 stdlib engine builds pack HTML files independently of the web app. Two Supabase Edge Functions handle checkout + webhook.

**Top-level folders**

| Path | Purpose |
| --- | --- |
| `src/main.jsx`, `src/App.jsx` | Entry + routing. Routes: `/`, `/auth`, `/packs`, `/leaderboard`, `/impressum`, `/bundles`, `/bundles/:bundleSlug`, `/bundles/:bundleSlug/:topicSlug`, `/study`, `/study/:packId`, `/dashboard`, `/checkout`, `/success`, `*` |
| `src/pages/` | 14 page components including `Landing.jsx` (18 KB — its own marketing page), `Study.jsx` (20 KB — card study UI), `Roadmap.jsx` (13 KB), plus `Auth`, `Bundles`, `BundleDetail`, `TopicDetail`, `Dashboard`, `Leaderboard`, `Packs`, `Checkout`, `Success`, `Impressum`, `NotFound` |
| `src/components/` | `Breadcrumb`, `ReviewSection`, `SkipToContent`, `StarRating`, `TechLogo` |
| `src/lib/supabase.js` | 13 KB domain API: auth, profiles, packs, cards, progress, streaks, leaderboard, purchases, pack-reviews, bundles, topics |
| `src/lib/payments.js` | Provider abstraction — Stripe (default), Gumroad, Lemon Squeezy via `VITE_PAYMENT_PROVIDER` |
| `src/lib/stripe.js` | Stripe checkout redirect client |
| `src/lib/i18n.jsx` | i18n provider (EN / DE) |
| `src/locales/` | `en.json`, `de.json` |
| `engine/gen_pack.py` | Canonical pack generator (14 KB, Python stdlib only) |
| `engine/build_all.py`, `engine/build_bundles.sh` | Batch + bundle builders |
| `engine/extract_pack.py` | Pulls cards from HTML packs into SQL seed rows (Template A / Template B) |
| `engine/audit_packs.py` | Read-only audit (classifies template, card count, tags) |
| `engine/migrate_design.py` | Bulk-migrates existing pack HTML to new design tokens |
| `engine/revenue_emit.py` | Writes revenue events to `~/.claude-private/events/` (ADR-0004); no call sites yet |
| `engine/pack_sources.json` | Maps DB pack IDs (`html-1`, `js-1`, `react-1`…) to source HTML files |
| `agents/pack_forge.py`, `agents/pack_forge_hermes.py` | PackForge v0 pipeline + Hermes LLM adapter (PR #20) |
| `public/packs/**` | ~80 pack HTML files across 29 topic subdirs (aws, bootstrap, cicd, css, docker, git, go, godot, html, interview, java, javascript, k8s, kotlin, misc, nextjs, nodejs, php, python, react, react-native, rust, security, sql, swift, sysadmin, tailwind, testing, typescript, unity, vscode) |
| `public/bundles/` | Ten pre-built ZIP bundles (sizes 28 KB – 2.3 MB; `all_access_bundle.zip` is 2.3 MB — committed binaries) |
| `catalog/` | Three standalone marketing HTML catalogs (product catalog + shop listings) |
| `db/schema.sql` | 18 KB SQL: extensions, tables, RLS, seed inserts for 31 packs |
| `db/migrations/` | Migrations folder (unexplored in this audit) |
| `supabase/functions/create-checkout/index.ts` | Edge function — creates Stripe session |
| `supabase/functions/stripe-webhook/` | Edge function — records purchases on Stripe webhook |
| `docs/` | Session handoffs (`NEXT_SESSION.md`, `SESSION_HANDOFF_2026-04-13_deploy.md`, two 2026-04-14 handoffs), bundle-builder prompt, legacy audit report, archive |
| `scripts/verify_flip.py`, `verify_flip_aws.py` | Playwright smoke tests (not in CI — see commit `975d619`) |
| `vite.config.js` | Vite config (default + react plugin) |
| `vercel.json` | SPA rewrite for client-side routing |

**Key modules & what they do** — the two heavy ones are `src/pages/Study.jsx` (20 KB card-study UI with flip, quiz, progress) and `src/lib/supabase.js` (the entire domain API). `engine/gen_pack.py` is the canonical HTML pack generator; `CLAUDE.md` rule #1 says *"Engine is canonical. Never recreate `engine/gen_pack.py`."*

**External services / APIs.** Supabase (DB + Auth + Edge Functions), Stripe (primary client-side SDK, server-side Edge Function), optionally Gumroad / Lemon Squeezy via env switch, Vercel (hosting), Google + GitHub OAuth (via Supabase), Google Fonts.

**Data model (Postgres).** Tables: `profiles`, `packs` (`id text pk`, `lang`, `level`, `color`, `icon`, `is_free`, `price_cents`, `stripe_price_id`, `topic_slug`), `cards` (`pack_id fk`, `category`, `question`, `hint`, `answer`, `code`, `card_order`), `progress` (`unique(user_id, card_id)`), `quiz_results`, `streaks`, `purchases`, `pack_reviews` (`unique(user_id, pack_id)`, rating 1–5), `bundles`, `topics`, `bundle_topics`, `bundle_purchases`. Plus a `leaderboard_view` computed from `progress` + `streaks` + `profiles`. RLS enabled on all user-owned tables; `packs` / `cards` are publicly readable. Seed inserts 31 pack rows; only 8 have real `cards` per the 2026-04-14 evening handoff.
