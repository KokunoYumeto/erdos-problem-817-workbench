#!/usr/bin/env python3
"""Exact bounded replay of the observation-faithful graph quotient.

Original edge labels and every orientation mask are retained. This program
uses no other contribution module. General proofs are in the companion note.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def components(n: int, edges: list[tuple[int,int]]) -> list[list[int]]:
    unseen=set(range(n)); result=[]
    while unseen:
        seed=min(unseen); unseen.remove(seed); stack=[seed]; c=[]
        while stack:
            u=stack.pop(); c.append(u)
            for a,b in edges:
                v=b if a==u else a if b==u else None
                if v in unseen: unseen.remove(v); stack.append(v)
        result.append(sorted(c))
    return result


def rank(rows: list[list[int]]) -> int:
    if not rows: return 0
    a=[list(map(Fraction,row)) for row in rows]; r=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][j]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]; q=a[r][j]; a[r]=[x/q for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][j]:
                q=a[i][j]; a[i]=[x-q*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r


def cycle_basis(n: int, edges: list[tuple[int,int]]) -> list[list[int]]:
    # Fundamental cycles in literal edge coordinates, with a specified forest.
    parent=list(range(n)); adjacency=[[] for _ in range(n)]; cycles=[]
    def find(x):
        while parent[x]!=x: x=parent[x]
        return x
    for j,(u,v) in enumerate(edges):
        a,b=find(u),find(v)
        if a!=b:
            parent[b]=a
            adjacency[u].append((v,j,1)); adjacency[v].append((u,j,-1))
        else:
            seen={v}; todo=[(v,[])]; path=None
            while todo:
                x,p=todo.pop()
                if x==u: path=p;break
                for y,i,sign in adjacency[x]:
                    if y not in seen:seen.add(y);todo.append((y,p+[(i,sign)]))
            require(path is not None,'forest path missing')
            c=[0]*len(edges);c[j]=1
            for i,sign in path:c[i]=sign
            cycles.append(c)
    return cycles


def boundary(n: int, edges: list[tuple[int,int]], c: list[int]) -> list[int]:
    z=[0]*n
    for x,(u,v) in zip(c,edges):z[u]-=x;z[v]+=x
    return z


def score_masks(n: int, edges: list[tuple[int,int]]) -> Counter:
    out=Counter()
    for mask in range(1<<len(edges)):
        s=[0]*n
        for j,(u,v) in enumerate(edges):s[v if mask>>j&1 else u]+=1
        out[tuple(s)]+=1
    return out


def check(n: int, edges: list[tuple[int,int]], marks: tuple[int,...], masks=True) -> dict:
    require(len(marks)==n,'mark type mismatch')
    weights=[abs(marks[v]-marks[u]) for u,v in edges]
    require(all(weights) and len(set(weights))==len(weights),'not a positive distinct edge image')
    levels=sorted(set(marks)); index={x:i for i,x in enumerate(levels)}
    p=[index[t] for t in marks]; m=len(levels)
    quotient=[(p[u],p[v]) for u,v in edges]
    require(all(u!=v for u,v in quotient),'loop was lost')
    require(len({tuple(sorted(e)) for e in quotient})==len(edges),'parallel edge was lost')
    require(weights==[abs(levels[v]-levels[u]) for u,v in quotient],'original weight changed')
    def push(z):
        out=[0]*m
        for u,x in enumerate(z):out[p[u]]+=x
        return out
    for j in range(len(edges)):
        c=[int(i==j) for i in range(len(edges))]
        require(push(boundary(n,edges,c))==boundary(m,quotient,c),'chain square failed')
    old=cycle_basis(n,edges); new=cycle_basis(m,quotient)
    for c in old:
        require(boundary(n,edges,c)==[0]*n and boundary(m,quotient,c)==[0]*m,'cycle inclusion failed')
    defects=[boundary(n,edges,c) for c in new]
    for c,z in zip(new,defects):
        require(boundary(m,quotient,c)==[0]*m and push(z)==[0]*m,'relative cycle defect lost')
        require(sum(x*t for x,t in zip(z,marks))==0,'relative defect action nonzero')
    expected=(n-len(components(n,edges)))-(m-len(components(m,quotient)))
    require(rank(defects)==expected==len(new)-len(old),'relative exact-sequence rank failed')
    require(rank(new)==len(new) and rank(old)==len(old),'cycle basis rank failed')
    mass=0; source_values=target_values=0
    if masks:
        source=score_masks(n,edges); target=score_masks(m,quotient); pushed=Counter()
        for s,multiplicity in source.items():pushed[tuple(push(s))]+=multiplicity
        require(pushed==target,'full mask multiplicity pushforward failed')
        source_values=len(source);target_values=len(target);mass=sum(source.values())
        groups=defaultdict(list)
        for s,mu in source.items():groups[tuple(push(s))].append((s,mu))
        for y,fibre in groups.items():
            total=target[y]
            gram=sum(Fraction(mu,total)**2/Fraction(mu) for _,mu in fibre)
            require(gram==Fraction(1,total),'original quotient metric return failed')
            require(sum(Fraction(mu,total) for _,mu in fibre)==1,'minimum section not a right inverse')
    return {'vertices':n,'edges':[list(e) for e in edges],'marks':list(marks),
            'observed_vertices':m,'vertex_map':p,'quotient_edges':[list(e) for e in quotient],
            'old_cycle_rank':len(old),'quotient_cycle_rank':len(new),
            'retained_relative_rank':expected,'source_score_values':source_values,
            'quotient_score_values':target_values,'word_mass':mass}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    rows=[];candidates=0
    for n in range(1,6):
        all_edges=list(combinations(range(n),2))
        marks_list=[tuple(2**i for i in range(n))]
        if n>=2:marks_list.append(tuple(0 if i<2 else 2**i for i in range(n)))
        for bits in range(1<<len(all_edges)):
            edges=[e for j,e in enumerate(all_edges) if bits>>j&1]
            for marks in marks_list:
                candidates+=1;w=[abs(marks[u]-marks[v]) for u,v in edges]
                if all(w) and len(set(w))==len(w):rows.append(check(n,edges,marks))
    theta=[]
    for r in range(1,13):
        edges=[];marks=[0,0]
        for j in range(r):
            a,b=2+2*j,3+2*j;marks.extend([19**j,8*19**j])
            edges.extend([(0,a),(a,b),(1,b)])
        rec=check(2+2*r,edges,tuple(marks),masks=r<=4)
        require(rec['old_cycle_rank']==r-1 and rec['quotient_cycle_rank']==r,'theta relative class lost')
        theta.append(rec)
    mutations=[]
    for name,fn in [
        ('delete the new relative class',lambda:require(theta[-1]['retained_relative_rank']==0,'relative class retained')),
        ('identify unequal arithmetic marks',lambda:check(3,[(0,1),(1,2)],(0,0,2))),
        ('silently merge repeated edge weights',lambda:check(3,[(0,1),(0,2)],(0,1,1))),
        ('replace weighted quotient metric by unit mass',lambda:require(Fraction(1,2)==1,'original metric required'))]:
        try:fn()
        except AssertionError:mutations.append(name)
        else:raise AssertionError('false comparison accepted: '+name)
    raw=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode()
    report={'schema':'ep817-observation-quotient-v1','status':'PASS','lean_checked':False,
            'scope':'all labelled simple graphs on 1..5 vertices, the two explicitly specified mark families, retaining only positive distinct edge images',
            'candidates':candidates,'admitted_cases':len(rows),'orientation_masks_checked':sum(x['word_mass'] for x in rows),
            'source_score_values':sum(x['source_score_values'] for x in rows),'quotient_score_values':sum(x['quotient_score_values'] for x in rows),
            'transcript_sha256':sha256(raw).hexdigest(),'theta_scope':'r=1..12 full relative incidence; original masks and quotient metrics for r<=4',
            'theta_cases':theta,'false_formulas_rejected':mutations,
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:report[k] for k in ['status','admitted_cases','orientation_masks_checked','transcript_sha256']},indent=2))

if __name__=='__main__':main()
