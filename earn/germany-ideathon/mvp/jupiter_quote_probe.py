"""Read-only Jupiter quote probe for ProofRoute MVP evidence.

No wallet, signature, transaction construction or submission is performed.
"""
import hashlib
import json
import sys
import urllib.parse
import urllib.request

INPUT_MINT="So11111111111111111111111111111111111111112"  # wrapped SOL
OUTPUT_MINT="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
PARAMS={
    "inputMint":INPUT_MINT,
    "outputMint":OUTPUT_MINT,
    "amount":"100000000",  # 0.1 SOL
    "slippageBps":"50",
    "instructionVersion":"V2",
}
BASES=[
    "https://api.jup.ag/swap/v1/quote",
    "https://lite-api.jup.ag/swap/v1/quote",
]

last=None
for base in BASES:
    url=base+"?"+urllib.parse.urlencode(PARAMS)
    try:
        req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"proofroute-mvp/0.1"})
        with urllib.request.urlopen(req,timeout=20) as resp:
            data=json.load(resp)
        required={"inputMint","outputMint","inAmount","outAmount","otherAmountThreshold","slippageBps","priceImpactPct","routePlan"}
        missing=required-set(data)
        if missing:
            raise RuntimeError("missing quote fields: "+",".join(sorted(missing)))
        canonical=json.dumps(data,sort_keys=True,separators=(",",":")).encode()
        result={
            "source":base,
            "inputMint":data["inputMint"],
            "outputMint":data["outputMint"],
            "inAmount":data["inAmount"],
            "outAmount":data["outAmount"],
            "otherAmountThreshold":data["otherAmountThreshold"],
            "slippageBps":data["slippageBps"],
            "priceImpactPct":data["priceImpactPct"],
            "contextSlot":data.get("contextSlot"),
            "routeSteps":len(data["routePlan"]),
            "evidenceHash":hashlib.sha256(canonical).hexdigest(),
        }
        print(json.dumps(result,indent=2))
        raise SystemExit(0)
    except Exception as exc:
        last=f"{base}: {type(exc).__name__}: {exc}"
        print("QUOTE_SOURCE_FAILED="+last,file=sys.stderr)

print("No Jupiter quote source succeeded. Last error: "+str(last),file=sys.stderr)
raise SystemExit(1)
