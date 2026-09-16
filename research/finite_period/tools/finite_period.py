#!/usr/bin/env python3
"""Exact finite-word enclosures for numerical subset-sum image switching.

Only the standard library is used. No root rounding is used for comparisons.
The code never discards an original radix or a generator reward.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations, product
from collections import defaultdict, Counter
from hashlib import sha256
import json


def require(ok: bool, message: str) -> None:
    if not ok: raise AssertionError(message)


def image(weights: tuple[int,...], q: int) -> tuple[int,...]:
    require(q>=2,'coefficient arity must be at least two')
    values={0}
    for a in weights:
        require(a>0,'positive generator required')
        values={x+c*a for x in values for c in range(q)}
    return tuple(sorted(values))


def shapes(q: int) -> tuple[tuple[int,...],...]:
    require(q>=2,'invalid arity')
    ans=set()
    for mask in range(1<<(q-2)):
        R=(0,)+tuple(i+1 for i in range(q-2) if mask>>i&1)
        reflected=tuple(sorted(R[-1]-r for r in R))
        ans.add(min(R,reflected))
    return tuple(sorted(ans,key=lambda R:(R[-1],len(R),R)))


def matrix(weights: tuple[int,...], b: int, q: int) -> tuple[tuple[int,...],...]:
    require(bool(weights) and tuple(sorted(set(weights)))==weights,'distinct ordered weights')
    require(b>sum(weights),'original canonical radix condition failed')
    D=image(weights,q); Rs=shapes(q); index={R:i for i,R in enumerate(Rs)};out=[]
    for R in Rs:
        fibers=defaultdict(set)
        for x in {d+r for d in D for r in R}:fibers[x%b].add(x//b)
        row=[0]*len(Rs)
        for fiber in fibers.values():
            h=min(fiber); S=tuple(sorted(x-h for x in fiber))
            ref=tuple(sorted(S[-1]-x for x in S));S=min(S,ref)
            require(S in index,'receiving shift shape left proved domain')
            row[index[S]]+=1
        out.append(tuple(row))
    return tuple(out)


def row_times(row, M):
    out=[0]*len(M)
    for i,c in enumerate(row):
        if c:
            for j,m in enumerate(M[i]):out[j]+=c*m
    return tuple(out)


def value(row,q):return sum(c*len(R) for c,R in zip(row,shapes(q)))


def root_compare(a:int,da:int,na:int,b:int,db:int,nb:int)->int:
    """Compare (a/da)**(1/na) and (b/db)**(1/nb) without root arithmetic."""
    require(min(a,da,na,b,db,nb)>0,'invalid positive algebraic base')
    left=a**nb*db**na;right=b**na*da**nb
    return (left>right)-(left<right)


def root_interval(a:int,d:int,n:int,bits:int=36)->list[str]:
    """Outward dyadic interval; endpoints are independently checkable integers."""
    scale=1<<bits;lo=0;hi=scale
    while hi**n*d<a*scale**n:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**n*d<=a*scale**n:lo=mid
        else:hi=mid
    require(lo**n*d<=a*scale**n<=hi**n*d,'root bracket failed')
    return [str(Fraction(lo,scale)),str(Fraction(hi,scale))]


def modular_witness(weights,b,k):
    D=set(image(weights,2))
    for a in range(b):
        for d in range(1,b):
            if all((a+i*d)%b in D for i in range(k)):return (a,d)
    return None


def actual_generators(dictionary,word):
    P=1;out=[]
    for i in word:
        b,A=dictionary[i];out.extend(P*a for a in A);P*=b
    require(len(set(out))==len(out),'cross-level generator collision')
    return tuple(sorted(out)),P


def finite_enclosures(dictionary,q,max_length):
    Ms=[matrix(A,b,q) for b,A in dictionary]
    initial=(1,)+(0,)*(len(Ms[0])-1)
    # Exact row/reward aggregation preserves every literal word count.
    states={(initial,0):('',1)};records=[];digest=sha256()
    for m in range(1,max_length+1):
        nxt={}
        for (row,n),(word,mult) in states.items():
            for i,M in enumerate(Ms):
                newrow=row_times(row,M);key=(newrow,n+len(dictionary[i][1]));newword=word+chr(65+i)
                if key in nxt:nxt[key]=(min(nxt[key][0],newword),nxt[key][1]+mult)
                else:nxt[key]=(newword,mult)
        states=nxt
        upper=lower=None
        for (row,n),(word,mult) in states.items():
            v=value(row,q)
            rec=(v,n,word)
            if upper is None or root_compare(v,1,n,upper[0],1,upper[1])<0 or (root_compare(v,1,n,upper[0],1,upper[1])==0 and word<upper[2]):upper=rec
            if lower is None or root_compare(v,q-1,n,lower[0],q-1,lower[1])<0 or (root_compare(v,q-1,n,lower[0],q-1,lower[1])==0 and word<lower[2]):lower=rec
        require(sum(x[1] for x in states.values())==len(dictionary)**m,'word count lost')
        def rec(v,den):return {'image_count':v[0],'denominator':den,'generator_reward':v[1],'word':v[2],'root_interval':root_interval(v[0],den,v[1])}
        record={'length':m,'literal_words':len(dictionary)**m,'distinct_row_reward_states':len(states),'lower':rec(lower,q-1),'upper':rec(upper,1)}
        digest.update((json.dumps(record,sort_keys=True)+'\n').encode());records.append(record)
    return {'q':q,'dictionary':[{'radix':b,'weights':list(A),'reward':len(A)} for b,A in dictionary], 'matrices':[[list(r) for r in M] for M in Ms], 'records':records, 'transcript_sha256':digest.hexdigest()}


def radix_ten_minimum(m):
    require(m>=0,'negative word length')
    if m==0:return 1
    if m==1:return 13
    q,r=divmod(m,3)
    if r==0:return 893**q
    if r==1:return 93**2*893**(q-1)
    return 93*893**q


def attaining_word(m):
    if m==0:return ''
    if m==1:return 'B'
    q,r=divmod(m,3)
    if r==0:return 'BAA'*q
    if r==1:return 'BABA'+'BAA'*(q-1)
    return 'BA'+'BAA'*q


def word_value(dictionary,word,q):
    Ms=[matrix(A,b,q) for b,A in dictionary];row=(1,)+(0,)*(len(Ms[0])-1);reward=0
    for x in word:
        i=ord(x)-65;row=row_times(row,Ms[i]);reward+=len(dictionary[i][1])
    return value(row,q),reward
