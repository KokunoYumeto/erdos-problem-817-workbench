#!/usr/bin/env python3
"""Independent arithmetic audit of the two full rank-five proof records.

Does not import either producer. Accepts plain JSON or lossless gzip JSON.
Checks coverage, actual digit images, return primitives, every retained and
excluded controller transfer, exact potentials, and the upper witnesses.
"""
from __future__ import annotations
import argparse, gzip, json
from collections import deque
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path


def check(ok, message):
    if not ok:raise AssertionError(message)


def all_blocks(n,budget,first=1,prefix=()):
    if n==0:
        yield prefix;return
    for x in range(first,budget+1):
        if n*x+n*(n-1)//2>budget:return
        yield from all_blocks(n-1,budget-x,x+1,prefix+(x,))


def digits(a):
    return {sum(w for w,bit in zip(a,bits) if bit) for bits in product((0,1),repeat=len(a))}


def delta(col):return tuple(col[i]+col[i+2]-2*col[i+1] for i in range(len(col)-2))


def columns_from(c,D,b):
    # Extension scans the actual admitted digits instead of taking a residue
    # representative as the producer does. Canonical digits give at most one.
    for x in D:
        for y in D:
            col=[x,y];target=[]
            for ci in c:
                matches=[z for z in D if (col[-2]+z-2*col[-1]+ci)%b==0]
                check(len(matches)<=1,'noncanonical or multiple residue choices')
                if not matches:break
                z=matches[0];target.append((col[-2]+z-2*col[-1]+ci)//b);col.append(z)
            else:yield tuple(target),tuple(col)


def mod_safe(D,b,k):
    return not any(all((x+j*d)%b in D for j in range(k)) for x in D for d in range(1,b))


def audit(path):
    raw=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
    record=json.loads(raw);r=record['result'];k=r['k'];Q=r['benchmark_base']
    expected=list(all_blocks(5,Q-1));lo,hi=r['evaluated_indices']
    check(0<=lo<hi<=len(expected) and r['complete_domain_size']==len(expected),'invalid audited interval')
    check([tuple(e['generators']) for e in r['domain']]==expected[lo:hi],'domain omission/reorder/duplication')
    zero=(0,)*(k-2);C=set(product((-1,0,1),repeat=k-2))
    statistics={'generators':hi-lo,'integer_obstructions':0,'return_rows':0,
                'bad_base_witnesses':0,'controller_transfers':0,'potential_edges':0,
                'complete_return_blocks':0,'controller_blocks':0}
    for entry in r['domain']:
        a=entry['generators'];D=digits(a);S=sum(a)
        if 'integer_obstruction' in entry:
            col=entry['integer_obstruction']
            check(len(col)==k and all(x in D for x in col) and col[1]!=col[0] and delta(col)==zero,
                  'invalid integer obstruction')
            statistics['integer_obstructions']+=1;continue
        full=entry['method']=='complete_return';section=entry['section'] if full else entry['return_section']
        f={tuple(c):tuple(col) for c,col in section}
        check(len(f)==len(section),'duplicate section row')
        for c,col in f.items():
            check(c in C and len(col)==k and all(x in D for x in col) and delta(col)==tuple(-x for x in c),
                  'section primitive does not return')
        statistics['return_rows']+=len(f)
        if full:
            statistics['complete_return_blocks']+=1;check(set(f)==C,'incomplete claimed total section')
            B=entry['best']['product'];check(entry['best']['length']==1 and B>=Q,'insufficient complete-return lower bound')
            ws=entry['smaller_base_obstructions']
            check([w['base'] for w in ws]==list(range(S+1,B)),'bad-base interval incomplete')
            for w in ws:
                b=w['base'];low_column=w['low'];high_column=w['high'];points=w['points']
                check(len(low_column)==k and len(high_column)==k and all(x in D for x in low_column+high_column),'bad digits')
                check(points==[low_column[i]+b*high_column[i] for i in range(k)] and points[1]!=points[0] and delta(points)==zero,
                      'integer bad-base witness failed')
                statistics['bad_base_witnesses']+=1
            check(mod_safe(D,B,k),'claimed first safe modulus fails')
        else:
            statistics['controller_blocks']+=1
            # Every omitted carry really lacks an integer return primitive.
            for c in C-set(f):
                check(not any(t==zero for t,col in columns_from(c,tuple(sorted(D)),2*S+2)),
                      'return set missing a primitive')
            states=[frozenset(tuple(c) for c in R) for R in entry['states']]
            check(len(states)==len(set(states)) and states[0]==frozenset(),'invalid state inventory')
            check(all(R<=C and not R.intersection(f) for R in states),'state meets returned support')
            edges=entry['edges'];by={(s,b):t for s,t,b in edges}
            check(len(by)==len(edges),'duplicate edge label')
            discarded={(s,b):(frozenset(tuple(c) for c in T),tuple(c),tuple(col))
                       for s,b,T,c,col in entry['discarded_edges']}
            check(len(discarded)==len(entry['discarded_edges']),'duplicate discarded edge')
            check(not set(by).intersection(discarded),'edge both retained and discarded')
            ds=tuple(sorted(D));successor={}
            # Only actual supported incoming carries are needed for the audit.
            admitted={zero}.union(*(set(R) for R in states))
            for b in range(S+1,2*S+3):
                for c in admitted:successor[b,c]=list(columns_from(c,ds,b))
                initial={t for t,col in successor[b,zero] if col[0]!=col[1]}
                for s,R in enumerate(states):
                    T=set(initial)
                    for c in R:T.update(t for t,col in successor[b,c])
                    if T.intersection(f):
                        check((s,b) in discarded and (s,b) not in by,'forced return edge retained')
                        stored,c,col=discarded[s,b]
                        check(stored==frozenset(T) and c in T and c in f and col==f[c],
                              'discarded support or primitive changed')
                    else:
                        check((s,b) in by and states[by[s,b]]==frozenset(T),'viable transfer not exact')
                    statistics['controller_transfers']+=1
            reachable={0};queue=deque([0])
            while queue:
                s=queue.popleft()
                for ss,t,b in edges:
                    if ss==s and t not in reachable:reachable.add(t);queue.append(t)
            check(reachable==set(range(len(states))),'unreachable state in inventory')
            h=list(map(Fraction,entry['potential']))
            check(len(h)==len(states) and all(x>0 for x in h),'invalid positive potential')
            for s,t,b in edges:
                check(b*h[t]>=Q*h[s],'potential inequality failed')
                statistics['potential_edges']+=1
    A=r['benchmark_generators'];check(len(A)==5 and tuple(sorted(set(A)))==tuple(A),'benchmark generators')
    check(sum(A)<Q and mod_safe(digits(A),Q,k),'global upper certificate failed')
    check(statistics['complete_return_blocks']==r['complete_return'] and statistics['controller_blocks']==r['full_controllers'],
          'block totals differ')
    return {'k':k,'status':'PASS','audited_indices':[lo,hi],'complete_domain_size':len(expected),
            'capacity_target':f'{Q}^(1/5)','counts':statistics,
            'plain_receipt_sha256':sha256(raw).hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('receipts',nargs='+',type=Path)
    p.add_argument('--output',type=Path);args=p.parse_args()
    out={'schema':'ep817-rank-five-independent-audit-v1','status':'PASS','lean_checked':False,
         'results':[audit(x) for x in args.receipts],
         'auditor_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':main()
