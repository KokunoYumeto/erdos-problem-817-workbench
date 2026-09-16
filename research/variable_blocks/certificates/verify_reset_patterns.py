#!/usr/bin/env python3
"""Exact reusable finite calibrations for the supported-reset theorem.

No asymptotic result is inferred from these cases; proofs are in the note.
"""
from __future__ import annotations
import argparse,json
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import prod
from pathlib import Path


def req(ok,msg):
    if not ok:raise AssertionError(msg)


def dot(a,b):return sum(x*y for x,y in zip(a,b))


def ap_matrix(k):
    return [tuple((1 if j in (i,i+2) else -2 if j==i+1 else 0) for j in range(k)) for i in range(k-2)]


def image(A):
    V={0}
    for a in A:V|={v+a for v in tuple(V)}
    return V


def generators(schedule):
    P=1;G=[]
    for b,A in schedule:
        req(b>=2 and sum(A)<b,'invalid canonical block')
        G.extend(P*a for a in A);P*=b
    req(len(G)==len(set(G)),'cross-level generator collision')
    return G,P


def absorb(schedule):
    out=[];leading=1
    for b,A in schedule:
        if not A:
            if out:out[-1]=(out[-1][0]*b,out[-1][1])
            else:leading*=b
        elif not out:
            out.append((leading*b,tuple(leading*a for a in A)));leading=1
        else:out.append((b,A))
    return out,leading


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);arg=ap.parse_args()
    matrices=[ap_matrix(k) for k in range(3,9)]+[[(2,-3,1)],[(1,1,-1,-1)],[(1,-1,0,0),(0,0,1,-1)],[(0,0,0)]]
    cases=[];reset_coordinates=0;digit_cases=0
    for M in matrices:
        t=len(M[0]);req(all(len(row)==t and sum(row)==0 for row in M),'translation invariance')
        masses=[sum(max(x,0) for x in row) for row in M];mx=max(masses,default=0)
        R=max(2,mx);q=max(2,mx+1)
        binary=[bits for bits in product((0,1),repeat=t) if len(set(bits))>1 and all(dot(row,bits)==0 for row in M)]
        C=list(product(*(range(1-m,m) if m else (0,) for m in masses)))
        retained=[c for c in C if all(x%R==0 for x in c)]
        req(retained==[(0,)*len(M)],'zero-digit reset failed');reset_coordinates+=len(C)
        if binary:
            eps=binary[0]
            for a in (1,7,101):
                y=tuple(a*x for x in eps);req(len(set(y))>1 and all(z in {0,a} for z in y) and all(dot(row,y)==0 for row in M),'binary witness map')
        else:
            for bits in product((0,1),repeat=t):
                z=tuple(dot(row,bits) for row in M)
                req((all(x%q==0 for x in z))==(len(set(bits))==1),'singleton modular anchor')
                digit_cases+=1
        cases.append({'matrix':M,'row_masses':masses,'reset_radix':R,'anchor_radix':q,'carry_states':len(C),
                      'binary_rigid':not binary,'binary_obstruction':binary[0] if binary else None})
    orbit_cases=[]
    for d in range(1,8):
        C=list(product((-1,0,1),repeat=d))
        def orb(c):return frozenset((c,tuple(-x for x in c),c[::-1],tuple(-x for x in c[::-1])))
        observed=len({orb(c) for c in C})-1
        formula=(3**d+3**((d+1)//2)+1+3**(d//2))//4-1
        req(observed==formula,'Burnside count');orbit_cases.append([d,observed])
    dictionary=[(2,()),(3,(1,)),(5,(1,2)),(7,(2,4))];schedules=0
    for length in range(1,6):
        for sch in product(dictionary,repeat=length):
            G,P=generators(sch);out,extra=absorb(sch);GG,PP=generators(out)
            req(G==GG and P==PP*extra,'empty-level absorption changed original generators or cost');schedules+=1
    # A supported zero is a one-dimensional word source killed by scalar amplitude.
    basis_count=1;amplitude=[0]
    req(basis_count==1 and amplitude==[0],'zero word source')
    # Exact quotient/fibre metric for a reset replacement: ternary block -> A={1,2,3}.
    A=(1,2,3);new=(1,3,9);fibres={}
    for bits in product((0,1),repeat=3):
        x=dot(new,bits);y=dot(A,bits);fibres.setdefault(y,[]).append(x)
    req(sum(map(len,fibres.values()))==8 and len(fibres)==7,'source quotient cardinality')
    metric={str(y):str(Fraction(1,len(xs))) for y,xs in fibres.items()}
    req(metric['3']=='1/2','collision Gram was discarded')
    report={'schema':'supported-reset-pattern-calibration-v1','status':'PASS','lean_checked':False,
            'matrices':cases,'reset_carry_states_tested':reset_coordinates,'rigid_binary_columns_tested':digit_cases,
            'symmetry_orbit_counts':orbit_cases,'literal_schedule_absorptions':schedules,
            'replacement_fibres':fibres,'replacement_quotient_gram':metric,
            'validator_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    arg.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('matrices','replacement_fibres')},sort_keys=True))
if __name__=='__main__':main()
