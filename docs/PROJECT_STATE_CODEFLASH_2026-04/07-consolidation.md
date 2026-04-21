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

---

## Addendum — 2026-04-21: ai-brain cross-references + revised recommendation

After reading ai-brain, the above original recommendation (Option C) is **overridden** by owner decision and ecosystem context. The live decision is **Path 2 — keep the split, wire Netlify Forms for lead capture, eliminate drift**. The reasoning is documented below with pointers into ai-brain so the trail doesn't go cold.

### Why Path 2 wins, not Option C

- **ADR-0008 already decided hosting by shape.** `ai-brain/decisions/0008-hosting-split-netlify-vercel.md` (proposed 2026-04-18): *"Static sites (no build step, no framework) host on Netlify. Framework apps host on Vercel. Test for which pile a project belongs in: does it have a build step?"* `codeflash` has no build step → Netlify. Option C would demote this rule for this one surface.
- **Netlify Forms is a free, built-in lead-capture channel** — the first-class reason ADR-0008 chose Netlify for static sites in the first place. Losing that by folding `codeflash` into the Vercel SPA leaves a real lead-capture pipeline on the floor.
- **Ecosystem hosting map already commits to `codeflash.lechner-studios.at`.** `ai-brain/open-items.md` §"Ecosystem Hosting Map" (decided 2026-04-20) lists `codeflash.lechner-studios.at` as a pending subdomain of the Lechner Studios umbrella. DNS work is trivially cheap; the decision is made.
- **Pack engine invariant holds either way.** `engine/gen_pack.py` remains canonical in `flashcards-programming-app`. Path 2 preserves this unchanged.

### Cross-references into ai-brain

| ai-brain file | Why it matters here |
| --- | --- |
| `backlog/codeflash-flashcards.md` P1 "Split-repo audit" | The open item this investigation was the evidence base for. Path 2 = owner-preferred "(b) keep split but document clear ownership boundary." |
| `backlog/codeflash-flashcards.md` P1 "FAGG § 18 Abs 1 Z 11 three-checkbox flow" | Pre-sale compliance blocker; applies to `flashcards-programming-app` checkout. Not resolved by consolidation either way. |
| `backlog/codeflash-flashcards.md` P1 "Button-Lösung § 312j BGB" | Same as above — pre-sale blocker, label requirement. |
| `backlog/codeflash-flashcards.md` P1 "Impressum + AGB + DSE (pre-sale)" | Blocked on controller-identity P0. |
| `backlog/codeflash-flashcards.md` P1 "Consumer pre-contract info (§ 4 FAGG / Art 246a EGBGB)" | Before pay-button placement. |
| `backlog/INDEX.md` 🔴 P0 "Controller-identity final decision" | Upstream blocker for six P1s across the portfolio, including everything under codeflash/flashcards pre-sale compliance. Consolidation does NOT unblock this. |
| `decisions/0008-hosting-split-netlify-vercel.md` | Codifies static → Netlify / framework → Vercel. Path 2 aligns. |
| `decisions/0002-brand-architecture-lechner-studios.md` | Working assumption: "Branded House for digital ecosystem." Footer should carry a *"a Lechner Studios product"* endorsement. Shipped via commit `31d9aed` (though with the wrong domain — patch list §3 fixes it). |
| `open-items.md` §"Ecosystem Hosting Map" | Commits `codeflash.lechner-studios.at` as the canonical subdomain. `codeflash.at` in the README was stale; corrected. |
| `open-items.md` closed item 2026-04-19 "Business-site foundation" | `hallo@lechner-studios.at` Zoho Mail box already live — can receive Netlify Forms notifications directly. |

### Correction to §6 (open-items)

Row *"Landing assets | favicon 64px never generated"* was a false positive. `assets/logos/codeflash_favicon_64.png` exists in this repo (3,870 bytes). The corresponding drift only existed in the product repo and was fixed by its own PR #23. No change needed to `codeflash/index.html`'s favicon refs.

### Revised next-action punch list (Path 2)

Ordered by leverage, not sequence:

1. **Drift fixes (landing this investigation branch).** Stats reconciliation, OG URLs, footer legal-link wiring, footer brand-domain correction, README design tokens, GAPS path. Enumerated in `docs/PATCHES_INDEX_HTML_2026-04-21.md`.
2. **Netlify deploy bring-up.** `netlify.toml`, connect site, DNS `codeflash.lechner-studios.at` CNAME, verify legal pages render with `noindex`.
3. **Netlify Forms email capture (Path 2 payoff).** Lead form with double-opt-in consent, notify `hallo@lechner-studios.at`. Add Netlify row to `ai-brain/compliance/sub-processors.md` (ADR-0008 downstream impact, pre-committed).
4. **Pack-sync GitHub Action.** Trigger on `flashcards-programming-app/public/packs/**` change → sync allow-listed files into `codeflash/packs/`. Kills GAPS.md #1.
5. **`Landing.jsx` one-landing decision** (separate branch in product repo). Trim to app-shell only; don't duplicate public marketing.
6. **Upstream P0 watch.** Controller-identity decision unblocks pre-sale compliance. Nothing in this repo ships monetised until that lands; legal pages stay `noindex` with visible `{{token}}` placeholders until then.

Nothing in this list conflicts with the Lemon Squeezy demo window — the Vercel app + its `/bundles` → `html-1` demo path remain untouched.
