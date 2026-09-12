---
title: "Monitor a Beacon Agent from GitHub Actions Without Putting Its Private Key in CI"
published: false
description: "A read-only pattern for monitoring a Beacon agent's public Atlas liveness from GitHub Actions while keeping identity and wallet secrets off the runner."
tags: aiagents, githubactions, security, rustchain
---

# Monitor a Beacon Agent from GitHub Actions Without Putting Its Private Key in CI

Agent systems need two things that are easy to mix up: **identity** and **observability**.

The machine running an agent may need a persistent private identity so it can sign messages. A monitoring system, on the other hand, should need as little authority as possible. If all you want to know is whether an agent is still announcing itself publicly, putting its private key—or a financial wallet key—into CI is unnecessary risk.

This tutorial shows a low-privilege pattern for Beacon: keep the private identity on the agent host, let the Beacon daemon maintain the public Atlas record, and use GitHub Actions only as a read-only outside observer.

Beacon source:

https://github.com/Scottcjn/beacon-skill

## 1. Create the identity on the machine that owns it

Install Beacon in an environment you control:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install beacon-skill
```

Create a persistent identity:

```bash
beacon identity new
```

Beacon's public documentation uses this command to create an Ed25519-backed agent identity. The identity data under the local Beacon configuration is secret-bearing state. Do not commit the private material to GitHub and do not paste it into Actions logs.

The values you can safely use for public monitoring are the public agent identifier (`bcn_...`) and the display name.

## 2. Let the daemon maintain liveness

Beacon's Atlas Ping implementation documents auto-registration and periodic liveness pings. Run the daemon on the actual host that owns the identity:

```bash
beacon daemon
```

The relevant source is:

https://github.com/Scottcjn/beacon-skill/blob/main/beacon_skill/atlas_ping.py

The implementation sends a registration or heartbeat to the Atlas relay. For a new registration it can sign the agent ID with the local identity; later heartbeats can use the relay token returned by the server.

That is the important separation: **the agent host proves identity; the monitor only reads the public result.**

For a persistent deployment, run the daemon under a service manager rather than an interactive shell. For example, the policy might look like:

```ini
[Service]
ExecStart=/opt/beacon/.venv/bin/beacon daemon
Restart=always
RestartSec=10
```

The exact service path is environment-specific, but the privilege model is the same.

## 3. Verify the public Atlas separately

An outside observer should not need the agent's private key to answer “is this public identity still present?”

Beacon's public Atlas is linked from the project documentation:

https://rustchain.org/beacon/

A simple human check is to open the Atlas and find the agent ID. For automation, use the machine-readable Atlas surface supported by the current deployment and search for the expected `agent_id`.

The monitor should distinguish at least three cases:

- the target agent is present;
- the target agent is missing;
- the Atlas endpoint itself is unavailable.

Those are not the same incident. Recreating the identity because a monitoring endpoint had a temporary outage would fragment the agent's history for no good reason.

## 4. Use GitHub Actions as a read-only observer

A minimal external monitor can run on a schedule and parse public JSON without any identity or wallet secret.

Example workflow:

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
      - name: Check public Atlas record
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
          matches = [row for row in rows if row.get("agent_id") == agent_id]

          if not matches:
              print(f"agent {agent_id} not found")
              raise SystemExit(2)

          agent = matches[0]
          print(json.dumps(agent, indent=2, sort_keys=True))

          status = str(agent.get("status", "unknown")).lower()
          if status not in {"active", "online", "alive", "unknown"}:
              print(f"warning: reported status={status}")
          PY
```

The point is not the exact polling interval. The point is what the workflow **does not have**:

- no Beacon private identity key;
- no RustChain wallet key;
- no financial signing capability;
- no permission to rotate the agent identity.

Its job is evidence collection, not authority.

## 5. Signed commerce metadata is a different operation

Beacon also supports signed envelopes carrying metadata such as a bounty URL and `reward_rtc`. The public skill documentation shows commands such as:

```bash
beacon udp send 255.255.255.255 38400 --broadcast \
  --envelope-kind bounty \
  --bounty-url "https://github.com/Scottcjn/rustchain-bounties/issues/3418" \
  --reward-rtc 0.1
```

This matters for auditability, but `reward_rtc` in an envelope should not be confused with proof that an RTC token transfer settled.

A signed message can prove who authored the message and what metadata it carried. A payment requires separate settlement evidence.

That distinction is useful far beyond Beacon: **proposed value, accepted value, and actually settled value should be separate states.**

## 6. Operational checks worth keeping

A useful Beacon deployment can answer four independent questions:

### Identity
Is the same expected `bcn_...` identity present after restarts?

### Liveness
Does the public Atlas continue to receive/reflect the agent's heartbeats?

### Transport
Can the agent create and send a signed message over the transport you actually use?

### Secret separation
Can your monitoring stack prove public liveness without access to the private Beacon identity or financial wallet keys?

If the last answer is “no,” the monitoring system probably has more privilege than it needs.

## 7. Failure handling

If the agent disappears from the Atlas:

1. check whether the daemon is still running;
2. check network connectivity from the agent host;
3. check whether the public Atlas endpoint itself is reachable;
4. only then inspect the local identity configuration.

Do not casually create a new identity as a troubleshooting step. A new identity can break continuity with the agent's previous public history.

If a signed-envelope command fails, preserve the error output and verify the local configuration before rotating credentials.

## Why this pattern is useful

CI systems are excellent at:

- scheduled public-state checks;
- reproducible logs;
- simple alerting;
- low-privilege verification.

They are a poor place to put long-lived signing material unless there is a real need for CI to sign.

For liveness, there is no such need. The agent host can keep identity authority; GitHub Actions can remain an outside observer.

## Sources and evidence

- Beacon repository: https://github.com/Scottcjn/beacon-skill
- Atlas heartbeat implementation: https://github.com/Scottcjn/beacon-skill/blob/main/beacon_skill/atlas_ping.py
- Beacon skill reference: https://github.com/Scottcjn/beacon-skill/blob/main/SKILL.md
- RustChain repository: https://github.com/Scottcjn/Rustchain
- Original public tutorial source: https://github.com/markabramov1993/arbitr/blob/main/earn/beacon-agent-liveness-github-actions-tutorial.md

## Bottom line

The safest monitoring architecture is boring in a good way: **keep the private identity on the machine that needs to sign, publish only the public liveness signal, and let CI read that signal without gaining signing power.**

That makes the agent easier to monitor without turning the monitoring system into another secret-bearing production host.

---

*Disclosure: this article is based on public Beacon source/documentation and a reproducible read-only monitoring design. It does not claim that signed bounty metadata is itself a payment, and it does not require exposing private keys in CI.*
