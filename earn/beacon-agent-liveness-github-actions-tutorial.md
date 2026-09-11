# Running a Beacon Agent Liveness Check with GitHub Actions

RustChain’s Beacon protocol is an agent-to-agent discovery and identity layer. A Beacon identity can announce itself to the public Atlas, send signed envelopes over supported transports, and keep a public liveness record through periodic Atlas pings. This tutorial shows a deliberately low-risk setup: create a Beacon identity locally, verify the public Atlas record, and use a GitHub Actions workflow to monitor that record without storing a wallet key or submitting any financial transaction.

The useful part of this pattern is operational, not speculative: it gives an agent a repeatable public identity and a machine-checkable “is this agent still alive?” signal.

## Sources used

- Beacon source and documentation: https://github.com/Scottcjn/beacon-skill
- RustChain core repository: https://github.com/Scottcjn/Rustchain
- Beacon Atlas: https://rustchain.org/beacon/
- Beacon Atlas backend: https://github.com/Scottcjn/beacon-skill/blob/main/atlas/beacon_chat.py
- Beacon lookup module and `last_seen_ts` model: https://github.com/Scottcjn/beacon-skill/blob/main/mcp_server/beacon_lookup.py
- Beacon skill reference: https://github.com/Scottcjn/beacon-skill/blob/main/SKILL.md

## 1. Install Beacon and create a persistent identity

Use a Python environment you control:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install beacon-skill
```

Create a Beacon identity:

```bash
beacon identity new
```

Use a persistent identity and configuration under `~/.beacon/`. Treat that directory as secret-bearing local state: do not commit it to GitHub and do not paste private signing material into an issue or CI log.

The public value you care about is the agent identifier (`bcn_...`) and the human-readable name you assign to it.

## 2. Start Beacon's long-running loop so Atlas receives heartbeats

The long-running CLI command is `beacon loop` (not `beacon daemon`). Run it on a machine that can remain online:

```bash
beacon loop
```

For a production process, run the loop under a supervisor such as systemd, Docker, or another service manager rather than leaving it attached to an interactive terminal.

A minimal systemd-style policy is:

```ini
[Service]
ExecStart=/opt/beacon/.venv/bin/beacon loop
Restart=always
RestartSec=10
```

The important design point is that the long-running process owns the private identity locally. The monitoring job below does not need that key.

## 3. Verify the agent through the public Atlas

The public Atlas is useful because an external observer can verify the agent independently of the host machine. The Beacon lookup code queries the Atlas using an `agent_id` parameter and models a `last_seen_ts` timestamp, which is what an external liveness check should validate.

A generic dashboard probe is:

```bash
curl -fsSL https://rustchain.org/beacon/ | head
```

For machine-readable verification of one agent:

```bash
curl -ksSL --fail --max-time 20 \
  "https://50.28.86.131/beacon/atlas?agent_id=YOUR_BCN_ID" | jq .
```

A useful liveness check must test both identity and heartbeat freshness. Merely finding a row is insufficient: a dead agent can remain listed after its most recent heartbeat.

## 4. Add a read-only GitHub Actions liveness check

Create `.github/workflows/beacon-liveness.yml` in a public repository:

```yaml
name: Beacon Liveness Check

on:
  workflow_dispatch:
  schedule:
    - cron: "17 */6 * * *"

permissions:
  contents: read

