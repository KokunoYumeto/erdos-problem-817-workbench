#!/usr/bin/env python3
"""Exact all-arity filtration calibrations for one-row positive integer kernels.

The written proof bounds every Graver element by l1 <= 2*max(A)-1.
This finite runner checks complete small input families using both conformal
primitive enumeration and independent numerical image-cardinality splitting.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json
from itertools import combinations,product
from math import gcd
from pathlib import Path

def require(ok: bool, message: str) -> None:
    if not ok: raise AssertionError(message)

def values(A,q):
    D={0}
    for a in A:D={x+j*a for x in D for j in range(q)}
    return D

def relation_candidates(A):
    M=max(A);bound=2*M-1;n=len(A)
    rows=[]
    for first in product(range(-bound,bound+1),repeat=n-1):
        size=sum(map(abs,first))
        if size>bound:continue
        t=-sum(a*x for a,x in zip(A,first))
        if t%A[-1]:continue
        last=t//A[-1];g=first+(last,)
        if any(g) and size+abs(last)<=bound:rows.append(g)
    return sorted(rows,key=lambda g:(sum(map(abs,g)),g))

def conformal(h,g):
    return all(x*y>=0 and abs(x)<=abs(y) for x,y in zip(h,g))

def graver(A):
    G=[]
    for g in relation_candidates(A):
        if not any(conformal(h,g) for h in G):G.append(g)
    return G

def verify_primitive_direct(A,g):
    whole=tuple(map(abs,g));signed=tuple(a if x>=0 else -a for a,x in zip(A,g))
    require(sum(a*x for a,x in zip(A,g))==0,'candidate not in original kernel')
    for t in product(*(range(abs(x)+1) for x in g)):
        if any(t) and t!=whole:
            require(sum(a*x for a,x in zip(signed,t))!=0,'proper conformal relation exists')

def walk(A,g):
    left=list(map(abs,g));current=0;partial=[];word=[]
    P=max(a for a,x in zip(A,g) if x>0);N=max(a for a,x in zip(A,g) if x<0)
    while any(left):
        use_positive=current<=0
        i=next(i for i in range(len(A)) if left[i] and (g[i]>0)==use_positive)
        left[i]-=1;step=A[i] if g[i]>0 else -A[i];current+=step;word.append(i)
        if any(left):partial.append(current)
    require(current==0 and all(partial) and len(set(partial))==len(partial),'zero-sum proper subword')
    require(all(1-N<=s<=P for s in partial),'literal partial sums left retained interval')
    require(len(word)<=P+N<=2*max(A)-1,'one-row size bound failed')
    return {'indices':word,'partial_sums':partial,'positive_max':P,'negative_max':N}

def components(A,G,q):
    n=len(A);parent=list(range(n))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for g in G:
        if max(map(abs,g))>=q:continue
        ids=[i for i,x in enumerate(g) if x]
        for i in ids[1:]:parent[find(i)]=find(ids[0])
    C={}
    for i in range(n):C.setdefault(find(i),[]).append(i)
    return sorted(C.values())

def by_cardinality(A,q):
    n=len(A);cache={0:1}
    def size(mask):
        if mask not in cache:cache[mask]=len(values([a for i,a in enumerate(A) if mask>>i&1],q))
        return cache[mask]
    def split(mask):
        pivot=mask&-mask;rest=mask^pivot;sub=rest
        while True:
            first=pivot|sub;other=mask^first
            if other and size(first)*size(other)==size(mask):return split(first)+split(other)
            if not sub:break
            sub=(sub-1)&rest
        return [[i for i in range(n) if mask>>i&1]]
    return sorted(split((1<<n)-1))

def run():
    records=[];total=0;comparisons=0
    for n in range(2,5):
        for A in combinations(range(1,9),n):
            G=graver(A);walks=[]
            for g in G:verify_primitive_direct(A,g);walks.append(walk(A,g))
            filtration=[];old=None
            for q in range(2,max(A)+2):
                C=components(A,G,q);require(C==by_cardinality(A,q),'filtration differs from direct image factors')
                if old is not None:require(all(any(set(B)<=set(T) for T in C) for B in old),'arity refinement reversed')
                old=C;filtration.append({'q':q,'components':C});comparisons+=1
            require(old==[list(range(n))],'explicit final merge bound failed')
            for i,j in combinations(range(n),2):
                d=gcd(A[i],A[j]);g=tuple(A[j]//d if h==i else -A[i]//d if h==j else 0 for h in range(n))
                require(g in G and max(map(abs,g))<=max(A),'pairwise primitive missing')
            records.append({'weights':A,'graver_elements':G,'retained_walks':walks,'filtration':filtration});total+=len(G)
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    return records,{'schema':'ep817-arity-filtration-v1','status':'PASS','lean_checked':False,
      'domain':{'distinct_positive_weights':[1,8],'sizes':[2,4]},'sets':len(records),
      'signed_graver_elements':total,'arity_comparisons':comparisons,
      'method':'Full bounded one-row kernel enumeration; direct conformal-subvector checks; literal alternating words; independent image-cardinality factor splitting.',
      'data_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},raw

def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=Path(__file__).parent);a=p.parse_args()
    rows,summary,raw=run();a.output_dir.mkdir(parents=True,exist_ok=True)
    (a.output_dir/'arity_filtration_data.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    text=json.dumps(summary,indent=2,sort_keys=True)+'\n';(a.output_dir/'arity_filtration_summary.json').write_text(text);print(text,end='')
if __name__=='__main__':main()
