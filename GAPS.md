# Code Gaps — Cross-Repo Analysis (codeflash slice)

Generated 2026-04-15 from a side-by-side profile of all 7 portfolio repos
(ai-brain, automatedcontentcreator, flashcards-programming-app, websites,
gute-haende-frontend, codeflash, vistera).

This file captures gaps that **only surface when comparing repos against
each other**. Local content work is out of scope.

## Role of this repo

Static marketing/landing site (HTML only, no build) for the CodeFlash
product. Pack HTML is **authored upstream** in
`flashcards-programming-app/packs/` and copied into this repo's
`bundles/`. Hosting: GitHub Pages.

This is **not** a fork of the well-known `codeflash-ai/codeflash` Python
optimizer, despite the matching name.

## codeflash's slice of the cross-repo backlog

### 1. Manual pack copy from `flashcards-programming-app` is a real
landmine
Pack HTML is hand-copied from the product repo. flashcards-programming-app
already has two incident reports (2026-04-10) about stalled pack-building
sessions with unverified build status. The drift is happening.

**Action:** receive a release-tag PR from flashcards-programming-app's
new release workflow (see flashcards GAPS item #2). Reject manual edits
to `bundles/*.html` via CODEOWNERS or a pre-commit guard.

### 2. Name collision with `flashcards-programming-app/package.json.name`
That package.json sets `name: "codeflash"`, shadowing this repo's
identity. Cross-repo confusion any time someone says "the codeflash repo."

**Action:** coordinate the rename in flashcards (see flashcards GAPS
item #1).

### 3. Pre-commit hook v2 missing
Same as other frontends. See ai-brain GAPS item #2.

### 4. Three open `claude/*` branches duplicate work in websites and
gute-haende
`claudemd-drift-propagation-lBvaw`, `continue-claude-framework-S2wCF`,
`currency-token-cleanup-Ht1TN`. Coordinate via portfolio-level issue.

### 5. No CMS pipeline from automatedcontentcreator
Blog/resources pages are flagged in CLAUDE.md as "once they exist."
automatedcontentcreator could generate them.

**Action:** see automatedcontentcreator GAPS item #1 — that repo will
add `src/repurpose/targets/codeflash_bundles.py`. Also extend it to a
`codeflash_blog.py` target when blog scaffolding lands.

### 6. AT legal pages
"Made in Austria" branding without an Impressum/Datenschutz. Same
problem as 4 sibling frontends.

**Action:** consume ai-brain's pending Austrian legal templates (see
ai-brain GAPS item #4).

## Cross-repo roadmap (full list)

See each sibling's `GAPS.md`. Items where this repo is critical path:
9 (receive pack-sync PRs), 8 (rename collision in flashcards).

## Anti-scope

- Adding a build step — repo is intentionally static-deployable
- AI/LLM dependencies — explicitly scoped out by CLAUDE.md
