#!/usr/bin/env python3
"""Exact finite evidence for all-block image/capacity theorems; not a Lean receipt."""
from __future__ import annotations
import argparse, hashlib, json, random
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from fractions import Fraction
from math import comb, gcd, isqrt
from image_tools import (require,values,masses,runs,statistics,matmul,image_chain,
                         count_chain,ap_witness,modular_ap,good_prime,amplify,quotient_basis,is_prime,collision_path)

ROOT=Path(__file__).resolve().parent

def transcript_hash(rows):
    h=hashlib.sha256()
    for row in rows:
        h.update((json.dumps(row,sort_keys=True,separators=(',',':'))+'\n').encode())
    return h.hexdigest()

def check_join(D,Y,b,weighted=False):
    s=statistics(D,b);X={d+b*y for d in D for y in Y}
    N,R=len(Y),runs(Y);T=s['matrix']
    require([len(X),runs(X)]==[T[0][0]*N+T[0][1]*R,T[1][0]*N+T[1][1]*R], 'two-state identity')
    fibres={}
    for d in D:
        for y in Y:fibres.setdefault(d+b*y,[]).append((d,y))
    B=quotient_basis(D,Y,b)
    require(all(len(f)<=2 for f in fibres.values()), 'fibre size exceeds two')
    require(len(B)==len(D)*len(Y)-len(X)==s['overlap']*(len(Y)-runs(Y)), 'kernel dimension')
    used=[]
    for u,v in B:
        require(u[0]+b*u[1]==v[0]+b*v[1], 'invalid relation column')
        used += [u,v]
    require(len(used)==len(set(used)), 'relation columns do not have disjoint supports')
    if weighted:
        # Arbitrary literal positive rational masses in both original factors.
        md={d:Fraction(i+2,i+1) for i,d in enumerate(sorted(D))}
        my={y:Fraction(2*i+3,i+2) for i,y in enumerate(sorted(Y))}
        for x,F in fibres.items():
            weights=[md[d]*my[y] for d,y in F]
            total=sum(weights)
            section=[w/total for w in weights]
            require(sum(section)==1, 'section inverse law')
            require(sum(z*z/w for z,w in zip(section,weights))==1/total,'quotient Gram')
            if len(F)==2:
                require(section[0]/weights[0]-section[1]/weights[1]==0,'boundary orthogonality')
    return [b,sorted(D),sorted(Y),len(X),runs(X),len(B)]

def general_digits():
    rows=[];counts=Counter();phase=Counter()
    tails=[{0},{0,2},{0,1,4},{-2,-1,1,2}]
    for b in range(2,7):
        for bits in range(1<<(2*b-2)):
            D={0}|{i for i in range(1,2*b-1) if bits>>(i-1)&1}
            s=statistics(D,b);counts['alphabets']+=1
            for Y in tails:rows.append(check_join(D,Y,b));counts['joins']+=1
            ns=[]
            for m in range(4):
                X=image_chain([(b,D)]*m)
                nr=count_chain([(b,D)]*m)
                require(nr==(len(X),runs(X)), 'word-length transfer')
                ns.append(len(X));counts['length_checks']+=1
            require(ns[2]==s['size']**2-s['two_level_kernel'],'first collision formula')
            tr,det=s['trace'],s['determinant']
            for m in (0,1):require(ns[m+2]==tr*ns[m+1]-det*ns[m],'quadratic recurrence')
            discriminant=tr*tr-4*det
            require(discriminant>=0,'nonreal roots')
            if discriminant==0:
                t=s['size']; require(s['matrix']==[[t,0],[0,t]],'nontrivial ternary Jordan block')
            determinant_at_b=b*b-tr*b+det
            require((determinant_at_b==0)==s['full_base_growth'],'full growth criterion')
            require(determinant_at_b>=0,'base spectral bound')
            phase['full_base' if s['full_base_growth'] else 'thin']+=1
            phase['independent' if s['no_cross_level_collisions'] else 'colliding']+=1
    return {'domain':'every D subset [0,2b-2] containing zero; b=2..6',**counts,
            'phase_counts':dict(phase),'transcript_sha256':transcript_hash(rows)}

def all_small_blocks():
    rows=[];count=0;weighted=0
    for n in range(1,5):
        for A in combinations(range(1,13),n):
            D=values(A,3);S=sum(A)
            for b in sorted({S+1,S+2,2*S+1,2*S+2}):
                s=statistics(D,b); row=check_join(D,D,b,weighted=count<24)
                weighted+=count<24;count+=1
                # Independent original generator count, not only a digit-language count.
                B=A+tuple(b*a for a in A)
                require(len(set(B))==2*n,'geometric generator overlap')
                require(values(B,3)=={d+b*y for d in D for y in D},'word/value bridge')
                short={x-2*S for x in values(A,5)}
                require((s['two_level_kernel']>0)==(1 in short and b in short),'two-level arithmetic criterion')
                rows.append([list(A),b,*row[-3:],s['matrix']])
    return {'generator_domain':'all nonempty subsets of [1,12] of size <=4',
            'radices':'distinct values S+1,S+2,2S+1,2S+2',
            'block_radix_cases':count,'weighted_quotient_cases':weighted,
            'transcript_sha256':transcript_hash(rows)}

