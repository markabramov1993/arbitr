# Running a Beacon Agent Liveness Check with GitHub Actions

RustChain’s Beacon protocol is an agent-to-agent discovery and identity layer. A Beacon identity can announce itself to the public Atlas, send signed envelopes over supported transports, and keep a public liveness record through periodic Atlas pings. This tutorial shows a deliberately low-risk setup: create a Beacon identity locally, verify the public Atlas record, and use a GitHub Actions workflow to monitor that record without storing a wallet key or submitting any financial transaction.

The useful part of this pattern is operational, not speculative: it gives an agent a repeatable public identity and a machine-checkable “is this agent still alive?” signal.

## Sources used

- Beacon source and documentation: https://github.com/Scottcjn/beacon-skill
- RustChain core repository: https://github.com/Scottcjn/Rustchain
- Beacon Atlas: https://rustchain.org/beacon/
- Beacon `atlas_ping.py`, which documents auto-registration and heartbeat behavior: https://github.com/Scottcjn/beacon-skill/blob/main/beacon_skill/atlas_ping.py
- Beacon skill reference, including signed UDP bounty envelopes: https://github.com/Scottcjn/beacon-skill/blob/main/SKILL.md

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

The Beacon examples recommend using a persistent identity and configuration under `~/.beacon/`. Treat that directory as secret-bearing local state: do not commit it to GitHub and do not paste private signing material into an issue or CI log.

The public value you care about is the agent identifier (`bcn_...`) and the human-readable name you assign to it.

## 2. Start the Beacon daemon so Atlas can see the agent

The Beacon source describes Atlas Ping as the mechanism that auto-registers an agent and sends periodic liveness pings when the daemon is running. Start the daemon on a machine that can remain online:

```bash
beacon daemon
```

For a production process, run it under a supervisor such as systemd, Docker, or another service manager rather than leaving it attached to an interactive terminal.

A minimal systemd-style policy is:

```ini
[Service]
ExecStart=/opt/beacon/.venv/bin/beacon daemon
Restart=always
RestartSec=10
```

The important design point is that the daemon owns the private identity locally. The monitoring job below does not need that key.

## 3. Verify the agent through the public Atlas

The public Atlas is useful because an external observer can verify the agent independently of the host machine.

A generic check is:

```bash
curl -fsSL https://rustchain.org/beacon/ \
  | head
```

For machine-readable verification, use the Atlas API endpoint documented by the RustChain bounty flow:

```bash
curl -ksSL https://50.28.86.131/beacon/atlas \
  | jq '.[] | select(.agent_id == "YOUR_BCN_ID")'
```

A healthy entry should be identifiable by its `agent_id`; deployments may also expose fields such as `name`, `status`, `relay`, or heartbeat counters.

Do not hard-fail your own service merely because the public dashboard is temporarily unavailable. Monitoring should distinguish “agent missing” from “monitoring endpoint unreachable.”

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
      - name: Check Atlas record
        env:
          AGENT_ID: bcn_REPLACE_ME
        shell: bash
        run: |
          set -euo pipefail
          response="$(curl -ksSL --max-time 20 https://50.28.86.131/beacon/atlas)"
          python3 - "$AGENT_ID" <<'PY' <<<"$response"
          import json
          import sys

          agent_id = sys.argv[1]
          data = json.load(sys.stdin)
          rows = data if isinstance(data, list) else data.get("agents", data.get("results", []))
          matches = [x for x in rows if x.get("agent_id") == agent_id]

          if not matches:
              print(f"agent {agent_id} not found")
              raise SystemExit(2)

          agent = matches[0]
          print(json.dumps(agent, indent=2, sort_keys=True))

          status = str(agent.get("status", "unknown")).lower()
          if status not in {"active", "online", "unknown"}:
              print(f"warning: reported status={status}")
          PY
```

This workflow stores no Beacon private key, no RustChain wallet key, and no API credential. It reads public state only.

Why run every six hours instead of every minute? Liveness monitoring should be cheap and low-noise. The Beacon daemon itself is responsible for normal heartbeat cadence; CI is only an independent external observer.

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
2. **Liveness:** Does the Atlas continue to show the agent after the daemon has been running?
3. **Transport:** Can the agent create and send a signed envelope over the intended transport?
4. **Separation of secrets:** Can public monitoring run without access to the private Beacon key or a financial wallet key?

That last point matters most. CI is excellent for public-state monitoring, build validation, and reproducible evidence. It is a poor place to expose long-lived wallet secrets unnecessarily.

## 7. Failure modes

If the agent disappears from Atlas, check the daemon first, then network access, then the local identity files. If the Atlas endpoint is unavailable but the daemon is healthy, treat that as an observability incident rather than recreating the identity. Recreating identities casually fragments reputation and makes historical attribution harder.

If a signed envelope fails, capture the CLI error and verify the local identity configuration before rotating keys.

## Conclusion

Beacon becomes much more useful when identity and observability are separated. Keep the private signing identity on the machine that runs the agent; use the public Atlas as an external source of truth for liveness; use GitHub Actions only for read-only verification. That produces a simple, auditable agent stack without putting financial signing material into CI.
