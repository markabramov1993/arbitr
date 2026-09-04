# RustChain Security Assessment — Bounty #398 Step 1

**Scope:** architecture reading only. No production exploitation was performed.  
**Target:** RustChain current public repository, with emphasis on attestation, hardware fingerprinting, RIP-200 epoch rewards, and one concrete hardening vector.  
**Author:** markabramov1993 / Profit Engine research.

## 1. Attestation flow

RustChain’s mining model does not rely only on a wallet address and a claimed CPU name. The Linux miner collects machine information and runs a set of hardware-fingerprint checks before the normal mining lifecycle. In the current miner, the preflight path runs the fingerprint suite, records whether the overall fingerprint passed, and then describes the next real steps as `attest -> enroll -> mine loop`.

The signing path is important. The miner attempts to attach an Ed25519 signature and public key to the attestation payload when its crypto module is available. The source describes canonical-JSON signing for the full attestation payload and later uses the same key relationship when building enrollment data. The purpose is to bind the attestation to a cryptographic identity rather than treating hardware claims as anonymous JSON.

The challenge/attestation boundary should therefore be thought of as two checks layered together: cryptographic ownership and physical-machine plausibility. A valid signing key is not enough to prove that a machine is genuine vintage hardware; a plausible fingerprint without a strong wallet binding is also not enough to establish who is entitled to the resulting mining identity. The security property comes from combining both.

## 2. Hardware fingerprinting and VM-farm resistance

The public fingerprint implementation documents six primary behavioral checks in the active Linux flow: oscillator/clock drift, cache timing, SIMD identity, thermal drift/entropy, instruction-path jitter, and anti-emulation behavior. A ROM fingerprint is also documented for retro-platform paths where it is relevant.

The design goal is not simply to detect a `hypervisor` string. Several checks measure behavior that should be harder to reproduce consistently in a large virtual-machine farm. Cache latency relationships, timing variance, thermal behavior, and microarchitectural jitter provide independent signals. The current Linux miner combines these checks into an overall fingerprint result and explicitly reports the failed checks. In a real CI dry-run I ran against the public code, five behavioral checks passed on a GitHub-hosted AMD EPYC virtual machine while `anti_emulation` failed, causing the overall fingerprint to fail. That is useful evidence that the system is not merely trusting the CPU model string.

This is still a defense-in-depth system, not a mathematical proof that emulation is impossible. Individual timing measurements can be noisy, hardware can sit behind unusual virtualization layers, and attackers can attempt to imitate distributions. The security value comes from requiring multiple independently meaningful signals, maintaining history, and correlating suspicious clusters rather than treating one timing number as a permanent identity.

## 3. RIP-200 epoch rewards

The public reward implementation exposes `settle_epoch_rip200()` and describes settlement using RIP-200 time-aged multipliers. The broader protocol model is “one unique hardware device gets one participation identity/vote,” while hardware antiquity changes reward weight. Reward eligibility therefore depends on more than possessing RTC or presenting raw compute power.

The settlement layer also integrates anti-double-mining logic. This is a critical separation of concerns: attestation decides whether the hardware identity is credible enough to participate, while settlement determines which enrolled/eligible identities receive the finite epoch reward and at what weight. A robust implementation must keep settlement atomic, prevent the same hardware identity from being counted multiple times, and ensure all nodes derive equivalent eligibility and reward results from equivalent chain state.

From a security perspective, reward code is consensus-adjacent even if it is implemented around a database. A small discrepancy in eligibility, multiplier activation, or settlement idempotency can become monetary divergence. The repository’s existing hardening work around anti-double-mining and settlement races is therefore appropriately treated as security-critical rather than as ordinary accounting code.

## 4. Attack vector / hardening focus: fail-open signature compatibility

The clearest risk I would keep at the top of the threat model is **fail-open compatibility around attestation/enrollment signatures**. The current Linux miner source explicitly catches signing errors and can fall through to an unsigned attestation path; it also comments that the server may accept unsigned compatibility traffic with warnings. Enrollment signing is similarly described as best-effort in the client.

That compatibility behavior is understandable during protocol migration, but it weakens the clean security story. If a network wants the wallet-to-hardware binding to be an authentication property, the invariant should eventually become: a reward-eligible attestation must carry a valid signature from the key bound to that miner identity, and enrollment must be bound to the same identity and epoch. Otherwise the physical fingerprint layer can be strong while the ownership layer remains softer than intended.

I am not claiming a new live exploit here. This is a design-level attack surface visible in the public client and should be validated against the current server policy. The safer direction is fail-closed activation: define an activation epoch/version after which missing/invalid signatures cannot receive reward-eligible status, make the activation consensus-visible, and keep compatibility only for explicitly non-rewarding telemetry if legacy clients still need an observation path.

## 5. Security conclusions

RustChain’s unusual security strength is that it combines standard cryptographic identity with measurements tied to physical machines. That raises the cost of Sybil farming compared with a system that accepts self-reported hardware. Its corresponding complexity is that security now spans several layers: signature correctness, fingerprint quality, historical clustering, enrollment, epoch eligibility, multiplier policy, and settlement atomicity.

The most important engineering principle is therefore **fail closed at reward boundaries**. No single heuristic needs to be perfect if uncertain identities are prevented from receiving normal reward weight until the required authentication and fingerprint conditions are satisfied. Conversely, a compatibility shortcut at the reward boundary can undermine several strong fingerprint checks upstream.

## Sources

- RustChain repository: https://github.com/Scottcjn/Rustchain
- Linux miner: https://github.com/Scottcjn/Rustchain/blob/main/miners/linux/rustchain_linux_miner.py
- Fingerprint checks: https://github.com/Scottcjn/Rustchain/blob/main/miners/linux/fingerprint_checks.py
- RIP-200 rewards: https://github.com/Scottcjn/Rustchain/blob/main/node/rewards_implementation_rip200.py
- Anti-double-mining: https://github.com/Scottcjn/Rustchain/blob/main/node/anti_double_mining.py
- Bounty #398: https://github.com/Scottcjn/rustchain-bounties/issues/398

## Validation note

The CI dry-run referenced above used the current public miner in safe `--dry-run --show-payload --verbose` mode on a GitHub-hosted Ubuntu 24.04 AMD EPYC runner. It did not mine, enroll, submit a production attestation, or modify RustChain state.