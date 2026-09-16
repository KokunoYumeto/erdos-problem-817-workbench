from certificates.carry_tools import *
from time import monotonic
import json,argparse
from pathlib import Path

def search(b,k,mode='carry',limit_n=8):
    best=();nodes=0;calls=0;cache={}
    def good(bits):
        nonlocal calls
        if bits in cache:return cache[bits]
        calls+=1
        if int_ap_bits(bits,k) is not None:ans=False
        else:
            digits={i for i in range(bits.bit_length()) if bits>>i&1}
            ans=(modular_witness(digits,b,k) is None) if mode=='modular' else carry_certificate(digits,b,k)['safe']
        cache[bits]=ans
        return ans
    def walk(a,total,h):
        nonlocal best,nodes
        nodes+=1
        if len(a)>len(best):best=a
        if len(a)>=limit_n:return
        first=a[-1]+1 if a else 1
        needed=max(1,len(best)+1-len(a))
        for v in range(first,b-total):
            if total+needed*v+needed*(needed-1)//2>=b:break
            hh=h|(h<<v)
            if good(hh):walk(a+(v,),total+v,hh)
    walk((),0,1)
    return best,nodes,calls
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=('carry','modular'),default='carry');p.add_argument('--max-base',type=int,default=80);p.add_argument('--min-base',type=int,default=3);p.add_argument('--k',type=int,nargs='+',default=[5,6]);a=p.parse_args()
    if not (2 <= a.min_base <= a.max_base) or any(k < 3 for k in a.k):
        p.error('require 2 <= min-base <= max-base and every k >= 3')
    t=monotonic();results=[]
    for k in a.k:
        best=(3,1)
        for b in range(a.min_base,a.max_base+1):
            block,nodes,calls=search(b,k,a.mode)
            r={'k':k,'base':b,'generators':block,'nodes':nodes,'candidate_checks':calls}
            results.append(r)
            if block and b**best[1]<best[0]**len(block):
                best=(b,len(block));print('IMPROVE',json.dumps(r),flush=True)
        print('DONE',k,round(monotonic()-t,2),flush=True)
    directory=Path(__file__).resolve().parent/'logs';directory.mkdir(exist_ok=True)
    path=directory/f'search_{a.mode}_{min(a.k)}_{max(a.k)}_{a.max_base}.json'
    path.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
