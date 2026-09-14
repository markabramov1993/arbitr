# Sources and claim map

All claims in this package are grounded in the public RustChain repository.

## Primary protocol source
`Scottcjn/Rustchain/docs/PROTOCOL.md`
https://github.com/Scottcjn/Rustchain/blob/main/docs/PROTOCOL.md

The protocol explicitly lists six core hardware-fingerprint checks:
1. clock drift / oscillator variance
2. cache timing characteristics
3. SIMD identity and timing
4. thermal entropy / load response
5. instruction-path jitter
6. anti-emulation heuristics

The same section explains the rationale used in the narration: VMs tend to have cleaner, more deterministic timing; emulators may flatten cache and thermal behavior; physical hardware shows small imperfections from silicon, aging, and heat; the stated goal is to make spoofing expensive and brittle rather than claim perfect certainty.

## Implementation source
`Scottcjn/Rustchain/miners/linux/fingerprint_checks.py`
https://github.com/Scottcjn/Rustchain/blob/main/miners/linux/fingerprint_checks.py

The implementation includes the six named checks and records `vm_detected` when the fingerprint fails validation.

## Claim-by-claim map
- “does not trust a model name alone” → protocol hardware-fingerprinting section describes behavioral verification and multiple agreeing signals.
- “six hardware-behavior checks” → protocol section 4.1.
- list of all six checks → protocol section 4.1 and Linux implementation.
- “VMs tend to look cleaner and more deterministic” → protocol section 4.2.
- “emulators can flatten cache and thermal behavior” → protocol section 4.2.
- “physical silicon is messier: heat, aging, oscillator variation” → protocol section 4.2 plus the clock-drift/thermal checks named in 4.1.
- “goal is ... make spoofing ... expensive and brittle” → protocol section 4.2, paraphrased conservatively.

No external benchmark, token-price, profitability, or performance claim is used in this package.
