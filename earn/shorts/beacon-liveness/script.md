# Beacon Liveness — 60s Shorts Script

**Hook (0–4s)**
“An AI agent can prove it is still alive — without exposing its private key.”

**4–12s**
Show terminal: `beacon identity new`.
Narration: “Beacon gives the agent a persistent cryptographic identity.”

**12–22s**
Show `beacon daemon` and a highlighted `bcn_...` id.
Narration: “The daemon announces that identity to the public Beacon Atlas and keeps it active with periodic pings.”

**22–34s**
Show a public Atlas JSON record with `agent_id`, `name`, and `status`.
Narration: “Now an external observer can check the public record instead of trusting the machine itself.”

**34–46s**
Show a GitHub Actions YAML snippet using `curl` to read the Atlas endpoint.
Narration: “GitHub Actions can monitor that liveness using only public data — no wallet key and no Beacon signing key in CI.”

**46–55s**
Show a signed Beacon envelope command with `--reward-rtc 0.1`.
Narration: “Beacon envelopes can also carry RTC bounty metadata, but metadata is not the same as an on-chain transfer.”

**55–60s**
On-screen CTA: “Beacon = identity + public liveness + signed agent messages.”
Narration: “That separation makes the agent easier to audit.”
