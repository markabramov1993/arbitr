# DealRail — programmable deposits and settlement for high-trust marketplace deals

**Tagline:** Turn a verbal “I’ll take it” into a verifiable, time-bounded deal in seconds.

## Problem

High-value peer-to-peer and dealer marketplace transactions — used cars, equipment, electronics and collectibles — still rely on screenshots, bank-transfer promises, cash deposits, PDFs and chat messages. The riskiest moment is often before the final payment: a buyer wants the seller to reserve the item, while the seller wants proof that the buyer is serious. Today that usually means an off-platform bank transfer or cash deposit with unclear refund rules and weak shared evidence.

This creates four recurring problems:

1. **Reservation fraud:** fake payment screenshots or reversible promises are used to “hold” an item.
2. **Ambiguous refunds:** buyer and seller disagree about when a deposit should be returned.
3. **Cross-border friction:** SEPA timing, weekends and different banks slow down deals.
4. **No shared state:** the marketplace, buyer and seller do not have one verifiable source of truth for “reserved / paid / expired / refunded”.

## Solution

DealRail is a lightweight Solana settlement layer for marketplace deposits and high-value handoffs.

A seller creates a deal with:
- asset description or listing URL;
- deposit amount;
- reservation expiry;
- refund/forfeit conditions;
- optional final settlement amount;
- buyer wallet or shareable payment link.

The buyer funds the deposit in a supported stablecoin. The program records the deal state on-chain and exposes a human-readable receipt that both parties can verify independently.

Core states:

`created → funded → reserved → completed`

with guarded exits:

`funded → refunded`

`reserved → expired/refunded`

`reserved → disputed` (MVP can make this “pause and require mutual action” rather than pretending to solve legal arbitration on-chain).

The key product is not “crypto escrow for everything”. It is a narrow, high-friction workflow: **reservation deposits and settlement evidence for marketplace transactions**.

## Why Solana is actually necessary

This is not blockchain added for decoration. The useful properties are:

- **shared state:** buyer, seller and marketplace can independently verify the same deal status;
- **programmable release/refund rules:** the deposit follows explicit state transitions instead of chat promises;
- **fast confirmation:** the seller can verify a funded reservation within seconds;
- **low transaction cost:** small deposits remain economical;
- **stablecoin settlement:** avoids forcing users to speculate on a volatile asset;
- **composability:** marketplaces, dealer CRMs and payment links can consume the same program state.

A normal database could work for one marketplace, but it recreates a trusted middleman. DealRail is designed as infrastructure that multiple marketplaces or independent dealers can use without one operator controlling the ledger of truth.

## Initial user

The initial target user is a small dealer, broker or power seller handling multiple inbound buyers per day. Their pain is operational rather than ideological: “Who actually paid a deposit? Until when is the item reserved? Can I prove the rule we agreed to?”

The product should feel like a payment link, not a DeFi dashboard.

## MVP for the Solana Hackathon

### 1. Deal program
A Solana program with deterministic deal accounts containing:
- seller;
- buyer (optional until claimed);
- mint;
- deposit amount;
- expiry timestamp;
- state;
- settlement/refund authority rules;
- immutable deal terms hash.

### 2. Payment-link web app
Seller enters the amount, expiry and short deal terms. DealRail returns a QR/link that opens a buyer payment screen.

### 3. Verifiable receipt
A public receipt page shows:
- amount funded;
- current deal state;
- expiry;
- wallet signatures shortened for normal users;
- Solana explorer transaction links;
- original terms hash.

### 4. Happy-path settlement
- seller creates deal;
- buyer funds stablecoin deposit;
- item becomes reserved;
- both parties confirm completion;
- funds release to seller or are credited toward final settlement.

### 5. Safe refund paths
- seller can refund before completion;
- expiry can unlock a predefined refund path;
- disputed state freezes automatic release and makes the limitation explicit.

## Hackathon demo

A two-minute demo can show one realistic transaction:

1. Seller creates a €500-equivalent reservation for a high-value listing.
2. Buyer opens the QR code and funds the deposit using a stablecoin on Solana devnet/test environment.
3. Seller dashboard changes to **Funded / Reserved** immediately.
4. A second browser independently opens the receipt URL and verifies the same state.
5. The parties complete the deal and the program executes the agreed release path.
6. A second example expires and demonstrates the refund path.

No real user money is required for the hackathon demo.

## Business model

The protocol can remain open while the hosted product charges for workflow value:

- free basic payment links;
- small flat fee or basis-point fee for completed commercial reservations;
- dealer/merchant subscription for CRM integrations, team roles and reconciliation;
- API plan for marketplaces that embed DealRail directly.

The wedge is reservation deposits. Future expansion can cover milestone payments, inspection holds, shipping handoffs and marketplace-native buyer protection.

## Distribution

Start with workflows where deals already begin in WhatsApp, Telegram, Facebook Marketplace, classified sites and dealer CRMs. A seller does not need marketplace integration to use a DealRail link, which removes the cold-start dependency.

After validating seller demand, integrations can expose “Reserve with DealRail” directly inside marketplace listings and dealer software.

## Differentiation

DealRail is intentionally narrower than generic escrow protocols:

- optimized for real marketplace reservation flows;
- plain-language expiry/refund states;
- stablecoin-first UX;
- shareable receipt designed for non-crypto users;
- marketplace/CRM integration surface;
- no claim that smart contracts replace consumer law or human dispute resolution.

The defensible product layer is the combination of workflow, integrations and reputation/history around completed deals — not merely an escrow contract.

## Key risks and how the MVP handles them

**Legal/compliance:** DealRail does not market itself as a court or universal escrow agent. The MVP uses explicit user-defined terms, non-custodial program logic and clear limitations. Any production rollout would require jurisdiction-specific review before handling regulated custody-like flows.

**Wallet friction:** payment links and QR flows should abstract chain details; the long-term UX can use embedded wallets/passkeys where appropriate.

**Stablecoin/off-ramp availability:** MVP supports a small allowlist and does not promise universal fiat conversion.

**Disputes:** the first version does not invent decentralized arbitration. A dispute can freeze automatic release and defer to an agreed off-chain process.

## Success metrics

For an early pilot:
- time from link creation to verified reservation;
- funded-deal conversion rate;
- percentage of deposits completed vs refunded/expired;
- seller repeat usage;
- reconciliation time saved versus chat + bank transfer;
- number of disputes caused by ambiguous terms.

## Why now

Stablecoin UX is becoming practical enough that the remaining opportunity is increasingly about **specific workflows**, not generic wallets. High-value marketplace transactions have a clear trust gap, repeated payment behavior and a natural moment where verifiable programmable settlement adds value.

DealRail turns that gap into a focused Solana product that can be built, demonstrated and tested during the hackathon instead of remaining a broad “blockchain marketplace” pitch.
