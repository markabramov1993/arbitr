# Storyboard — Proof of Antiquity

## Shot 1 — 0:00–0:10
Split-screen: modern mining rig on the left, old PowerPC desktop on the right. On-screen text: `Fastest hardware? Biggest stake? Or oldest verified machine?`

## Shot 2 — 0:10–0:25
Simple three-column graphic: PoW = hash power, PoS = stake, PoA = verified physical machine + antiquity. Keep the labels factual and neutral.

## Shot 3 — 0:25–0:45
Terminal-style animation showing: `RIP-200 → unique hardware → one vote per epoch`. Then show ten VM icons collapsing into one physical server silhouette to illustrate the Sybil question.

## Shot 4 — 0:45–1:10
Six tiles appear one by one:
- Clock drift
- Cache timing
- SIMD identity
- Thermal drift
- Instruction jitter
- Anti-emulation

Use oscilloscope/timing-style visual language rather than fake semiconductor imagery.

## Shot 5 — 1:10–1:35
Show a real terminal capture from the GitHub Actions dry-run. Highlight five PASS lines and the final `Anti-Emulation Checks... FAIL`. Beside it show the runner fact: `Hypervisor vendor: Microsoft`.

## Shot 6 — 1:35–2:00
Hardware timeline: modern x86 at 1.0x, Apple Silicon M1 at 1.2x, PowerPC G4 at 2.5x. Add text: `Reward weight ≠ compute speed`.

## Shot 7 — 2:00–2:20
Old laptop stays powered on while a recycling/e-waste pile fades into the background. Do not claim measured environmental savings unless a sourced number is shown.

## Shot 8 — 2:20–2:50
Adversarial section. Red-team style diagram: VM farm → fingerprint checks → rejected/penalized path. Caption: `Experimental system: resistance must be tested continuously.`

## Shot 9 — 2:50–3:20
Screen recording of terminal commands:

```bash
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain/miners/linux
python3 rustchain_linux_miner.py --dry-run --show-payload
```

Then show the read-only `/health` response and `version: 2.2.1-rip200` from the reproduced run.

## Shot 10 — 3:20–4:00
Return to the three consensus models. Final visual focuses on the old computer with label: `The machine itself becomes part of identity.` End card with RustChain GitHub URL.

## Capture notes
- Use only repository screenshots/terminal captures produced from the public code or generated diagrams.
- Avoid price predictions, guaranteed-profit language, or claims that spoofing is impossible.
- 16:9 master, 1080p preferred.
- Large subtitles; keep terminal text zoomed enough to read on mobile.