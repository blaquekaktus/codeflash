# CodeFlash (frontend) — Universal CLAUDE.md Framework

> This repo participates in the Universal CLAUDE.md Framework.
> Universal rules (Layer 0 + Ecosystem + Guardrails) appear first.
> Project-specific rules for this repo are below the divider —
> currently a minimal scaffold, to be filled in as the marketing/
> landing-site workflow matures.
>
> Framework version: Patch 2026-04-12-A

---

## Layer 0 — Identity & Privacy Policy (NON-NEGOTIABLE)

### UIDs Only — Never Commit Real Identities

Every person, client, lawyer, or prospect referenced in ANY repo uses a
UID. Real names, emails, phones, and addresses live ONLY in
`~/.claude-private/` — never in any committed file.

**UID format:** `[Category][Owner]-[8 hex chars]`

- Categories: `P` (person), `C` (client), `L` (lawyer individual), `U` (lead/prospect)
- Owners: `S` (Self), `J` (Jason)
- Examples: `CS-3a7f2c1e`, `LJ-a91b4e5d`, `US-f3b8a24e`

Law firm names are public entities and MAY be committed (firm only,
never individual lawyers inside them — those still use `L[S|J]-xxxxxxxx`).

### Units Only — Never Commit Currency Amounts

Financial values are expressed in abstract **units**, never in
USD/EUR/etc. The conversion factor lives ONLY in
`~/.claude-private/units.conf` — never committed, never sent to any
remote system, not in GBrain's Supabase.

Precision: **3 decimal places** (e.g. `0.450 units`).

### Agent Rules (every session in this repo)

**No conversational sign-offs.** Do not add closing lines like "Branches pushed, no PRs opened per your standing rule" or similar acknowledgments at the end of turns. State what's done inside the task output only; the turn ends when the summary ends.

**PR discipline.** One logical change per PR — a feature, a fix, or a refactor, not all three. If a task touches more than ~400 lines or 5 files across unrelated concerns, split it. Prefer merging small PRs fast over one large PR that sits in review. Use `isolation: worktree` when invoking the `experiment` agent for speculative or risky changes.

You MUST:

- NEVER commit real names, emails, phones, or postal addresses.
- NEVER commit currency symbols or currency codes.
- If a real identity appears in context, replace with a UID placeholder
  and flag that the user must add the offline mapping entry.
- If a currency figure appears in context, replace with `[X units]`
  and flag for local conversion.
- Screenshots/logs containing PII are never committed or sent to remote
  MCPs without redaction.

Before any commit, scan the diff for email markers, currency symbols,
digit-heavy phone-like patterns. If found → abort, sanitize with
UIDs/units, re-stage. The canonical pre-commit hook spec lives in
`ai-brain/patterns/precommit-hook.md`.

### Offline Secrets Directory

Location: `~/.claude-private/`
Contents:
- `units.conf` — conversion factor
- `persons.json` / `clients.json` / `lawyers.json` / `leads.json` — UID→identity maps
- `revenue-unmasked.log` — denormalized local-only view

Recommended: place this directory inside a dedicated encrypted volume
(LUKS on Linux, FileVault on macOS, VeraCrypt cross-platform).
Defer if not yet comfortable with volume encryption — the non-commit
rule is the primary safeguard.

---

## Ecosystem Context

This project is part of an interconnected portfolio. Every feature,
design decision, and content choice should consider how it connects
to the other projects.

### Portfolio Map

- **Vistera** (repo: `vistera`) — PropTech platform. 4K cinematic + VR
  ("DUO Standard"). Austria launch, global positioning.
- **CodeFlash product** (repo: `flashcards-programming-app`) — Spaced-
  repetition learning engine and pack library. The product this repo
  markets.
- **CodeFlash frontend** (repo: `codeflash`, this repo) — Public
  marketing/landing site for the CodeFlash product. Funnels discovery
  → signup.
- **Websites** (repo: `websites`) — Client-facing website build
  service. Entry point for many ecosystem funnels.
- **The AI Shortcut** (repo: `automatedcontentcreator`) — Automated
  content pipeline. Marketing engine and standalone revenue stream.
- **ai-brain** (repo: `ai-brain`) — Knowledge layer: compliance,
  opportunities, revenue, decisions, patterns.
- **Gute Hände** (repo: `gute-haende-frontend`) — Platform connecting
  individuals seeking safe, consensual, non-sexual human touch and
  presence-based sessions with trained practitioners in a structured,
  ethical environment. Firewalled from marketing-style cross-
  pollination (see rule 7 below).

