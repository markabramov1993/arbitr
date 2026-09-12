---
title: "RustChain Miner Dry-Run in GitHub Actions: What the Hardware Fingerprint Actually Detects"
published: false
description: "A reproducible, no-mining GitHub Actions test of RustChain's hardware fingerprint on a hosted Azure VM, including the exact dry-run output and what it does—and does not—prove."
tags: rustchain, githubactions, security, devops
---

# RustChain Miner Dry-Run in GitHub Actions: What the Hardware Fingerprint Actually Detects

I wanted to answer a narrow, practical question: **what does the current RustChain miner actually report when its hardware fingerprint runs inside a normal hosted CI virtual machine?**

Instead of assuming the answer from documentation, I ran the miner in its own dry-run mode on a clean GitHub Actions runner and kept the test deliberately non-destructive: no real mining loop, no wallet funding, and no attempt to bypass the fingerprint.

The result was useful because it was not simply “VM = every test fails.” Five lower-level checks passed. The dedicated anti-emulation check failed, and the overall fingerprint was rejected.

## Environment

The run used a standard GitHub-hosted Ubuntu runner:

- Ubuntu 24.04 LTS
- x86_64
- AMD EPYC 7763 reported to the guest
- 4 vCPUs
- Microsoft hypervisor reported by `lscpu`

The RustChain source revision used for the original evidence run was:

```text
7c5cb6f5a228c70b82742d86d5f5e304473ee0b9
```

The public source repository is:

https://github.com/Scottcjn/Rustchain

## The exact dry-run command

After cloning the repository and installing the miner's Python dependencies, I ran:

```bash
cd Rustchain/miners/linux
python3 rustchain_linux_miner.py --dry-run --show-payload --verbose
```

The important part is `--dry-run`. The current miner has an explicit preflight mode so you can exercise the local fingerprint and inspect its payload without entering the normal attest/enroll/mine loop.

A minimal GitHub Actions workflow is:

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
        run: python3 -m pip install requests pynacl cryptography

      - name: Run dry-run
        run: |
          cd Rustchain/miners/linux
          python3 rustchain_linux_miner.py --dry-run --show-payload --verbose
```

This is a good CI task because it produces reproducible evidence without needing a funded RTC wallet.

## What the fingerprint reported

The run produced this summary:

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

That is consistent with the host environment. The runner also reported:

```text
Hypervisor vendor: Microsoft
Virtualization type: full
```

So the anti-emulation failure was not an abstract test case: the machine really was running under a hypervisor.

## Why can five checks pass inside a VM?

Because these checks measure different signals.

A virtual machine still executes on physical silicon. Timing variation, cache behavior, SIMD behavior, thermal/noise proxies, and instruction-path jitter can all produce values that satisfy individual heuristics. It would be a mistake to assume that virtualization must force every low-level measurement to fail.

The interesting part of this run was therefore the **composition** of the checks. Five signals were individually acceptable, but the dedicated anti-emulation stage detected the environment and the overall result failed.

That is a healthier design than pretending one timing measurement alone can reliably distinguish every physical host from every virtualized environment.

## The live node smoke test is a separate signal

The dry-run also performed a read-only health check against the public RustChain node and received HTTP 200 during the original evidence run.

That matters because “the local fingerprint code ran” and “the public node is reachable” are different facts. A local test can pass while a node is unavailable, and an HTTP 200 does not prove the hardware fingerprint is valid.

For automation, I prefer to record those as separate checks rather than collapsing them into one green/red result.

## What this does *not* prove

This test does **not** prove that RustChain's hardware identity is impossible to spoof. It does not prove that every hypervisor will fail the same stage. It does not test an adversarially modified guest or a custom virtualization stack.

It proves something much narrower and reproducible:

> On the tested GitHub-hosted Azure VM, the current miner completed its dry-run, five fingerprint subchecks passed, the anti-emulation stage failed, and the overall fingerprint was rejected.

That is exactly the sort of evidence a preflight mode should make visible.

## Useful next experiments

A meaningful compatibility matrix would repeat the same command and preserve raw output across:

1. bare-metal modern x86;
2. WSL2;
3. Docker on bare metal;
4. KVM/QEMU;
5. VMware or VirtualBox;
6. pre-2010 physical hardware;
7. PowerPC where RustChain's vintage-hardware paths are especially relevant.

The important rule is to record the environment and the raw pass/fail output instead of deciding the expected result first and then looking for confirmation.

## Reproducibility evidence

The original public tutorial and workflow evidence are preserved here:

- Tutorial source: https://github.com/markabramov1993/arbitr/blob/main/earn/rustchain-github-actions-dryrun-tutorial.md
- Evidence workflow run: https://github.com/markabramov1993/arbitr/actions/runs/33838143501
- RustChain source: https://github.com/Scottcjn/Rustchain

## Bottom line

RustChain's dry-run is useful as a genuine preflight tool: it exposes what the machine reports, what the fingerprint accepted or rejected, and whether the public node was reachable, without requiring a user to start real mining.

The most valuable lesson from this run is not “VMs fail.” It is that **multiple hardware signals can look plausible inside a VM, so explicit anti-emulation logic and transparent raw evidence matter.**

---

*Disclosure: this article was prepared from an actually executed GitHub Actions dry-run and public source review. It contains no claim of guaranteed mining income, investment return, or universal anti-VM resistance.*