def mixed_blocks():
    rng=random.Random(8171609);rows=[]
    blocks=[(1,),(2,),(1,3),(3,8),(1,7,8),(1,3,4,7)]
    for _ in range(160):
        levels=[];source=[];P=1
        for __ in range(rng.randrange(1,4)):
            A=rng.choice(blocks);b=sum(A)+rng.randrange(1,8)
            levels.append((b,values(A,3)))
            source.extend(P*a for a in A);P*=b
        X=values(tuple(source),3)
        N,R=count_chain(levels)
        require((len(X),runs(X))==(N,R),'mixed block theorem')
        rows.append([[[b,sorted(D)] for b,D in levels],N,R])
    return {'mixed_schedules':len(rows),'max_levels':3,'transcript_sha256':transcript_hash(rows)}

def target_cases():
    blocks=[('six_97',(1,4,5,17,21,22),97),('six_93',(1,4,5,17,21,22),93),
            ('ten_1651',(3,4,7,34,37,41,216,250,253,257),1651),
            ('noncanonical_residue_overlap',(3,8),13),('unit',(1,),3)]
    out=[]
    for name,A,b in blocks:
        D=values(A,3);s=statistics(D,b);t=s['size'];N=[count_chain([(b,D)]*m)[0] for m in range(7)]
        s.update(name=name,weights=list(A),cardinalities_through_m6=N)
        if name=='six_97':require(all(47*N[m]==68*97**m-21*3**m for m in range(7)),'prior 97 formula')
        if name=='six_93':require(all(45*N[m]==68*93**m-23*3**m for m in range(7)),'prior 93 formula')
        if name=='ten_1651':require(all(781*N[m]==1007*1651**m-226*89**m for m in range(7)),'prior 1651 formula')
        if name=='noncanonical_residue_overlap':
            require(s['overlap']>0 and s['runs']==t and N==[9**m for m in range(7)],'faithful overlap example')
        out.append(s)
    A=(1,4,5,17,21,22);D=values(A,3)
    M97=statistics(D,97)['matrix'];M141=statistics(D,141)['matrix'];period=matmul(M97,M141)
    require(period==[[13567,42],[6,3]],'mixed period matrix')
    require(matmul(M141,M97)!=period,'noncommutativity lost')
    require(modular_ap(values(A,2),97,5) is None and modular_ap(values(A,2),141,5) is None,'binary period certificate')
    out.append({'name':'mixed_97_141','weights':list(A),'matrix_97':M97,'matrix_141':M141,
                'period_matrix':period,'radix_product':97*141,'period_trace':13570,
                'period_determinant':40449,'two_level_counts_by_order':[count_chain([(97,D),(141,D)])[0],
                                                                        count_chain([(141,D),(97,D)])[0]]})
    return out

def prime_cases():
    rows=[]
    for n in range(1,4):
        for A in combinations(range(1,11),n):
            r=good_prime(A);r['binary_admissible_lengths']=[]
            for k in (3,4,5,6):
                if ap_witness(values(A,2),k) is None:
                    require(modular_ap(values(A,2),r['prime'],k) is None,'modular preservation')
                    r['binary_admissible_lengths'].append(k)
            rows.append(r)
    targets=[]
    for A in [(1,7,8),(1001,7007,8008),(1,4,5,17,21,22),(1,200560490130)]:
        targets.append(good_prime(A))
    amplified=[]
    for A in [(1,),(1,3),(1,7,8)]:
        hcard=len(values(A,5))
        for r in range(1,4):
            if hcard**r>80000:continue
            R,B=amplify(A,r)
            D5=values(B,5)
            require(len(D5)==hcard**r,'five-valued tensor cardinality')
            pr=good_prime(B)
            explicit=256+2*(hcard**r-1)*r*R.bit_length()
            require(pr['prime']<=pr['bound']<=explicit,'tensor prime budget')
            pr.update(original_block=list(A),copies=r,separation_base=R,
                      five_valued_cardinality=len(D5),tensor_bound=explicit)
            amplified.append(pr)
    general=[]
    for A,h in [((1,3),1),((1,7,8),1),((1,3),3),((2,9,35),3)]:
        general.append(good_prime(A,h))
    # Literal noncanonical all-length lift examples, checked through three blocks.
    A=(1001,7007,8008);p=good_prime(A)['prime'];direct=[]
    require(p==19 and max(A)>p,'noncanonical prime example')
    for m in (1,2,3):
        B=tuple(p**j*a for j in range(m) for a in A)
        X=values(B,2)
        require(len(set(B))==3*m and len(X)==7**m,'noncanonical image bridge')
        require(ap_witness(X,4) is None,'noncanonical lift introduced progression')
        direct.append({'levels':m,'generators':3*m,'subset_values':len(X)})
    return {'small_cases':rows,'targets':targets,'amplifications':amplified,
            'general_pattern_radii':general,'noncanonical_direct_lifts':direct,
            'small_case_transcript_sha256':transcript_hash(rows)}

