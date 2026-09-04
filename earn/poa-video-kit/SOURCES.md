# SOURCES

Every factual claim in this package is grounded in public source material.

## Consensus / one CPU = one vote
- RustChain whitepaper: https://github.com/Scottcjn/Rustchain/blob/main/docs/WHITEPAPER.md
- Main README / Proof-of-Antiquity overview: https://github.com/Scottcjn/Rustchain/blob/main/README.md

## Hardware fingerprint checks
- Linux fingerprint implementation: https://github.com/Scottcjn/Rustchain/blob/main/miners/linux/fingerprint_checks.py
- Linux miner dry-run and anti-emulation reporting: https://github.com/Scottcjn/Rustchain/blob/main/miners/linux/rustchain_linux_miner.py

## Antiquity multipliers
- Main README hardware multiplier table: https://github.com/Scottcjn/Rustchain/blob/main/README.md

## Reproduced VM evidence
- Public GitHub Actions run: https://github.com/markabramov1993/arbitr/actions/runs/33838143501
- Source revision recorded by the run: `7c5cb6f5a228c70b82742d86d5f5e304473ee0b9`
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