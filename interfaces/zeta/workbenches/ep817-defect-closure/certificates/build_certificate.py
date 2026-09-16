#!/usr/bin/env python3
"""Build exact K_3,3 binary-switch proofs, tensor witnesses and closure replays."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations,product,permutations
from pathlib import Path
import argparse,gzip,json,random
from exact_closure import require,dot,sub,coefficients,closure,scalar_realization,integer_ap,infeasibility_certificate

EDGES33=tuple((i,j) for i in range(3) for j in range(3,6))
EDGES4=tuple(combinations(range(4),2))

def score_data(n,edges):
    fibres={}
    for mask in range(1<<len(edges)):
        s=[0]*n
        for e,(u,v) in enumerate(edges):s[v if (mask>>e)&1 else u]+=1
        fibres.setdefault(tuple(s),[]).append(mask)
    return fibres

def root(v):
    return sum(x==1 for x in v)==sum(x==-1 for x in v)==1 and all(x in (-1,0,1) for x in v)

def delta(seq):
    n=len(seq[0])
    return [tuple(seq[i][j]-2*seq[i+1][j]+seq[i+2][j] for j in range(n)) for i in range(len(seq)-2)]

def packet(source,a,v,sigma,r):
    seq=[tuple(x+i*y+t*z for x,y,z in zip(a,v,r)) for i,t in enumerate(sigma)]
    require(all(s in source for s in seq),'packet left original score source')
    return {'anchor':a,'step':v,'switch':sigma,'scores':seq,
            'orientation_masks':[source[s][0] for s in seq]}

def tail_packet(source,r,k=5):
    n=len(r)
    for i in range(n):
      for j in range(n):
        if i==j:continue
        v=tuple(int(h==j)-int(h==i) for h in range(n))
        for y in sorted(source):
            a=tuple(y[h]-(k-2)*v[h] for h in range(n))
            last=tuple(y[h]+v[h]+r[h] for h in range(n))
            if a in source and last in source:
                return packet(source,a,v,[0]*(k-1)+[1],r)
    return None

def binary_pair(source,r):
    found=[]
    # Only actual binary switches are considered; no divided or enlarged defects.
    for a in sorted(source):
      for b in sorted(source):
       for t in (0,1):
        v=tuple(y-x-t*z for x,y,z in zip(a,b,r))
        if not any(v) or any(v==tuple(p['step']) for p in found):continue
        sig=[0,t]
        for j in range(2,5):
            x=tuple(a[h]+j*v[h] for h in range(6))
            y=tuple(x[h]+r[h] for h in range(6))
            if x in source:sig.append(0)
            elif y in source:sig.append(1)
            else:break
        else:
            p=packet(source,a,v,sig,r)
            if root(v):return [p],[1],v
            for other in found:
                if root(sub(v,other['step'])):
                    return [other,p],[-1,1],sub(v,other['step'])
                if root(tuple(x+y for x,y in zip(v,other['step']))):
                    return [other,p],[1,1],tuple(x+y for x,y in zip(v,other['step']))
            found.append(p)
    raise AssertionError(f'no root-exposure packets for {r}')

def canon(r):
    a=tuple(sorted(r[:3]));b=tuple(sorted(r[3:]));na=tuple(sorted(-x for x in r[:3]));nb=tuple(sorted(-x for x in r[3:]));return min(a+b,b+a,na+nb,nb+na)

def symmetry(r,rep):
    # output coordinate i reads input p[i]; sign -1 complements every score.
    for swap in (False,True):
      for a in permutations(range(3)):
       for b in permutations(range(3,6)):
        p=tuple(b+a if swap else a+b)
        for sign in (1,-1):
            if tuple(sign*rep[p[i]] for i in range(6))==tuple(r):return p,sign
    raise AssertionError('uncovered symmetry')

def move_packet(p,perm,sign):
    seq=[tuple(s[i] if sign==1 else 3-s[i] for i in perm) for s in p['scores']]
    return {'anchor':seq[0], 'step':tuple(sign*p['step'][i] for i in perm),
            'switch':p['switch'],'scores':seq}

def get_packets(r,table,source):
    row=table[canon(r)];perm,sign=symmetry(r,tuple(row['difference']))
    ps=[move_packet(p,perm,sign) for p in row['packets']]
    aux=None
    if row['kind']=='divided-local':aux=move_packet(row['auxiliary_local_packet'],perm,sign)
    return ps,aux

def actual_generators(marks,edges):
    return tuple(abs(marks[j]-marks[i]) for i,j in edges)

def score_to_subset(mask,marks,edges):
    ans=0
    for i,(u,v) in enumerate(edges):
        head=v if (mask>>i)&1 else u
        if marks[head]==min(marks[u],marks[v]):ans|=1<<i
    return ans

def tensor_witness(left,right,marks,table,source):
    h=len(left);rs=[sub(y,x) for x,y in zip(left,right)]
    require(sum(dot(t,r) for t,r in zip(marks,rs))==0,'not a total collision')
    active=next(i for i,r in enumerate(rs) if any(r));ps,aux=get_packets(rs[active],table,source)
    chosen=next((p for p in ps if dot(marks[active],p['step'])!=0),None)
    local=False
    if chosen is None:
        require(aux is not None,'root exposure failed for distinct marks')
        chosen=aux;local=True
    require(dot(marks[active],chosen['step'])!=0,'local escape step vanished')
    tuples=[]
    for row in range(5):
        xs=[]
        for block in range(h):
            if block==active:xs.append(tuple(chosen['scores'][row]))
            elif local:xs.append(tuple(left[block]))
            else:xs.append(tuple(right[block] if chosen['switch'][row] else left[block]))
        tuples.append(xs)
    values=[];masks=[]
    weights=[actual_generators(t,EDGES33) for t in marks]
    for xs in tuples:
        mm=[score_to_subset(source[s][0],t,EDGES33) for s,t in zip(xs,marks)]
        val=sum(sum(w for e,w in enumerate(ww) if (mask>>e)&1) for mask,ww in zip(mm,weights))
        values.append(val);masks.append(mm)
    d=values[1]-values[0]
    require(d!=0 and all(x==values[0]+i*d for i,x in enumerate(values)),'tensor AP failed')
    return {'left':left,'right':right,'marks':marks,'weights':weights,'active':active,
            'used_local_escape':local,'score_tuples':tuples,'subset_masks':masks,'values':values,'step':d}

def tensor_cases(table,source):
    rng=random.Random(817515);S=sorted(source);ans=[]
    for h,count in [(2,20),(3,10),(5,5)]:
        trials=0
        while sum(len(x['marks'])==h for x in ans)<count:
            trials+=1;require(trials<20000,'sampling failed')
            left=[rng.choice(S) for _ in range(h)];right=[rng.choice(S) for _ in range(h)]
            r=sum([list(sub(y,x)) for x,y in zip(left,right)],[])
            if not any(r):continue
            pivot=next(i for i,x in enumerate(r) if x);d=r[pivot]
            z=[rng.randrange(-10000,10001) for _ in r]
            t=[d*x for x in z];t[pivot]=-sum(r[i]*z[i] for i in range(len(r)) if i!=pivot)
            marks=[t[i*6:(i+1)*6] for i in range(h)]
            ws=[w for m in marks for w in actual_generators(m,EDGES33)]
            if min(ws)==0 or len(set(ws))!=len(ws) or any(len(set(m))!=6 for m in marks):continue
            ans.append(tensor_witness(left,right,marks,table,source))
    return ans

def moments(source,edges):
    S=sorted(source);n=len(S[0]);m=len(S);mean=[F(sum(s[i] for s in S),m) for i in range(n)]
    C=[[sum((F(s[i])-mean[i])*(F(s[j])-mean[j]) for s in S)/m for j in range(n)] for i in range(n)]
    Lap=[[sum(i in e for e in edges) if i==j else -sum(set(e)=={i,j} for e in edges) for j in range(n)] for i in range(n)]
    if n==6:
        u=[1,1,1,-1,-1,-1];pred=[[F(25,82)*Lap[i][j]-F(u[i]*u[j],164) for j in range(n)] for i in range(n)]
    else:pred=[[F(25,76)*Lap[i][j] for j in range(n)] for i in range(n)]
    require(C==pred,'covariance identity failed')
    return {'cardinality':m,'word_count':sum(map(len,source.values())),
            'multiplicity_histogram':dict(sorted(Counter(map(len,source.values())).items())),
            'mean':list(map(str,mean)),'covariance':[[str(x) for x in row] for row in C]}

def closure_replay():
    records=[];negative=0
    for n in (2,3):
        S=list(product((0,1),repeat=n))
        initial_vectors=[v for v in product(range(-2,3),repeat=n) if any(v)]
        for k in range(3,7):
          for r in initial_vectors:
            W,proof=closure(S,[r],k)
            model=scalar_realization(S,W)
            if model is not None:
                a=model['weights'];require(dot(a,r)==0,'lost imposed relation')
                require(integer_ap([dot(a,s) for s in S],k) is None,'realization has a forbidden AP')
            else:negative+=1
            # Independently sampled observers test necessity, not completeness.
            for a in product(range(1,6),repeat=n):
                if len(set(a))<n or dot(a,r)!=0:continue
                if integer_ap([dot(a,s) for s in S],k) is None:
                    require(all(dot(a,w)==0 for w in W),'closure killed an admissible observer')
            records.append({'n':n,'k':k,'initial':[r],'closed_basis':W,'rounds':proof,'model':model,
                            'infeasibility':infeasibility_certificate(W,n) if model is None else None})
    return records,negative

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).with_name('proof_data.json.gz'));args=ap.parse_args()
    S33=score_data(6,EDGES33);S4=score_data(4,EDGES4)
    differences={sub(x,y) for x in S33 for y in S33};counts=Counter(canon(r) for r in differences if any(r))
    rows=[];types=Counter()
    for r,cnt in sorted(counts.items()):
        p=tail_packet(S33,r)
        if p is not None:row={'difference':r,'orbit_size':cnt,'kind':'root-tail','packets':[p],'root':p['step'],'combination':[1]}
        elif r==(-2,-2,-2,2,2,2):
            v=(1,1,1,-1,-1,-1);a=(0,0,0,3,3,3)
            p=packet(S33,a,v,[0,0,0,0,1],r);h=tuple(x//2 for x in r);aux=tail_packet(S33,h)
            require(aux is not None and all(x==-2*y for x,y in zip(r,v)),'divided local proof failed')
            row={'difference':r,'orbit_size':cnt,'kind':'divided-local','packets':[p],
                 'retained_factor':2,'local_difference':h,'auxiliary_local_packet':aux}
        else:
            ps,coeffs,rho=binary_pair(S33,r)
            row={'difference':r,'orbit_size':cnt,'kind':'two-switch','packets':ps,'root':rho,'combination':coeffs}
        types[row['kind']]+=1;rows.append(row)
    table={tuple(row['difference']):row for row in rows}
    k4=[]
    for r in sorted({sub(x,y) for x in S4 for y in S4}-{(0,)*4}):
        p=tail_packet(S4,r);require(p is not None,'K4 tail coverage failed');k4.append({'difference':r,'packet':p})
    records,neg=closure_replay()
    proof={'schema':'ep817-defect-closure-v1','status':'PASS','lean_checked':False,
           'source_K33':{'vertices':6,'edges':EDGES33,'scores':[{'score':s,'masks':ms} for s,ms in sorted(S33.items())]},
           'K33_difference_count':len(differences),'K33_orbits':rows,'orbit_types':dict(types),
           'K4_packets':k4,'tensor_cases':tensor_cases(table,S33),
           'moments':{'K33':moments(S33,EDGES33),'K4':moments(S4,EDGES4)},
           'closure_records':records,'closure_negative_instances':neg,
           'source_hashes':{p.name:sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('exact_closure.py')]}}
    raw=(json.dumps(proof,sort_keys=True,indent=2)+'\n').encode();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(gzip.compress(raw,mtime=0))
    summary={'status':'PASS','K33_scores':len(S33),'K33_differences':len(differences),
             'K33_orbits':len(rows),'types':dict(types),'K4_nonzero_differences':len(k4),
             'tensor_cases':len(proof['tensor_cases']),'closure_cases':len(records),
             'closure_no_realization':neg,'moments':proof['moments'],
             'proof_uncompressed_sha256':sha256(raw).hexdigest(),
             'proof_compressed_sha256':sha256(args.output.read_bytes()).hexdigest(),
             'source_hashes':proof['source_hashes'],'lean_checked':False}
    Path(__file__).with_name('producer_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__':main()
