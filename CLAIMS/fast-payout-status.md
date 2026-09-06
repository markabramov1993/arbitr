# Fast payout status — audited 2026-09-06

## Confirmed
- USD/stablecoin bounty cash actually received: **$0**.
- RTC live balance: **being re-queried from RustChain; do not assume zero or count nominal claims as balance**.

## Highest-priority payout paths
1. **RustChain #16601** — official paid bounty, review SLA 7 days, accepted -> paid. Two distinct Type C packages were already submitted by email on Sep 4; both were re-audited against the current source and bounty requirements. Public issue comments are desirable for queue visibility but GitHub App external-comment writes still return 403.
2. **Mermail / Superteam** — submission already filed; official PR #174 is open and mergeable. Await sponsor/maintainer judging; 500 USDC is a prize pool, not receivable cash.
3. **Mova #91 / PR #257** — $90 issue remains open. Branch was corrected on Sep 6 to pin explicit Soroban event topics (`pay`, `create_order`, `dispatch`, `refund`). Competing PR #343 exists, so payout probability is lower than previously assumed.

## Archived / low-probability
- Lilly $635 batch: all nine upstream issues are now closed as completed by others/maintainers, with no acceptance evidence for our fallback branches/emails. Keep as historical work only, not active expected income.
- Do not prioritize capital-risking bounties, fabricated activity, region-ineligible work, or stale scraped bounty amounts.
