# /techdebt

Audit accumulated technical debt in this repo. Output only — do not fix anything inline.

## Scan

1. **TODO / FIXME / HACK / XXX** — grep with file:line references
   ```bash
   grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" --include="*.md" . | grep -v node_modules | grep -v .next
   ```

2. **Files over 500 lines** — split candidates
   ```bash
   find . -name "*.ts" -o -name "*.tsx" -o -name "*.py" | grep -v node_modules | xargs wc -l 2>/dev/null | sort -rn | head -20
   ```

3. **Stale comments** — references to old PRs, removed features, or obsolete APIs (scan manually from TODO grep output)

4. **Missing .claude/** tooling — is explore.md present? preflight.md? settings.json?

## Output format

Ranked list: **blocking** → **soon** → **parking lot**, with `file:line` for each item.

Add any blocking or soon items to the relevant `backlog/*.md` file in ai-brain before closing the session.

