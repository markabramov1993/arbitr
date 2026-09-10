# RustChain #398 — Step 2: Reproduce Known Fix — Mock Signature Mode

Contributor: `markabramov1993`  
RTC wallet: `RTC7558d7acadad7a32a710459a4c16c0fc1c56f43d`  
Target quest: `Scottcjn/rustchain-bounties#398`  
Known vulnerability selected: **Mock Signature Mode**

This is a local/source-level reproduction of a known, already-fixed vulnerability. I did **not** probe or attempt to bypass a production RustChain node.

## 1. What the attack looked like before the fix

RustChain's older signed-header ingest implementation kept a testnet compatibility path next to the real Ed25519 verifier. In the historical/deprecated node source, `TESTNET_ALLOW_MOCK_SIG` could be controlled from the environment (`RC_TESTNET_ALLOW_MOCK_SIG`). When enabled, `/headers/ingest_signed` had a mock-acceptance branch that set the header to accepted when the supplied signature matched the test pattern (including an all-zero 128-hex-character signature), instead of reaching `VerifyKey.verify()`.

The dangerous condition was therefore operational rather than a break of Ed25519 itself:

1. a production-like node starts with the test flag enabled;
2. a caller submits a syntactically valid signed-header payload;
3. the mock-signature branch accepts a test signature without proving possession of the miner's private key;
4. downstream header-continuity/state logic now processes a header whose authenticity was never cryptographically established.

Historical evidence still present in the repository:

- `deprecated/old_nodes/rustchain_v2_active.py` defines `TESTNET_ALLOW_MOCK_SIG` from `RC_TESTNET_ALLOW_MOCK_SIG`;
- the historical ingest branch contains the mock acceptance condition before the real Ed25519 verification path;
- the repository keeps those sources under `deprecated/`, which is useful for understanding the original failure mode without touching production.

The security property at risk is simple: a route named `ingest_signed` must not allow a runtime configuration mistake to turn "signed" into "has a signature-shaped string".

## 2. What the current fix does

I rechecked current RustChain `main` at commit:

`883c18ad50778657ed386d55b2284220ebff7707`

The current code uses multiple independent controls.

### A. Production defaults are hard-disabled

`node/ed25519_config.py` now contains:

```python
TESTNET_ALLOW_INLINE_PUBKEY = False
TESTNET_ALLOW_MOCK_SIG = False
```

The integrated node also defines both test-only flags as `False` by default. This removes the old "environment variable silently enables the dangerous branch" default/configuration pattern from the normal production configuration.

### B. There is an explicit runtime fail-closed guard

`node/rustchain_v2_integrated_v2.2.1_rip200.py` defines `enforce_mock_signature_runtime_guard()`. It resolves the runtime from `RC_RUNTIME_ENV` / `RUSTCHAIN_ENV` (defaulting to production) and raises `RuntimeError` if `TESTNET_ALLOW_MOCK_SIG` is true outside the explicit non-production set:

`test`, `testing`, `dev`, `development`, `local`, `testnet`.

This is stronger than relying only on a default. A future edit or test fixture that flips the module flag in a production runtime is supposed to stop startup rather than silently weaken signature verification.

### C. The production WSGI entry point calls the guard before initialization

`node/wsgi.py` loads the integrated node and immediately calls:

```python
rustchain_main.enforce_mock_signature_runtime_guard()
rustchain_main.enforce_hardware_binding_runtime_guard()
```

Only after those checks does WSGI expose the Flask app and call `init_db()`.

That ordering matters: the safety check is a startup invariant, not merely a warning emitted after the service has already initialized.

### D. The behavior has focused regression tests

`node/tests/test_mock_signature_guard.py` currently covers three important cases:

1. `TESTNET_ALLOW_MOCK_SIG = True` + production runtime -> raises;
2. mock signatures enabled in an explicit test runtime -> allowed;
3. WSGI startup calls the guard before database initialization.

## 3. Independent reproduction performed for this submission

I added a disposable GitHub Actions reproduction in my public `arbitr` repository. It clones the current RustChain repository, records the exact upstream head, checks the fail-closed flags and WSGI guard, then runs the upstream focused regression tests.

Workflow:

`https://github.com/markabramov1993/arbitr/actions/runs/34531744614`

Observed output:

```text
RUSTCHAIN_HEAD=883c18ad50778657ed386d55b2284220ebff7707
26:TESTNET_ALLOW_INLINE_PUBKEY = False
27:TESTNET_ALLOW_MOCK_SIG = False
25:rustchain_main.enforce_mock_signature_runtime_guard()
...                                                                      [100%]
3 passed in 1.06s
```

The workflow completed successfully. It was source/local CI validation only; no production state-changing request was made.

## 4. Why the fix is sufficient for the known vulnerability

For the vulnerability described by the quest, the current defense is sufficient under the documented production startup path because it combines two different safety layers:

- **safe default:** mock signature mode is off;
- **fail-closed startup invariant:** if the flag is somehow turned on in a production runtime, WSGI refuses to continue.

This directly addresses the original failure mode: a test-only signature bypass cannot be enabled by an ordinary production environment setting and remain unnoticed during normal WSGI startup.

The tests also protect the most important ordering property: the guard executes before normal database initialization.

## 5. Residual-risk assessment

I would still treat mock-signature support as high-risk compatibility code because any alternate service entry point must preserve the same startup invariant. The safest long-term design is to keep mock acceptance unavailable in production builds entirely, rather than merely unreachable through configuration.

The current implementation is nevertheless materially stronger than the historical one: an operator/configuration mistake must now defeat both a hard-disabled default and an explicit production runtime guard. The focused upstream test suite makes regression visible.

A useful future regression test would enumerate every supported production entry point (WSGI, direct service launcher, container command) and assert that each invokes the same guard before serving requests. That is defense-in-depth, not evidence that the known fix is currently broken.

## 6. Verification summary

- [x] Selected one of the six known BuilderFred findings
- [x] Described the pre-fix attack path
- [x] Located historical/deprecated evidence of the mock acceptance branch
- [x] Located the current hard-disabled configuration
- [x] Located the current fail-closed runtime guard
- [x] Verified WSGI calls the guard before initialization
- [x] Ran current upstream regression tests in a clean public CI job
- [x] `3 passed in 1.06s`
- [x] No production exploit attempt or state-changing request

Requested quest step: **Step 2 — 15 RTC**, subject to maintainer verification. This write-up does not assert acceptance or payment.
