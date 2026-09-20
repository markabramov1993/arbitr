# Narration Script — “How a RustChain Bounty Actually Becomes RTC”

**Target length:** 4–5 minutes.  
**Style:** technical, transparent, no token-price or profit claims.

## 1. Work is not money yet

A bounty can show a reward, and a contributor can finish the work, but neither fact means the money is already in a wallet.

RustChain’s bounty tooling separates several stages. First comes the contribution: a bug report, review, content package, or other deliverable. Then a gate or maintainer decides whether the work is actually eligible. Only after that does the payout layer try to create a transfer.

That separation sounds boring, but it prevents the most dangerous accounting mistake in bounty work: treating a sticker price as cash before anyone has accepted it.

## 2. Verification comes before payout

In the current bounty payout script, a claim is not paid merely because its issue exists. The script looks for verified eligibility, resolves the claimant’s payout destination, excludes already-confirmed claims, and then calls the transfer endpoint.

The code also uses an idempotency key per claim. That matters because a timeout or retry should not become a second reward.

The same repository has learned this lesson the hard way. Its payout-audit bounty documents earlier silent-success defects where automation could appear successful while the intended financial effect did not actually happen.

## 3. “Queued” is not “settled”

The transfer API is explicitly two-phase.

A successful payout request can return a phase of “pending,” a pending ID, a transaction hash, and a confirmation window. The current payout script deliberately describes that state as **queued**, not settled.

That wording matters. During the pending period, the balance has not necessarily moved yet. A contributor should not count the reward as spendable merely because the payout request returned HTTP 200.

RustChain’s own API example shows a transfer-pending response with a 24-hour confirmation window.

## 4. The wallet is the final evidence

Once the pending transfer clears, the wallet balance and transaction history become the authoritative evidence that the RTC actually arrived.

Here is a real public example from this production kit’s builder account.

A GitHub Actions job queried the RustChain wallet endpoint on September twentieth. The result was HTTP 200, a settled balance of **126.1 RTC**, and eleven settled inbound transfer records from the founder-community payout wallet.

The important point is not the amount. The important point is the evidence chain: accepted work, payout creation, pending state, then a later wallet read showing settled transfer-in records.

That is a much stronger accounting model than “the issue said 30 RTC, so I earned 30 RTC.”

## 5. Why this matters for autonomous agents

Agents are especially vulnerable to state confusion because they can process hundreds of opportunities at once.

If an agent collapses “opportunity,” “accepted,” “queued,” and “settled” into one number, it can make bad decisions immediately: send duplicate claims, assume a payout exists, or try to spend value that is still only a promise.

A safer agent keeps each state separate and attaches evidence to every transition.

For example:
- an open bounty is an opportunity;
- a maintainer acceptance is a receivable;
- a pending transfer is queued value;
- a wallet receipt is settled value.

Only the final state should be treated as money already received.

## 6. The broader lesson

This payout pipeline is really a small trust protocol.

The contribution creates a claim. Verification decides whether the claim deserves payment. Idempotency prevents accidental duplication. The pending window separates request creation from final settlement. And wallet history closes the loop with an independently readable result.

That same pattern applies far beyond bounties.

Any autonomous system that moves value needs explicit states, evidence, and a rule for when a promise becomes a fact.

For RustChain contributors, the practical rule is simple:

**Do not count the bounty. Count the receipt.**
