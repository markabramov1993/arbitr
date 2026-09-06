# Second Life Viewer — Autobuild replacement

## Phase 0 proposal: dependency map + Conan 2 `llcommon` proof of concept

**RFP:** `secondlife/viewer#4390`  
**Proposer:** `markabramov1993`  
**Contact:** `leadspodzakaz@gmail.com`  
**Proposal date:** 2026-09-06

## Executive summary

I propose a deliberately narrow first milestone before committing Linden Lab or a contributor to a full build-system migration.

The current Viewer tree already contains an optional Conan integration in `indra/CMakeLists.txt` (`include(conanbuildinfo ...)`, `USE_CONAN`, `NO_AUTOBUILD_3P`), but it is an older integration style and the repository remains substantially coupled to Autobuild through `autobuild.xml`, `indra/cmake/FindAutobuild.cmake`, `indra/cmake/Prebuilt.cmake`, `indra/cmake/Variables.cmake`, `build.sh`, package-reporting scripts, and individual dependency modules that reference `AUTOBUILD_INSTALL_DIR` or `use_prebuilt_binary()`.

That makes a flag-day replacement unnecessarily risky. My recommendation is to validate a **parallel Conan 2 lane** first, using modern `CMakeToolchain` / `CMakeDeps`, while the existing Autobuild lane remains intact.

The Phase 0 success criterion is intentionally concrete: **build `indra/llcommon` without relying on Autobuild to supply the migrated third-party dependency set**, prove the approach in CI, measure it, and produce the dependency/risk map needed to price and schedule the full Viewer migration responsibly.

## Why Conan 2 is the lead candidate

I would evaluate both Conan 2 and vcpkg in the written comparison, but start the PoC with Conan 2 because the Viewer has several characteristics that favor an explicit recipe/profile model:

- Windows + macOS are first-class, while Linux and arm64 need to remain easy for downstream viewers.
- Third-party viewers need to override or substitute dependencies without forking a centralized package manifest beyond recognition.
- Some dependencies may need project-specific patches, build options, or binary packaging rather than a stock registry recipe.
- Conan profiles and lockfiles provide an explicit place to encode compiler/runtime/architecture settings and make dependency resolution reproducible.
- `CMakeToolchain` and `CMakeDeps` let CMake consume imported targets without preserving the legacy Autobuild installation-directory model.
- A staged Conan lane can coexist with Autobuild while dependencies are moved one at a time.

vcpkg remains a viable alternative and will be scored against the same criteria, especially Windows developer experience, manifest mode, overlays, binary caching, arm64 triplets, and CI maintenance.

## Phase 0 deliverables

### 1. Autobuild coupling and dependency inventory

A machine-readable + human-readable map covering at minimum:

- packages declared/configured by `autobuild.xml`;
- CMake files using `use_prebuilt_binary()`;
- consumers of `AUTOBUILD_INSTALL_DIR`, `ARCH_PREBUILT_DIRS*`, and Autobuild environment variables;
- dependencies needed to configure/build `indra/llcommon`;
- packages that are straightforward registry dependencies vs. packages requiring a custom recipe/overlay, patch, generated asset, proprietary artifact, or special runtime packaging.

Output: `docs/dependency-migration-inventory.md` plus a CSV/JSON inventory suitable for tracking the later migration.

### 2. Conan 2 proof-of-concept lane for `indra/llcommon`

A focused branch/PR containing only what is required for the PoC, such as:

- Conan 2 manifest/recipe;
- project profiles or documented profile generation;
- `CMakeToolchain` / `CMakeDeps` integration;
- CMake preset(s) or an equally simple configure command;
- the minimum CMake adjustments required for `llcommon` to consume proper imported targets;
- no deletion of the existing Autobuild path in Phase 0.

The target user experience should be close to:

```text
conan install ... --build=missing
cmake --preset <platform-preset>
cmake --build --preset <platform-preset> --target llcommon
```

with exact commands documented and reproducible.

### 3. CI proof

Add a bounded PoC workflow that demonstrates the new dependency lane on:

- Windows;
- macOS;
- Linux smoke validation where the current tree permits it without broad unrelated platform work.

The CI evidence will capture tool versions, dependency resolution, configure result, and `llcommon` build result. Code signing remains outside the dependency resolver: the proposal will document where signing credentials/artifacts enter the later packaging pipeline so the migration does not weaken that boundary.

### 4. Before/after comparison

Record, for the PoC scope:

- clean dependency-setup time;
- warm/cached dependency-setup time;
- configure + `llcommon` build time;
- downloaded/cached dependency footprint;
- number of manual environment/setup steps;
- platform-specific exceptions discovered.

The purpose is not to manufacture a benchmark win; it is to expose the actual migration cost and operational tradeoffs.

### 5. Full-migration plan and risk register

The final Phase 0 report will split the remaining work into migration waves, for example:

1. leaf libraries with clean upstream packages;
2. libraries requiring Viewer-specific options/patches;
3. generated/data dependencies currently treated like Autobuild packages;
4. platform-specialized/proprietary dependencies;
5. packaging, signing, symbols, and CI release integration;
6. removal of legacy Autobuild glue only after parallel-build parity exists.

For each wave: affected modules, blockers, rollback strategy, testing gate, and rough effort range.

## Third-party Viewer / downstream requirement

The migration design will preserve downstream flexibility. The Phase 0 report will explicitly demonstrate how a TPV can:

- override a package version;
- use an alternate recipe/package source;
- apply a downstream patch;
- point one dependency at a local editable checkout;
- keep the rest of the locked dependency graph unchanged.

This is treated as an acceptance criterion, not an optional documentation note.

## Non-goals for Phase 0

- removing Autobuild from the whole Viewer;
- changing unrelated Viewer behavior;
- rewriting packaging/signing infrastructure before dependency parity is proven;
- claiming Linux upstream support is solved by the dependency-manager PoC alone;
- committing to a full-migration fixed price before the high-risk dependency inventory exists.

## Bid

**Fixed price for Phase 0: USD 750.**

**Schedule:** 5 business days from confirmed kickoff and repository/workflow access needed for the PoC.

**Payment:** on acceptance of the Phase 0 deliverables above. No upfront payment requested.

A full Viewer migration would be proposed and priced separately from the measured Phase 0 results rather than guessed in advance.

## Acceptance for this milestone

Phase 0 is complete when Linden Lab has:

1. the dependency/autobuild coupling inventory;
2. a reviewable Conan 2 PoC for `indra/llcommon`;
3. reproducible CI evidence for the agreed platform matrix;
4. before/after measurements;
5. Conan-vs-vcpkg tradeoff analysis;
6. a staged full-migration plan with risks and rollback gates;
7. documented downstream/TPV override workflow.

If the PoC shows Conan 2 is a worse fit than vcpkg on measured criteria, the report will say so and recommend vcpkg instead. The milestone is successful if it produces a defensible migration decision and working evidence, not if it forces a predetermined package manager.

## Verification note

This proposal was prepared after inspecting the current public Viewer tree rather than only the RFP text. In particular, the audit verified the existing optional Conan path and multiple active Autobuild coupling points in CMake/build scripts. Any implementation work will continue with the same source-backed, reproducible approach.
