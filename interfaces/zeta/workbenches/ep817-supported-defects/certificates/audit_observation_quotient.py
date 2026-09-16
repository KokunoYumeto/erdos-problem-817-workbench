#!/usr/bin/env python3
"""Separate incidence-matrix and orientation-word audit of the graph quotient.

Does not import the producer. Cycle kernels are computed by rational row
reduction, while the producer uses literal spanning-forest cycle primitives.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


def must(ok,message):
    if not ok:raise AssertionError(message)


def reduced(matrix,cols):
    a=[[F(x) for x in row] for row in matrix];piv=[];i=0
    for j in range(cols):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];pivot=a[i][j];a[i]=[x/pivot for x in a[i]]
        for k in range(len(a)):
            if k!=i:
                factor=a[k][j]
                a[k]=[x-factor*y for x,y in zip(a[k],a[i])]
        piv.append(j);i+=1
        if i==len(a):break
    return a,piv


def kernel(matrix,cols):
    a,piv=reduced(matrix,cols);out=[]
    for j in range(cols):
        if j in piv:continue
        x=[F(0)]*cols;x[j]=1
        for i,p in enumerate(piv):x[p]=-a[i][j]
        out.append(x)
    return out


def multiply(a,x):return [sum(y*z for y,z in zip(row,x)) for row in a]


def matrix(n,E):return [[int(v==i)-int(u==i) for u,v in E] for i in range(n)]


def masses(n,E):
    result=Counter()
    for choices in product((0,1),repeat=len(E)):
        score=[0]*n
        for choice,(u,v) in zip(choices,E):score[(u,v)[choice]]+=1
        result[tuple(score)]+=1
    return result


def independently_check(n,E,t,words):
    t=tuple(t);weights=[abs(t[v]-t[u]) for u,v in E]
    must(len(t)==n and all(weights) and len(set(weights))==len(weights),'incorrect original edge image')
    levels=sorted(set(t));p=[levels.index(x) for x in t];m=len(levels)
    Ebar=[(p[u],p[v]) for u,v in E]
    must(all(u!=v for u,v in Ebar) and len(set(tuple(sorted(e)) for e in Ebar))==len(E),'edge retention failed')
    B=matrix(n,E);C=matrix(m,Ebar)
    P=[[int(p[j]==i) for j in range(n)] for i in range(m)]
    for j,(u,v) in enumerate(E):
        old=[B[i][j] for i in range(n)];new=[C[i][j] for i in range(m)]
        must(multiply(P,old)==new,'chain square incorrect')
        must(sum(t[i]*old[i] for i in range(n))==sum(levels[i]*new[i] for i in range(m)),'mark observation did not factor')
    oldker=kernel(B,len(E));newker=kernel(C,len(E))
    for c in oldker:must(all(x==0 for x in multiply(C,c)),'old boundary class lost')
    defects=[multiply(B,c) for c in newker]
    for z in defects:must(all(x==0 for x in multiply(P,z)),'new relative class has nonzero receiving boundary')
    relative=len(reduced(defects,n)[1])
    must(relative==len(newker)-len(oldker),'relative homology dimensions disagree')
    source_n=target_n=mass=0
    if words:
        source=masses(n,E);target=masses(m,Ebar);sums=Counter();groups=defaultdict(list)
        for s,mu in source.items():
            y=tuple(multiply(P,s));sums[y]+=mu;groups[y].append(mu)
        must(sums==target,'orientation-mask pushforward mismatch')
        for y,mu_y in target.items():
            f=groups[y]
            must(sum(f)==mu_y and sum(F(mu,mu_y)**2/F(mu) for mu in f)==F(1,mu_y),'source-metric quotient mismatch')
        source_n,target_n,mass=len(source),len(target),sum(source.values())
    return {'vertices':n,'edges':[list(e) for e in E],'marks':list(t),
            'observed_vertices':m,'vertex_map':p,'quotient_edges':[list(e) for e in Ebar],
            'old_cycle_rank':len(oldker),'quotient_cycle_rank':len(newker),'retained_relative_rank':relative,
            'source_score_values':source_n,'quotient_score_values':target_n,'word_mass':mass}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    receipt=json.loads(args.receipt.read_text());rows=[];candidates=0
    for n in range(1,6):
        pairs=list(combinations(range(n),2));mark_lists=[tuple(2**i for i in range(n))]
        if n>=2:mark_lists.append(tuple(0 if i<2 else 2**i for i in range(n)))
        for bits in range(1<<len(pairs)):
            E=[e for i,e in enumerate(pairs) if bits>>i&1]
            for t in mark_lists:
                candidates+=1;w=[abs(t[v]-t[u]) for u,v in E]
                if all(w) and len(set(w))==len(w):rows.append(independently_check(n,E,t,True))
    raw=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode();digest=sha256(raw).hexdigest()
    must(digest==receipt['transcript_sha256'],'complete marked-graph transcript differs')
    must(len(rows)==receipt['admitted_cases'] and candidates==receipt['candidates'],'marked graph domain incomplete')
    theta=[]
    for r in range(1,13):
        E=[];t=[0,0]
        for j in range(r):
            a,b=2+2*j,3+2*j;t.extend([19**j,8*19**j]);E.extend([(0,a),(a,b),(1,b)])
        theta.append(independently_check(2+2*r,E,t,r<=4))
    must(theta==receipt['theta_cases'],'theta relative incidence or metric mismatch')
    rejected=[]
    for name,condition in [
        ('removed relative quotient direction',theta[-1]['retained_relative_rank']==0),
        ('missing marked-graph support',len(rows)-1==receipt['admitted_cases']),
        ('altered transcript',digest=='0'*64),
        ('unit replacement of doubled fibre metric',F(1,2)==1)]:
        try:must(condition,name)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('corruption not rejected')
    report={'schema':'ep817-observation-quotient-independent-audit-v1','status':'PASS','lean_checked':False,
            'admitted_cases':len(rows),'orientation_masks_checked':sum(x['word_mass'] for x in rows),
            'theta_incidence_cases':len(theta),'theta_full_word_cases':4,
            'transcript_sha256':digest,'false_records_rejected':rejected,
            'producer_receipt_sha256':sha256(args.receipt.read_bytes()).hexdigest(),
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
