#!/usr/bin/env python3
"""Read-only Chainlink SVR -> Aave V3 Base pre-liquidation detector.

No private key, no bid, no transactions. It indexes recent USDC borrowers, snapshots
near-HF accounts, then listens to the public SVR solver feed. When an ETH/USD
future median arrives, it projects the account HF using the future ETH price.
"""
import asyncio, json, subprocess, sys, time, urllib.request, urllib.error
from collections import defaultdict
import websockets

WS='wss://svr-bid-endpoint.chain.link/ws/solver'
LOG_RPC='https://mainnet.base.org'
RPC='https://base-mainnet.g.alchemy.com/public'
POOL='0xA238Dd80C259a72e81d7e4664a9801593F98d1c5'
ORACLE='0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156'
WETH='0x4200000000000000000000000000000000000006'
WETH_ATOKEN='0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7'
WETH_VTOKEN='0x24e6e0795b3c7c71D965fCc4f371803d1c1DcA1E'
USDC='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
USDC_VTOKEN='0x59dca05b6c26dbd64b5381374aAaC5CD05644C28'
BASE_CONTROL='0xa5e1a36938769cbd5a26f5e19d8fcb379f597c83'
BASE_ATLAS='0x583dcfef0d240dc80753f0f0b26513fee27d9b77'
ETH_FEEDS={
 '0x83f3425a5b32655dc645f7f4e422dd60e9741794':18,
 '0xd772f6d9b7a35cb96fddfe569964ab1c05017bf9':8,
}

def rpc(url, method, params, timeout=25):
    body=json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode()
    req=urllib.request.Request(url,data=body,headers={'Content-Type':'application/json','User-Agent':'profit-engine-svr-preliq/0.1'})
    with urllib.request.urlopen(req,timeout=timeout) as r: d=json.load(r)
    if d.get('error'): raise RuntimeError(str(d['error']))
    return d['result']

def batch_eth_calls(calls, chunk=80):
    out={}
    for pos in range(0,len(calls),chunk):
        part=calls[pos:pos+chunk]
        payload=[]
        for i,(key,to,data) in enumerate(part):
            payload.append({'jsonrpc':'2.0','id':i,'method':'eth_call','params':[{'to':to,'data':data},'latest']})
        body=json.dumps(payload).encode(); req=urllib.request.Request(RPC,data=body,headers={'Content-Type':'application/json','User-Agent':'profit-engine-svr-preliq/0.1'})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req,timeout=30) as r: rows=json.load(r)
                byid={x['id']:x for x in rows}
                for i,(key,_,__) in enumerate(part):
                    row=byid.get(i,{})
                    if 'result' in row: out[key]=row['result']
                break
            except Exception:
                if attempt==3: raise
                time.sleep(1.5*(attempt+1))
        time.sleep(0.05)
    return out

def sig(s): return subprocess.check_output(['cast','sig',s],text=True).strip()
def arg_addr(a): return '0'*24+a.lower().replace('0x','')
def calldata(selector,a): return selector+arg_addr(a)
def uint1(raw):
    if not raw or raw=='0x': return 0
    return int(raw,16)
def words(raw,n):
    h=raw[2:] if raw.startswith('0x') else raw
    return [int(h[i*64:(i+1)*64],16) for i in range(n)]
def toint(v):
    if isinstance(v,int): return v
    if isinstance(v,str): return int(v,0)
    return 0

def index_usdc_borrowers(max_users=1200, lookback=1_500_000):
    latest=int(rpc(RPC,'eth_blockNumber',[]),16); start=max(0,latest-lookback)
    topic0=subprocess.check_output(['cast','keccak','Borrow(address,address,address,uint256,uint8,uint256,uint16)'],text=True).strip()
    reserve='0x'+'0'*24+USDC[2:].lower()
    seen={}; log_count=0; failed=0
    for lo in range(start,latest+1,10_000):
        hi=min(latest,lo+9_999)
        try:
            logs=rpc(LOG_RPC,'eth_getLogs',[{'address':POOL,'fromBlock':hex(lo),'toBlock':hex(hi),'topics':[topic0,reserve]}])
        except Exception:
            failed+=1; continue
        log_count+=len(logs)
        for lg in logs:
            ts=lg.get('topics') or []
            if len(ts)>=3:
                u='0x'+ts[2][-40:]
                seen[u]=max(seen.get(u,0),int(lg['blockNumber'],16))
    users=[u for u,_ in sorted(seen.items(),key=lambda x:x[1],reverse=True)[:max_users]]
    print('BORROW_INDEX',json.dumps({'latestBlock':latest,'fromBlock':start,'borrowEvents':log_count,'uniqueBorrowers':len(seen),'selected':len(users),'failedLogChunks':failed},separators=(',',':')))
    return users

