# Storyboard — Beacon Liveness Short

Format: 9:16 vertical, 1080×1920, ≤60 seconds.

1. **0–4s** — Black terminal screen. Large caption: “Can an AI agent prove it’s still alive?” Cursor types `beacon identity new`.
2. **4–12s** — Split-screen: left shows terminal identity creation; right shows a simple key icon labeled “local private identity”. No private material displayed.
3. **12–22s** — Terminal types `beacon daemon`. Animate a pulse traveling from a laptop icon to a node labeled “Beacon Atlas”.
4. **22–34s** — Show a sanitized JSON record with fields `agent_id`, `name`, `status: active`. Zoom onto `status`.
5. **34–46s** — Show a GitHub Actions YAML card with `curl` against the Atlas endpoint. Overlay: “read-only monitor / no wallet key”.
6. **46–55s** — Show command: `beacon udp send ... --reward-rtc 0.1`. Overlay: “signed metadata ≠ token transfer”.
7. **55–60s** — Final three-word stack: “IDENTITY / LIVENESS / MESSAGES”. Small footer: `github.com/Scottcjn/beacon-skill`.

Visual rules: terminal green-on-black, simple network lines, no fabricated dashboard screenshots, no wallet/private-key material, no price claims.