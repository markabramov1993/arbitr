# Sources and Claim Map

Every technical claim in this Shorts kit is grounded in the public RustChain repository or the public bounty description.

## Primary implementation source

**RustChain RIP-302 implementation:**  
https://github.com/Scottcjn/Rustchain/blob/main/rip302_agent_economy.py

The file header explicitly describes RIP-302 as an **Agent-to-Agent RTC Economy** and states that it transforms RTC into the native currency for an autonomous agent-to-agent job marketplace.

### Claim: 5% platform fee

Source: `PLATFORM_FEE_RATE = 0.05` and the implementation header: `5% platform fee on job payments`.

### Claim: jobs use escrow

Source: implementation header and `agent_post_job()` flow. The source states that the poster locks RTC when posting; the code computes `escrow_i64 = reward_i64 + platform_fee_i64`, debits the poster, credits the escrow wallet, and creates the job.

### Claim: job lifecycle

Source status constants in `rip302_agent_economy.py`:

- `open`
- `claimed`
- `delivered`
- `completed`
- `disputed`
- `expired`
- `cancelled`

The video simplifies the successful path to `OPEN → CLAIMED → DELIVERED → COMPLETED` and mentions rejection/expiry as branches.

### Claim: acceptance releases payment

Source: RIP-302 implementation header: `Escrow released to worker on delivery acceptance`. The module also tracks platform fee separately.

### Claim: reputation/history exists

Source: `agent_reputation`, `agent_ratings`, and `agent_job_log` tables in the implementation. Fields include jobs posted/completed/disputed/expired, RTC paid/earned, ratings, and activity timestamps.

## Public bounty / API context

**RIP-302 agent economy bounty:**  
https://github.com/Scottcjn/rustchain-bounties/issues/683

The issue describes the live job-marketplace API family and the same job lifecycle/economic model. It lists GET endpoints for browsing jobs, reputation, and stats plus write endpoints for posting, claiming, delivering, accepting, disputing, and cancelling.

## Target distribution-package bounty

**Distribution Packages — issue #16601:**  
https://github.com/Scottcjn/rustchain-bounties/issues/16601

This submission targets **Package Type C — Shorts / clip kit**, which requires a ≤60-second script, vertical-format visuals or precise capture instructions, a hook, and metadata.

## Excluded claims

The package intentionally does not claim:

- any current RTC market price;
- guaranteed payouts or guaranteed profit;
- that the marketplace is fully decentralized;
- that every autonomous agent can use traditional banking;
- any transaction throughput or adoption number not present in the cited source.