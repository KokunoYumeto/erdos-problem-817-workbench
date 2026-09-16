#!/usr/bin/env python3
"""Build exact universal-isolation and canonical-factor certificates.

Run from any directory. No network, compiled extension, or third-party package.
The proof is in the companion note; finite tests have their precise domains here.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,json,random
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
from math import lcm,prod
from exact_source import *

PRISM=[(0,1),(0,2),(0,3),(1,2),(1,4),(2,5),(3,4),(3,5),(4,5)]
K33=[(i,j) for i in range(3) for j in range(3,6)]

def moments(S,edges):
    n=len(next(iter(S)));M=len(S);mu=[F(sum(x[i] for x in S),M) for i in range(n)]
    C=[[sum((F(s[i])-mu[i])*(F(s[j])-mu[j]) for s in S)/M for j in range(n)] for i in range(n)]
    return {'values':M,'words':sum(map(len,S.values())),
            'multiplicity_histogram':{str(k):v for k,v in sorted(Counter(map(len,S.values())).items())},
            'mean':list(map(str,mu)),'covariance':[[str(v) for v in row] for row in C]}

def source_record(S,n,edges):
    return {'vertices':n,'edges':edges,'fibres':[{'score':s,'masks':m} for s,m in sorted(S.items())]}

def root_exposure(S,r,ps,edges):
    n=len(r)
    # A literal final-defect root packet is the smallest independent certificate.
    for i,j in combinations(range(n),2):
        for sign in(1,-1):
            v=tuple(sign*(int(h==j)-int(h==i)) for h in range(n))
            if v in ps:return {'packets':[ps[v]],'coefficients':['1'],'root':v}
    steps=list(ps)
    for i,j in combinations(range(n),2):
        v=tuple(int(h==j)-int(h==i) for h in range(n));c=coeff(steps,v)
        if c is not None:
            ids=[h for h,x in enumerate(c) if x]
            return {'packets':[ps[steps[h]] for h in ids], 'coefficients':[str(c[h]) for h in ids], 'root':v}
    return None

def local_graph(name,edges):
    S=score_source(6,edges);D,autos,reps=orbits(S,6,edges);rows=[];types=Counter();packet_lengths=Counter()
    for r,count in reps:
        ps=packets_cubic(S,r);selected=cone_packets(S,r,ps)
        record={'difference':r,'orbit_size':count}
        if selected is not None:
            record.update(kind='integral-packets',packets=selected,multiplier=1,coefficients=[-1]*len(selected))
            packet_lengths[len(selected)]+=1
        else:
            c=coeff(list(ps),r)
            if c is not None:
                denominator=lcm(*(x.denominator for x in c));nums=[int(x*denominator) for x in c]
                record.update(kind='saturation',packets=list(ps.values()),multiplier=denominator,coefficients=nums)
                parity=(1,1,1,0,0,0)
                require(denominator==2 and all(dot(parity,v)%2==0 for v in ps) and dot(parity,r)%2!=0,'saturation parity case changed')
                record['parity_functional']=parity
            else:
                W,rounds=union_closure(S,r,5);c=coeff(W,r)
                require(c is not None and len(rounds)==2,'second closure failed')
                record.update(kind='second-closure',first_round_packets=list(ps.values()),
                              closed_basis=W,rounds=rounds,final_coefficients=list(map(str,c)))
                old=list(ps);detector=next(v for v in annihilator(old,6) if dot(v,r))
                record['first_round_detector']=detector
        if name=='prism':
            exposure=root_exposure(S,r,ps,edges)
            require(exposure is not None,'prism local scalar faithfulness needs another step')
            record['root_exposure']=exposure
        else:
            record['faithfulness']=collision_closure(S,r,5)
        types[record['kind']]+=1;rows.append(record)
    return {'source':source_record(S,6,edges),'difference_count':len(D),'automorphisms':autos,
            'orbit_count':len(rows),'types':dict(types),'packet_lengths':dict(packet_lengths),
            'records':rows,'moments':moments(S,edges)}

def clique_suite():
    complete=[];sampled=[];rng=random.Random(817_20260916)
    for m in range(2,6):
        E=list(combinations(range(m),2));S=score_source(m,E);diffs={sub(a,b) for a in S for b in S};diffs.discard((0,)*m)
        cases=[clique_derivation(m,r) for r in sorted(diffs)]
        complete.append({'m':m,'score_count':len(S),'differences':len(cases),'cases':cases})
    for m in range(6,13):
        E=list(combinations(range(m),2))
        for _ in range(12):
            left=rng.getrandbits(len(E));right=rng.getrandbits(len(E));r=sub(score(right,m,E),score(left,m,E))
            if not any(r):right^=1;r=sub(score(right,m,E),score(left,m,E))
            sampled.append({'m':m,'left_mask':left,'right_mask':right,'certificate':clique_derivation(m,r)})
    return {'complete_through_m':5,'complete':complete,'sampled_m_range':[6,12],'samples':sampled}

def factor_record(A,q):
    partition,primitive=primitive_components(A,q)
    return {'weights':A,'alphabet_size':q,'partition':partition,'primitive_count':len(primitive),
            'image_size':len(digit_image(A,q))}

def canonical_suite():
    records=[];hashes={};counts={}
    for q,N,maxn in((2,12,5),(3,10,4)):
        digest=hashlib.sha256();total=0
        for n in range(1,maxn+1):
            for A in combinations(range(1,N+1),n):
                row=factor_record(A,q);records.append(row);total+=1
                digest.update((json.dumps(row,sort_keys=True)+'\n').encode())
        hashes[str(q)]=digest.hexdigest();counts[str(q)]={'universe_max':N,'maximum_size':maxn,'cases':total}
    A=(1,4,5,17,21,22,97)
    T=(0,1,5,25,125,625);P=tuple(sorted(abs(T[a]-T[b]) for a,b in PRISM))
    targets=[factor_record(A,2),factor_record(A,3),factor_record(P,2),factor_record(P+(3125,),2)]
    require(targets[0]['partition']==[[0,1,2,3,4,5],[6]],'binary components changed')
    require(targets[1]['partition']==[list(range(7))],'ternary merger missing')
    relation=(1,0,2,0,2,2,-1);require(dot(A,relation)==0,'higher-arity witness arithmetic failed')
    return {'domains':counts,'hashes':hashes,'records':records,'targeted':targets,
            'higher_arity_relation':relation,'prequotient_ternary_values':417,'ternary_values':333,'receiving_kernel_rank':84}

def modular_empty(digits,q,k):
    bits=sum(1<<d for d in digits);mask=(1<<q)-1
    for step in range(1,q):
        starts=bits
        for j in range(1,k):
            shift=(j*step)%q
            shifted=bits if not shift else ((bits>>shift)|(bits<<(q-shift)))&mask
            starts&=shifted
            if not starts:break
        if starts:return False
    return True

def applications():
    T=(0,1,5,25,125,625);A=tuple(sorted(abs(T[a]-T[b]) for a,b in PRISM));D=digit_image(A)
    require(len(D)==314 and modular_empty(D,3125,5),'prism nonvacuity certificate failed')
    C=(1,4,5,17,21,22);overlap=C+(6,)
    require(ap_witness(digit_image(overlap),5)==(0,6,12,18,24),'overlap witness changed')
    require(modular_empty(digit_image(C),97,5),'existing K4 control failed')
    require(ap_witness(digit_image(C+(97,)),5) is None,'higher-arity example is inadmissible')
    masks={}
    for m in range(1<<len(overlap)):
        value=sum(a for i,a in enumerate(overlap) if m>>i&1);masks.setdefault(value,m)
    return {'prism_marks':T,'prism_generators':A,'sum':sum(A),'modulus':3125,
            'subset_sums':len(D),'modular_parameters':3125*3124,'nonconstant_modular_aps':0,
            'overlap_generators':overlap,'overlap_progression':[0,6,12,18,24],
            'overlap_masks':[masks[x] for x in (0,6,12,18,24)],
            'pure_prism_finite_lower':{'1':55,'2':12009,'3':3078707}}

def local_test():
    # Universal isolation must retain its progression-length threshold.
    for m in range(2,9):
        X=set(range(m));Y={0,1};Z={x+y for x in X for y in Y}
        require(len(Z)<len(X)*len(Y) and ap_witness(Z,m+2) is None,'threshold counterexample failed')
    return {'larger_length_counterexamples':7,
            'scope':'S=[0,m-1], Y={0,1}; collision but no (m+2)-term progression, m=2..8'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path(__file__).with_name('proof_data.json.gz'));a=p.parse_args()
    data={'schema':'ep817-canonical-isolation-v1','status':'PASS','lean_checked':False,
          'clique':clique_suite(),'prism':local_graph('prism',PRISM),'K33':local_graph('K33',K33),
          'canonical':canonical_suite(),'applications':applications(),'threshold':local_test(),
          'source_hashes':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),Path(__file__).with_name('exact_source.py')]}}
    raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode();a.output.write_bytes(gzip.compress(raw,mtime=0))
    summary={'schema':'ep817-canonical-isolation-producer-summary-v1','status':'PASS','lean_checked':False,
             'uncompressed_sha256':hashlib.sha256(raw).hexdigest(),'compressed_sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),
             'clique_complete_differences':sum(c['differences'] for c in data['clique']['complete']),
             'clique_root_steps':sum(len(x['stages']) for row in data['clique']['complete'] for x in row['cases']),
             'clique_larger_rank_samples':len(data['clique']['samples']),
             'prism_differences':data['prism']['difference_count'],'prism_orbits':data['prism']['orbit_count'],
             'prism_packet_lengths':data['prism']['packet_lengths'],'K33_types':data['K33']['types'],
             'K33_differences':data['K33']['difference_count'],'canonical_domains':data['canonical']['domains'],
             'source_hashes':data['source_hashes']}
    a.output.with_name('producer_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__': main()
