# DealRail — Superteam Germany Ideathon submission

## Project name
DealRail

## Tagline
Turn a verbal “I’ll take it” into a verifiable, time-bounded deal in seconds.

## Short description
DealRail is a Solana settlement layer for reservation deposits and high-value marketplace handoffs. Sellers create a deal with a deposit amount, expiry and refund/release rules; buyers fund it in a supported stablecoin; both sides get the same verifiable deal state and receipt instead of relying on screenshots, chat promises or ambiguous bank-transfer evidence.

The wedge is intentionally narrow: reservation deposits for used cars, equipment, electronics, collectibles and similar high-trust transactions. Solana provides shared state, fast confirmation, low-cost programmable release/refund paths and stablecoin settlement that multiple marketplaces or independent dealers can verify without one operator controlling the ledger of truth.

## Why this is a strong hackathon idea
- Clear repeated problem: proving a buyer actually reserved an item and under what terms.
- Blockchain is functional, not decorative: the product depends on independently verifiable shared state and programmable settlement rules.
- Small enough for a credible hackathon MVP: deal program, payment link, receipt page, completion/refund path.
- Easy two-minute demo: create -> fund -> reserved -> verify in a second browser -> settle; then show an expiry/refund path.
- Real distribution wedge: links can start in WhatsApp, Telegram, Facebook Marketplace, classifieds or dealer CRMs before any deep marketplace integration exists.

## MVP build plan
1. Solana program with deterministic deal accounts and explicit state transitions.
2. Stablecoin deposit funding on devnet/test environment.
3. Seller payment-link / QR creation flow.
4. Public receipt page showing amount, state, expiry and transaction evidence.
5. Mutual completion plus safe refund/expiry paths.
6. Demo script covering happy path and one refund/expiry case.

## Business model
Free basic links, then a flat or basis-point fee for completed commercial reservations, merchant subscriptions for reconciliation/team workflows, and API plans for marketplace integrations.

## Full public concept
https://github.com/markabramov1993/arbitr/blob/main/docs/dealrail-solana-ideathon.md

## Submission checklist
- [x] Project name
- [x] Tagline
- [x] Short problem/solution description
- [x] Public idea document
- [ ] Colosseum registration completed with country set to Germany
- [ ] Follow @SuperteamDE on X
- [ ] Submit through Superteam Earn
