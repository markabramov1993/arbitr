# DriveProof — Cross-Border Used-Car Escrow & Provenance on Solana

**Tagline:** Buy a used car across borders without trusting a stranger, a screenshot, or a bank transfer.

## The problem

Cross-border used-car purchases are still surprisingly manual. A buyer may need to send a deposit before seeing the vehicle in person, while the seller does not want to release the car or original documents before payment is final. Transporters, inspection reports, export paperwork, invoices, registration documents and proof of handover live across email, chat apps and PDFs.

That creates three recurring failure modes:

1. **Payment trust:** buyers fear sending money before delivery; sellers fear handing over the vehicle before settlement.
2. **Document trust:** VINs, inspection reports, invoices and handover evidence can be incomplete, altered or attached to the wrong vehicle.
3. **Cross-border coordination:** buyer, seller and transporter often operate in different countries, currencies and banking hours, so disputes are hard to resolve quickly.

Traditional marketplaces help buyers discover cars, but the highest-risk part of the transaction happens after discovery.

## The idea

**DriveProof** is a transaction layer for cross-border used-car deals. It combines milestone escrow with a tamper-evident vehicle deal record.

A deal starts with a VIN and agreed terms. The buyer funds an escrow. The parties then complete predefined milestones such as:

- seller identity and ownership check completed;
- VIN / vehicle document package uploaded;
- independent inspection completed;
- transporter pickup confirmed;
- vehicle delivered;
- buyer handover window completed.

Documents themselves remain off-chain in encrypted storage. DriveProof stores only hashes, timestamps, signer identities and milestone state on Solana. This creates a compact, auditable timeline without publishing sensitive paperwork.

Funds release only according to the agreed milestone rules. For higher-value deals, optional neutral inspectors or logistics partners can serve as attesters for specific milestones rather than becoming custodians of the whole transaction.

## Why Solana is necessary

A normal database can store a deal record, but it cannot give mutually distrustful parties a neutral settlement layer.

Solana adds three properties that materially change the product:

- **Programmable escrow:** funds can be released according to transparent milestone logic rather than by one marketplace operator.
- **Shared provenance:** buyer, seller, transporter and inspector can all verify the same transaction state without trusting one party's private database.
- **Low-cost attestations:** VIN-linked document hashes and milestone receipts can be recorded cheaply enough to use throughout the deal instead of only at final settlement.

The blockchain is not used to store car photos, PDFs or personal data. It is used only where neutrality, ordering and settlement matter.

## User flow

1. **Create deal** — seller enters VIN, price, currency, expiry date and milestone template.
2. **Invite buyer** — buyer reviews the exact settlement conditions before funding.
3. **Attach evidence** — inspection and vehicle documents are uploaded; their hashes are anchored to the deal.
4. **Fund escrow** — buyer funds the transaction using supported stablecoin settlement.
5. **Pickup attestation** — transporter or seller confirms pickup and signs the milestone.
6. **Delivery attestation** — buyer confirms delivery or the predefined inspection window expires.
7. **Release** — escrow releases funds according to the agreed rules and a final transaction receipt is created.
8. **Dispute path** — contested deals pause automatically and move to the dispute mechanism chosen at deal creation.

## MVP for the Colosseum Hackathon

The first version can be deliberately narrow and shippable:

- Solana program for one-car / one-buyer milestone escrow;
- stablecoin-denominated deal amount;
- wallet-based signatures for buyer, seller and optional inspector/transporter;
- VIN-based deal ID;
- off-chain document upload with on-chain SHA-256 hash commitments;
- three milestones: funded → picked up → delivered;
- configurable buyer inspection window;
- web dashboard showing deal state, evidence hashes and signatures;
- downloadable final transaction receipt.

No token is required.

## Initial market

The wedge is professional and semi-professional cross-border used-car trade inside Europe, where a single transaction can involve thousands of euros and several independent parties.

The first users are not consumers browsing inventory. They are dealers, vehicle sourcing agents, exporters, transporters and repeat buyers who already coordinate deals through WhatsApp, email and bank transfers.

DriveProof can initially charge a small fixed transaction fee or basis-point fee only when escrow is used. Inspection and logistics partners can later offer paid attestations inside the workflow.

## Why this can become a startup

The long-term asset is not the escrow contract itself. It is the **portable vehicle transaction graph** created across repeated deals: VIN-linked ownership events, inspection attestations, transport handovers and settlement receipts.

Over time, that can support:

- dealer-to-dealer trade;
- vehicle sourcing networks;
- export/import workflows;
- warranty and inspection products;
- financing based on verified transaction history;
- APIs for marketplaces that want a neutral settlement layer without becoming custodians.

## Competitive advantage

Existing car marketplaces optimize discovery. Payment providers optimize money movement. Vehicle-history products optimize historical records. DriveProof connects the three risk points of an actual cross-border transaction: **money, evidence and handover**.

The product is intentionally not a generic "put cars on blockchain" concept. The chain is invisible to the normal user and only secures the parts where neither side should have unilateral control.

## Key risks and how to handle them

**Garbage-in evidence:** a hash proves a document was not changed after submission, not that the document is true. Mitigation: allow trusted inspectors, dealers and logistics partners to sign specific attestations.

**Disputes:** not every delivery problem can be solved by code. Mitigation: every deal chooses its dispute policy before funding; the smart contract freezes instead of guessing when a contested condition occurs.

**Privacy / GDPR:** vehicle and identity documents must not be public. Mitigation: encrypted off-chain storage, minimal on-chain metadata and document hashes only.

**Stablecoin / regulatory constraints:** the MVP should avoid acting as an exchange or lender and use non-custodial smart-contract escrow with clear jurisdictional review before production launch.

## Success metric

The MVP succeeds if two parties who do not know each other can complete a simulated cross-border vehicle purchase and independently verify:

- what they agreed to;
- which evidence was submitted and when;
- who confirmed pickup and delivery;
- why and when settlement was released.

That is the core promise of DriveProof: **a cross-border car deal with fewer trust assumptions, without putting the car itself "on-chain."**
