# Sources and claim mapping

All technical claims in this package are grounded in the public `Scottcjn/Rustchain` repository.

## 1. “One physical CPU, one vote”
Source: `docs/PROTOCOL_v1.1.md`
Public repository text states that RIP-200 replaces hash power with hardware identity and that the core principle is **1 CPU = 1 Vote**, weighted by hardware antiquity.

Also supported by `docs/PROTOCOL.md`, which states:
- 1 CPU = 1 vote for baseline participation
- hardware antiquity changes reward weight
- attestation proves the machine is real enough to participate

## 2. Hardware attestation / fingerprinting
Source: `specs/RIP_POA_SPEC_v1.0.md`
The spec describes a hardware fingerprint attestation protocol intended to bind participation to distinct physical CPUs and resist emulator / VM-based Sybil attacks.

Source: `docs/whitepaper/hardware-fingerprinting.md`
The hardware-fingerprinting documentation describes rewarding real physical hardware while discounting or rejecting virtualized environments that can scale without corresponding physical cost.

## 3. Antiquity-weighted rewards
Source: `node/rip_200_round_robin_1cpu1vote.py`
The implementation comments describe rewards as weighted by a time-decaying antiquity multiplier.

Source: `specs/RIP_POA_SPEC_v1.0.md`
The spec states that vintage and exotic hardware can receive time-decaying reward multipliers / antiquity bonuses.

## 4. VM resistance
Source: `MANIFESTO.md`
The project explains the emulation/Sybil threat model and the requirement that attestations pass hardware fingerprint checks.

Source: `devlog/DEVELOPMENT_LOG.md`
The development log records a Proxmox VM being correctly detected and receiving a dramatically discounted reward, providing a concrete public example of VM detection behavior.

## 5. No invented multiplier or token-price claims
This Shorts package deliberately avoids quoting a specific antiquity multiplier or RTC market price because those values can vary by hardware class or market state. The storyboard instructs the publisher to show only repository-backed qualitative reward-weight behavior unless a current measured value is captured directly from the source at production time.

Repository: https://github.com/Scottcjn/Rustchain
Bounty: https://github.com/Scottcjn/rustchain-bounties/issues/16601
