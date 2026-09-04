#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, time

RPC='https://base-mainnet.g.alchemy.com/public'
UNI_QUOTER='0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a'
AERO_QUOTER='0x514c8B5f54112481E28028F1166Bd78501089259'
USDC='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
CBBTC='0xcbb7C0000ab88B473b1f5aFd9ef808440eed33bF'

def call(addr,sig,*args):
    last=''
    for _ in range(3):
        p=subprocess.run(['cast','call',addr,sig,*map(str,args),'--rpc-url',RPC],capture_output=True,text=True,timeout=15)
        if p.returncode==0: return p.stdout.strip()
        last=(p.stderr or p.stdout).strip(); time.sleep(.25)
    raise RuntimeError(last)

def first(s): return int(s.split()[0],0)

def uni(amount):
    return first(call(UNI_QUOTER,
        'quoteExactInputSingle((address,address,uint256,uint24,uint160))(uint256,uint160,uint32,uint256)',
        f'({USDC},{CBBTC},{amount},100,0)'))

def aero(amount):
    return first(call(AERO_QUOTER,
        'quoteExactInputSingle(address,address,int24,uint256,uint160)(uint256)',
        CBBTC,USDC,50,amount,0))

def reverse_aero(amount):
    return first(call(AERO_QUOTER,
        'quoteExactInputSingle(address,address,int24,uint256,uint160)(uint256)',
        USDC,CBBTC,50,amount,0))

def reverse_uni(amount):
    return first(call(UNI_QUOTER,
        'quoteExactInputSingle((address,address,uint256,uint24,uint160))(uint256,uint160,uint32,uint256)',
        f'({CBBTC},{USDC},{amount},100,0)'))

def test(amount_usdc, route):
    inp=int(amount_usdc*1e6)
    if route=='uni-aero': mid=uni(inp); out=aero(mid)
    else: mid=reverse_aero(inp); out=reverse_uni(mid)
    pnl=out-inp
    return {'kind':'quote','route':route,'amount_in_usdc':amount_usdc,'cbBTC_mid':mid/1e8,'amount_out_usdc':out/1e6,'gross_pnl_usdc':pnl/1e6,'gross_bps':pnl/inp*10000}

def main():
    rows=[]
    for amount in (100,500,1000,2500,5000,10000,25000,50000):
        for route in ('uni-aero','aero-uni'):
            try:
                r=test(amount,route); rows.append(r); print(json.dumps(r,separators=(',',':')))
            except Exception as e:
                print(json.dumps({'kind':'error','route':route,'amount':amount,'error':str(e)[:240]},separators=(',',':')))
    positive=[x for x in rows if x['gross_pnl_usdc']>0]
    best=max(rows,key=lambda x:x['gross_pnl_usdc']) if rows else None
    print(json.dumps({'kind':'summary','quotes':len(rows),'positive':len(positive),'best':best},separators=(',',':')))
if __name__=='__main__': main()
