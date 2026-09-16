#!/usr/bin/env python3
"""Independent direct subset-image tests of graph-core isolation with reservoirs."""
from __future__ import annotations
import json
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
from itertools import product

def require(x,m):
    if not x:raise ValueError(m)

def image(A):
    C={0:1}
    for a in A:
        old=list(C.items())
        for v,n in old:C[v+a]=C.get(v+a,0)+n
    return C

def ap(P,k=5):
    b=sum(1<<x for x in P);top=max(P)
    for d in range(1,top//(k-1)+1):
        z=b
        for j in range(1,k):
            z &= b>>(j*d)
            if not z:break
        if z:
            lo=(z & -z).bit_length()-1
            vals=tuple(lo+j*d for j in range(k))
            require(all(v in P for v in vals),'bit witness outside actual image')
            return vals
    return None

def variance(P):
    n=len(P);a=Fraction(sum(P),n)
    return sum((Fraction(x)-a)**2 for x in P)/n

def main():
    T=(0,1,5,25,125,625)
    blocks=[('K4',(1,4,5,17,21,22),300),('K33',tuple(abs(T[j]-T[i]) for i in range(3) for j in range(3,6)),5000)]
    out=[];transcript=sha256()
    for name,A,maximum in blocks:
        D=image(A);require(ap(D) is None,'bad initial core')
        safe=bad=coupled=0
        for b in range(1,maximum+1):
            if b in A:continue
            P=set(D)|{x+b for x in D};w=ap(P);collision=len(P)<2*len(D)
            if w is None:
                safe+=1;require(not collision,'admissible core coupled to singleton reservoir')
            else:bad+=1
            coupled+=collision
            transcript.update((repr((name,b,collision,w))+'\n').encode())
        R=2*sum(A)+1;B=(R,2*R);E=image(B);full=image(A+B)
        require(ap(full) is None,'separated reservoir not admissible')
        require(len(full)==len(D)*len(E),'value-product cardinality failed')
        for x,m in D.items():
            for y,n in E.items():require(full[x+y]==m*n,'representation product failed')
        require(variance(full)==variance(D)+variance(E),'unweighted variance sum failed')
        out.append({'source':name,'weights':A,'singleton_domain':[1,maximum],
                    'distinct_extensions':safe+bad,'admissible':safe,'inadmissible':bad,
                    'binary_coupling_obstructions':coupled,'separated_reservoir':B,
                    'separated_image_cardinality':len(full),'variance':str(variance(full))})
    result={'status':'PASS','scope':'direct finite singleton extensions and specified two-generator reservoirs',
            'cases':out,'transcript_sha256':transcript.hexdigest(),'lean_checked':False,
            'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(result,sort_keys=True,indent=2)+'\n';Path(__file__).with_name('reservoir_receipt.json').write_text(text);print(text,end='')
if __name__=='__main__':main()
