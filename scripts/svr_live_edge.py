#!/usr/bin/env python3
"""Read-only Chainlink SVR edge sampler for Base.

For every Base Atlas notification, record the hinted median price and immediately
query the current Base block + aggregator latestAnswer. No keys, bids, or writes.
Only auctions whose deadline is not already behind the observed block are tagged
fresh.
"""
import asyncio, json, time, urllib.request
import websockets

WS='wss://svr-bid-endpoint.chain.link/ws/solver'
RPC='https://base-mainnet.g.alchemy.com/public'
BASE=8453
LATEST_ANSWER='0x50d25bcd'


def jrpc(method, params):
    body=json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode()
    req=urllib.request.Request(RPC,data=body,headers={'Content-Type':'application/json','User-Agent':'profit-engine-svr-edge/0.1'})
    with urllib.request.urlopen(req,timeout=8) as r:
        d=json.load(r)
    if d.get('error'): raise RuntimeError(d['error'])
    return d['result']


def asint(v):
    if v is None:return None
    if isinstance(v,int):return v
    if isinstance(v,str):
        try:return int(v,0)
        except:return int(v)
    if isinstance(v,dict):
        for k in ('hex','value','_hex'):
            if k in v:return asint(v[k])
    return None


def addr(v):
    if not v:return None
    if isinstance(v,str):return v.lower()
    return str(v).lower()


def decode_int256(h):
    n=int(h,16)
    if n >= 1<<255:n-=1<<256
    return n


def get_hint(hints, key):
    if not isinstance(hints,dict):return None
    v=hints.get(key)
    # Some gateway serializers wrap hint values.
    if isinstance(v,dict):
        for k in ('value','data','raw'):
            if k in v:return v[k]
    return v


async def run(seconds=300):
    start=time.monotonic(); total=base=fresh=0
    async with websockets.connect(WS,max_size=4*1024*1024,ping_interval=20,ping_timeout=20) as ws:
        await ws.send(json.dumps({'jsonrpc':'2.0','id':1,'method':'solver_subscribe','params':['userOperations']}))
        print('ACK',await ws.recv(),flush=True)
        while time.monotonic()-start < seconds:
            left=max(1,seconds-(time.monotonic()-start))
            try: raw=await asyncio.wait_for(ws.recv(),timeout=min(30,left))
            except asyncio.TimeoutError: continue
            msg=json.loads(raw); params=msg.get('params') or {}; n=params.get('result') or params.get('data') or {}
            if not isinstance(n,dict):continue
            po=n.get('partial_user_operation') or n.get('partialUserOperation') or {}
            chain=asint(po.get('chainId') or po.get('chain_id'))
            total+=1
            if chain!=BASE:continue
            base+=1
            hints=po.get('hints') or {}
            agg=addr(get_hint(hints,'aggregator'))
            median=asint(get_hint(hints,'medianPrice'))
            deadline=asint(po.get('deadline'))
            observed_ns=time.time_ns()
            try:
                block=int(jrpc('eth_blockNumber',[]),16)
            except Exception as e:
                block=None
            old=None
            if agg:
                try: old=decode_int256(jrpc('eth_call',[{'to':agg,'data':LATEST_ANSWER},'latest']))
                except Exception as e: pass
            isfresh=bool(block is not None and deadline is not None and deadline>=block)
            if isfresh:fresh+=1
            delta=None
            if old not in (None,0) and median is not None:delta=(median-old)/old*100
            rec={'auction_id':n.get('auction_id') or n.get('auctionId'),'observed_unix_ns':observed_ns,'block_at_receive':block,'deadline':deadline,'blocks_to_deadline':None if block is None or deadline is None else deadline-block,'fresh':isfresh,'aggregator':agg,'old_answer_at_receive':old,'hinted_median':median,'delta_pct':delta,'userOpHash':po.get('userOpHash')}
            print('BASE_EDGE '+json.dumps(rec,separators=(',',':')),flush=True)
    print('SUMMARY '+json.dumps({'seconds':seconds,'notifications':total,'base':base,'fresh_base':fresh},separators=(',',':')),flush=True)

if __name__=='__main__': asyncio.run(run())
