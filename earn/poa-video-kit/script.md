# Video Script — Proof of Antiquity: Why RustChain Rewards Old Hardware

**Target duration:** ~4 minutes

## 0:00–0:25 — Hook

Most crypto networks reward either the fastest hardware or the largest capital base. RustChain tries something different: it treats the physical identity and age of a machine as part of consensus. Its core idea is called **Proof of Antiquity** — one unique physical CPU gets one vote, and verified older hardware can receive a higher reward weight.

## 0:25–0:55 — What “1 CPU = 1 vote” means

RustChain's public whitepaper describes RIP-200 as a deterministic system where each unique hardware device receives one vote per epoch instead of letting hash power decide the voting weight. That changes the scarce resource. Buying ten times more hash rate is not supposed to give one physical CPU ten independent identities.

The obvious problem is Sybil resistance: how does a network know that ten claimed machines are not ten virtual machines on one server?

## 0:55–1:40 — The hardware fingerprint

The current RustChain miner runs six main fingerprint checks:

1. clock-skew and oscillator drift,
2. cache timing,
3. SIMD identity,
4. thermal drift entropy,
5. instruction-path jitter,
6. anti-emulation detection.

These signals are not identical proofs. They are independent clues about the physical substrate. The project also has ROM-specific checks for some retro platforms.

A useful detail is that the miner can run these checks in dry-run mode before mining. On a GitHub-hosted Azure VM that we tested, the first five checks passed but the dedicated anti-emulation check failed. The runner itself reported a Microsoft hypervisor. The miner therefore marked the overall fingerprint as failed.

That is a much more interesting result than simply saying “VMs are banned”: individual timing signals can look plausible in a VM, so a separate virtualization check matters.

## 1:40–2:20 — Why older machines get a multiplier

RustChain's public README lists higher multipliers for several vintage architectures. A PowerPC G4 is shown at 2.5x, while modern x86_64 is the 1.0x baseline. The network's thesis is that keeping working older computers alive should be economically rewarded instead of treating them as obsolete by default.

The multiplier changes the reward weight; it does not magically make an old CPU faster. A G4 still cannot compete with a modern GPU for raw compute. RustChain is valuing verified scarcity and preservation, not throughput.

## 2:20–2:55 — What this does not prove

Proof of Antiquity should not be presented as impossible to spoof. Hardware attestation is adversarial. The correct question is whether faking many independent old physical identities is expensive enough that real hardware remains the cheaper path.

The project itself has security tests, anti-emulation logic, timing checks and ongoing bounty programs because this assumption has to be attacked continuously.

## 2:55–3:25 — How to try it safely

The easiest first step is not to mine. It is to run the miner in dry-run mode:

```bash
pip install clawrtc
```

or clone the RustChain repository and run the Linux miner with:

```bash
python3 rustchain_linux_miner.py --dry-run --show-payload
```

The dry-run prints detected hardware and fingerprint status, then performs a read-only health probe. It does not enter the normal attest, enroll and mining loop.

## 3:25–4:00 — Closing

Proof of Work asks: how much computation can you buy? Proof of Stake asks: how much stake can you lock? RustChain's Proof of Antiquity asks a stranger question: can a network assign value to the fact that a real machine has physically existed, aged, and remained useful?

That idea is experimental, and the anti-Sybil problem is the part worth watching. But it is also what makes RustChain technically distinct: the machine itself is part of the identity model, not just a replaceable source of compute.

**End card:** RustChain — github.com/Scottcjn/Rustchain