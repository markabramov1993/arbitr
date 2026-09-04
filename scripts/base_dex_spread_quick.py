#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess

RPC='https://base-mainnet.g.alchemy.com/public'
UNI_FACTORY='0x33128a8fC17869897dcE68Ed026d694621f6FDfD'
AERO_FACTORY='0xf8f2eB4940CFE7d13603DDDD87f123820Fc061Ef'
TOKENS={
 'USDC':('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',6),
 'WETH':('0x4200000000000000000000000000000000000006',18),
 'cbBTC':('0xcbb7C0000ab88B473b1f5aFd9ef808440eed33bF',8),
 'cbXRP':('0xcb585250f852C6c6bf90434AB21A00f02833a4af',6),
}

def call(addr,sig,*args):
 p=subprocess.run(['cast','call',addr,sig,*map(str,args),'--rpc-url',RPC],capture_output=True,text=True,timeout=12)
 if p.returncode: raise RuntimeError((p.stderr or p.stdout).strip())
 return p.stdout.strip()

def addr(s): return s.split()[0]
def first(s): return int(s.split()[0],0)

def pool_price(pool, a_sym, b_sym):
 a,ad=TOKENS[a_sym]; b,bd=TOKENS[b_sym]
 t0=addr(call(pool,'token0()(address)')).lower()
 sq=first(call(pool,'slot0()(uint160,int24,uint16,uint16,uint16,bool)'))
 raw=(sq*sq)/(2**192)
 # raw is token1 raw units per token0 raw unit. Convert to human.
 if t0==a.lower():
  price_b_per_a=raw*(10**ad)/(10**bd)
 else:
  # raw = Araw/Braw; invert for B per A and adjust decimals.
  price_b_per_a=(1/raw)*(10**ad)/(10**bd)
 return price_b_per_a

def main():
 try:
  spacings=[int(x,0) for x in call(AERO_FACTORY,'tickSpacings()(int24[])').replace('[','').replace(']','').replace(',',' ').split() if x.lstrip('-').isdigit()]
 except Exception:
  spacings=[1,10,50,100,200]
 print(json.dumps({'kind':'meta','aero_spacings':spacings},separators=(',',':')))
 for mid in ('WETH','cbBTC','cbXRP'):
  usdc,_=TOKENS['USDC']; tok,_=TOKENS[mid]
  venues=[]
  for fee in (100,500,3000,10000):
   try:
    p=addr(call(UNI_FACTORY,'getPool(address,address,uint24)(address)',tok,usdc,fee))
    if int(p,16):
     pr=pool_price(p,mid,'USDC'); venues.append(('uni',fee,p,pr,fee/1e6))
   except Exception: pass
  for sp in spacings:
   try:
    p=addr(call(AERO_FACTORY,'getPool(address,address,int24)(address)',tok,usdc,sp))
    if int(p,16):
     pr=pool_price(p,mid,'USDC')
     try: fee=first(call(AERO_FACTORY,'getSwapFee(address)(uint24)',p))
     except Exception: fee=0
     venues.append(('aero',sp,p,pr,fee/1e6))
   except Exception: pass
  for v in venues:
   print(json.dumps({'kind':'pool','pair':f'{mid}/USDC','venue':v[0],'tier':v[1],'pool':v[2],'price_usdc_per_asset':v[3],'fee_fraction':v[4]},separators=(',',':')))
  for i,a in enumerate(venues):
   for b in venues[i+1:]:
    if a[0]==b[0]: continue
    low,high=(a,b) if a[3]<b[3] else (b,a)
    spread=(high[3]/low[3]-1)
    fee_sum=low[4]+high[4]
    edge=spread-fee_sum
    print(json.dumps({'kind':'spread','pair':f'{mid}/USDC','buy_venue':low[0],'buy_tier':low[1],'sell_venue':high[0],'sell_tier':high[1],'spread_bps':spread*10000,'fees_bps_approx':fee_sum*10000,'spot_edge_bps_before_slippage_gas':edge*10000},separators=(',',':')))
 return 0
if __name__=='__main__': raise SystemExit(main())
