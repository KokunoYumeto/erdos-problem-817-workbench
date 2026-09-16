#!/usr/bin/env python3
"""Independent exact arithmetic audit; imports neither producer nor source library.

Score fibres are reconstructed by dynamic orientation extension. Canonical
factors are recomputed by image-cardinality splitting, not by relation generators.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,permutations,product
from math import prod
from pathlib import Path

def check(ok,msg):
    if not ok:raise AssertionError(msg)

def smask(mask,n,edges):
    check(isinstance(mask,int) and 0<=mask<(1<<len(edges)),'invalid original orientation mask')
    s=[0]*n
    for j,(u,v) in enumerate(edges):s[[u,v][(mask>>j)&1]]+=1
    return tuple(s)

def source(n,edges):
    D={(0,)*n:[0]}
    for j,(u,v) in enumerate(edges):
        nxt={}
        for row,masks in D.items():
            for h,w in enumerate((u,v)):
                s=list(row);s[w]+=1;s=tuple(s)
                nxt.setdefault(s,[]).extend(mask|(h<<j) for mask in masks)
        D=nxt
    return {s:sorted(v) for s,v in D.items()}

def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sumrows(cs,B,n):
    check(len(cs)==len(B) and all(len(b)==n for b in B),'coefficient/source dimension mismatch')
    return tuple(sum(F(c)*b[j] for c,b in zip(cs,B)) for j in range(n))
def signed_direction(v):
    v=tuple(v)
    return v if next(x for x in v if x)>0 else tuple(-x for x in v)

def audit_clique(m,row):
    edges=list(combinations(range(m),2));r=tuple(row['difference']);current=r;basis=[];total=0
    check(len(r)==m and any(r) and sum(r)==0,'invalid clique difference')
    budget=sum(max(0,x) for x in r)
    for item in row['stages']:
        check(tuple(item['current'])==current,'unrecorded residual change')
        i=item['i'];j=item['j'];check(current[i]==max(current) and current[j]==min(current),'wrong extrema')
        alpha=tuple(int(h==j)-int(h==i) for h in range(m));check(tuple(item['alpha'])==alpha,'altered integral root')
        xs=[smask(mask,m,edges) for mask in item['masks']];check(len(xs)==m+1,'missing clique packet row')
        # Reconstruct every row in the original S union (S+r), not a new quotient source.
        zs=[tuple(x[h]+(r[h] if t<m else 0) for h in range(m)) for t,x in enumerate(xs)]
        check(sub(zs[1],zs[0])==alpha,'wrong observed step')
        prev=sumrows([1]*len(basis),basis,m)
        check(tuple(current[h]-r[h] for h in range(m))==prev,'missing old relation identity')
        for t in range(m-1):
            actual=tuple(zs[t][h]-2*zs[t+1][h]+zs[t+2][h] for h in range(m))
            check(actual==((0,)*m if t<m-2 else prev),'packet defects are not old relations')
        current=tuple(current[h]+alpha[h] for h in range(m));basis.append(alpha);total+=1
        check(sum(max(0,x) for x in current)==budget-total,'wrong termination budget')
    check(not any(current) and len(basis)<=m*m//4,'unfinished clique contraction')
    check(sumrows([-1]*len(basis),basis,m)==r,'final initial-class identity failed')
    return total

def audit_packet(p,r,n,edges):
    sigma=p['switch'];check(len(sigma)==5 and sigma[0]==0 and all(t in(0,1) for t in sigma),'nonbinary switch')
    a=p['anchor'];v=tuple(p['step']);xs=[smask(mask,n,edges) for mask in p['masks']]
    check(len(a)==n and len(v)==n and len(xs)==5 and any(v),'invalid packet')
    for j,s in enumerate(xs):
        check(s==tuple(a[h]+j*v[h]+sigma[j]*r[h] for h in range(n)),'original mask/packet mismatch')
    return v

def audit_rounds(rounds,S,r,n,edges,initial=()):
    W=list(map(tuple,initial));steps=0
    for rnd in rounds:
        old=list(W);check(list(map(tuple,rnd['old_basis']))==old,'closure basis was silently changed')
        for item in rnd['steps']:
            xs=[]
            for rep in item['representatives']:
                s=smask(rep['mask'],n,edges);t=rep['shift'];check(t in(0,1),'unsupported translated source')
                check(s in S,'original score absent');xs.append(tuple(s[i]+t*r[i] for i in range(n)))
            check(len(xs)==5,'closure tuple length changed')
            step=sub(xs[1],xs[0]);check(step==tuple(item['step']) and any(step),'closure step mismatch')
            check(len(item['coefficients'])==3 and len(item['defects'])==3,'closure premises missing')
            for i in range(3):
                d=tuple(xs[i][j]-2*xs[i+1][j]+xs[i+2][j] for j in range(n))
                check(tuple(item['defects'][i])==d,'retained defect mismatch')
                check(len(item['coefficients'][i])==len(old),'wrong primitive dimension')
                check(sumrows(item['coefficients'][i],old,n)==d,'uncertified closure premise')
            W.append(step);steps+=1
    return W,steps

def all_union_directions(S,r):
    U=set(S)|{tuple(x+y for x,y in zip(s,r)) for s in S};P=sorted(U);ans=set()
    for i,a in enumerate(P):
        for b in P[i+1:]:
            v=sub(b,a)
            if all(tuple(x+j*y for x,y in zip(a,v)) in U for j in (2,3,4)):
                ans.add(signed_direction(v))
    return ans

def audit_local(data,name):
    sr=data['source'];n=sr['vertices'];edges=list(map(tuple,sr['edges']));S=source(n,edges)
    check({tuple(x['score']):x['masks'] for x in sr['fibres']}==S,'word fibres changed')
    D={sub(a,b) for a in S for b in S};D.discard((0,)*n);check(len(D)==data['difference_count'],'difference domain count')
    edge_set=set(edges);autos=[p for p in permutations(range(n)) if {tuple(sorted((p[u],p[v]))) for u,v in edges}==edge_set]
    check(list(map(tuple,data['automorphisms']))==autos,'automorphism list incomplete')
    covered=set();counts=Counter();closure_steps=0
    for row in data['records']:
        r=tuple(row['difference']);orbit={tuple(t*r[p[i]] for i in range(n)) for p in autos for t in(-1,1)}
        check(orbit<=D and not orbit&covered and len(orbit)==row['orbit_size'],'orbit coverage mismatch');covered|=orbit
        kind=row['kind'];counts[kind]+=1
        if kind in('integral-packets','saturation'):
            vs=[audit_packet(p,r,n,edges) for p in row['packets']]
            check(len(row['coefficients'])==len(vs),'coefficient count')
            check(sumrows(row['coefficients'],vs,n)==tuple(row['multiplier']*x for x in r),'initial difference identity')
            if kind=='integral-packets':
                check(row['multiplier']==1 and all(x==-1 for x in row['coefficients']),'primitive integral identity was rescaled')
                if name=='prism':check(len(vs)<=4,'prism packet count bound')
            else:
                parity=row['parity_functional'];check(row['multiplier']==2,'saturation order changed')
                check(all(dot(parity,v)%2==0 for v in vs) and dot(parity,r)%2==1,'order-two class lost')
                check(all_union_directions(S,r)=={signed_direction(v) for v in vs},'first-round lattice omitted directions')
        elif kind=='second-closure':
            vs=[audit_packet(p,r,n,edges) for p in row['first_round_packets']]
            detector=row['first_round_detector'];check(all(dot(detector,v)==0 for v in vs) and dot(detector,r)!=0,'free first-round class lost')
            check(all_union_directions(S,r)=={signed_direction(v) for v in vs},'first-round span omitted directions')
            W,total=audit_rounds(row['rounds'],S,r,n,edges);closure_steps+=total
            check(len(row['rounds'])==2 and list(map(tuple,row['closed_basis']))==W,'wrong second closure source')
            check(sumrows(row['final_coefficients'],W,n)==r,'second closure missed initial class')
        else:raise AssertionError('unexpected local certificate kind')
        if name=='prism':
            e=row['root_exposure'];vs=[audit_packet(p,r,n,edges) for p in e['packets']];root=tuple(e['root'])
            check(sorted(root)==[-1,0,0,0,0,1] and sumrows(e['coefficients'],vs,n)==root,'unproved prism faithfulness')
        else:
            f=row['faithfulness'];check(f['initial_basis']==[list(r)],'different initial collision')
            W,total=audit_rounds(f['rounds'],S,(0,)*n,n,edges,[r]);closure_steps+=total
            check(list(map(tuple,f['final_basis']))==W,'faithfulness final basis mismatch')
            root=tuple(f['root']);check(sorted(root)==[-1,0,0,0,0,1] and sumrows(f['coefficients'],W,n)==root,'no root consequence')
    check(covered==D and len(data['records'])==data['orbit_count'],'incomplete collision certificate')
    check(dict(counts)==data['types'],'type counts mismatch')
    M=len(S);mean=[F(sum(s[i] for s in S),M) for i in range(n)]
    C=[[sum((F(s[i])-mean[i])*(F(s[j])-mean[j]) for s in S)/M for j in range(n)] for i in range(n)]
    check([[str(v) for v in row] for row in C]==data['moments']['covariance'],'covariance was weighted incorrectly')
    check({str(k):v for k,v in sorted(Counter(map(len,S.values())).items())}==data['moments']['multiplicity_histogram'],'multiplicity histogram')
    if name=='prism':
        # Entire matrix in original vertex coordinates, including nonedge terms.
        for i in range(6):
            for j in range(6):
                num=573 if i==j else -195 if i//3==j//3 else -181 if i%3==j%3 else -1
                check(C[i][j]==F(num,628),'prism covariance decomposition')
        u=(1,1,1,-1,-1,-1)
        L=[[3 if i==j else -int(tuple(sorted((i,j))) in edge_set) for j in range(6)] for i in range(6)]
        # Anti-copy, within-triangle sum-zero projector.
        PA=[[F((1 if i//3==j//3 else -1),2)*(F(int(i%3==j%3))-F(1,3)) for j in range(6)] for i in range(6)]
        P0=[[F(u[i]*u[j],6) for j in range(6)] for i in range(6)]
        check(all(C[i][j]==F(49,157)*L[i][j]-F(13,314)*P0[i][j]-F(8,157)*PA[i][j] for i in range(6) for j in range(6)), 'variance upper correction omitted')
    return {'values':M,'words':sum(map(len,S.values())),'differences':len(D),'orbits':len(data['records']),'kinds':dict(counts),'closure_steps_checked':closure_steps}

def images(weights,q):
    D={0}
    for w in weights:D={x+i*w for x in D for i in range(q)}
    return D

def cardinal_partition(weights,q):
    n=len(weights);cache={0:1}
    def count(mask):
        if mask not in cache:cache[mask]=len(images([weights[i] for i in range(n) if mask>>i&1],q))
        return cache[mask]
    def split(mask):
        first=mask&-mask;rest=mask^first;subset=rest
        while True:
            a=subset|first;b=mask^a
            if b and count(a)*count(b)==count(mask):return split(a)+split(b)
            if subset==0:break
            subset=(subset-1)&rest
        return [[i for i in range(n) if mask>>i&1]]
    return sorted(split((1<<n)-1))

def primitive_count_brute(A,q):
    total=0
    for r in product(range(1-q,q),repeat=len(A)):
        if not any(r) or dot(A,r)!=0:continue
        options=[range(abs(x)+1) for x in r];whole=tuple(abs(x) for x in r)
        signed=[a if x>=0 else -a for a,x in zip(A,r)]
        if any(any(t) and t!=whole and dot(t,signed)==0 for t in product(*options)):continue
        total+=1
    return total

def audit_canonical(data):
    expected={(q,A) for q,N,m in((2,12,5),(3,10,4)) for n in range(1,m+1) for A in combinations(range(1,N+1),n)}
    seen=set();partitions={};hashes={2:hashlib.sha256(),3:hashlib.sha256()}
    for row in data['records']:
        A=tuple(row['weights']);q=row['alphabet_size'];key=(q,A);check(key in expected and key not in seen,'canonical domain duplicated or invented');seen.add(key)
        P=cardinal_partition(A,q);check(P==row['partition'] and len(images(A,q))==row['image_size'],'finest factorization mismatch')
        check(primitive_count_brute(A,q)==row['primitive_count'],'conformal primitive count mismatch')
        partitions[key]=P;hashes[q].update((json.dumps(row,sort_keys=True)+'\n').encode())
    check(seen==expected,'canonical domain incomplete')
    for q in hashes:check(hashes[q].hexdigest()==data['hashes'][str(q)],'canonical transcript hash mismatch')
    refined=0
    for (q,A),P in partitions.items():
        if q!=3:continue
        P2=partitions[(2,A)];check(all(any(set(C)<=set(D) for D in P) for C in P2),'higher-arity partition split a component');refined+=1
    for row in data['targeted']:
        A=tuple(row['weights']);q=row['alphabet_size'];check(cardinal_partition(A,q)==row['partition'],'target factorization mismatch')
        check(len(images(A,q))==row['image_size'],'target image count')
    A=(1,4,5,17,21,22,97);r=data['higher_arity_relation'];check(dot(A,r)==0 and max(map(abs,r))==2,'higher-arity relation lost')
    check(len(images(A[:-1],3))*3==417 and len(images(A,3))==333 and 417-333==data['receiving_kernel_rank'],'additional receiving kernel mismatch')
    return {'all_cases':len(seen),'arity_refinements':refined,'targeted_cases':len(data['targeted'])}

def audit_app(data):
    A=tuple(data['prism_generators']);D=images(A,2);q=data['modulus'];check(len(D)==314 and sum(A)==data['sum'] and sum(A)<q,'invalid literal block')
    # Independent direct start/step scan, including nonunits modulo q.
    for start in D:
        for step in range(1,q):
            check(not all((start+i*step)%q in D for i in range(1,5)),'modular five-progression found')
    weights=data['overlap_generators'];ys=[sum(w for i,w in enumerate(weights) if mask>>i&1) for mask in data['overlap_masks']]
    check(ys==data['overlap_progression']==[0,6,12,18,24],'overlapping-core subset witness invalid')
    for h,t in data['pure_prism_finite_lower'].items():
        h=int(h);num=157*(314**(2*h)-1);den=5292*h
        check((t-1)**2*den<num<=t*t*den,'finite lower rounding failed')
    return {'literal_modular_starts':len(D),'nonzero_steps':q-1,'start_step_pairs':len(D)*(q-1),'overlap_witness':ys}

def audit_all(data):
    check(data['status']=='PASS' and data['lean_checked'] is False,'evidence scope changed')
    total=0;count=0
    for batch in data['clique']['complete']:
        m=batch['m'];S=source(m,list(combinations(range(m),2)));D={sub(a,b) for a in S for b in S};D.discard((0,)*m)
        check(len(S)==batch['score_count'] and {tuple(r['difference']) for r in batch['cases']}==D,'clique full domain mismatch')
        check(len(batch['cases'])==len(D)==batch['differences'],'duplicate clique source')
        for row in batch['cases']:total+=audit_clique(m,row);count+=1
    check(count==3300,'clique coverage unexpectedly changed')
    for row in data['clique']['samples']:
        m=row['m'];E=list(combinations(range(m),2));r=sub(smask(row['right_mask'],m,E),smask(row['left_mask'],m,E))
        check(tuple(row['certificate']['difference'])==r,'sample masks do not supply difference');audit_clique(m,row['certificate'])
    return {'clique_differences':count,'clique_root_steps':total,'larger_rank_samples':len(data['clique']['samples']),
            'prism':audit_local(data['prism'],'prism'),'K33':audit_local(data['K33'],'K33'),
            'canonical':audit_canonical(data['canonical']),'applications':audit_app(data['applications'])}

def mutations(data):
    accepted=0
    def reject(fn):
        nonlocal accepted
        try:fn()
        except (AssertionError,ValueError,KeyError,IndexError):accepted+=1
        else:raise AssertionError('deliberately corrupted certificate was accepted')
    row=copy.deepcopy(data['clique']['complete'][0]['cases'][0]);row['stages'][0]['masks'][-1]^=1
    reject(lambda:audit_clique(2,row))
    row=copy.deepcopy(data['clique']['complete'][0]['cases'][0]);row['stages'][0]['alpha'][0]+=1
    reject(lambda:audit_clique(2,row))
    local=copy.deepcopy(data['prism']);local['records'].pop();reject(lambda:audit_local(local,'prism'))
    local=copy.deepcopy(data['prism']);local['records'][0]['packets'][0]['switch'][1]=2;reject(lambda:audit_local(local,'prism'))
    local=copy.deepcopy(data['K33']);sat=next(r for r in local['records'] if r['kind']=='saturation');sat['multiplier']=1;reject(lambda:audit_local(local,'K33'))
    local=copy.deepcopy(data['K33']);row=next(r for r in local['records'] if r['kind']=='second-closure');row['rounds'][-1]['steps'][0]['coefficients'][0][0]='99';reject(lambda:audit_local(local,'K33'))
    local=copy.deepcopy(data['prism']);local['moments']['covariance'][0][4]='0';reject(lambda:audit_local(local,'prism'))
    canonical=copy.deepcopy(data['canonical']);canonical['records'].pop();reject(lambda:audit_canonical(canonical))
    app=copy.deepcopy(data['applications']);app['overlap_masks'][0]^=1;reject(lambda:audit_app(app))
    return accepted

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).with_name('proof_data.json.gz'));p.add_argument('--output',type=Path,default=Path(__file__).with_name('independent_audit.json'));a=p.parse_args()
    raw=gzip.decompress(a.input.read_bytes());data=json.loads(raw);result=audit_all(data);result['rejected_corruptions']=mutations(data)
    out={'schema':'ep817-canonical-isolation-independent-audit-v1','status':'PASS','lean_checked':False,
         'method':'Separate source DP, direct original-mask equations, independently reconstructed symmetry coverage, direct first-round AP sets, and cardinality-based factor splitting; no producer imports.',
         'results':result,'uncompressed_input_sha256':hashlib.sha256(raw).hexdigest(),
         'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(out,sort_keys=True,indent=2)+'\n';a.output.write_text(text);print(text,end='')
if __name__=='__main__':main()
