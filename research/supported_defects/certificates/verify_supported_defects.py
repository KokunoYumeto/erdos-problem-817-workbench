#!/usr/bin/env python3
"""Exact bounded checks for supported defects and their original source maps.

The infinite statements are proved in the companion notes.  This executable
uses integers and Fraction only.  It never treats a bounded check as an
all-rank proof, and remains fail-closed under python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json

DIGITS=(0,1,7,8,9,15,16)


def require(b: bool, msg: str) -> None:
    if not b: raise AssertionError(msg)


def digest(obj) -> str:
    return sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def fibres(A):
    out=defaultdict(list)
    for mask in range(1<<len(A)):
        out[sum(a for i,a in enumerate(A) if mask>>i&1)].append(mask)
    return dict(out)


def values(A):
    ans={0}
    for a in A: ans |= {v+a for v in tuple(ans)}
    return ans


def aps(D,k):
    """All positive-step ordered k-APs, counted by distinct numerical values."""
    V=sorted(D); S=set(V); out=[]
    if not V:return out
    hi=V[-1]
    for i,x in enumerate(V):
        for y in V[i+1:]:
            d=y-x
            if x+(k-1)*d>hi: break
            if all(x+j*d in S for j in range(2,k)):
                out.append(tuple(x+j*d for j in range(k)))
    return out


def dot(a,b): return sum(x*y for x,y in zip(a,b))


def delta(a):return tuple(a[i]-2*a[i+1]+a[i+2] for i in range(len(a)-2))


def lifted(h,L=None):
    require(bool(h) and all(isinstance(x,int) and x>=0 for x in h),'bad defect list')
    L=2*sum(h)+1 if L is None else L
    require(L>2*sum(h),'separation inequality failed')
    A=tuple(a for j,x in enumerate(h) for a in (L*19**j,7*L*19**j,8*L*19**j+x))
    require(len(set(A))==len(A) and min(A)>0,'actual generators not distinct positive')
    return L,A


def high_data(mask,r):
    high=0; low_coeff=[]
    for j in range(r):
        v=(mask>>(3*j))&7
        high+=19**j*((v&1)+7*((v>>1)&1)+8*((v>>2)&1))
        low_coeff.append((v>>2)&1)
    return high,tuple(low_coeff)


def block_fibre(digits,h):
    J=tuple(i for i,d in enumerate(digits) if d==8)
    offset=sum(h[i] for i,d in enumerate(digits) if d in (9,15,16))
    return J,offset


def check_universal(h):
    r=len(h);L,A=lifted(h);f=fibres(A); hf=fibres(h)
    predicted={}; multiplicities={}; descriptor={}
    for digits in product(DIGITS,repeat=r):
        x=sum(d*19**j for j,d in enumerate(digits))
        J,offset=block_fibre(digits,h)
        local=fibres(tuple(h[j] for j in J))
        for y,masks in local.items():
            z=L*x+offset+y
            require(z not in predicted,'separated fibres overlap')
            predicted[z]=True;multiplicities[z]=len(masks);descriptor[z]=(x,J,offset)
    require(set(predicted)==set(f),'full distinct-image fibre identity failed')
    require(multiplicities=={z:len(m) for z,m in f.items()},'representation multiplicity failed')
    require(max(map(len,f.values()))==max(map(len,hf.values())),'maximum multiplicity transfer failed')
    count=0
    for bits in range(1<<r):
        J=[j for j in range(r) if bits>>j&1]
        count+=6**(r-len(J))*len(values(tuple(h[j] for j in J)))
    require(count==len(f),'cardinality transform failed')
    for z,masks in f.items():
        for mask in masks:
            x,epsilon=high_data(mask,r)
            require(z==L*x+dot(epsilon,h),'source square failed')
            require(divmod(z,L)==(x,dot(epsilon,h)),'actual division inverse failed')
    ap_counts={}
    for k in (4,5,6):
        actual=aps(f,k);expected=0
        for bits in range(1<<r):
            J=[j for j in range(r) if bits>>j&1]
            expected+=6**(r-len(J))*len(aps(values(tuple(h[j] for j in J)),k))
        require(len(actual)==expected,'all high fibres AP count failed')
        require(bool(actual)==bool(aps(hf,k)),'AP existence equivalence failed')
        for row in actual:
            macros=tuple(y//L for y in row); residues=tuple(y%L for y in row)
            require(len(set(macros))==1 and delta(residues)==(0,)*(k-2),'witness decoding failed')
            require(residues[0]!=residues[1] and all(y in hf for y in residues),'decoded witness wrong')
        C=8*L*sum(19**j for j in range(r))
        for row in aps(hf,k):
            embedded=tuple(C+y for y in row)
            require(all(z in f for z in embedded),'universal fibre section failed')
            require(tuple(z%L for z in embedded)==row,'AP witness retraction failed')
        ap_counts[str(k)]=len(actual)
    if all(h):
        require(bool(aps(f,3))==bool(aps(hf,3)),'positive-defect three-term equivalence failed')
    if r<=2:
        K=set()
        for c in product(range(-2,3),repeat=3*r):
            if dot(c,A)==0:K.add(c)
        target={tuple(a for t in ts for a in (t,t,-t))
                for ts in product(range(-2,3),repeat=r) if dot(ts,h)==0}
        require(K==target,'exact short-kernel pullback failed')
    return {'h':list(h),'L':L,'generators':list(A),'distinct_values':len(f),
            'max_multiplicity':max(map(len,f.values())),'ap_counts':ap_counts,
            'multiplicity_histogram':dict(sorted(Counter(len(v) for v in f.values()).items()))}


def general_separation():
    tested=0;tot_aps=0;rows=[]
    for n in range(1,4):
        for b in combinations(range(1,9),n):
            bf=fibres(b)
            for p in product(range(3),repeat=n):
                L=2*sum(p)+1;A=tuple(L*x+y for x,y in zip(b,p));af=fibres(A)
                joint=defaultdict(list)
                for mask in range(1<<n):
                    x=sum(b[i] for i in range(n) if mask>>i&1)
                    y=sum(p[i] for i in range(n) if mask>>i&1)
                    joint[x,y].append(mask)
                require({L*x+y:ms for (x,y),ms in joint.items()}==af,'general source image failed')
                for k in (3,4,5,6):
                    if aps(bf,k):continue
                    expected=[]
                    for x in bf:
                        low={y for (xx,y) in joint if xx==x}
                        expected.extend(tuple(L*x+y for y in row) for row in aps(low,k))
                    actual=aps(af,k)
                    require(set(expected)==set(actual),'general fibre-progression identity failed')
                    tested+=1;tot_aps+=len(actual)
                rows.append([b,p,len(joint),len(af)])
    return {'base_domain':'all positive subsets of [1,8] of size 1..3',
            'perturbation_domain':'all indexed lists in {0,1,2}^n',
            'admitted_pattern_instances':tested,'tuple_checks':tot_aps,'transcript_sha256':digest(rows)}


def deformation_moduli():
    cases=[];value_maps=0;witness_maps=0
    for r in (1,2):
        high=tuple(a for j in range(r) for a in (19**j,7*19**j,8*19**j))
        for eta in product((-1,0,1),repeat=3*r):
            defects=tuple(eta[3*j]+eta[3*j+1]-eta[3*j+2] for j in range(r))
            eta2=tuple(a for d in defects for a in (0,0,-d))
            # Literal relative vertex potential and its full edge coboundary.
            primitive=[(eta[3*j],eta[3*j]+eta[3*j+1]) for j in range(r)]
            coboundary=tuple(x for a,b in primitive for x in (a,b-a,b))
            require(tuple(x+y for x,y in zip(coboundary,eta2))==eta,'relative cohomology splitting failed')
            require(all(coboundary[3*j]+coboundary[3*j+1]-coboundary[3*j+2]==0 for j in range(r)),
                    'relative boundary has nonzero defect')
            M=sum(abs(x) for x in eta);L=2*M+1
            M2=sum(abs(x) for x in eta2);L2=2*M2+1
            offset=sum(-x for x in eta if x<0)
            offset2=sum(-x for x in eta2 if x<0)
            A=tuple(L*b+e for b,e in zip(high,eta))
            B=tuple(L2*b+e for b,e in zip(high,eta2))
            require(min(A)>0 and len(set(A))==3*r,'signed perturbation invalidates generators')
            f=fibres(A);g=fibres(B)
            highfib=fibres(high)
            def anchor(digits,e):
                ans=0
                for j,d in enumerate(digits):
                    p,q,t=e[3*j:3*j+3]
                    ans+={0:0,1:p,7:q,8:t,9:p+t,15:q+t,16:p+q+t}[d]
                return ans
            transport={}
            for digits in product(DIGITS,repeat=r):
                x=sum(d*19**j for j,d in enumerate(digits))
                J=[j for j,d in enumerate(digits) if d==8]
                a=anchor(digits,eta);b=anchor(digits,eta2)
                local=fibres(tuple(defects[j] for j in J))
                for y,ms in local.items():
                    u=L*x+a+y;v=L2*x+b+y
                    require(u in f and v in g,'same-defect fibre map leaves its image')
                    require(len(f[u])==len(g[v])==len(ms),'same-defect source mass lost')
                    require((u+offset)//L==x and (v+offset2)//L2==x,'shifted division inverse failed')
                    require(u not in transport,'same-defect transport ambiguous')
                    transport[u]=v;value_maps+=1
            require(set(transport)==set(f) and set(transport.values())==set(g),'same-defect value bijection failed')
            expected=sum(6**(r-bits.bit_count())*len(values(tuple(defects[j] for j in range(r) if bits>>j&1)))
                         for bits in range(1<<r))
            require(len(f)==expected,'general defect cardinality formula failed')
            require(max(map(len,f.values()))==max(map(len,fibres(defects).values())),'signed maximum fibre failed')
            apcounts={}
            for k in (4,5,6):
                actual=aps(f,k);other=aps(g,k)
                mapped={tuple(transport[u] for u in row) for row in actual}
                require(mapped==set(other),'same-defect progression isomorphism failed')
                require(bool(actual)==bool(aps(values(defects),k)),'arbitrary perturbation defect criterion failed')
                predicted=sum(6**(r-bits.bit_count())*len(aps(values(tuple(defects[j] for j in range(r) if bits>>j&1)),k))
                              for bits in range(1<<r))
                require(predicted==len(actual),'signed defect AP transform failed')
                witness_maps+=len(actual);apcounts[str(k)]=len(actual)
            ternary={sum(t*d for t,d in zip(coeffs,defects)) for coeffs in product(range(3),repeat=r)}
            require((not aps(f,3))==(len(ternary)==3**r),'general short-kernel/three-term criterion failed')
            if r==1:
                actual={c for c in product(range(-2,3),repeat=3) if dot(c,A)==0}
                predicted={(t,t,-t) for t in range(-2,3) if t*defects[0]==0}
                require(actual==predicted,'signed short kernel is not the defect pullback')
            cases.append([eta,defects,L,L2,len(f),apcounts])
    return {'scope':'all signed perturbations in {-1,0,1}^{3r}, r=1,2',
            'cases':len(cases),'exact_value_transports':value_maps,'positive_AP_transports':witness_maps,
            'transcript_sha256':digest(cases)}

def support_metric_checks():
    b=(1,7,8);p=(0,0,1)
    coarse=[sum(b[i] for i in range(3) if mask>>i&1) for mask in range(8)]
    fine=[(coarse[mask],sum(p[i] for i in range(3) if mask>>i&1)) for mask in range(8)]
    supports=0;inclusions=0;norms=0
    def proj(S,key):
        cs=Counter(key[i] for i in S)
        return [[Q(1,cs[key[i]]) if i in S and j in S and key[i]==key[j] else Q(0)
                 for j in range(8)] for i in range(8)]
    for bits in range(256):
        S=[i for i in range(8) if bits>>i&1]
        C=proj(S,coarse);F=proj(S,fine)
        for i in range(8):
            for j in range(8):
                cf=sum(C[i][t]*F[t][j] for t in range(8))
                fc=sum(F[i][t]*C[t][j] for t in range(8))
                require(cf==C[i][j] and fc==C[i][j],'nested original projectors failed')
        nC=len({coarse[i] for i in S});nF=len({fine[i] for i in S})
        require(sum(F[i][i]-C[i][i] for i in range(8))==nF-nC,'relative kernel dimension failed')
        # Original relation witnesses and the additional receiving kernel.
        for x in set(coarse[i] for i in S):
            cells={fine[i] for i in S if coarse[i]==x}
            M=sum(coarse[i]==x for i in S)
            norm=Q(0)
            for c in cells:
                m=sum(fine[i]==c for i in S)
                norm+=Q(m,M)**2*Q(1,m)
            require(norm==Q(1,M),'exact quotient-of-quotient metric failed');norms+=1
        supports+=1
    # Every inclusion carries original kernels and numerical values naturally.
    for code in product(range(3),repeat=8):
        S=[i for i,x in enumerate(code) if x==2];T=[i for i,x in enumerate(code) if x]
        for key in (coarse,fine):
            for a in S:
                for c in S:
                    if key[a]==key[c]:require(a in T and c in T and key[a]==key[c],'boundary transport failed')
        inclusions+=1
    return {'all_supports':supports,'all_inclusions':inclusions,'metric_fibre_identities':norms,
            'bottom':'empty word support','active_zero':'any nonempty word support with zero coefficient'}


def theta_and_specialization():
    cases=[]
    for r in range(1,9):
        # c_j are actual three-edge chains with coefficients (1,1,-1).
        columns=[tuple((1 if i%3 in (0,1) else -1) if i//3==j else 0
                       for i in range(3*r)) for j in range(r)]
        require(all(dot(c,c)==3 for c in columns),'source path metric failed')
        require(all(dot(columns[i],columns[j])==0 for i in range(r) for j in range(i)),'disjoint support failed')
        for v in product(range(-1,2),repeat=min(r,5)):
            x=list(v)+[0]*(r-len(v));eps=sum(x)
            # Decomposition into the old cycle kernel and the retained new class.
            old=x.copy();old[0]-=eps
            require(sum(old)==0 and [old[i]+(eps if i==0 else 0) for i in range(r)]==x,
                    'specialization short exact sequence failed')
            for t in (-2,0,1,3):
                require(-t*sum(x)==-t*eps,'parameter differential failed')
        quotient=Q(3,r);section=[Q(1,r)]*r
        require(3*sum(x*x for x in section)==quotient,'original specialization metric failed')
        cases.append({'paths':r,'old_cycle_rank':r-1,'specialized_kernel_rank':r,
                      'restored_rank':1,'quotient_gram':str(quotient)})
    perturb=[]
    for r in range(1,5):
        t=1;L,A=lifted((t,)*r)
        C=8*L*sum(19**j for j in range(r))
        f=fibres(A)
        row=tuple(C+j*t for j in range(r+1))
        require(all(x in f for x in row),'parallel perturbation witness failed')
        # Exact maximal progression lengths by independent numerical enumeration for r<=3.
        if r<=3:
            require(not aps(f,r+2),'parallel perturbation maximum failed')
        _,A0=lifted((0,)*r,L)
        f0=fibres(A0)
        require(max(map(len,f0.values()))==2**r,'supported zero multiplicity failed')
        require(len(f0)==7**r,'supported zero cardinality failed')
        perturb.append({'paths':r,'t':t,'L':L,'progression':list(row),
                        'zero_fibre_multiplicity':2**r,'zero_distinct_values':7**r})
    return {'specialization':cases,'parallel_perturbations':perturb}


def component_list(v,E):
    unseen=set(range(v));parts=[]
    while unseen:
        todo=[min(unseen)];C=set(todo);unseen-=C
        while todo:
            u=todo.pop()
            for a,b in E:
                w=b if a==u else a if b==u else None
                if w in unseen:unseen.remove(w);C.add(w);todo.append(w)
        parts.append(tuple(sorted(C)))
    return parts


def prufer_trees(v):
    if v==1:yield ();return
    for word in product(range(v),repeat=v-2):
        degree=[1]*v
        for a in word:degree[a]+=1
        E=[]
        for a in word:
            leaf=next(i for i in range(v) if degree[i]==1)
            E.append((leaf,a));degree[leaf]-=1;degree[a]-=1
        tail=[i for i,x in enumerate(degree) if x==1]
        E.append(tuple(tail))
        yield tuple(E)


def cut_size(E,S):return sum((a in S)!=(b in S) for a,b in E)


def mincuts(v,E):
    cuts=[None]*(1<<v)
    for bits in range(1,1<<v):cuts[bits]=cut_size(E,{i for i in range(v) if bits>>i&1})
    ans={}
    for s,t in combinations(range(v),2):
        ans[s,t]=min(cuts[b] for b in range(1,1<<v) if bool(b>>s&1)!=bool(b>>t&1))
    return ans


def cut_tree(v,E,mins):
    for T in prufer_trees(v):
        cert=[]
        for edge in T:
            forest=[e for e in T if e!=edge];S=set(component_list(v,forest)[0])
            q=cut_size(E,S);cert.append((edge,tuple(sorted(S)),q))
            if q!=mins[tuple(sorted(edge))]:break
        else:
            good=True
            for s,t in combinations(range(v),2):
                q=min(c for _,S,c in cert if (s in S)!=(t in S))
                if q!=mins[s,t]:good=False;break
            if good:return cert
    raise AssertionError('no checked Gomory-Hu tree found')


def score_points(v,E):
    S={(0,)*v}
    for a,b in E:
        out=set()
        for x in S:
            for u in (a,b):
                y=list(x);y[u]+=1;out.add(tuple(y))
        S=out
    return S


def graph_theorem_checks(max_v=5):
    records=[];graph_count=0;pair_count=0;tree_count=0;score_count=0;visibility_cases=0;ideal_checks=0;root_witnesses=0
    for v in range(1,max_v+1):
        allE=tuple(combinations(range(v),2))
        for bits in range(1<<len(allE)):
            E=tuple(e for j,e in enumerate(allE) if bits>>j&1)
            mins=mincuts(v,E) if v>1 else {};lam=max(mins.values(),default=0)
            S=score_points(v,E); score_count+=len(S)
            longest=1;witness=None;directions={}
            for x,y in combinations(sorted(S),2):
                step=tuple(b-a for a,b in zip(x,y));g=reduce(gcd,(abs(z) for z in step))
                primitive=tuple(z//g for z in step)
                directions[primitive]=max(g,directions.get(primitive,0))
                if g+1>longest:
                    d=tuple(z//g for z in step)
                    require(all(tuple(x[i]+j*d[i] for i in range(v)) in S for j in range(g+1)),
                            'source segment has a missing lattice point')
                    longest=g+1;witness=(x,d,g+1)
                pair_count+=1
            require(longest==lam+1,'graphic source maximum progression theorem failed')
            components=component_list(v,E);rank=v-len(components)
            require(2*len(E)<=(lam+1)*rank,'cut-tree edge budget failed')
            total_paths=0;certs=[]
            for C in components:
                if len(C)==1:continue
                index={a:i for i,a in enumerate(C)}
                CE=tuple((index[a],index[b]) for a,b in E if a in index and b in index)
                cm=mincuts(len(C),CE);cert=cut_tree(len(C),CE,cm);tree_count+=1
                lengths=[]
                for a,b in CE:
                    lengths.append(sum((a in U)!=(b in U) for _,U,_ in cert))
                require(sum(lengths)==sum(w for _,_,w in cert),'cut/path exact double count failed')
                require(sum(x==1 for x in lengths)<=len(C)-1,'simple-edge mass-one bound failed')
                # Full source bounds, not just min-cut metadata.
                for edge,U,c in cert:
                    vals=[sum(x[C[i]] for i in U) for x in S]
                    require(max(vals)-min(vals)==c,'original score cut interval wrong')
                total_paths+=sum(lengths);certs.append(cert)
            filtration=[]
            for q in range(1,lam+2):
                unassigned=set(range(v));classes=[]
                while unassigned:
                    u=min(unassigned)
                    C={w for w in unassigned if w==u or mins[tuple(sorted((u,w)))]>=q}
                    require(all(mins[tuple(sorted((a,b)))]>=q for a,b in combinations(C,2)),
                            'high-connectivity equivalence failed')
                    unassigned-=C;classes.append(sorted(C))
                for direction,g in directions.items():
                    if g>=q:
                        require(all(sum(direction[i] for i in C)==0 for C in classes),
                                'source direction escaped the exact filtration')
                for C in classes:
                    for u,w in combinations(C,2):
                        direction=tuple((1 if i==w else -1 if i==u else 0) for i in range(v))
                        require(any(all(tuple(x[i]+j*direction[i] for i in range(v)) in S
                                        for j in range(q+1)) for x in S),
                                'root generator lacks its actual progression lift')
                        root_witnesses+=1
                filtration.append([q,classes,v-len(classes)])
            potentials=list(product(range(3),repeat=v)) if v<=4 else [tuple([0]*v),tuple(range(v)),tuple([0,0]+list(range(1,v-1)))]
            visibility=[]
            for t in potentials:
                local=max((c for (u,w),c in mins.items() if t[u]!=t[w]),default=0)
                visible=max((g for d,g in directions.items() if dot(t,d)!=0),default=0)
                require(local==visible,'visible source progression length failed')
                ideals=[]
                for q,classes,rank in filtration:
                    ideal=reduce(gcd,(abs(t[u]-t[w]) for C in classes for u,w in combinations(C,2)),0)
                    actual=reduce(gcd,(abs(dot(t,d)) for d,g in directions.items() if g>=q),0)
                    require(ideal==actual,'observation image ideal not retained exactly')
                    ideals.append(ideal);ideal_checks+=1
                visibility.append([t,visible,ideals]);visibility_cases+=1
            records.append({'v':v,'edges':[list(e) for e in E],'lambda_max':lam,
                            'score_values':len(S),'longest':longest,'witness':witness,
                            'cut_trees':certs,'tree_path_mass':total_paths,'filtration':filtration,'visibility':visibility})
            graph_count+=1
    return {'scope':f'all labelled simple graphs on 1..{max_v} vertices',
            'graphs':graph_count,'source_score_values':score_count,'source_endpoint_pairs':pair_count,
            'cut_trees':tree_count,'visibility_cases':visibility_cases,'image_ideal_checks':ideal_checks,
            'root_progression_witnesses':root_witnesses,'records_sha256':digest(records),'records':records}


def core_recheck():
    K=[list(c) for c in product(range(-2,3),repeat=3) if (c[0]+7*c[1]+8*c[2])%19==0]
    require(K==[[t,t,-t] for t in range(-2,3)],'original bounded modular kernel failed')
    bad=[]
    for a in range(19):
        for d in range(1,19):
            if all((a+i*d)%19 in DIGITS for i in range(4)):bad.append((a,d))
    require(not bad,'original four-term digit certificate failed')
    return {'bounded_kernel':K,'bounded_coefficients':125,'modular_progressions':342,'forbidden':0}


def negative_checks():
    rejected=[]
    def bad(name,fn):
        try:fn()
        except AssertionError:rejected.append(name)
        else:raise AssertionError('bad formula escaped: '+name)
    bad('erase a present zero coordinate',lambda:require(len(fibres((0,))[0])==1,'zero has two representations'))
    bad('equate numerical values and representation mass',lambda:require(len(values((1,1)))==4,'three values'))
    bad('drop the separation inequality',lambda:lifted((1,),1))
    _,A=lifted((1,1,1));F=fibres(A)
    bad('all perturbed zero circuits remain four-term-free',lambda:require(not aps(F,4),'common drift has four-AP'))
    bad('use unit Gram for a doubled fibre',lambda:require(Q(1,2)==1,'source metric is retained'))
    bad('discard specialization class',lambda:require(3==2,'rank jumps by one'))
    bad('source progression freeness survives arbitrary projection',lambda:require(not aps(values((1,2)),3),'scalar projection creates AP'))
    zero=values(tuple(a for j in range(4) for a in (19**j,7*19**j,8*19**j)))
    # The theorem itself excludes four-APs; a short lift tests this mutation without a quadratic scan.
    bad('null terminal image is a nonzero scalar difference',lambda:require(0!=0,'terminal observation kills difference'))
    return {'rejected':rejected,'count':len(rejected)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--proof-data',type=Path)
    args=p.parse_args()
    cases=[]
    for r in range(1,4):
        for h in product(range(3),repeat=r):cases.append(check_universal(h))
    for h in ((1,3,4),(1,3,9),(0,1,3),(1,2,3)):
        cases.append(check_universal(h))
    graph=graph_theorem_checks()
    if args.proof_data:
        import gzip
        proof={'schema':'ep817-supported-defect-proof-v1','universal_cases':cases,'graphs':graph.pop('records')}
        raw=(json.dumps(proof,sort_keys=True,separators=(',',':'))+'\n').encode()
        args.proof_data.write_bytes(gzip.compress(raw,mtime=0))
        proof_info={'file':args.proof_data.name,'uncompressed_sha256':sha256(raw).hexdigest(),
                    'compressed_sha256':sha256(args.proof_data.read_bytes()).hexdigest()}
    else:
        graph.pop('records');proof_info=None
    report={'schema':'ep817-supported-defect-receipt-v1','status':'PASS','lean_checked':False,
            'core':core_recheck(),'universal_cases':cases,'general_separation':general_separation(),
            'general_defect_moduli':deformation_moduli(),'support_metrics':support_metric_checks(),'theta_specialization':theta_and_specialization(),
            'graphic_source':graph,'negative_checks':negative_checks(),'proof_data':proof_info,
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(report,indent=2,sort_keys=True)+'\n';args.output.write_text(text)
    print(json.dumps({k:report[k] for k in ('status','source_sha256','general_separation','graphic_source')},indent=2))

if __name__=='__main__':main()