### Cross-Pollination Rules (subtle, never forced)

1. **CodeFlash frontend ↔ CodeFlash product** — This repo is the
   discovery surface; every CTA lands in
   `flashcards-programming-app`. Product updates (new packs, new
   verticals) surface here within the release sprint.
2. **CodeFlash frontend ↔ The AI Shortcut** — AI Shortcut content
   about programming/AI/security education links here. This site's
   content surfaces (blog, free-sample page) reference AI Shortcut
   episodes where genuinely relevant.
3. **CodeFlash frontend → Websites** — If a visitor lands via an
   ecosystem client build (e.g. a trainer client site), footer offers
   Websites as the build path.
4. **Vistera ↔ Websites clients** — Real-estate/property clients get
   DUO Standard as a premium listing upsell.
5. **CodeFlash ↔ Vistera** — CodeFlash can teach the tech behind
   Vistera (4K video, VR, spatial computing); CodeFlash users creating
   content are AI Shortcut candidates.
6. **ALL → Websites** — Every project needs web presence.
7. **Gute Hände — firewalled from inbound marketing bridges.**
   Other ecosystem repos do not pipe prospects INTO Gute Hände. Narrow
   allowed bridges only: Websites may serve as a build contractor for
   a Gute-Hände landing surface; The AI Shortcut may use Gute Hände
   as a digital-product-design case study only with explicit written
   approval from the Gute Hände owner.

Integration style: footer links, "related tool" suggestions, genuine
references in content. Never pop-ups, never ads.

### This Project's Role in the Ecosystem

CodeFlash public frontend — marketing/landing site for the CodeFlash
spaced-repetition product (`flashcards-programming-app`). Funnels
discovery → product signup.

Every page in this repo should answer one of three questions for a
visitor: (a) what is CodeFlash, (b) why should I care, (c) where do I
start. Pages that don't serve one of those three get pruned.
Marketing copy is insider/no-BS (same voice as The AI Shortcut) —
evidence first, hype never.

### Adjacent Opportunity Detection (passive background task)

While working on this project, watch for:

- Visitor/prospect questions that the current site cannot answer →
  content-gap signal.
- Pack/vertical requests from visitors that product doesn't yet cover
  → product-roadmap signal.
- Traffic sources (referrers, campaigns) that convert unexpectedly
  well → channel signal.
- Visitors arriving from ecosystem projects (AI Shortcut, Websites)
  → cross-pollination signal worth strengthening.
- Embed/integration requests from trainers or schools → B2B
  whitespace signal.

Do NOT interrupt the current task. Log briefly (UID-redacted) with
intent to append to `ai-brain/opportunities/signals.md` on the next
ai-brain visit. The weekly opportunity scan evaluates them.

Cluster-detection questions for every visitor/prospect interaction:

1. What does this visitor NEED that CodeFlash doesn't yet cover?
2. What tool or resource do they reach for BEFORE the flashcards?
3. What tool or resource do they reach for AFTER the flashcards?
4. Who else in this visitor's workflow (team lead, trainer, peer)
   would benefit from the same content?
5. What adjacent vertical (languages, medical, legal, finance) would
   value a CodeFlash-style pack library?

---

## Financial & Operational Guardrails

- **Pre-revenue projects:** organic/free channels only. Zero paid spend.
- **Spending ceiling:** 25% of ACCRUED revenue (cash-in-hand, not
  projected). Values in units. Tracked in
  `ai-brain/revenue/ceilings.md`.
- **Autonomous ad spend** requires segment-benchmarked conversion
  projection (market data × 0.6 newcomer credibility factor). A/B test
  budget for unproven creative/audience capped below a configured
  threshold (documented in `ai-brain/revenue/budgets/`) before positive
  signal is required.
- **Compliance gate** runs before any outreach → see
  `ai-brain/compliance/countries/[region].md`.
- **Expert consultation discipline** — do not propose paid expert
  consultation to re-confirm a rule that public statutes, portals, or
  settled case law already make plain. See
  `ai-brain/patterns/research-discipline.md` for the decision test.

---

## gstack Skills (aspirational reference)

These slash commands are part of the GStack framework. They only work
**after GStack is installed locally**:

```bash
git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

Until installed this section is informational only.

Available once active: `/office-hours`, `/plan-ceo-review`,
`/plan-eng-review`, `/plan-design-review`, `/design-consultation`,
`/review`, `/ship`, `/land-and-deploy`, `/canary`, `/benchmark`,
`/browse`, `/qa`, `/qa-only`, `/design-review`,
`/setup-browser-cookies`, `/setup-deploy`, `/retro`, `/investigate`,
`/document-release`, `/codex`, `/cso`, `/autoplan`, `/careful`,
`/freeze`, `/guard`, `/unfreeze`, `/gstack-upgrade`.

Rule: use `/browse` for web browsing; never use
`mcp__claude-in-chrome__*` tools.

---

<!-- =========================================================== -->
<!-- PROJECT-SPECIFIC RULES BELOW — codeflash repo               -->
<!-- =========================================================== -->

# CodeFlash frontend — Engineering Rules (scaffold)

> This section is a minimal starter modelled on `websites/CLAUDE.md`.
> Fill it in as the marketing/landing-site workflow matures and
> conventions stabilise.

## Repo shape

Static site. Current layout:

- `index.html` — landing page.
- `packs/` — published free-sample pack HTML (served as-is; the pack
  HTML is produced by the `flashcards-programming-app` generator).
- `assets/` — static assets (images, fonts, stylesheets).
- `bundles/` — downloadable pack bundles (ZIP/PDF).

Keep the repo static-deployable (no build step required) until a real
reason to add one appears. Hosting: GitHub Pages or equivalent.

## Content and identity handling

- Every visitor/prospect/client referenced in committed content uses a
  `US-xxxxxxxx` / `CS-xxxxxxxx` UID — never their real name, company,
  or contact.
- Testimonials and case studies require explicit written opt-in from
  the source. Sanitize before commit; keep originals in
  `~/.claude-private/testimonials/` only.
- No analytics keys, Stripe keys, or mailing-list API tokens in
  committed files — `.env` only, `.gitignore`d.

## Cross-pollination surfaces

- **Footer** — persistent link to the CodeFlash product repo
  (`flashcards-programming-app`) as the canonical source of packs.
- **Footer** — link to The AI Shortcut when content-led traffic warrants
  (contextual, not ornamental).
- **Footer** — link to Websites for ecosystem client builds.
- **Blog/resources pages** (once they exist) — reference AI Shortcut
  episodes on adjacent topics where genuinely relevant.

Never force cross-pollination. No pop-ups, no ads, no intrusive
placements. Subtle, genuine references only.

## Design system

Typography, colour tokens, and voice are **not decided per-repo**. The
canonical spec lives in `ai-brain/design-system/` and applies to every
frontend repo in the ecosystem (this one, `websites`, `vistera`,
`gute-haende-frontend`, `automatedcontentcreator`).

- **Typography:** `ai-brain/design-system/typography.md`
  (currently: Inter body + JetBrains Mono for code/numerics/labels).
- **Colour tokens:** `ai-brain/design-system/tokens.md`
  (dark surface, `--accent` green, semantic warn/blue/pink/purple).
- **Voice:** `ai-brain/design-system/voice.md`
  (insider/no-BS, evidence first, hype never).

Before any styling or copy change, read the relevant spec file. If the
change conflicts with the spec, update the spec first in `ai-brain`
(single source of truth), then propagate — never branch the tokens in
this repo.

Deviations need a written reason committed alongside the change (e.g.
a line in the PR description pointing at why this page legitimately
departs from the spec). "It looked better" is not a reason.

## Build + deploy conventions

- Accessibility baseline: WCAG 2.1 AA.
- Performance baseline: Lighthouse mobile score ≥ 90 for the landing
  page before any release.
- Pack HTML is authored in `flashcards-programming-app` and copied
  here — never re-author pack content in this repo.
- Before shipping any copy change, run the canonical pre-commit hook
  (`ai-brain/patterns/precommit-hook.md`) locally.

## Hard rules

1. **No visitor/client PII in commits.** Names, emails, phones,
   addresses go only in `~/.claude-private/`.
2. **No secrets in commits.** Analytics/payment/mailing keys live in
   `.env` and are `.gitignore`d.
3. **Pack content is downstream of product.** Never edit pack HTML
   here; edit in `flashcards-programming-app` and re-publish.
4. **Accessibility is not optional.** WCAG 2.1 AA is the floor, not
   the target.

## Output format

Until project-specific engineering rules are codified, default to the
Vistera repo's protocol: diagnose first, smallest footprint, verify
before asking user to test.
