#!/usr/bin/env python3
"""Exhaustive fixed-five-generator mixed-radix capacities at k=5 and k=6.

Uses complete carry-return sections where they exist; otherwise retains the
full finite controller. Companion proofs explain the uniform outer cutoffs.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from time import monotonic
import verify_outer_control as v


def blocks(n,total,lo=1,prefix=()):
    if n==0:
        yield prefix;return
    for a in range(lo,total+1):
        if n*a+n*(n-1)//2>total:break
        yield from blocks(n-1,total-a,a+1,prefix+(a,))


def modular_witness(D,b,k):
    bits=sum(1<<d for d in D);mask=(1<<b)-1
    for step in range(1,b):
        starts=bits
        for i in range(1,k):
            shift=(i*step)%b
            rotated=bits if shift==0 else ((bits>>shift)|(bits<<(b-shift)))&mask
            starts &= rotated
            if not starts:break
        if starts:
            start=(starts & -starts).bit_length()-1
            col=tuple((start+i*step)%b for i in range(k))
            v.require(all(x in D for x in col),'modular bit witness failed')
            return start,step,col
    return None


def return_section(D,k):
    present=set(D);table=[]
    for c in product((-1,0,1),repeat=k-2):
        found=None
        for first in D:
            for second in D:
                col=[first,second]
                for ci in c:
                    z=2*col[-1]-col[-2]-ci
                    if z not in present:break
                    col.append(z)
                else:
                    found=tuple(col);break
            if found is not None:break
        if found is None:return None,c
        v.require(all(found[i+2]-2*found[i+1]+found[i]==-c[i] for i in range(k-2)),
                  'literal return section fails')
        table.append((c,found))
    return table,None


def run(k,Q,benchmark,start_index=0,stop_index=None):
    v.require(v.period_safe(benchmark,k,(Q,)) and len(benchmark)==5,'invalid five-generator benchmark')
    domain=[];best={'generators':benchmark,'cycle':{'product':Q,'length':1,'bases':[Q]}};count=0;admiss=0;complete=0;start=monotonic()
    all_blocks=list(blocks(5,Q-1))
    stop_index=len(all_blocks) if stop_index is None else min(stop_index,len(all_blocks))
    v.require(0<=start_index<stop_index<=len(all_blocks),'invalid shard range')
    for a in all_blocks[start_index:stop_index]:
        count+=1;D=tuple(sorted(v.values(a)));bad=v.direct_ap(D,k)
        if bad:
            domain.append({'generators':a,'integer_obstruction':bad});continue
        admiss+=1;section,missing=return_section(D,k)
        if section is not None:
            complete+=1;S=sum(a);tested=[];smallest=None
            dictionary=dict(section)
            for b in range(S+1,2*S+2):
                bad=modular_witness(D,b,k)
                if bad is None:
                    smallest=b;break
                x,d,col=bad
                c=tuple((col[i+2]-2*col[i+1]+col[i])//b for i in range(k-2))
                high=dictionary[c]
                witness=tuple(col[i]+b*high[i] for i in range(k))
                v.require(witness[1]!=witness[0] and all(witness[i+2]-2*witness[i+1]+witness[i]==0 for i in range(k-2)),
                          'two-level return witness fails')
                tested.append({'base':b,'low':col,'high':high,'points':witness})
            v.require(smallest is not None,'universal base was not safe')
            C={'product':smallest,'length':1,'bases':[smallest]}
            entry={'generators':a,'method':'complete_return','section':section,
                   'smaller_base_obstructions':tested,'best':C}
        else:
            print('controller_start',k,a,'seconds',round(monotonic()-start,2),flush=True)
            graph=v.controller(a,k,enumerate_cycles=False,prune_returns=True);C={'product':2*sum(a)+1,'length':1,'bases':[2*sum(a)+1]}
            print('controller_done',k,a,len(graph['states']),len(graph['edges']),flush=True)
            potential=v.lower_potential(graph['edges'],len(graph['states']),Q,1)
            entry={'generators':a,'method':'full_controller','missing_return':missing,
                   'states':graph['states'],'edges':graph['edges'],
                   'return_section':graph['return_section'],'discarded_edges':graph['discarded_edges'],
                   'potential':potential,'certified_lower_base':Q}
        domain.append(entry)
        v.require(C['product']>=Q,'smaller constant base discovered; revise target and replay')
        if admiss%100==0:
            print('progress',k,count,admiss,complete,'best',best,'seconds',round(monotonic()-start,2),flush=True)
    v.require(best is not None,'no optimum')
    P=best['cycle']['product'];ell=best['cycle']['length']
    v.require(P<=Q**ell,'benchmark comparison')
    v.require(v.period_safe(best['generators'],k,tuple(best['cycle']['bases'])),'upper period fails')
    for entry in domain:
        if entry.get('method')=='complete_return':
            v.require(entry['best']['product']**ell>=P,'return lower comparison')
        elif entry.get('method')=='full_controller':
            entry['potential']=v.lower_potential(entry['edges'],len(entry['states']),P,ell)
    return {'evaluated_indices':[start_index,stop_index],'complete_domain_size':len(all_blocks),
            'k':k,'block_size':5,'benchmark_base':Q,'benchmark_generators':benchmark,
            'exhaustive_generator_sets':count,'integer_admissible':admiss,'complete_return':complete,
            'full_controllers':admiss-complete,'best':best,'root_exponent':5*ell,'domain':domain}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--k',type=int,choices=[5,6],required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--start-index',type=int,default=0);p.add_argument('--stop-index',type=int)
    args=p.parse_args()
    Q,A=(65,(1,2,5,15,20)) if args.k==5 else (47,(1,2,6,7,14))
    result=run(args.k,Q,A,args.start_index,args.stop_index)
    report={'schema':'ep817-global-rank-five-v1','status':'PASS','lean_checked':False,
            'result':result,'validator_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'helper_sha256':sha256(Path(v.__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('COMPLETE',result['best'],result['exhaustive_generator_sets'],result['integer_admissible'],flush=True)

if __name__=='__main__':main()
