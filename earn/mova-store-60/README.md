# Mova Store bounty #60 — ready patch

Target: `Movalabs-crew/mova-store#60` — **$50**.

The README environment-variable reference omits four EmailJS variables that are already documented in `.env.local.example`.

The prepared patch adds:

- `NEXT_PUBLIC_EMAILJS_SERVICE_ID` — required
- `NEXT_PUBLIC_EMAILJS_TEMPLATE_ID` — required
- `NEXT_PUBLIC_EMAILJS_PUBLIC_KEY` — required
- `NEXT_PUBLIC_DEFAULT_RECIPIENT_EMAIL` — optional

The required/optional markers mirror the source `.env.local.example`. This is documentation-only and does not alter runtime behavior.

GitHub claimant: `markabramov1993`.
