#!/usr/bin/env bash
set -euo pipefail

deny_names="$HOME/.claude-private/deny-names.txt"

# Pathspecs: repo root + binary excludes
pathspecs=(. ':!*.lock' ':!*.png' ':!*.jpg' ':!*.jpeg' ':!*.gif' ':!*.webp' ':!*.pdf' ':!*.zip' ':!*.mp4' ':!*.mov' ':!*.ico')

# Repo-specific excludes from .layer0-allow at repo root (optional file).
# Lines starting with # are comments; blank lines ignored.
# Entries are pathspec patterns (e.g. "mockups/", "index.html", "docs/Preisstrategie.md").
if [ -f .layer0-allow ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    line="${line%$'\r'}"
    line="${line#"${line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"
    [ -z "$line" ] && continue
    case "$line" in \#*) continue;; esac
    pathspecs+=(":!$line")
  done < .layer0-allow
fi

diff="$(git diff --cached --unified=0 -- "${pathspecs[@]}")"
added="$(printf '%s\n' "$diff" | grep -E '^\+' | grep -Ev '^\+\+\+' || true)"

fail() {
  printf '\n\033[31mpre-commit blocked:\033[0m %s\n' "$1" >&2
  printf '%s\n' "$2" >&2
  printf '\nBypass only if certain: git commit --no-verify\n' >&2
  exit 1
}

if m=$(printf '%s\n' "$added" | grep -En '[[:alnum:]._%+-]+@[[:alnum:].-]+\.[[:alpha:]]{2,}' || true); [ -n "$m" ]; then
  fail 'email-like token found' "$m"
fi

if m=$(printf '%s\n' "$added" | grep -En '[€£¥]|\$[0-9]' || true); [ -n "$m" ]; then
  fail 'currency symbol found — use units' "$m"
fi

if m=$(printf '%s\n' "$added" | grep -Enw 'USD|EUR|GBP|CHF|JPY|AUD|CAD' || true); [ -n "$m" ]; then
  fail 'currency code found — use units' "$m"
fi

if m=$(printf '%s\n' "$added" | grep -En '(^|[^0-9a-f-])(\+?[0-9][0-9 ()\-]{6,15}[0-9])($|[^0-9a-f-])' || true); [ -n "$m" ]; then
  fail 'phone-like digit run found' "$m"
fi

if [ -f "$deny_names" ]; then
  while IFS= read -r name; do
    [ -z "$name" ] && continue
    case "$name" in \#*) continue;; esac
    if m=$(printf '%s\n' "$added" | grep -Fn "$name" || true); [ -n "$m" ]; then
      fail "deny-listed identity '$name' found" "$m"
    fi
  done < "$deny_names"
fi

# Defense-in-depth: Python SDK second pass (catches patterns the bash regex misses)
if command -v python3 &>/dev/null && python3 -c "import ai_brain_sdk" 2>/dev/null; then
  set +e
  git diff --cached | python3 -m ai_brain_sdk validate-layer0
  SDK_EXIT=$?
  set -e
  if [ $SDK_EXIT -ne 0 ]; then
    echo "ai-brain-sdk: Layer 0 violations detected — commit blocked." >&2
    exit 1
  fi
fi
# If SDK not installed, bash regex above is still the gate — not a hard failure

exit 0
