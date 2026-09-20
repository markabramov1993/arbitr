"""ProofRoute MVP: bounded execution intents, verifier quorum and receipts.

Dependency-free reference implementation of the policy/invariant layer that
will later map to Solana/Anchor accounts. It never moves real funds.
"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field
from statistics import median
from typing import Iterable

@dataclass(frozen=True)
class Intent:
    intent_id: str
    proposer: str
    input_mint: str
    output_mint: str
    max_input: int
    min_output: int
    expiry_slot: int
    route_id: str
    evidence_hash: str
    def fingerprint(self) -> str:
        return sha256_json({
            "input_mint": self.input_mint, "output_mint": self.output_mint,
            "max_input": self.max_input, "min_output": self.min_output,
            "expiry_slot": self.expiry_slot, "route_id": self.route_id,
            "evidence_hash": self.evidence_hash,
        })

@dataclass(frozen=True)
class Verification:
    intent_id: str
    verifier: str
    reproduced_output: int
    evidence_hash: str
    observed_slot: int
    passed: bool
    reason: str

@dataclass(frozen=True)
class Policy:
    quorum: int = 2
    max_output_spread_bps: int = 25
    def __post_init__(self):
        if self.quorum < 1: raise ValueError("quorum must be >= 1")
        if self.max_output_spread_bps < 0: raise ValueError("spread must be >= 0")

@dataclass(frozen=True)
class Authorization:
    intent_id: str
    authorized: bool
    reason: str
    quorum: int
    passing_verifiers: tuple[str, ...] = field(default_factory=tuple)
    reproduced_output_median: int | None = None

@dataclass(frozen=True)
class ExecutionReceipt:
    intent_id: str
    executor: str
    actual_input: int
    actual_output: int
    fee_paid: int
    settled_slot: int
    expected_output_median: int
    slippage_bps_vs_verified: int
    receipt_hash: str

def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()

def sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()

def evidence_hash(evidence: object) -> str:
    return sha256_json(evidence)

def create_intent(*, intent_id, proposer, input_mint, output_mint, max_input,
                  min_output, expiry_slot, route_id, evidence) -> Intent:
    if not intent_id or not proposer or not route_id:
        raise ValueError("intent_id, proposer and route_id are required")
    if max_input <= 0 or min_output <= 0 or expiry_slot <= 0:
        raise ValueError("bounds and expiry must be positive")
    return Intent(intent_id, proposer, input_mint, output_mint, max_input,
                  min_output, expiry_slot, route_id, evidence_hash(evidence))

def verify_intent(intent: Intent, *, verifier: str, reproduced_output: int,
                  evidence: object, observed_slot: int) -> Verification:
    got_hash = evidence_hash(evidence)
    if observed_slot > intent.expiry_slot:
        return Verification(intent.intent_id, verifier, reproduced_output, got_hash,
                            observed_slot, False, "intent_expired")
    if got_hash != intent.evidence_hash:
        return Verification(intent.intent_id, verifier, reproduced_output, got_hash,
                            observed_slot, False, "evidence_hash_mismatch")
    if reproduced_output < intent.min_output:
        return Verification(intent.intent_id, verifier, reproduced_output, got_hash,
                            observed_slot, False, "below_min_output")
    return Verification(intent.intent_id, verifier, reproduced_output, got_hash,
                        observed_slot, True, "verified")

def authorize_intent(intent: Intent, verifications: Iterable[Verification],
                     policy: Policy = Policy(), *, current_slot: int) -> Authorization:
    if current_slot > intent.expiry_slot:
        return Authorization(intent.intent_id, False, "intent_expired", policy.quorum)
    rows = [v for v in verifications if v.intent_id == intent.intent_id]
    seen = set()
    for row in rows:
        if row.verifier in seen:
            return Authorization(intent.intent_id, False, "duplicate_verifier", policy.quorum)
        seen.add(row.verifier)
    passing = [v for v in rows if v.passed and v.evidence_hash == intent.evidence_hash]
    if len(passing) < policy.quorum:
        return Authorization(intent.intent_id, False, "quorum_not_met", policy.quorum,
                             tuple(v.verifier for v in passing))
    outputs = [v.reproduced_output for v in passing]
    med = int(median(outputs))
    spread = max(outputs) - min(outputs)
    spread_bps = (spread * 10_000) // med if med else 10_000
    if spread_bps > policy.max_output_spread_bps:
        return Authorization(intent.intent_id, False, "verifier_disagreement", policy.quorum,
                             tuple(v.verifier for v in passing), med)
    return Authorization(intent.intent_id, True, "authorized", policy.quorum,
                         tuple(v.verifier for v in passing), med)

def settle_intent(intent: Intent, authorization: Authorization, *, executor: str,
                  actual_input: int, actual_output: int, fee_paid: int,
                  settled_slot: int) -> ExecutionReceipt:
    if not authorization.authorized:
        raise ValueError("intent is not authorized: " + authorization.reason)
    if authorization.intent_id != intent.intent_id:
        raise ValueError("authorization belongs to a different intent")
    if settled_slot > intent.expiry_slot:
        raise ValueError("cannot settle expired intent")
    if actual_input < 0 or actual_input > intent.max_input:
        raise ValueError("actual input violates max_input")
    if actual_output < intent.min_output:
        raise ValueError("actual output violates min_output")
    if fee_paid < 0:
        raise ValueError("fee_paid cannot be negative")
    expected = authorization.reproduced_output_median
    if not expected:
        raise ValueError("authorization has no verified output")
    slippage_bps = (max(0, expected - actual_output) * 10_000) // expected
    body = {
        "intent_id": intent.intent_id, "executor": executor,
        "actual_input": actual_input, "actual_output": actual_output,
        "fee_paid": fee_paid, "settled_slot": settled_slot,
        "expected_output_median": expected,
        "slippage_bps_vs_verified": slippage_bps,
    }
    return ExecutionReceipt(**body, receipt_hash=sha256_json(body))

class IntentRegistry:
    def __init__(self):
        self._fingerprints = {}
    def add(self, intent: Intent):
        fp = intent.fingerprint()
        if fp in self._fingerprints:
            raise ValueError("duplicate intent of " + self._fingerprints[fp])
        self._fingerprints[fp] = intent.intent_id
