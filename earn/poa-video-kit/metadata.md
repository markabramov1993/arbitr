# Metadata

## Primary title
Proof of Antiquity: Why RustChain Rewards Old Computers

## Alternate titles
1. A Blockchain Where a 2003 PowerPC Can Earn More Than Modern x86
2. How RustChain Tries to Detect Real Hardware Instead of VM Farms

## Description
RustChain is an experimental blockchain built around Proof of Antiquity: one verified physical machine receives one vote per epoch, while older verified hardware can receive a larger reward weight.

This video explains the current six-check fingerprinting model, shows a reproduced GitHub Actions dry-run where a hosted VM fails the anti-emulation check, and separates reward weighting from raw compute performance.

Sources and reproducible test material:
- https://github.com/Scottcjn/Rustchain
- https://github.com/markabramov1993/arbitr/actions/runs/33838143501

Try the safe preflight first:
`python3 rustchain_linux_miner.py --dry-run --show-payload`

## Tags
RustChain, Proof of Antiquity, DePIN, vintage computing, PowerPC, hardware attestation, anti emulation, blockchain, crypto mining, e-waste, AI agents

## Chapters
00:00 Three consensus questions
00:25 One CPU = one vote
00:55 Six hardware fingerprint checks
01:10 Real VM dry-run result
01:40 Antiquity multipliers
02:20 Limitations and adversarial testing
02:55 Safe dry-run setup
03:25 What makes Proof of Antiquity different