#!/usr/bin/env python3
"""Independent integer audit. Imports neither producer nor image_tools."""
from __future__ import annotations
import argparse,copy,hashlib,json
from collections import Counter,deque
from itertools import combinations,product
from math import isqrt
from pathlib import Path

HERE=Path(__file__).resolve().parent

def check(x,msg):
    if not x:raise AssertionError(msg)

def polynomial(A,q):
    P={0:1}
    for a in A:
        Q={}
        for x,v in P.items():
            for c in range(q):Q[x+c*a]=Q.get(x+c*a,0)+v
        P=Q
    return P

def components(D):
    L=sorted(D)
    return sum(i==0 or L[i]!=L[i-1]+1 for i in range(len(L)))

def datum(D,b):
    buckets=[[] for _ in range(b)]
    for x in D:buckets[x%b].append(x//b)
    check(max(map(len,buckets))<=2,'residue multiplicity bound')
    v=sum(bool(B) for B in buckets);beta=sum(len(B)==2 for B in buckets)
    E=set(D)|{d+1 for d in D}
    vE=len({x%b for x in E});kap=components(D)
    return [[v,beta],[vE-v,kap-vE+v]]

def six_step_count(D,b):
    # Four-state residue subset automaton; not the two-state derivation.
    states=[frozenset(),frozenset({0}),frozenset({1}),frozenset({0,1})]
    index={s:i for i,s in enumerate(states)};edges=[]
    for R in states:
        row=Counter()
        for z in range(b):
            S=frozenset((d+c-z)//b for c in R for d in D if (d+c)%b==z)
            check(S in index,'carry outside original two-value alphabet')
            row[index[S]]+=1
        edges.append(row)
    vec=[0,1,0,0];counts=[]
    for _ in range(7):
        counts.append(sum(v*len(R) for v,R in zip(vec,states)))
        nxt=[0]*4
        for i,row in enumerate(edges):
            for j,mass in row.items():nxt[j]+=vec[i]*mass
        vec=nxt
    return counts

def prime(p):
    if p<2:return False
    d=2
    while d*d<=p:
        if p%d==0:return False
        d+=1
    return True

def audit_prime(r):
    A=tuple(r['weights']);h=r['coefficient_radius'];S=sum(A)
    check(A and min(A)>0 and len(set(A))==len(A),'prime source invalid')
    vals=set(polynomial(A,h+1));signed={x-h*S for x in polynomial(A,2*h+1)}
    plus=sorted(x for x in signed if x>0)
    check(len(plus)==r['exact_positive_difference_count'],'difference count altered')
    p=r['prime'];check(prime(p),'not prime')
    check(len({x%p for x in vals})==len(vals),'selected observation not injective')
    check(all(x%p for x in plus),'lost bounded nonzero relation')
    check(r['max_difference']==h*S and r['bit_budget']==(h*S).bit_length(),'height budget altered')
    bound=256+4*len(plus)*(h*S).bit_length()
    check(r['bound']==bound and p<=bound,'prime budget')
    old=[z for z in range(2,p) if prime(z)]
    check([x[0] for x in r['excluded_primes']]==old,'prime-search coverage')
    for z,w in r['excluded_primes']:
        check(w in signed and w>0 and w%z==0,'bad prime witness')
    check(r['observed_image_size']==len(vals),'observation size')
    check(r['noncanonical']==(S>=p),'actual digit range lost')
    if 'copies' in r:
        B=tuple(r['original_block']);t=r['copies'];R=4*sum(B)+1
        check(r['separation_base']==R,'amplification radix')
        check(A==tuple(R**j*a for j in range(t) for a in B),'amplification source')
        f=len(polynomial(B,5))
        check(len(polynomial(A,5))==r['five_valued_cardinality']==f**t,'tensor fibres')
        check(r['tensor_bound']==256+2*(f**t-1)*t*R.bit_length(),'quantitative tensor budget')

def audit_targets(a):
    for r in a['targets']:
        A=tuple(r['weights']);D=set(polynomial(A,3))
        if r['name']=='mixed_97_141':
            U,V=datum(D,97),datum(D,141)
            P=[[sum(U[i][k]*V[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
            check(r['matrix_97']==U and r['matrix_141']==V and r['period_matrix']==P,'mixed matrix')
            check(r['period_determinant']==P[0][0]*P[1][1]-P[0][1]*P[1][0],'mixed determinant')
            cnt=[len({d+b*e for d in D for e in D}) for b in (97,141)]
            check(cnt==r['two_level_counts_by_order'],'mixed order count')
            continue
        b=r['base'];M=datum(D,b)
        check(sorted(D)==r['digits'] and M==r['matrix'],'target full source/transfer')
        check(len(D)==r['size'] and components(D)==r['runs'],'target scalar data')
        check(r['overlap']==M[0][1] and r['cyclic_boundary']==M[1][0] and r['residues']==M[0][0], 'target overlap data')
        ns=six_step_count(D,b)
        check(ns==r['cardinalities_through_m6'],'independent residue automaton')
        check(len(D)**2-ns[2]==r['two_level_kernel'],'target quotient dimension')

def fast_receipt(a):
    check(a['status']=='PASS' and a['lean_checked'] is False,'status boundaries')
    check(a['general_digit_replay']['alphabets']==1364,'all-alphabet count')
    check(a['small_generator_blocks']['block_radix_cases']==3171,'block domain count')
    check(a['collision_horizon']['cases']==720,'horizon domain count')
    audit_targets(a)
    check(a['sparse_schedule']['prefix_checks']==1024 and a['sparse_schedule']['limiting_loss_factor']=='2245/3197','sparse support')
    expected=[list(A) for n in (1,2,3) for A in combinations(range(1,11),n)]
    check([r['weights'] for r in a['prime_replay']['small_cases']]==expected,'small prime source coverage')
    groups=['small_cases','targets','amplifications','general_pattern_radii']
    for key in groups:
        for r in a['prime_replay'][key]:audit_prime(r)
    ex=a['collision_horizon']['sharp_example'];check(ex['weights']==[3,11] and ex['base']==17 and ex['arity']==4,'sharp input')
    W=ex['witness'];D=set(polynomial((3,11),4))
    check(W['levels']==3 and len(W['left'])==len(W['right'])==3,'sharp length')
    check(all(x in D for x in W['left']+W['right']),'sharp actual digits')
    check(W['left']!=W['right'],'distinct words')
    check(sum(x*17**j for j,x in enumerate(W['left']))==W['value']==sum(x*17**j for j,x in enumerate(W['right'])),'sharp equality')
    check(len({x+17*y for x in D for y in D})==len(D)**2,'first two levels not injective')

def exhaustive_audit():
    alphabets=joins=lengths=0;rows=[]
    for b in range(2,7):
        for code in range(1<<(2*b-2)):
            D={0}|{i for i in range(1,2*b-1) if code>>(i-1)&1}
            M=datum(D,b);alphabets+=1
            N0,N1=1,len(D);tr=M[0][0]+M[1][1];det=M[0][0]*M[1][1]-M[0][1]*M[1][0]
            ns=six_step_count(D,b)
            check(ns[:2]==[N0,N1],'initial values')
            for m in range(5):check(ns[m+2]==tr*ns[m+1]-det*ns[m],'all automaton recurrence')
            lengths+=7
            for Y in [{0},{0,2},{0,1,4},{-2,-1,1,2}]:
                images=Counter(x+b*y for x in D for y in Y)
                check(len(images)==M[0][0]*len(Y)+M[0][1]*components(Y),'join count')
                check(components(images)==M[1][0]*len(Y)+M[1][1]*components(Y),'join runs')
                check(max(images.values())<=2,'join fibre size')
                check(sum(v-1 for v in images.values())==M[0][1]*(len(Y)-components(Y)),'join relation rank')
                joins+=1
            rows.append([b,code,M,ns])
    h=hashlib.sha256()
    for r in rows:h.update((repr(r)+'\n').encode())
    return dict(alphabets=alphabets,joins=joins,automaton_length_counts=lengths,transcript_sha256=h.hexdigest())

def mutations(a):
    edits=[lambda x:x['targets'][0]['matrix'][0].__setitem__(1,43),
           lambda x:x['targets'][0].__setitem__('two_level_kernel',0),
           lambda x:x['targets'][3].__setitem__('runs',8),
           lambda x:x['prime_replay']['targets'][1].__setitem__('prime',7),
           lambda x:x['prime_replay']['targets'][3]['excluded_primes'].pop(),
           lambda x:x['prime_replay']['small_cases'].pop(),
           lambda x:x['collision_horizon']['sharp_example']['witness'].__setitem__('levels',2),
           lambda x:x['targets'][-1].__setitem__('period_determinant',0)]
    rejected=0
    for edit in edits:
        b=copy.deepcopy(a);edit(b)
        try:fast_receipt(b)
        except (AssertionError,KeyError):rejected+=1
        else:raise AssertionError('mutated record accepted')
    return rejected

def sparse_audit(a):
    from fractions import Fraction
    c=Fraction(2245,3197)
    for row in a['sparse_schedule']['samples']:
        m=row['levels'];N=R=1;L=0
        for j in range(m-1,-1,-1):
            v=j//3 if j%3==0 else 0
            special=v>0 and v&(v-1)==0
            if special:N,R=97*N+42*R,3*R;L+=1
            else:N,R=139*N,2*N+R
        check(L==row['special_levels'] and hashlib.sha256(str(N).encode()).hexdigest()==row['image_sha256'],'sparse direct row recurrence')
        if L:check(Fraction(1,2)*c**L<=Fraction(N,139**m)<=2*c**(L-1),'sparse bounds')
    return len(a['sparse_schedule']['samples'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--receipt',type=Path,default=HERE/'all_block_image_receipt.json');p.add_argument('--output',type=Path,default=HERE/'independent_audit.json');args=p.parse_args()
    a=json.loads(args.receipt.read_text());fast_receipt(a)
    result={'schema':'ep817-all-block-image-independent-audit-v1','status':'PASS','lean_checked':False,
            'receipt_sha256':hashlib.sha256(args.receipt.read_bytes()).hexdigest(),
            'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'sparse_prefixes_rechecked':sparse_audit(a),'complete_residue_replay':exhaustive_audit(),
            'prime_records':sum(len(a['prime_replay'][key]) for key in ['small_cases','targets','amplifications','general_pattern_radii']),
            'rejected_mutations':mutations(a),
            'scope':'separate finite implementation; no external reviewer or theorem-prover claim'}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
