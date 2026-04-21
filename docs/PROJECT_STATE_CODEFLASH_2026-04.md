# CodeFlash Project State — 2026-04

Cross-repo archaeology of `blaquekaktus/codeflash` (this repo) and `blaquekaktus/flashcards-programming-app`. Investigation date: 2026-04-21. Default branches: both `main`. Latest commits: `codeflash` `310269d` 2026-04-19, `flashcards-programming-app` `8a296fb` 2026-04-20.

The report is split across a folder of per-section files because a single document repeatedly hit stream timeouts. Read this index for the verdict and critical questions; drill into the sections for evidence.

## Decision recorded — 2026-04-21

**Path 2 — keep the split, wire Netlify Forms for lead capture, eliminate drift.**

Rationale: Netlify Forms on the static `codeflash` surface is a real lead-capture channel with no added SaaS cost, and ADR-0008 already blesses static→Netlify as the portfolio hosting shape. The "hidden backend" narrative does not hold (both repos are public), but the lead-capture value of a purpose-built static marketing surface is real enough to justify the ongoing propagation cost — **if** the drift is actively closed.

Acceptance criteria for Path 2:

- `codeflash.lechner-studios.at` pointed at Netlify; marketing lives there.
- `flashcards-programming-app` continues on Vercel; `Landing.jsx` demoted to an in-app shell (not duplicate public marketing).
- Pack sync automated (GitHub Action from product repo → this repo's `packs/`).
- `compliance/sub-processors.md` updated with Netlify row (ADR-0008 downstream impact).
- Double-opt-in consent copy live on the lead form before any outreach.

Resolves P1 "Split-repo audit" in `ai-brain/backlog/codeflash-flashcards.md`.

## Sections

1. [Identity of each repo](./PROJECT_STATE_CODEFLASH_2026-04/01-identity.md)
2. [Relationship between them](./PROJECT_STATE_CODEFLASH_2026-04/02-relationship.md)
3. [The split decision itself](./PROJECT_STATE_CODEFLASH_2026-04/03-split-decision.md)
4. [Structure (per repo)](./PROJECT_STATE_CODEFLASH_2026-04/04-structure.md)
5. [Decisions already made](./PROJECT_STATE_CODEFLASH_2026-04/05-decisions.md)
6. [What's still open (table)](./PROJECT_STATE_CODEFLASH_2026-04/06-open-items.md)
7. [Consolidation assessment](./PROJECT_STATE_CODEFLASH_2026-04/07-consolidation.md) (now includes Path 2 addendum + ai-brain cross-refs)

Also: [Pending edits to `index.html`](./PATCHES_INDEX_HTML_2026-04-21.md) — drift-fix list that a single tool-call rewrite could not land safely in this session.

## Original critical questions (resolved 2026-04-21)

1. ~~Where does `codeflash.at` actually point?~~ **Stale README copy.** Canonical URL is `https://codeflash.lechner-studios.at/` per `ai-brain/open-items.md` §Ecosystem Hosting Map (decided 2026-04-20). README + OG metadata corrected.
2. ~~Is `Landing.jsx` or `codeflash/index.html` the public front door?~~ **codeflash/index.html.** Under Path 2, the static surface owns public marketing; `Landing.jsx` becomes the app-internal landing and should be trimmed to avoid duplicating the public marketing copy.
3. ~~What threat model did the split try to address?~~ **Not a security threat model — a lead-capture / form-tooling optimisation** (static→Netlify Forms vs framework→Vercel). ADR-0008 codifies the shape rule.

## Still pending (not resolved by this investigation)

- **Controller-identity P0** (`ai-brain/backlog/INDEX.md`). Blocks codeflash/flashcards pre-sale compliance (FAGG, Button-Lösung, Impressum populated, DSE). Consolidation does not unblock this.
- **Lemon Squeezy demo surface.** `flashcards-programming-app` Vercel URL needs to remain the demo target until LS approval lands — don't reshuffle during the review window.
- **`Landing.jsx` one-landing decision.** Tracked in the product repo, not resolvable here.

## Method & caveats

All paths in backticks are GitHub paths. Evidence is commit SHA, PR number, or file path — not inference. Aspirational README copy is flagged as such where the code doesn't back it up. "Unclear" means "not documented and not visible in code I read" — not "I skipped it."
