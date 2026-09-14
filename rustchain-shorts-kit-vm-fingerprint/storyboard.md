# Storyboard — 9:16 vertical, 55–60s

## Production rules
- Canvas: 1080×1920, 30 fps.
- Use only repository/terminal captures and original text/diagram overlays.
- Keep code readable: crop tightly; highlight only the relevant identifier.
- Burn captions for the full narration.

## Shot list

### 0:00–0:04 — Hook
Visual: split-screen silhouette: “VM” on left, “old physical PC” on right. Large text: **CAN A VM FAKE THIS?**
Motion: quick 8-frame glitch only on VM side.

### 0:04–0:12 — Six checks, not a model string
Visual: screen capture of `docs/PROTOCOL.md`, scrolling into “The six core checks”.
Overlay: **6 signals must agree**.

### 0:12–0:30 — Check stack
Visual: six cards appear one every ~3 seconds:
1. Clock drift
2. Cache timing
3. SIMD identity/timing
4. Thermal entropy
5. Instruction-path jitter
6. Anti-emulation
Background: blurred capture of `miners/linux/fingerprint_checks.py`.

### 0:30–0:43 — Physical vs virtual behavior
Visual: two simple line traces. VM trace: smooth/repeating. Physical trace: lightly irregular.
On-screen labels: **more deterministic** / **physical imperfections**.
Small footer: “Conceptual illustration — not benchmark data.”

### 0:43–0:54 — Defense-in-depth
Visual: six circles converge into one “trusted fingerprint” node. Then show one fake signal turning red while the others remain independent.
Overlay: **Spoof several independent signals at once**.

### 0:54–0:59 — CTA
Visual: GitHub paths typed into a terminal-style card:
`docs/PROTOCOL.md`
`miners/linux/fingerprint_checks.py`
Final text: **Inspect the checks yourself → github.com/Scottcjn/Rustchain**

## Editor notes
- Do not claim the checks are impossible to spoof; use the protocol's wording: the aim is to make spoofing expensive and brittle.
- Do not show invented reward multipliers or profitability figures.
- The smooth-vs-irregular timing traces are explanatory graphics, not measured data; label them accordingly.
