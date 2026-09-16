#!/usr/bin/env python3
"""Exact bounded-rank variable-block certificates. Standard library only.

The theorem in variable-block-control.md reduces all block values and all
infinite canonical schedules with at most r generators per nonempty block to
this complete finite dictionary. This runner proves each requested finite
optimum using a positive rational potential and an attaining periodic word.
"""
from __future__ import annotations
import argparse,gzip,json
from collections import Counter,deque
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import prod
from pathlib import Path


def require(ok:bool,message:str)->None:
    if not ok:raise AssertionError(message)


def all_blocks(n:int,budget:int,first:int=1):
    if n==0:
        yield ();return
    for a in range(first,budget+1):
        if n*a+n*(n-1)//2>budget:return
        for tail in all_blocks(n-1,budget-a,a+1):yield (a,)+tail


def digit_fibres(A:tuple[int,...]):
    out={}
    for mask in range(1<<len(A)):
        y=sum(a for j,a in enumerate(A) if mask>>j&1)
        out.setdefault(y,[]).append(mask)
    return out


def columns(c:tuple[int,...],D:tuple[int,...],b:int):
    present=set(D)
    for x in D:
        for y in D:
            row=[x,y];target=[]
            for ci in c:
                t=2*row[-1]-row[-2]-ci;z=t%b
                if z not in present:break
                target.append((z-t)//b);row.append(z)
            else:
                require(all(-1<=t<=1 for t in target),'carry escaped')
                yield tuple(target),tuple(row)


def carry_orbits(k:int):
    Z=(0,)*(k-2)
    def orb(c):return tuple(sorted({c,tuple(-v for v in c),c[::-1],tuple(-v for v in c[::-1])}))
    return tuple(sorted({orb(c) for c in product((-1,0,1),repeat=k-2) if c!=Z}))


def anchors(r:int):
    known={1:(3,(1,)),2:(5,(1,2)),3:(13,(1,3,4)),4:(23,(1,3,4,7))}
    return {n:known.get(n,(3**n,tuple(3**j for j in range(n)))) for n in range(1,r+1)}


def build(k:int,r:int,limit:int=100000):
    require(3<=k<=6 and 1<=r<=4,'implemented exhaustive runner: 3<=k<=6, 1<=r<=4')
    O=carry_orbits(k);Z=(0,)*(k-2);m=len(O);reject_bit=1<<m
    index={c:i for i,o in enumerate(O) for c in o}
    def encode(T):return (reject_bit if Z in T else 0)|sum(1<<i for i in {index[c] for c in T if c!=Z})
    def expand(mask):return ({Z} if mask&reject_bit else set())|{c for i,o in enumerate(O) if mask>>i&1 for c in o}
    A0=anchors(r)
    for n,(b,A) in A0.items():
        require(len(A)==n and sum(A)<b,'anchor typing')
        require(not any(row[0]!=row[1] for _,row in columns(Z,tuple(digit_fibres(A)),b)),'invalid modular anchor')
    labels=[(2,())]+[(b,A) for n in range(1,r+1) for b in range(2,2*A0[n][0]+1) for A in all_blocks(n,b-1)]
    profiles=[];valid=[];edge_hash=sha256();raw_columns=0
    for li,(b,A) in enumerate(labels):
        fibres=digit_fibres(A);D=tuple(sorted(fibres))
        initial=set();obstruction=None
        for t,row in columns(Z,D,b):
            if row[0]!=row[1]:
                initial.add(t)
                if t==Z and obstruction is None:obstruction=row
        if obstruction is not None:
            profiles.append({'base':b,'generators':A,'integer_obstruction':obstruction});continue
        im=encode(initial);require(expand(im)==initial,'initial symmetry loss')
        transfers=[]
        for o in O:
            T=set()
            for c in o:
                for target,row in columns(c,D,b):
                    T.add(target);raw_columns+=1
                    edge_hash.update((repr((li,c,target,row))+'\n').encode())
            mask=encode(T);require(expand(mask)==T,'orbit transfer symmetry loss');transfers.append(mask)
        profiles.append({'base':b,'generators':A,'fibres':[[d,fibres[d]] for d in D],
                         'initial':im,'transfers':transfers})
        valid.append(li)
    print(f'profiles k={k},r={r}: {len(labels)} literal labels, {len(valid)} usable',flush=True)
    states=[0];seen={0:0};queue=deque([0]);best={};accepted=0;rejected=0;trace=sha256()
    while queue:
        R=queue.popleft();u=seen[R];active=[i for i in range(m) if R>>i&1]
        for li in valid:
            p=profiles[li];T=p['initial']
            for i in active:T|=p['transfers'][i]
            trace.update((repr((u,li,T))+'\n').encode())
            if T&reject_bit:rejected+=1;continue
            if T not in seen:
                require(len(states)<limit,'runner resource limit exceeded; no conclusion')
                seen[T]=len(states);states.append(T);queue.append(T)
            accepted+=1;v=seen[T];b=p['base'];n=len(p['generators']);key=(u,v,n)
            if key not in best or b<best[key][2]:best[key]=(u,v,b,n,li)
    E=sorted(best.values());N=len(states)
    print(f'graph k={k},r={r}: {N} states, {accepted} safe labels, {len(E)} cost representatives',flush=True)
    B,power=(8,2) if r==1 else ((5,2) if r<=3 else (23,4))
    h=[Fraction(1)]*N;factors=[Fraction(B**e[3],e[2]**power) for e in E];parents=[None]*N
    for rounds in range(N):
        changed=None
        for e,f in zip(E,factors):
            u,v=e[:2];new=h[u]*f
            if new>h[v]:h[v]=new;changed=v;parents[v]=e
        if changed is None:break
    else:
        v=changed
        for _ in range(N):v=parents[v][0]
        cycle=[];cur=v
        while True:
            e=parents[cur];cycle.append(e);cur=e[0]
            if cur==v:break
        raise AssertionError('target disproved by exact cycle '+repr(cycle[::-1]))
    require(all(e[2]**power*h[e[1]]>=B**e[3]*h[e[0]] for e in E),'potential failed')
    period=[(2,(1,)),(4,(2,))] if r==1 else ([(5,(1,2))] if r<=3 else [(23,(1,3,4,7))])
    label_ids=[labels.index(w) for w in period];orbit_states=[];seen_phase={};R=0;j=0
    while (j%len(period),R) not in seen_phase:
        seen_phase[(j%len(period),R)]=j;orbit_states.append(seen[R]);li=label_ids[j%len(period)];pr=profiles[li]
        T=pr['initial']
        for i in range(m):
            if R>>i&1:T|=pr['transfers'][i]
        require(not T&reject_bit,'upper period accepts');R=T;j+=1
    start=seen_phase[(j%len(period),R)]
    cycle_labels=[label_ids[t%len(period)] for t in range(start,j)]
    CB=prod(profiles[i]['base'] for i in cycle_labels);CN=sum(len(profiles[i]['generators']) for i in cycle_labels)
    require(CN>0 and CB**power==B**CN,'attaining period rate mismatch')
    return {'schema':'ep817-variable-block-proof-v1','status':'PASS','lean_checked':False,'k':k,'max_block_size':r,
            'anchor_blocks':[[n,b,A] for n,(b,A) in sorted(A0.items())],
            'orbits':O,'reject_bit':reject_bit,'profiles':profiles,'states':states,'representative_edges':E,
            'potential':[str(x) for x in h],'target':{'base':B,'root':power},
            'attainment':{'period':period,'visited_states':orbit_states,'cycle_start':start,'cycle_label_ids':cycle_labels},
            'counts':{'dictionary_labels':len(labels),'usable_labels':len(valid),'integer_obstructions':len(labels)-len(valid),
                      'raw_labeled_nonzero_source_columns':raw_columns,'reachable_states':N,'safe_transfers':accepted,
                      'rejected_transfers':rejected,'cost_representative_edges':len(E),'potential_passes':rounds+1},
            'full_column_transcript_sha256':edge_hash.hexdigest(),'controller_transcript_sha256':trace.hexdigest(),
            'validator_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--k',type=int,required=True);ap.add_argument('--rank',type=int,required=True)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    rec=build(a.k,a.rank);raw=(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(gzip.compress(raw,mtime=0) if a.output.suffix=='.gz' else raw)
    print(json.dumps({'status':'PASS','k':a.k,'rank':a.rank,'target':rec['target'],'counts':rec['counts'],
                      'plain_sha256':sha256(raw).hexdigest(),'file_sha256':sha256(a.output.read_bytes()).hexdigest()},sort_keys=True),flush=True)

if __name__=='__main__':main()
