# SOURCES

Every factual claim in this package is grounded in public source material.

## Source revision used for the final review pass
- RustChain main rechecked on 2026-09-10 at commit `e805b5ff18f515a7f315807b75b39ed1c5eca972`.
- Current README: https://github.com/Scottcjn/Rustchain/blob/e805b5ff18f515a7f315807b75b39ed1c5eca972/README.md
- Current whitepaper: https://github.com/Scottcjn/Rustchain/blob/e805b5ff18f515a7f315807b75b39ed1c5eca972/docs/WHITEPAPER.md

## Consensus / one CPU = one vote
- RustChain whitepaper: https://github.com/Scottcjn/Rustchain/blob/e805b5ff18f515a7f315807b75b39ed1c5eca972/docs/WHITEPAPER.md
- Main README / Proof-of-Antiquity overview: https://github.com/Scottcjn/Rustchain/blob/e805b5ff18f515a7f315807b75b39ed1c5eca972/README.md

## Hardware fingerprint checks
- Linux fingerprint implementation: https://github.com/Scottcjn/Rustchain/blob/e805b5ff18f515a7f315807b75b39ed1c5eca972/miners/linux/fingerprint_checks.py
- Linux miner dry-run and anti-emulation reporting: https://github.com/Scottcjn/Rustchain/blob/e805b5ff18f515a7f315807b75b39ed1c5eca972/miners/linux/rustchain_linux_miner.py

## Antiquity multipliers
At the pinned revision, both the main README and whitepaper list:
- PowerPC G4: `2.5x`
- Apple Silicon M1: `1.2x`
- Modern x86_64: `0.8x`

Some older secondary docs in the repository still contain historical `1.0x` modern-x86 examples. The package deliberately uses the current README/whitepaper value rather than those stale secondary examples.

## Reproduced VM evidence
- Public GitHub Actions run: https://github.com/markabramov1993/arbitr/actions/runs/33838143501
- Source revision recorded by that run: `7c5cb6f5a228c70b82742d86d5f5e304473ee0b9`
- Environment observed in the run: Ubuntu 24.04.4, Python 3.12.3, AMD EPYC 7763, Microsoft hypervisor.
- Observed fingerprint result: clock drift PASS, cache timing PASS, SIMD identity PASS, thermal drift PASS, instruction jitter PASS, anti-emulation FAIL.

## Public node
- Health endpoint: https://rustchain.org/health
- Reproduced run returned HTTP 200 and version `2.2.1-rip200` at test time.

## Accuracy constraints used in the script
- No claim that spoofing is impossible.
- No profit guarantee or token-price prediction.
- No environmental savings number is used unless explicitly sourced.
- Reward multiplier is described as reward weight, not compute-speed acceleration.
- Historical source drift is called out rather than silently mixing old and current multiplier tables.
