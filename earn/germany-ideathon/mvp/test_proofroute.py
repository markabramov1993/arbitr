import unittest
from proofroute import IntentRegistry, Policy, authorize_intent, create_intent, settle_intent, verify_intent

EVIDENCE={"route":["USDC","SOL","USDC"],"quote_slot":1000,"simulated_output":1010000,"fees_included":True}

class ProofRouteTests(unittest.TestCase):
    def make_intent(self):
        return create_intent(intent_id="intent-001", proposer="agent-alpha",
            input_mint="USDC", output_mint="USDC", max_input=1000000,
            min_output=1005000, expiry_slot=1100, route_id="jupiter-route-A",
            evidence=EVIDENCE)

    def good_rows(self, intent):
        return [
            verify_intent(intent, verifier="v1", reproduced_output=1010000, evidence=EVIDENCE, observed_slot=1020),
            verify_intent(intent, verifier="v2", reproduced_output=1009900, evidence=EVIDENCE, observed_slot=1021),
        ]

    def test_happy_path_quorum_and_receipt(self):
        i=self.make_intent()
        a=authorize_intent(i,self.good_rows(i),Policy(quorum=2,max_output_spread_bps=25),current_slot=1025)
        self.assertTrue(a.authorized)
        r=settle_intent(i,a,executor="executor-1",actual_input=1000000,actual_output=1009000,fee_paid=500,settled_slot=1030)
        self.assertEqual(len(r.receipt_hash),64)

    def test_expired_intent_rejected(self):
        i=self.make_intent()
        v=verify_intent(i,verifier="v1",reproduced_output=1010000,evidence=EVIDENCE,observed_slot=1101)
        self.assertFalse(v.passed); self.assertEqual(v.reason,"intent_expired")

    def test_changed_evidence_rejected(self):
        i=self.make_intent(); changed=dict(EVIDENCE,quote_slot=1001)
        v=verify_intent(i,verifier="v1",reproduced_output=1010000,evidence=changed,observed_slot=1020)
        self.assertFalse(v.passed); self.assertEqual(v.reason,"evidence_hash_mismatch")

    def test_below_minimum_rejected(self):
        i=self.make_intent()
        v=verify_intent(i,verifier="v1",reproduced_output=999000,evidence=EVIDENCE,observed_slot=1020)
        self.assertFalse(v.passed); self.assertEqual(v.reason,"below_min_output")

    def test_duplicate_verifier_blocks_authorization(self):
        i=self.make_intent()
        rows=[verify_intent(i,verifier="same",reproduced_output=1010000,evidence=EVIDENCE,observed_slot=1020),
              verify_intent(i,verifier="same",reproduced_output=1010000,evidence=EVIDENCE,observed_slot=1021)]
        a=authorize_intent(i,rows,current_slot=1025)
        self.assertFalse(a.authorized); self.assertEqual(a.reason,"duplicate_verifier")

    def test_disagreement_blocks_authorization(self):
        i=self.make_intent()
        rows=[verify_intent(i,verifier="v1",reproduced_output=1010000,evidence=EVIDENCE,observed_slot=1020),
              verify_intent(i,verifier="v2",reproduced_output=1007000,evidence=EVIDENCE,observed_slot=1021)]
        a=authorize_intent(i,rows,Policy(quorum=2,max_output_spread_bps=20),current_slot=1025)
        self.assertFalse(a.authorized); self.assertEqual(a.reason,"verifier_disagreement")

    def test_settlement_enforces_max_input(self):
        i=self.make_intent(); a=authorize_intent(i,self.good_rows(i),current_slot=1025)
        with self.assertRaisesRegex(ValueError,"max_input"):
            settle_intent(i,a,executor="e",actual_input=1000001,actual_output=1009000,fee_paid=1,settled_slot=1030)

    def test_registry_deduplicates_equivalent_intents(self):
        i=self.make_intent()
        d=create_intent(intent_id="intent-002",proposer="agent-beta",input_mint=i.input_mint,
            output_mint=i.output_mint,max_input=i.max_input,min_output=i.min_output,
            expiry_slot=i.expiry_slot,route_id=i.route_id,evidence=EVIDENCE)
        reg=IntentRegistry(); reg.add(i)
        with self.assertRaisesRegex(ValueError,"duplicate intent"): reg.add(d)

if __name__=="__main__": unittest.main()
