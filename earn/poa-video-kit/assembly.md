# Assembly Map — Proof of Antiquity Type B

Target master: 16:9, 1920×1080, ~4:00. The editor should use the exact narration in `script.md` and the capture directions in `storyboard.md`.

| Time | Script section | Visual / capture | On-screen anchor |
|---|---|---|---|
| 0:00–0:25 | Hook | Split-screen modern rig vs old PowerPC, then PoW/PoS/PoA three-column graphic | `Fastest hardware? Biggest stake? Or oldest verified machine?` |
| 0:25–0:55 | One CPU = one vote | `RIP-200 → unique hardware → one vote per epoch`; VM icons collapse into one physical host | `Sybil question: ten machines, or ten VMs?` |
| 0:55–1:10 | Fingerprint checks | Six labeled tiles, one per check | Clock / Cache / SIMD / Thermal / Jitter / Anti-emu |
| 1:10–1:40 | Reproduced VM result | Crop real GitHub Actions output from run `33838143501`; show the five PASS lines, anti-emulation FAIL, and Microsoft hypervisor fact | `Real Azure/GitHub Actions dry-run` |
| 1:40–2:20 | Antiquity weighting | Hardware timeline using pinned current values | `Modern x86_64 0.8× · M1 1.2× · G4 2.5×` |
| 2:20–2:55 | Limits / red-team | VM-farm → checks → rejected/penalized flow; no “unbreakable” language | `Resistance must be tested continuously` |
| 2:55–3:25 | Safe first step | Terminal capture of clone + Linux miner dry-run command; then read-only `/health` result | `--dry-run --show-payload` |
| 3:25–4:00 | Close | Return to PoW/PoS/PoA comparison, then old machine/end card | `The machine itself becomes part of identity` |

## Asset plan

- `thumbnail.png` — primary: current multiplier contrast + VM/fingerprint hook.
- `thumbnail-alt-1.png` — anti-emulation / real VM result angle.
- `thumbnail-alt-2.png` — “1 CPU = 1 vote” / Proof of Antiquity angle.
- All thumbnail art is original programmatic typography/geometry; no third-party photos or logos are embedded.
- Real terminal material must come from the cited public GitHub Actions run or a fresh rerun of the same public test.

## Edit rules

- Do not invent benchmark, token-price, earnings, emissions, or environmental numbers.
- Keep current multiplier values synchronized with `SOURCES.md`; the 2026-09-10 review pass uses RustChain commit `e805b5ff18f515a7f315807b75b39ed1c5eca972`.
- Never imply that the fingerprint makes spoofing impossible.
- Large subtitles and terminal zoom for mobile readability.
- Music, if added by the publisher, must be original or properly licensed; no music is required by this package.

## Validation

The package is designed so a human publisher can assemble the video without needing unstated project context: narration, shot timing, source map, metadata, three thumbnail options, and exact evidence locations are all included.