def snapshot(users):
    s_acc=sig('getUserAccountData(address)')
    s_bal='0x70a08231'
    s_price=sig('getAssetPrice(address)')
    p_raw=rpc(RPC,'eth_call',[{'to':ORACLE,'data':calldata(s_price,WETH)},'latest'])
    weth_price_base=uint1(p_raw)
    calls=[]
    for u in users:
        calls += [
          ((u,'acc'),POOL,calldata(s_acc,u)),
          ((u,'wa'),WETH_ATOKEN,calldata(s_bal,u)),
          ((u,'wv'),WETH_VTOKEN,calldata(s_bal,u)),
          ((u,'uv'),USDC_VTOKEN,calldata(s_bal,u)),
        ]
    res=batch_eth_calls(calls)
    near=[]
    for u in users:
        try:
            a=words(res.get((u,'acc'),'0x'),6)
            if len(a)<6: continue
            coll,debt,avail,liqthr,ltv,hf=a
            if debt==0 or hf==0: continue
            oldhf=hf/1e18
            if not (0.995 <= oldhf <= 1.035): continue
            wa=uint1(res.get((u,'wa'))); wv=uint1(res.get((u,'wv'))); uv=uint1(res.get((u,'uv')))
            weth_coll=wa*weth_price_base/1e18
            weth_debt=wv*weth_price_base/1e18
            cf=min(1.0,weth_coll/coll) if coll else 0.0
            df=min(1.0,weth_debt/debt) if debt else 0.0
            usdc_debt_base=uv*100.0  # USDC 6d -> Aave base 8d
            uf=min(1.0,usdc_debt_base/debt) if debt else 0.0
            near.append({'user':u,'hf':oldhf,'collBase':coll,'debtBase':debt,'wethCollateralFraction':cf,'wethDebtFraction':df,'usdcDebtFraction':uf,'wethAToken':wa,'usdcDebt':uv/1e6})
        except Exception:
            continue
    near.sort(key=lambda x:x['hf'])
    print('SNAPSHOT',json.dumps({'wethAavePriceUSD':weth_price_base/1e8,'nearHF':len(near),'minHF':near[0]['hf'] if near else None},separators=(',',':')))
    for x in near[:20]: print('NEAR',json.dumps(x,separators=(',',':')))
    return near,weth_price_base

async def monitor(near,weth_price_base,seconds=300):
    found=[]; seen=set(); deadline=time.monotonic()+seconds
    async with websockets.connect(WS,open_timeout=15,ping_interval=20,ping_timeout=20,max_size=8*1024*1024) as ws:
        await ws.send(json.dumps({'jsonrpc':'2.0','id':1,'method':'solver_subscribe','params':['userOperations']}))
        ack=json.loads(await asyncio.wait_for(ws.recv(),15)); print('SUBSCRIBE_ACK',json.dumps(ack,separators=(',',':')))
        while time.monotonic()<deadline:
            try: raw=await asyncio.wait_for(ws.recv(),min(15,max(.1,deadline-time.monotonic())))
            except asyncio.TimeoutError: continue
            try: msg=json.loads(raw)
            except: continue
            result=((msg.get('params') or {}).get('result') or {})
            p=result.get('partial_user_operation') or result.get('partialUserOperation') or {}
            if toint(p.get('chainId',0))!=8453: continue
            if str(p.get('control','')).lower()!=BASE_CONTROL or str(p.get('to','')).lower()!=BASE_ATLAS: continue
            h=p.get('hints') or {}; agg=str(h.get('aggregator','')).lower()
            if agg not in ETH_FEEDS: continue
            med=toint(h.get('medianPrice',0)); dec=ETH_FEEDS[agg]
            future_usd=med/(10**dec)
            current_aave_usd=weth_price_base/1e8
            ratio=future_usd/current_aave_usd if current_aave_usd else 1
            key=(agg,med)
            if key in seen: continue
            seen.add(key)
            event={'auction':result.get('auction_id'),'aggregator':agg,'futureETHUSD':future_usd,'aaveETHUSD':current_aave_usd,'deltaPct':(ratio-1)*100,'deadline':p.get('deadline'),'maxFeePerGas':p.get('maxFeePerGas')}
            print('SVR_ETH',json.dumps(event,separators=(',',':')))
            for x in near:
                cf=x['wethCollateralFraction']; df=x['wethDebtFraction']
                # only high-confidence exposures: mostly WETH collateral, mostly non-WETH debt and active USDC debt
                if cf < .60 or df > .15 or x['usdcDebtFraction'] < .40: continue
                newhf=x['hf']*((1+cf*(ratio-1))/(1+df*(ratio-1)))
                if x['hf']>=1 and newhf<1:
                    row=dict(x); row.update({'projectedHF':newhf,'futureETHUSD':future_usd,'shockPct':(ratio-1)*100,'auction':result.get('auction_id'),'confidence':'high'})
                    found.append(row); print('CROSSED',json.dumps(row,separators=(',',':')))
                elif newhf<1.005:
                    row={'user':x['user'],'hf':x['hf'],'projectedHF':newhf,'wethCollateralFraction':cf,'usdcDebt':x['usdcDebt'],'shockPct':(ratio-1)*100}
                    print('PRE_NEAR',json.dumps(row,separators=(',',':')))
    print('PRELIQ_SUMMARY',json.dumps({'ethAuctions':len(seen),'crossed':len(found),'uniqueCrossed':len({x['user'] for x in found})},separators=(',',':')))
    return found

def main():
    users=index_usdc_borrowers(); near,price=snapshot(users); asyncio.run(monitor(near,price,300))
if __name__=='__main__': main()
