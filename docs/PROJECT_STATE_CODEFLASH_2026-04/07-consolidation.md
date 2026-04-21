# 7. Consolidation assessment

## Is the split still justified?

**No — or more precisely, it has become cargo cult.** The recollected rationale ("public frontend, hidden backend") is not what the split delivers today:

- `flashcards-programming-app` is itself **public**. Source code, SQL, edge functions, design system — all visible.
- The Supabase anon key + project URL are already committed in `docs/NEXT_SESSION.md`. Anon keys are *designed* to be public and gated by RLS, so this isn't a leak — but it also means there's no "backend to hide." The genuinely sensitive things (Stripe secret key, Stripe webhook secret, service-role key) live in Vercel env vars, not in the repo, and would live there regardless of monorepo vs split.
- `codeflash` does not consume any API from the product — all numbers are hardcoded. Split gives zero runtime isolation.
- Both repos now serve landing pages (one static HTML, one React). The product repo's own handoff doc calls `codeflash` "legacy static marketing/content site (untouched)".

What the split actually buys today:

1. A separate GitHub URL for the marketing surface (cosmetic — any repo can be public).
2. A static-deploy-friendly root (no `dist/` step) — useful for GitHub Pages, but a one-line Pages workflow from a monorepo solves this.
3. A clean `CLAUDE.md` boundary (framework rules scoped per repo) — but the framework files drift anyway, and a monorepo can scope rules to subfolders.

What it costs is catalogued in section 3 (content drift, design-token drift, stat drift, broken OG URL, broken favicon ref, manual pack sync, paired propagation PRs, two landing pages, hardcoded pricing in `codeflash` that will diverge from DB pricing in product).

## Simpler alternatives that achieve the same "public frontend" goal

| Option | How | Pros | Cons |
| --- | --- | --- | --- |
| **A. Private monorepo + Pages deploy from a built artifact** | Keep `flashcards-programming-app` as-is; **flip it private**. Add a `packages/marketing/` (or `apps/marketing/`) with the landing source. A GitHub Actions job builds it and force-pushes `dist/` to a public `blaquekaktus/codeflash-public` repo as GitHub Pages source. | Real "public surface" separation. Truly hides the rest of the source. Single source of truth. | Requires flipping product repo private (breaks issues/PRs visibility). |
| **B. Vercel monorepo with two projects from one repo** | One repo, two Vercel Projects (`codeflash` static + `flashcards-programming-app` React). Vercel supports this natively via `rootDirectory`. | Zero CI plumbing. Matches current Vercel flow. Shared types / tokens trivial. | Repo stays public (same posture as today). Marketing stops being on GitHub Pages. |
| **C. Single-repo, same public posture, delete `codeflash`** | Let `src/pages/Landing.jsx` be the only landing surface. Point `codeflash.at` at Vercel. Archive this repo. | Smallest diff. Already halfway there (`Landing.jsx` exists, is 18 KB, serves same purpose). | Need a decent static preview for "Store Opening Soon" that works without auth. |
| **D. Status quo + automation** | Keep two repos. Add a pack-sync GitHub Action. Add a drift-checker Action. Extract counts to a single JSON source imported by both. | Least disruption. | Doesn't fix the conceptual confusion; still duplicates the landing; still costs propagation PRs. |

**Concrete recommendation: Option C** (delete `codeflash`; make `Landing.jsx` the public front door; keep product repo public), **or Option B** if keeping the static site feels non-negotiable.

Rationale: the React app's `Landing.jsx` is already 18 KB of actual landing content and it's already wired into a real deploy (Vercel). The static `codeflash/index.html` is 37 KB of duplicate copy that drifts — it answers exactly the three landing questions (what is it, why care, where start) that `Landing.jsx` also answers, for a product that only the React app can actually sell.

Option A is technically the cleanest "hidden backend" answer, but the premise (wanting the product hidden) doesn't match current reality, so it solves a problem you don't have.

## Effort estimates

- **Option C (recommended):** ~1–2 focused sessions. (1) Audit `codeflash/index.html` against `Landing.jsx` and port missing sections (pricing grid, FAQ, demo cards, legal footer, bundle catalog) into React. (2) Migrate `legal/impressum.html` + `legal/datenschutz.html` into React pages (Impressum already exists there). (3) Point DNS / repo-Pages URL at Vercel. (4) Archive `codeflash`. Net code delta is small because `Landing.jsx` + product repo already contain equivalents for most sections.
- **Option B:** ~1 session. Move `codeflash/*` under `apps/marketing/` in product repo. Add Vercel project. Remove duplicated content over time.
- **Option A:** ~2–3 sessions. Set up the public mirror repo, wire the Actions workflow, verify GitHub Pages + custom domain, flip product repo private, move all issues/PR history across (or accept the reset).
- **Status quo cost (Option D):** ongoing. Every content edit needs a paired PR. Drift keeps happening. Two `CLAUDE.md`s, two `GAPS.md`s, two `scripts/precommit-hook.sh` copies to maintain.

## Recommendation, with caveats

**YES, consolidate — specifically Option C.** Delete `codeflash` once `Landing.jsx` has parity. The split's stated justification doesn't hold; the product repo is already public; the React app is already serving a landing page; the Vercel deploy is already the canonical surface per the product repo's own handoff doc.

**Caveats:**

1. **Only if `codeflash.at` points at Vercel (or can).** If the domain has to live on GitHub Pages specifically (e.g. cost, SSL, EU hosting reason), Option B or the Option A variant where you publish `dist/` to a public mirror is the right call.
2. **Do not consolidate while Lemon Squeezy review is mid-flight.** Per `SESSION_HANDOFF_2026-04-14_evening.md`, the LS reviewer expects a working demo URL. Don't risk their approval by reshuffling deploy surfaces mid-review. Ship the demo first; consolidate after approval.
3. **The three questions in the index file must be answered first.** The right consolidation depends entirely on (a) where DNS is pointed, (b) which landing is "the" landing, and (c) what threat model the split was actually trying to address.
4. **Keep `engine/gen_pack.py` canonical.** Any consolidation must preserve the Python engine as the single source of pack HTML — that invariant is the one piece of the current architecture that is genuinely load-bearing.

## Final answer

**Consolidate: yes.** Risk is low, cost is a session or two, the upside is killing a whole class of drift (stat mismatch, pack sync, design tokens, propagation PRs, two landings, stale OG URLs). The only reason to keep the split is if a specific public/private threat model requires it — and today that threat model is not documented, not enforced, and not delivered.