def elementary_prime_checks():
    rows=[]
    for N in range(2,701):
        z=N//2;c=comb(2*z,z)
        lcm=1
        for i in range(1,N+1):lcm=lcm*i//gcd(lcm,i)
        require(lcm%c==0,'central binomial divisibility')
        primorial=1
        for p in range(2,N+1):
            if is_prime(p):primorial*=p
        require(lcm//primorial<=N**isqrt(N),'prime-power remainder bound')
        if N>=256:require(primorial**4>3**N,'theta lower bound integer strengthening')
        rows.append([N,c,lcm,primorial])
    # Positive ternary-independent inputs illustrating nonattainment of the q=5 infimum.
    for n in range(1,9):
        A=tuple(3**j for j in range(n));D=values(A,5)
        require(len(D)==2*3**n-1 and D==set(range(2*(3**n-1)+1)),'nonattainment family')
    return {'binomial_lcm_N':[2,700],'primorial_check_N':[256,700],
            'nonattainment_prefixes':8,'transcript_sha256':transcript_hash(rows)}

def collision_checks():
    rows=[];short_direct=0
    for n in (1,2):
        for A in combinations(range(1,9),n):
            for q in range(2,7):
                for b in range(sum(A)+1,sum(A)+5):
                    r=collision_path(A,b,q);D=values(A,q)
                    for m in (1,2,3):
                        injective=len(image_chain([(b,D)]*m))==len(D)**m
                        expected=r['independent'] or r['witness']['levels']>m
                        require(injective==expected,'carry/direct collision comparison')
                        short_direct+=1
                    rows.append(r)
    example=collision_path((3,11),17,4)
    require(not example['independent'] and example['witness']['levels']==3,'sharp arity-four example')
    return {'domain':'all nonempty subsets of [1,8] of size <=2; q=2..6; b=S+1..S+4',
            'cases':len(rows),'direct_length_comparisons':short_direct,
            'witness_counts':dict(Counter('none' if r['independent'] else str(r['witness']['levels']) for r in rows)),
            'transcript_sha256':transcript_hash(rows),'sharp_example':example}


def sparse_schedule():
    T97=[[97,42],[0,3]];T141=[[139,0],[2,1]]
    M=[[1,0],[0,1]];source=1;L=0;special={3*2**j for j in range(11)};samples=[]
    c=Fraction(2245,3197)
    for m in range(1,1025):
        if m-1 in special:
            T=T97;L+=1
        else:T=T141
        M=matmul(M,T);source*=139;N=sum(M[0])
        if L:
            require(Fraction(1,2)*c**L <= Fraction(N,source) <=2*c**(L-1), 'sparse exact loss enclosure')
        else:require(N==source,'pre-collision factorization')
        if m in (1,4,5,8,16,32,64,128,256,512,1024):
            samples.append({'levels':m,'special_levels':L,'image_sha256':hashlib.sha256(str(N).encode()).hexdigest(),
                            'image_bits':N.bit_length(),'local_product_bits':source.bit_length()})
    return {'domain':'all prefixes m=1..1024; base 97 at zero-based positions 3*2^j and 141 elsewhere',
            'prefix_checks':1024,'limiting_loss_factor':'2245/3197','samples':samples,
            'scope':'exact finite matrix inequalities; full-prefix AP freeness follows from the certified digit lifts'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'all_block_image_receipt.json')
    args=ap.parse_args()
    result={'schema':'ep817-all-block-image-v1','status':'PASS','lean_checked':False,
      'scope':'ordinary general proofs; exact bounded checks with literal sources',
      'sparse_schedule':sparse_schedule(),'collision_horizon':collision_checks(),'general_digit_replay':general_digits(),
      'small_generator_blocks':all_small_blocks(),'mixed_block_replay':mixed_blocks(),
      'targets':target_cases(),'prime_replay':prime_cases(),'elementary_checks':elementary_prime_checks()}
    result['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'image_tools.py']}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','output':str(args.output),'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'digits':result['general_digit_replay'],'blocks':result['small_generator_blocks']},indent=2))
if __name__=='__main__': main()
