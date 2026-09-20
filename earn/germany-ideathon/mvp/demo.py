from dataclasses import asdict
import json
from proofroute import IntentRegistry, Policy, authorize_intent, create_intent, settle_intent, verify_intent

good_evidence={"adapter":"jupiter-quote-snapshot","route":["USDC","SOL","USDC"],"quote_slot":1000000,
               "expected_input":1000000,"expected_output":1012000,"fees_included":True}
intent=create_intent(intent_id="intent-profitable-001",proposer="searcher-agent-a",input_mint="USDC",
    output_mint="USDC",max_input=1000000,min_output=1008000,expiry_slot=1000120,
    route_id="jupiter-route-usdc-sol-usdc",evidence=good_evidence)
reg=IntentRegistry(); reg.add(intent)
rows=[
    verify_intent(intent,verifier="verifier-east",reproduced_output=1011900,evidence=good_evidence,observed_slot=1000020),
    verify_intent(intent,verifier="verifier-west",reproduced_output=1012000,evidence=good_evidence,observed_slot=1000021),
]
auth=authorize_intent(intent,rows,Policy(quorum=2,max_output_spread_bps=25),current_slot=1000025)
receipt=settle_intent(intent,auth,executor="executor-demo",actual_input=1000000,actual_output=1010500,fee_paid=500,settled_slot=1000030)

bad_evidence=dict(good_evidence,route=["USDC","ALT","USDC"],expected_output=1003000)
bad=create_intent(intent_id="intent-negative-002",proposer="searcher-agent-b",input_mint="USDC",
    output_mint="USDC",max_input=1000000,min_output=1008000,expiry_slot=1000120,
    route_id="alternate-route",evidence=bad_evidence)
bad_v=verify_intent(bad,verifier="verifier-east",reproduced_output=1003000,evidence=bad_evidence,observed_slot=1000020)

print(json.dumps({"accepted_intent":intent.intent_id,"authorization":asdict(auth),
    "receipt":asdict(receipt),"rejected_intent":{"intent_id":bad.intent_id,"passed":bad_v.passed,"reason":bad_v.reason}},indent=2))
