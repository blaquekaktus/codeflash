# /context-dump

Export session state as a structured handoff before /compact or /clear.

Output the following snapshot — do not skip any section:

## Task
One sentence: what was I working on?

## Files touched
List every file modified, created, or deleted this session with one-line reason.

## Commits made
Run `git log --oneline -10` and list commits made since this session started. If none, say "none".

## Open items surfaced
Any new TODOs, bugs discovered, or follow-up tasks identified this session.

## Blockers or decisions needed
Anything that needs human input before work can continue.

## Layer 0 flags
Any PII, currency-symbol, or identity-leak risks raised (even if resolved).

## Next-session primer
One paragraph a fresh session could paste as context to pick up exactly where this left off. Include branch name, last file touched, and the single most important next action.

