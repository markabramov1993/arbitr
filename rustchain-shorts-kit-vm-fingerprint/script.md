# Script — “Can a VM Fake Old Hardware?”

**Target duration:** 55–60 seconds

**0:00–0:04 — Hook**
Can a virtual machine pretend to be a twenty-year-old computer and mine RustChain like the real thing?

**0:04–0:12**
RustChain does not trust a model name alone. Its protocol describes six hardware-behavior checks that have to agree.

**0:12–0:30**
It looks at clock drift, cache timing, SIMD behavior, thermal response, instruction-path jitter, and anti-emulation signals.

**0:30–0:43**
Why combine them? Virtual machines tend to look cleaner and more deterministic. Emulators can flatten cache and thermal behavior. Physical silicon is messier: heat, aging, and oscillator variation leave small fingerprints.

**0:43–0:54**
So the goal is not magical certainty. It is to make spoofing several independent physical signals at once expensive and brittle.

**0:54–0:59 — CTA**
Want to inspect the checks yourself? Open RustChain's `docs/PROTOCOL.md` and the Linux fingerprint implementation on GitHub.
