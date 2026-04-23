# Code Gaps — Cross-Repo Analysis (codeflash slice)

Generated 2026-04-15 from a side-by-side profile of all 7 portfolio repos
(ai-brain, automatedcontentcreator, flashcards-programming-app, websites,
gute-haende-frontend, codeflash, vistera). Updated 2026-04-15 after the
portfolio cleanup cycle. Further corrections 2026-04-21 (path + hosting).

This file captures gaps that **only surface when comparing repos against
each other**. Local content work is out of scope.

## Role of this repo

Static marketing/landing site (HTML only, no build) for the CodeFlash
product. Pack HTML is **authored upstream** in
`flashcards-programming-app/public/packs/` and copied into this repo's
`packs/` directory. (Corrected 2026-04-21: prior wording said
`flashcards-programming-app/packs/` → `this repo's bundles/` — both
were wrong. Product repo moved pack HTML to `public/packs/` in commit
`871d4ce`; downstream copies land in `codeflash/packs/`. `bundles/`
in this repo holds hand-authored bundle preview pages, not copies.)

**Hosting.** Target host is **Netlify** per `ai-brain/decisions/0008-hosting-split-netlify-vercel.md` (static sites → Netlify); canonical URL
`https://codeflash.lechner-studios.at/` per the ecosystem hosting map in
`ai-brain/open-items.md` (decided 2026-04-20). README still says
"GitHub Pages" — will be corrected.

This is **not** a fork of the well-known `codeflash-ai/codeflash` Python
optimizer, despite the matching name.

## codeflash's slice of the cross-repo backlog

### 1. ~~Manual pack copy from `flashcards-programming-app`~~ → **partially resolved**
Path mapping clarified 2026-04-21: source is
`flashcards-programming-app/public/packs/**`; downstream target is
`codeflash/packs/<topic>/`. Allow-list for downstream copy is the
free-sample subset (anything marked `is_free=true` in Supabase plus
any explicitly-chosen marketing samples). Automation candidate:
GitHub Action in product repo triggers on `public/packs/**` change,
opens a sync PR here.

**Update 2026-04-16 (bundle side resolved):** upstream build script
fixed (flashcards-programming-app PR #19; was pointing at stale
`../packs`, script didn't run at all). Owner confirmed 15 bundle ZIPs
now build cleanly from 82 source packs via
`bash engine/build_bundles.sh`. Old stale `FLASHCARDS_TOTAL/` folder
(manual assembly from Apr 10) deleted — fully regenerable. Bundle
ZIPs are gitignored in flashcards and distribute via Supabase Storage
/ Gumroad — **not committed to codeflash**. This sync item applies
ONLY to the free-sample HTML subset for the marketing-site preview.

**Status:** mapping clear; upstream build fixed; bundle-side resolved.
Remaining: wire the GitHub Action for free-sample HTML sync.

### 2. ~~Name collision with `flashcards-programming-app/package.json.name`~~ → **done**
✅ Upstream renamed to `flashcards-programming-app` in
   flashcards-programming-app PR #12. No more shadowing.

### 3. ~~Pre-commit hook v2 missing~~ → **phase 1 done**
✅ `.layer0-allow` installed (PR #4).
❌ Hook script propagation blocked on ai-brain#13. Tracked in #5 here.

Update 2026-04-21: phase 2 landed via PR #8 on 2026-04-15;
`scripts/precommit-hook.sh` is the canonical source.

### 4. Three open `claude/*` branches duplicate work in websites and gute-haende
Still open. `claudemd-drift-propagation-lBvaw`,
`continue-claude-framework-S2wCF`, `currency-token-cleanup-Ht1TN`.
Coordinate via portfolio-level issue.

### 5. No CMS pipeline from automatedcontentcreator
Blog/resources pages still flagged in CLAUDE.md as "once they exist."
Upstream repo (automatedcontentcreator) has 18 stub modules; nothing to
consume yet.

**Status:** open, upstream pending.

### 6. ~~AT legal pages~~ → **skeleton rendered; owner values pending**
✅ Austrian Impressum + Datenschutz scaffolds shipped in ai-brain
   `compliance/templates/at/` (checklists + placeholder templates with
   statute citations).
✅ Static HTML pages rendered from the templates: `legal/impressum.html`
   and `legal/datenschutz.html`. Theme matches the CodeFlash landing
   page (dark + JetBrains Mono + Inter + `--accent` green).
   `{{token}}` placeholders are visibly flagged in a JetBrains-Mono
   pill style, and each page carries a draft banner pointing at the
   ai-brain checklist.
❌ Placeholders not filled (business legal name, Firmenbuchnummer,
   contact email, processing-purpose blocks, cookie/tracking block,
   etc.). Owner task before going live — blocked on ai-brain P0
   "Controller-identity decision" (natural person / Einzelunternehmen
   / GmbH).
❌ Footer link from `index.html` not yet added. Enumerated in
   `docs/PATCHES_INDEX_HTML_2026-04-21.md` §3 — ready to apply.

**Status:** scaffold rendered; footer-wiring enumerated; real values
blocked on controller-identity P0 (see `ai-brain/backlog/INDEX.md`).

## New in this cycle (not in the original GAPS analysis)

### 7. Portfolio hygiene baseline shipped
✅ `.github/ISSUE_TEMPLATE/`, PR template, `.gitattributes`,
   `.github/workflows/file-size-guard.yml` (PR #6).

### 8. Split-repo audit completed 2026-04-21
See `docs/PROJECT_STATE_CODEFLASH_2026-04.md`. Decision recorded:
**Path 2 — keep the split, wire Netlify Forms for lead capture,
eliminate drift.** Resolves the P1 split-repo-audit row in
`ai-brain/backlog/codeflash-flashcards.md`.

## Cross-repo roadmap (full list)

See each sibling's `GAPS.md`. Items where this repo is critical path:

- #9 (pack-sync) — **partially resolved**: bundle zips handled
  upstream via build + storage; free-sample HTML sync Action still TODO
- #8 (rename collision) — **done**

## Anti-scope

- Adding a build step — repo is intentionally static-deployable
- AI/LLM dependencies — explicitly scoped out by CLAUDE.md
