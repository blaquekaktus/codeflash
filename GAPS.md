# Code Gaps — Cross-Repo Analysis (codeflash slice)

Generated 2026-04-15 from a side-by-side profile of all 7 portfolio repos
(ai-brain, automatedcontentcreator, flashcards-programming-app, websites,
gute-haende-frontend, codeflash, vistera). Updated 2026-04-15 after the
portfolio cleanup cycle.

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

### 1. Manual pack copy from `flashcards-programming-app` is a real landmine
Pack HTML still hand-copied from the product repo. The sync workflow
was deferred pending explicit path mapping from the owner ("which
flashcards paths actually belong downstream"). Drift remains real —
flashcards has incident reports about stalled pack-building sessions.

**Status:** open, blocked on mapping.

### 2. ~~Name collision with `flashcards-programming-app/package.json.name`~~ → **done**
✅ Upstream renamed to `flashcards-programming-app` in
   flashcards-programming-app PR #12. No more shadowing.

### 3. ~~Pre-commit hook v2 missing~~ → **phase 1 done**
✅ `.layer0-allow` installed (PR #4).
❌ Hook script propagation blocked on ai-brain#13. Tracked in #5 here.

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
   page (dark + JetBrains Mono + Outfit + `--accent` green).
   `{{token}}` placeholders are visibly flagged in a JetBrains-Mono
   pill style, and each page carries a draft banner pointing at the
   ai-brain checklist.
❌ Placeholders not filled (business legal name, Firmenbuchnummer,
   contact email, processing-purpose blocks, cookie/tracking block,
   etc.). Owner task before going live.
❌ Footer link from `index.html` not yet added. Trivial follow-up:
   add `<a href="legal/impressum.html">Impressum</a> ·
   <a href="legal/datenschutz.html">Datenschutz</a>` to the existing
   `<footer>`.

**Status:** scaffold rendered; wiring + real values pending.

## New in this cycle (not in the original GAPS analysis)

### 7. Portfolio hygiene baseline shipped
✅ `.github/ISSUE_TEMPLATE/`, PR template, `.gitattributes`,
   `.github/workflows/file-size-guard.yml` (PR #6).

## Cross-repo roadmap (full list)

See each sibling's `GAPS.md`. Items where this repo is critical path:

- #9 (receive pack-sync PRs) — open, blocked on mapping
- #8 (rename collision) — **done**

## Anti-scope

- Adding a build step — repo is intentionally static-deployable
- AI/LLM dependencies — explicitly scoped out by CLAUDE.md
