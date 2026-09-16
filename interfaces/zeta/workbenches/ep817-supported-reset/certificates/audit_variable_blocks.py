#!/usr/bin/env python3
"""Independent exact audit. Imports no producer or optimization code.

Reconstructs the full generator/radix domain with itertools.combinations;
uses a closed prefix-defect formula for columns; checks every source carry,
every admitted/forbidden controller edge, rational potentials, and attainment.
"""
from __future__ import annotations
import argparse,gzip,json
from collections import deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations,product
from math import prod
from pathlib import Path


def check(ok,message):
    if not ok:raise AssertionError(message)


def source_image(A):
    F={}
    for bits in product((0,1),repeat=len(A)):
        y=sum(a*e for a,e in zip(A,bits));mask=sum(e<<i for i,e in enumerate(bits))
        F.setdefault(y,[]).append(mask)
    return {y:sorted(v) for y,v in F.items()}


def delta(row):return tuple(row[i]+row[i+2]-2*row[i+1] for i in range(len(row)-2))


def direct_columns(c,D,b):
    # Independent closed-form solution of the modular second-difference equations.
    t=len(c)+2;offset=[0,0]+[sum((i-1-j)*c[j] for j in range(i-1)) for i in range(2,t)]
    DD=set(D)
    for x in D:
        for y in D:
            row=[(x+i*(y-x)-offset[i])%b for i in range(t)]
            if all(v in DD for v in row):
                dd=delta(row);num=tuple(ci+z for ci,z in zip(c,dd))
                check(all(v%b==0 for v in num),'closed-form divisibility')
                target=tuple(v//b for v in num)
                check(all(-1<=v<=1 for v in target),'carry escape')
                yield target,tuple(row)


def audit(rec,source_sha=None,verbose=False):
    k=rec['k'];r=rec['max_block_size'];check(5<=k<=6 and 1<=r<=4,'wrong classified domain')
    check(rec['status']=='PASS' and rec['lean_checked'] is False,'evidence status')
    if source_sha is not None:check(rec['validator_sha256']==source_sha,'producer identity')
    anchors=rec['anchor_blocks'];check([a[0] for a in anchors]==list(range(1,r+1)),'anchor coverage')
    Z=(0,)*(k-2);caps={}
    for n,b,A in anchors:
        check(len(A)==n and A==sorted(set(A)) and min(A)>0 and sum(A)<b,'anchor inputs')
        D=source_image(A)
        check(not any(all((x+i*d)%b in D for i in range(k)) for x in D for d in range(1,b)),'modular anchor')
        caps[n]=2*b
    expected=[(2,())]
    for n in range(1,r+1):
        tuples=list(combinations(range(1,caps[n]),n))
        expected.extend(sorted((b,A) for A in tuples if sum(A)<caps[n] for b in range(sum(A)+1,caps[n]+1)))
    profiles=rec['profiles']
    check([(p['base'],tuple(p['generators'])) for p in profiles]==expected,'literal domain omitted/reordered/changed')
    def orbit(c):return tuple(sorted({c,tuple(-v for v in c),c[::-1],tuple(-v for v in c[::-1])}))
    O=sorted({orbit(c) for c in product((-1,0,1),repeat=k-2) if c!=Z})
    check(rec['orbits']==[[list(c) for c in o] for o in O],'orbit data')
    index={c:i for i,o in enumerate(O) for c in o};rb=1<<len(O);check(rec['reject_bit']==rb,'accepting bit')
    def encode(T):return (rb if Z in T else 0)|sum(1<<i for i in {index[c] for c in T if c!=Z})
    def expand(mask):return ({Z} if mask&rb else set())|{c for i,o in enumerate(O) if mask>>i&1 for c in o}
    raw_count=0;colhash=sha256();valid=[];invalid=0;all_carry_checks=0
    for li,p in enumerate(profiles):
        b=p['base'];A=p['generators'];F=source_image(A);D=tuple(sorted(F))
        if 'integer_obstruction' in p:
            row=p['integer_obstruction'];check(len(row)==k and row[0]!=row[1] and all(x in F for x in row) and delta(row)==Z,'false obstruction')
            invalid+=1;continue
        valid.append(li)
        check(p['fibres']==[[d,F[d]] for d in D],'representation fibres changed')
        init={t for t,row in direct_columns(Z,D,b) if row[0]!=row[1]}
        im=encode(init);check(Z not in init and im==p['initial'] and expand(im)==init,'initial transfer')
        checks=[]
        for o in O:
            T=set()
            for c in o:
                all_carry_checks+=1
                for target,row in direct_columns(c,D,b):
                    T.add(target);raw_count+=1
                    colhash.update((repr((li,c,target,row))+'\n').encode())
            mask=encode(T);check(expand(mask)==T,'symmetry expansion changed support');checks.append(mask)
        check(checks==p['transfers'],'orbit transition profile')
    if verbose:print('independent profiles checked',k,r,len(profiles),flush=True)
    check(raw_count==rec['counts']['raw_labeled_nonzero_source_columns'] and colhash.hexdigest()==rec['full_column_transcript_sha256'],'column transcript')
    states=rec['states'];check(states[0]==0 and len(set(states))==len(states) and all(0<=s<rb for s in states),'safe support list')
    idx={s:i for i,s in enumerate(states)};h=list(map(Fraction,rec['potential']))
    check(len(h)==len(states) and all(x>0 for x in h),'positive potential')
    B=rec['target']['base'];pwr=rec['target']['root'];check(B>1 and pwr>0,'target typing')
    queue=deque([0]);seen={0};order=[0];safe=bad=0;best={};trace=sha256()
    while queue:
        R=queue.popleft();u=idx[R];active=[i for i in range(len(O)) if R>>i&1]
        for li in valid:
            p=profiles[li];T=p['initial']
            for i in active:T|=p['transfers'][i]
            trace.update((repr((u,li,T))+'\n').encode())
            if T&rb:bad+=1;continue
            safe+=1;check(T in idx,'unlisted reachable support');v=idx[T];b=p['base'];n=len(p['generators'])
            check(b**pwr*h[v]>=B**n*h[u],'all-edge potential inequality')
            key=(u,v,n)
            if key not in best or b<best[key][2]:best[key]=[u,v,b,n,li]
            if T not in seen:seen.add(T);order.append(T);queue.append(T)
    check(order==states,'BFS support coverage/order')
    check(sorted(best.values())==rec['representative_edges'],'parallel-edge cost summary')
    check(trace.hexdigest()==rec['controller_transcript_sha256'],'controller transcript')
    count=rec['counts'];check(count['safe_transfers']==safe and count['rejected_transfers']==bad and count['dictionary_labels']==len(profiles) and count['usable_labels']==len(valid) and count['integer_obstructions']==invalid and count['reachable_states']==len(states) and count['cost_representative_edges']==len(best),'count report')
    at=rec['attainment'];period=[(b,tuple(A)) for b,A in at['period']];ids=[expected.index(p) for p in period]
    CB=prod(b for b,A in period);CN=sum(len(A) for b,A in period)
    check(CN>0 and CB**pwr==B**CN,'period exact rate')
    seenphase={};R=0;j=0;visited=[]
    while (j%len(period),R) not in seenphase:
        seenphase[j%len(period),R]=j;visited.append(idx[R]);p=profiles[ids[j%len(period)]];T=p['initial']
        for i in range(len(O)):
            if R>>i&1:T|=p['transfers'][i]
        check(not T&rb,'period unsafe');R=T;j+=1
    start=seenphase[j%len(period),R]
    check(at['visited_states']==visited and at['cycle_start']==start and at['cycle_label_ids']==[ids[t%len(period)] for t in range(start,j)],'attainment trace')
    return {'status':'PASS','k':k,'rank':r,'target':rec['target'],'literal_labels':len(profiles),'valid_source_carries':all_carry_checks,
            'nonzero_source_labeled_columns':raw_count,'all_safe_controller_transfers':safe,'all_rejected_controller_transfers':bad,
            'safe_supports':len(states),'attainment_period':at['period'],
            'scope':'Independent exact full-domain, fibre, column, support, potential and periodic-attainment replay; no external human review or Lean claim.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('receipt',type=Path);ap.add_argument('--producer',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    raw=gzip.decompress(a.receipt.read_bytes()) if a.receipt.suffix=='.gz' else a.receipt.read_bytes()
    report=audit(json.loads(raw),sha256(a.producer.read_bytes()).hexdigest(),True)
    report.update({'auditor_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'producer_sha256':sha256(a.producer.read_bytes()).hexdigest(),
                   'plain_receipt_sha256':sha256(raw).hexdigest(),'receipt_file_sha256':sha256(a.receipt.read_bytes()).hexdigest()})
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,sort_keys=True),flush=True)
if __name__=='__main__':main()
