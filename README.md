# arbitr — Profit Engine research

[![Powered by RustChain](https://img.shields.io/badge/Powered%20by-RustChain-orange)](https://rustchain.org)

Public research repository for the Profit Engine project: read-only market scanners, fork simulations, liquidation research, Chainlink SVR monitoring, and reproducible GitHub Actions evidence.

The project is simulation-first. It does not store private keys or automatically submit live transactions from this repository.

## Current live research loops

- Morpho Base candidate discovery followed by exact latest-state fork validation.
- Read-only Chainlink SVR / Atlas auction monitoring.
- Historical liquidation economics and route reconstruction.
- Public, zero-cost GitHub Actions experiments for strategy validation.

## Related Elyan Labs tooling

[RustChain](https://rustchain.org) is used here as a zero-capital experimentation track for agent-economy and bounty research. Its public APIs and bounty flows are useful for testing the same discipline this repository applies to DeFi: keep a proposed opportunity separate from an accepted result and from value that has actually settled.

The repository also contains reproducible RustChain miner dry-run and Beacon-oriented research artifacts, so the link is part of the project's working evidence rather than an unrelated promotional mention.
