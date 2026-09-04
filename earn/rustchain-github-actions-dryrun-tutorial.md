# RustChain Miner Dry-Run in GitHub Actions: What the Hardware Fingerprint Actually Detects

This tutorial shows how to run the current RustChain Linux miner in **dry-run mode** on a clean GitHub Actions runner, record the hardware-fingerprint result, and verify the public node health endpoint without starting mining or modifying RustChain network state.

The useful part is not the marketing claim that virtual machines are penalized. The useful part is that we can reproduce the check on an ordinary hosted CI machine and inspect which checks pass and which one fails.

## What we tested

On 2026-09-04 I ran the current `Scottcjn/Rustchain` Linux miner from commit:

`7c5cb6f5a228c70b82742d86d5f5e304473ee0b9`

The test ran on a standard GitHub-hosted Ubuntu runner:

- Ubuntu 24.04.4 LTS
- Python 3.12.3
- x86_64
- AMD EPYC 7763 reported by the VM
- 4 vCPUs
- Microsoft hypervisor detected by `lscpu`

The exact command was:

```bash
cd Rustchain/miners/linux
python3 rustchain_linux_miner.py --dry-run --show-payload --verbose
```

The miner explicitly states in dry-run mode that it does not begin the real mining loop. The current source passes `persist_key=not args.dry_run`, so a dry-run uses an ephemeral identity instead of persisting the normal miner key.

## Reproducible GitHub Actions workflow

A minimal workflow looks like this:

```yaml
name: RustChain miner dry-run
on: workflow_dispatch

jobs:
  dry-run:
    runs-on: ubuntu-24.04
    steps:
      - name: Clone RustChain
        run: git clone --depth 1 https://github.com/Scottcjn/Rustchain.git

      - name: Install miner dependencies
        run: |
          python3 -m pip install requests pynacl cryptography

      - name: Run exact dry-run
        run: |
          cd Rustchain/miners/linux
          python3 rustchain_linux_miner.py --dry-run --show-payload --verbose
```

No RTC wallet balance is required for this test and the command does not enter the `attest -> enroll -> mine` loop.

## The result: five checks passed, anti-emulation failed

The run produced the following six hardware fingerprint results:

```text
[1/6] Clock-Skew & Oscillator Drift... PASS
[2/6] Cache Timing Fingerprint...      PASS
[3/6] SIMD Unit Identity...            PASS
[4/6] Thermal Drift Entropy...         PASS
[5/6] Instruction Path Jitter...       PASS
[6/6] Anti-Emulation Checks...         FAIL

OVERALL RESULT: FAILED
Failed checks: ['anti_emulation']
```

That is a useful test because the machine really was virtualized. The runner's `lscpu` output reported:

```text
Hypervisor vendor: Microsoft
Virtualization type: full
```

So the anti-emulation failure is consistent with the host environment rather than being an arbitrary failure on a physical desktop.

## Why the first five checks can still pass inside a VM

A common misunderstanding is that every timing-oriented fingerprint check must fail in a virtual machine. That is not how the current implementation behaves.

The current fingerprint module tests several different signals. A hosted VM still executes on real silicon, so timing variation, cache behavior and instruction jitter can produce values that satisfy individual checks. The decisive distinction in this run was the dedicated anti-emulation stage.

That separation is useful operationally: one noisy signal does not have to carry the entire physical-machine decision.

## Node connectivity was also verified

The dry-run performs a read-only health probe. Our run reached:

`https://rustchain.org/health`

and received HTTP 200 with node version:

```text
2.2.1-rip200
```

The response also reported `ok: true` and `db_rw: true` at the time of the test.

This matters because a local hardware test and a live endpoint smoke test are two separate things. A fingerprint implementation can work locally while the node is unreachable; conversely, an HTTP 200 does not prove the local attestation logic is valid. The dry-run gives us both signals without enrolling a miner.

## What this test does *not* prove

It does not prove that RustChain's hardware identity system is impossible to spoof. It also does not prove that every VM will fail exactly the same check. Hardware attestation is adversarial by nature, and a serious evaluation would include multiple hypervisors, containers, bare-metal hosts and vintage systems.

It does prove something narrower and reproducible: on a GitHub-hosted Azure VM, the current miner successfully identified the environment as failing the overall fingerprint because of its anti-emulation check while the other five checks passed.

## Useful next experiments

A good compatibility matrix would repeat the exact same workflow or command on:

1. a bare-metal modern x86 PC;
2. a consumer laptop under WSL2;
3. Docker on bare metal;
4. KVM/QEMU;
5. a pre-2010 physical machine;
6. PowerPC hardware where the ROM-specific path is relevant.

The important rule is to record both the environment and the raw pass/fail output instead of assuming a result in advance.

## Source references

- RustChain repository: https://github.com/Scottcjn/Rustchain
- Linux miner: `miners/linux/rustchain_linux_miner.py`
- Fingerprint checks: `miners/linux/fingerprint_checks.py`
- Public node health: https://rustchain.org/health
- Test evidence workflow run: https://github.com/markabramov1993/arbitr/actions/runs/33838143501

## Bottom line

RustChain's dry-run is useful as a genuine preflight tool. It can exercise the hardware fingerprint, expose the detected environment, and probe the live node before a user commits to running a miner. In our reproduced CI test, a real hosted VM passed five lower-level signal checks but was rejected by the dedicated anti-emulation stage — exactly the kind of result a preflight should make visible.