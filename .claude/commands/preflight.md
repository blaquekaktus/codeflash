# /preflight

Pre-commit checklist for codeflash (marketing frontend).

1. **Pricing sync** — any price/feature change here must match `flashcards-programming-app` exactly. Cross-check before committing.
2. **CTA links** — all "Sign up" / "Get started" CTAs must point to the live flashcards app URL, not localhost or placeholder.
3. **No PII in commits** — use UIDs for any person/client references.
4. **Layer 0 scan** — no currency symbols in internal files, no real emails in committed code.
5. **No secrets** — `.env` only, gitignored.
6. **Accessibility** — interactive elements labelled, images have alt text.

Report pass / warn / fail per item.