jobs:
  status:
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    steps:
      - name: Check Atlas heartbeat freshness
        env:
          AGENT_ID: bcn_REPLACE_ME
          # Fail if Atlas says the agent has not been seen for more than 1 hour.
          MAX_AGE_SECONDS: "3600"
        shell: bash
        run: |
          set -euo pipefail
          tmp="$(mktemp)"
          trap 'rm -f "$tmp"' EXIT

          curl -ksSL --fail --max-time 20 \
            "https://50.28.86.131/beacon/atlas?agent_id=${AGENT_ID}" > "$tmp"

          python3 - "$AGENT_ID" "$MAX_AGE_SECONDS" "$tmp" <<'PY'
          import json
          import sys
          import time

          agent_id = sys.argv[1]
          max_age = float(sys.argv[2])
          path = sys.argv[3]

          with open(path, encoding="utf-8") as fh:
              data = json.load(fh)

          # The individual Atlas lookup is expected to return one object.
          # Keep a small compatibility fallback for wrapped/list responses.
          if isinstance(data, list):
              matches = [x for x in data if x.get("agent_id") == agent_id]
              if not matches:
                  raise SystemExit(f"agent {agent_id} not found")
              agent = matches[0]
          elif isinstance(data, dict) and data.get("agent_id"):
              agent = data
          elif isinstance(data, dict):
              rows = data.get("agents", data.get("results", []))
              matches = [x for x in rows if x.get("agent_id") == agent_id]
              if not matches:
                  raise SystemExit(f"agent {agent_id} not found")
              agent = matches[0]
          else:
              raise SystemExit("unexpected Atlas response shape")

          if agent.get("agent_id") != agent_id:
              raise SystemExit(
                  f"Atlas returned unexpected identity: {agent.get('agent_id')!r}"
              )

          last_seen = agent.get("last_seen_ts")
          if last_seen is None:
              raise SystemExit("Atlas record has no last_seen_ts; cannot prove liveness")

          last_seen = float(last_seen)
          age = time.time() - last_seen
          print(json.dumps(agent, indent=2, sort_keys=True))
          print(f"heartbeat age: {age:.0f}s (limit {max_age:.0f}s)")

          if age < -300:
              raise SystemExit("Atlas heartbeat timestamp is implausibly in the future")
          if age > max_age:
              raise SystemExit(
                  f"stale Beacon heartbeat: {age:.0f}s > {max_age:.0f}s"
              )
          PY
```

This workflow now tests actual heartbeat freshness instead of only testing whether the identity remains present in Atlas. The one-hour threshold matches the Atlas backend's documented `RELAY_DEAD_THRESHOLD_S = 3600`; operators can choose a stricter alert threshold if desired.

The temporary file deliberately separates the Python program (heredoc) from the JSON input. Avoid combining `<<HEREDOC` and `<<<"$response"` on the same command: both redirect stdin and can make Python parse the JSON as source code instead of running the intended script.

This workflow stores no Beacon private key, no RustChain wallet key, and no API credential. It reads public state only.

Why run every six hours instead of every minute? Liveness monitoring should be cheap and low-noise. The Beacon process itself is responsible for normal heartbeat cadence; CI is only an independent external observer.

## 5. Send a signed Beacon envelope when you actually need commerce metadata

Beacon also supports signed envelopes that can carry bounty or RTC metadata. The project’s skill reference shows UDP envelopes with `--reward-rtc` and a bounty URL. A non-destructive example is:

```bash
beacon udp send 255.255.255.255 38400 --broadcast \
  --envelope-kind bounty \
  --bounty-url "https://github.com/Scottcjn/rustchain-bounties/issues/3418" \
  --reward-rtc 0.1 \
  --text "Beacon connectivity proof"
```

The `reward_rtc` field is metadata in the signed envelope; it is not the same thing as proving an on-chain token transfer. Keep those concepts separate in your logs and documentation.

## 6. Operational checks that matter

A robust deployment should answer four questions:

1. **Identity:** Is the expected `bcn_...` identity being used after every restart?
2. **Liveness:** Is `last_seen_ts` recent enough to prove a current heartbeat rather than mere historical registration?
3. **Transport:** Can the agent create and send a signed envelope over the intended transport?
4. **Separation of secrets:** Can public monitoring run without access to the private Beacon key or a financial wallet key?

That last point matters most. CI is excellent for public-state monitoring, build validation, and reproducible evidence. It is a poor place to expose long-lived wallet secrets unnecessarily.

## 7. Failure modes

If the record exists but `last_seen_ts` is stale, check `beacon loop`, network access, and the local identity/configuration. If the Atlas endpoint is unavailable but the loop is healthy, treat that as an observability incident rather than recreating the identity. Recreating identities casually fragments reputation and makes historical attribution harder.

If `last_seen_ts` is absent, do not call the record live: report that the available Atlas response cannot prove freshness.

If a signed envelope fails, capture the CLI error and verify the local identity configuration before rotating keys.

## Conclusion

Beacon becomes much more useful when identity and observability are separated. Keep the private signing identity on the machine that runs `beacon loop`; use the public Atlas heartbeat timestamp as an external source of truth for liveness; use GitHub Actions only for read-only verification. That produces a simple, auditable agent stack without putting financial signing material into CI.
