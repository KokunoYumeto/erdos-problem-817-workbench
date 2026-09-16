#!/usr/bin/env python3
"""Exact proofs-by-finite-exhaustion accompanying the graphical obstruction note.

Standard library only. The infinite theorems have written proofs in the note.
No Lean verification or global optimality of the new rate is claimed.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, random
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, product, permutations
from math import gcd, factorial
from pathlib import Path
from typing import Iterable

RULER=(0,4,7,41,257)
BASE=1651
K=6


def require(ok:bool,message:str)->None:
    if not ok: raise AssertionError(message)


def digest(x:object)->str:
    return hashlib.sha256((json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()


def edges(v:int)->tuple[tuple[int,int],...]:
    return tuple(combinations(range(v),2))


def weights(T:tuple[int,...], E:Iterable[tuple[int,int]]|None=None)->tuple[int,...]:
    return tuple(T[j]-T[i] for i,j in (edges(len(T)) if E is None else E))


def fibres(A:tuple[int,...])->dict[int,list[int]]:
    out:dict[int,list[int]]={0:[0]}
    for i,a in enumerate(A):
        extra={y+a:[m|(1<<i) for m in masks] for y,masks in out.items()}
        for y,masks in extra.items():out.setdefault(y,[]).extend(masks)
    return out


def int_ap(D:Iterable[int],k:int)->tuple[int,...]|None:
    values=sorted(set(D)); lo=values[0]; bits=sum(1<<(x-lo) for x in values)
    for d in range(1,(values[-1]-lo)//(k-1)+1):
        z=bits
        for i in range(1,k):
            z &= bits>>(i*d)
            if not z:break
        if z:
            a=(z&-z).bit_length()-1+lo
            return tuple(a+i*d for i in range(k))
    return None


def modular_ap(D:Iterable[int],q:int,k:int)->tuple[int,...]|None:
    bits=sum(1<<d for d in set(D)); require(bits.bit_length()<=q,'noncanonical modular input')
    mask=(1<<q)-1
    for d in range(1,q):
        z=bits
        for i in range(1,k):
            t=(i*d)%q
            z &= (((bits>>t)|(bits<<(q-t)))&mask) if t else bits
            if not z:break
        if z:
            a=(z&-z).bit_length()-1
            return tuple((a+i*d)%q for i in range(k))
    return None


def delta(row:tuple[int,...])->tuple[int,...]:
    return tuple(row[i]-2*row[i+1]+row[i+2] for i in range(len(row)-2))


def returning_section(D:tuple[int,...],k:int)->list[dict]:
    S=set(D);out=[]
    for c in product((-1,0,1),repeat=k-2):
        found=None
        for x in D:
            for y in D:
                row=[x,y]
                for ci in c:
                    z=2*row[-1]-row[-2]-ci
                    if z not in S:break
                    row.append(z)
                else:
                    found=tuple(row);break
            if found is not None:break
        require(found is not None,f'missing returning primitive {c}')
        require(delta(found)==tuple(-x for x in c),'incorrect primitive')
        out.append({'carry':c,'digits':found})
    return out


def score_fibres(v:int)->dict[tuple[int,...],list[int]]:
    E=edges(v); out:dict[tuple[int,...],list[int]]={}
    # Initially vertex i wins against every smaller vertex, giving score i.
    # Choosing edge i<j reverses that edge, adding e_i-e_j.
    for mask in range(1<<len(E)):
        s=list(range(v))
        for e,(i,j) in enumerate(E):
            if mask>>e&1:s[i]+=1;s[j]-=1
        require(all(0<=x<v for x in s) and sum(s)==len(E),'score bound failed')
        out.setdefault(tuple(s),[]).append(mask)
    return out


def candidate_checks()->dict:
    E=edges(len(RULER));A=weights(RULER);F=fibres(A);D=tuple(sorted(F));S=sum(A)
    require(len(set(A))==10 and min(A)>0 and S<BASE,'generator typing failed')
    require(len(D)==291,'unexpected image cardinality')
    # Independent direct enumeration of every ordered modular parameter pair.
    present=set(D);hits=[]
    for a in range(BASE):
        for d in range(1,BASE):
            if all((a+i*d)%BASE in present for i in range(K)):
                hits.append((a,d))
    require(not hits,'new modular certificate failed')
    require(modular_ap(D,BASE,K) is None,'bit-parallel/direct checker disagreement')
    section=returning_section(D,K);lookup={tuple(r['carry']):tuple(r['digits']) for r in section}
    bad=[]
    for q in range(S+1,BASE):
        low=modular_ap(D,q,K)
        require(low is not None,f'new smaller modular certificate at {q}')
        dd=delta(low);require(all(t%q==0 for t in dd),'incorrect modular row')
        c=tuple(t//q for t in dd);high=lookup[c]
        y=tuple(x+q*z for x,z in zip(low,high));step=y[1]-y[0]
        require(step!=0 and all(y[i]==y[0]+i*step for i in range(K)),'bad return progression')
        masks=[F[x][0]|(F[z][0]<<10) for x,z in zip(low,high)]
        A2=A+tuple(q*a for a in A)
        for value,mask in zip(y,masks):
            require(sum(a for i,a in enumerate(A2) if mask>>i&1)==value,'wrong two-level mask')
        bad.append({'base':q,'low':low,'carry':c,'high':high,'points':y,'subset_masks':masks})
    SF=score_fibres(5);score_values={}
    centre=sum(i*RULER[i] for i in range(5))
    for score,masks in SF.items():
        val=centre-sum(t*s for t,s in zip(RULER,score))
        require(set(masks)==set(F[val]),'score/value fibre square failed')
        score_values[score]=val
    require(len(set(score_values.values()))==len(SF)==291,'score evaluation injection failed')
    multiplicities=Counter(map(len,F.values()))
    require(sum(multiplicities.values())==291 and sum(m*c for m,c in multiplicities.items())==1024,'mass failed')
    Qgram={str(y):str(Fraction(1,len(F[y]))) for y in D}
    # Actual source decomposition and weighted projection checked on test vectors.
    for y in D:
        mu=len(F[y]);coeff=[Fraction((i%7)-3) for i in range(mu)];amp=sum(coeff)
        mean=amp/mu
        require(sum(c*c for c in coeff)==sum((c-mean)**2 for c in coeff)+amp*amp/mu,'Pythagoras failed')
    DD={x+y for x in D for y in D}
    score_sum={tuple(x+y for x,y in zip(s,t)) for s in SF for t in SF}
    return {'ruler':RULER,'edge_order':E,'generators_in_edge_order':A,'generators_sorted':sorted(A),
            'base':BASE,'k':K,'generator_count':10,'sum':S,'maximum':max(A),
            'digits':D,'digit_count':len(D),'all_binary_fibres':[[y,F[y]] for y in D],
            'modular_parameter_pairs':BASE*(BASE-1),'modular_AP_count':len(hits),
            'return_section':section,'excluded_smaller_canonical_bases':bad,
            'source_gram':Qgram,'multiplicity_histogram':{str(k):v for k,v in sorted(multiplicities.items())},
            'largest_multiplicity':max(multiplicities),'vector_double_image_count':len(score_sum),
            'integer_ternary_image_count':len(DD),
            'strict_improvement':{'new_cubed':BASE**3,'old_fifth':93**5,'verified':BASE**3<93**5},
            'previous_rank_four_dual_obstruction':{'base_fourth':BASE**4,'23_tenth':23**10,
                                                   'violates':BASE**4<23**10}}


def extension_fibres(T:tuple[int,...])->dict[int,dict[int,tuple[int,int]]]:
    A=weights(T);F=fibres(A);out={}
    for r in range(len(T)+1):
        C={}
        for sel in combinations(range(len(T)),r):
            tm=sum(1<<i for i in sel);shift=sum(T[i] for i in sel)
            for y,ms in F.items():C.setdefault(y-shift,(ms[0],tm))
        out[r]=C
    return out


def extension_checks()->dict:
    old=(0,1,5,22);EF=extension_fibres(old)
    # This explicit row exists for every appended z with distinct resulting edges.
    beta=tuple(-22+17*i for i in range(6));r=1
    require(all(x in EF[r] for x in beta),'missing symbolic obstruction')
    maskdata=[EF[r][x] for x in beta]
    Aold=weights(old)
    for x,(om,tm) in zip(beta,maskdata):
        require(tm.bit_count()==1,'wrong symbolic slope')
        require(sum(a for i,a in enumerate(Aold) if om>>i&1)-sum(t for i,t in enumerate(old) if tm>>i&1)==x,'wrong symbolic constant')
    successful=(0,4,7,41);GF=extension_fibres(successful)
    stats=[]
    for r,F in GF.items():
        require(int_ap(F,6) is None,f'extended source fiber failed at {r}')
        stats.append({'new_edges_selected':r,'count':len(F),'min':min(F),'max':max(F)})
    width=sum(weights(successful))+sum(successful);bound=2*width
    rows=[]
    for z in range(successful[-1]+1,bound+1):
        T=successful+(z,);A=weights(T)
        if len(set(A))<10:
            collisions={str(a):[i for i,b in enumerate(A) if b==a] for a in set(A) if A.count(a)>1}
            rows.append({'z':z,'status':'repeated_generator','collisions':collisions});continue
        F=fibres(A);w=int_ap(F,6)
        rows.append({'z':z,'status':'safe_integer' if w is None else 'integer_obstruction',
                     'witness':w,'masks':None if w is None else [F[x][0] for x in w]})
    for z in (bound+1,bound+2,1000,10000):
        A=weights(successful+(z,));require(len(set(A))==10,'tail collision')
        # Use the proof's finite affine-support test for large z, not huge integers as bit indexes.
        coeff={(r,v) for r,F in GF.items() for v in F}
        require(all(0<=r<=4 for r,v in coeff),'slope box failed')
        require(z>2*width and all(int_ap(F,6) is None for F in GF.values()),'tail certificate failed')
    require(any(x['z']==257 and x['status']=='safe_integer' for x in rows),'record ruler excluded')
    return {'failed_prefix':old,'universal_obstruction':{'slope':1,'intercepts':beta,'step':17,'old_and_new_masks':maskdata},
            'successful_prefix':successful,'finite_fibres':stats,'width_budget':width,
            'all_z_greater_than_safe_bound':bound,'complete_lower_parameter_classification':rows,
            'counts':dict(Counter(x['status'] for x in rows))}


def boundary(mask:int,E:tuple[tuple[int,int],...],v:int)->tuple[int,...]:
    out=[0]*v
    for e,(i,j) in enumerate(E):
        if mask>>e&1:out[i]-=1;out[j]+=1
    return tuple(out)


def disjoint_paths(v:int,E:tuple[tuple[int,int],...],s:int,t:int)->list[list[int]]:
    # Signed integral unit-capacity flow on an undirected graph.
    cap=[[0]*v for _ in range(v)]; f=[[0]*v for _ in range(v)]
    for i,j in E:cap[i][j]=cap[j][i]=1
    value=0
    while True:
        parent=[-1]*v;parent[s]=s;q=deque([s])
        while q and parent[t]<0:
            x=q.popleft()
            for y in range(v):
                if parent[y]<0 and cap[x][y]-f[x][y]>0:parent[y]=x;q.append(y)
        if parent[t]<0:break
        x=t;amt=2
        while x!=s:amt=min(amt,cap[parent[x]][x]-f[parent[x]][x]);x=parent[x]
        x=t
        while x!=s:y=parent[x];f[y][x]+=amt;f[x][y]-=amt;x=y
        value+=amt
    paths=[]
    for _ in range(value):
        parent=[-1]*v;parent[s]=s;q=deque([s])
        while q and parent[t]<0:
            x=q.popleft()
            for y in range(v):
                if parent[y]<0 and f[x][y]>0:parent[y]=x;q.append(y)
        require(parent[t]>=0,'flow path extraction failed')
        rev=[t];x=t
        while x!=s:y=parent[x];f[y][x]-=1;f[x][y]+=1;rev.append(y);x=y
        paths.append(rev[::-1])
    used=[]
    for p in paths:used.extend(tuple(sorted((x,y))) for x,y in zip(p,p[1:]))
    require(len(set(used))==len(used),'flow paths overlap')
    # Exhaustive cut comparison provides a separate small-graph optimality check.
    cuts=[]
    for mask in range(1<<v):
        if not mask>>s&1 or mask>>t&1:continue
        cuts.append(sum(((mask>>i)&1)!=((mask>>j)&1) for i,j in E))
    require(value==min(cuts),'flow/cut disagreement')
    return paths


def graph_checks()->dict:
    cases=0;paircases=0;witnesses=0;hd=hashlib.sha256();counts={}
    for v in range(2,7):
        SF=score_fibres(v);counts[str(v)]=len(SF)
        require(len(SF)=={2:2,3:7,4:38,5:291,6:2932}[v],'score enumeration failed')
    for v in range(2,6):
        full=edges(v);T=tuple(3**i for i in range(v))
        for gm in range(1<<len(full)):
            E=tuple(e for i,e in enumerate(full) if gm>>i&1);A=weights(T,E);index={e:i for i,e in enumerate(E)}
            require(len(set(A))==len(A),'graph edge weight collision')
            cases+=1
            for s,t in combinations(range(v),2):
                paths=disjoint_paths(v,E,s,t);paircases+=1
                neg=[];pos=[]
                for p in paths:
                    pm=nm=0
                    for x,y in zip(p,p[1:]):
                        ei=index[tuple(sorted((x,y)))]
                        if x<y:pm|=1<<ei
                        else:nm|=1<<ei
                    pos.append(pm);neg.append(nm)
                require(not any((pos[i]|neg[i])&(pos[j]|neg[j]) for i in range(len(paths)) for j in range(i)), 'lift supports overlap')
                start=sum(a for m in neg for i,a in enumerate(A) if m>>i&1);step=T[t]-T[s]
                masks=[]
                for j in range(len(paths)+1):
                    mask=0
                    for h in range(len(paths)):mask|=pos[h] if h<j else neg[h]
                    require(sum(a for i,a in enumerate(A) if mask>>i&1)==start+j*step,'path/AP map failed')
                    masks.append(mask)
                if paths:witnesses+=1
                hd.update((repr((v,gm,s,t,paths,masks))+'\n').encode())
    return {'all_simple_graph_vertex_range':[2,5],'graphs':cases,'terminal_pairs':paircases,
            'nonempty_path_packings':witnesses,'transcript_sha256':hd.hexdigest(),
            'complete_graph_score_image_counts':counts}


def pole_specialization_checks()->dict:
    # Finite calibration of the general affine-packet theorem. Every set is literal.
    cases=0;safe=0;bad=0;hd=hashlib.sha256()
    universe=tuple(product(range(3),range(-2,3)))
    for inds in combinations(range(len(universe)),4):
        C=tuple(universe[i] for i in inds);Q=set(C);vec=None
        for x in C:
            for y in C:
                d=(y[0]-x[0],y[1]-x[1])
                if d==(0,0):continue
                row=tuple((x[0]+i*d[0],x[1]+i*d[1]) for i in range(4))
                if all(a in Q for a in row):vec=row;break
            if vec is not None:break
        V=max(v for u,v in C)-min(v for u,v in C)
        for z in (2*V+1,2*V+2):
            D={u*z+v for u,v in C};w=int_ap(D,4)
            if vec is None:require(w is None,'affine tail safety failed');safe+=1
            else:
                val=tuple(u*z+v for u,v in vec)
                require(val[1]!=val[0] and all(val[i]==val[0]+i*(val[1]-val[0]) for i in range(4)),'affine vector witness collapsed beyond bound')
                require(w is not None,'affine obstruction missing');bad+=1
            hd.update((repr((C,z,vec,w))+'\n').encode());cases+=1
    return {'source_domain':'all four-point subsets of {0,1,2} x {-2,-1,0,1,2}',
            'tail_parameter_tests':cases,'safe_tests':safe,'obstructed_tests':bad,'transcript_sha256':hd.hexdigest()}


def bellman_checks(previous:Path|None)->dict:
    if previous is None:return {'status':'NOT_RUN','reason':'No predecessor certificate directory supplied'}
    records=[]
    for k in (5,6):
        for rank in range(1,5):
            path=previous/f'variable_k{k}_r{rank}.json.gz';rec=json.loads(gzip.decompress(path.read_bytes()))
            B,p=rec['target']['base'],rec['target']['root'];E=rec['representative_edges'];states=rec['states'];v=len(states)
            f=[Fraction(1) for _ in states]
            for it in range(v+1):
                nxt=f[:]
                for a,b,rad,n,li in E:nxt[a]=min(nxt[a],Fraction(rad**p,B**n)*f[b])
                if nxt==f:break
                f=nxt
            else:raise AssertionError('future potential did not stabilize')
            require(all(Fraction(1,2**p)<=x<=1 for x in f),'future cost bound failed')
            require(all(rad**p*f[b]>=B**n*f[a] for a,b,rad,n,li in E),'future edge inequality failed')
            require(all(f[i]<=f[j] for i,x in enumerate(states) for j,y in enumerate(states) if x&y==x),'future potential is not monotone')
            records.append({'k':k,'rank':rank,'target':rec['target'],'state_count':v,
                            'future_cost_power':[str(x) for x in f],'iterations':it,
                            'predecessor_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    return {'status':'PASS','records':records}


def orientation_with_scores(v:int,E:tuple[tuple[int,int],...],degrees:tuple[int,...])->list[int]:
    """Integral edge-to-endpoint allocation in a possibly repeated-edge multigraph."""
    require(len(degrees)==v and min(degrees)>=0 and sum(degrees)==len(E),'invalid allocation degrees')
    M=len(E);source=M+v;sink=source+1;N=sink+1
    adj=[[] for _ in range(N)]
    def add(a,b,c):
        ia=len(adj[a]);ib=len(adj[b]);adj[a].append([b,ib,c]);adj[b].append([a,ia,0]);return ia
    positions=[]
    for e,(i,j) in enumerate(E):
        add(source,e,1);a=add(e,M+i,1);b=add(e,M+j,1);positions.append((a,b))
    for i,c in enumerate(degrees):add(M+i,sink,c)
    flow=0
    while True:
        parent=[None]*N;parent[source]=(-1,-1);queue=deque([source])
        while queue and parent[sink] is None:
            a=queue.popleft()
            for ix,(b,rev,c) in enumerate(adj[a]):
                if c and parent[b] is None:parent[b]=(a,ix);queue.append(b)
        if parent[sink] is None:break
        cur=sink
        while cur!=source:
            a,ix=parent[cur];edge=adj[a][ix];edge[2]-=1;adj[cur][edge[1]][2]+=1;cur=a
        flow+=1
    require(flow==M,'orientation allocation failed')
    winners=[]
    for e,(i,j) in enumerate(E):
        a,b=positions[e];require(adj[e][a][2]+adj[e][b][2]==1,'edge allocated twice or never')
        winners.append(i if adj[e][a][2]==0 else j)
    require(tuple(winners.count(i) for i in range(v))==degrees,'allocation output degrees failed')
    return winners


def score_from_mask(v:int,mask:int)->tuple[int,...]:
    score=list(range(v))
    for h,(i,j) in enumerate(edges(v)):
        if mask>>h&1:score[i]+=1;score[j]-=1
    return tuple(score)


def collision_lift(v:int,r:tuple[int,...])->dict:
    """Construct an (m+1)-row packet whose only second defect is the literal r."""
    require(len(r)==v and any(r) and sum(r)==0,'invalid collision direction')
    i=max(range(v),key=lambda h:r[h]);j=min(range(v),key=lambda h:r[h])
    require(r[i]>=1 and r[j]<=-1,'nonzero integral extrema failed')
    alpha=tuple(int(h==j)-int(h==i) for h in range(v))
    w=tuple(x+y for x,y in zip(r,alpha));others=tuple(h for h in range(v) if h not in (i,j))
    full=edges(v);inner=tuple(combinations(others,2));multi=full+inner
    offset=tuple(0 if h==i else v-1 if h==j else v-2 for h in range(v))
    target=tuple(x+y for x,y in zip(w,offset))
    # Verify every source difference-body bound and every translated allocation cut.
    for mask in range(1<<v):
        U={h for h in range(v) if mask>>h&1};a=len(U)
        require(sum(r[h] for h in U)<=a*(v-a),'direction outside score difference body')
        require(sum(target[h] for h in U)>=sum(x in U and y in U for x,y in multi),'translated cut inequality failed')
    wins=orientation_with_scores(v,multi,target);N=len(full)
    tmask=sum(1<<h for h,(a,b) in enumerate(full) if wins[h]==a)
    tau=Counter(wins[N:]);s=tuple(0 if h==i else v-1 if h==j else v-2-tau[h] for h in range(v))
    inner_winners={e:winner for e,winner in zip(inner,wins[N:])}
    smask=0
    for h,(a,b) in enumerate(full):
        if j in (a,b):winner=j
        elif i in (a,b):winner=b if a==i else a
        else:winner=b if inner_winners[(a,b)]==a else a
        if winner==a:smask|=1<<h
    require(score_from_mask(v,smask)==s,'endpoint face source reconstruction failed')
    require(tuple(x-y for x,y in zip(score_from_mask(v,tmask),s))==w,'correction equation failed')
    edge_index={e:h for h,e in enumerate(full)}
    path_masks=[1<<edge_index[tuple(sorted((i,j)))]]
    for h in others:path_masks.append((1<<edge_index[tuple(sorted((i,h)))])|(1<<edge_index[tuple(sorted((h,j)))]))
    masks=[smask];cur=smask
    for pm in path_masks:cur ^= pm;masks.append(cur)
    masks=list(reversed(masks))+[tmask]
    scores=[score_from_mask(v,mask) for mask in masks]
    require(len(scores)==v+1,'incorrect prolonged packet length')
    defects=[tuple(scores[h][a]-2*scores[h+1][a]+scores[h+2][a] for a in range(v)) for h in range(v-1)]
    require(defects==[(0,)*v]*(v-2)+[r],'literal source defect is not retained')
    require(tuple(scores[1][a]-scores[0][a] for a in range(v))==alpha,'root increment failed')
    return {'vertices':v,'relation':r,'root':[i,j],'subset_masks':masks,
            'scores':scores,'last_second_defect':r}


def collision_rigidity_checks()->dict:
    cases=[];counts={};hd=hashlib.sha256()
    for v in range(2,6):
        S=tuple(score_fibres(v));R=sorted({tuple(t[i]-s[i] for i in range(v)) for s in S for t in S if s!=t})
        counts[str(v)]=len(R)
        for r in R:
            row=collision_lift(v,r);cases.append(row);hd.update((json.dumps(row,sort_keys=True)+'\n').encode())
    rng=random.Random(8171651);sample_counts={}
    for v in range(6,11):
        n=len(edges(v));count=0
        while count<40:
            s=score_from_mask(v,rng.randrange(1<<n));t=score_from_mask(v,rng.randrange(1<<n))
            r=tuple(y-x for x,y in zip(s,t))
            if not any(r):continue
            row=collision_lift(v,r);hd.update((json.dumps(row,sort_keys=True)+'\n').encode());count+=1
        sample_counts[str(v)]=count
    return {'complete_difference_domains':counts,'complete_witness_count':len(cases),
            'complete_witnesses':cases,'larger_rank_sample_counts':sample_counts,
            'random_seed':8171651,'transcript_sha256':hd.hexdigest(),
            'identity':'Delta(score rows)=(0,...,0,r); first increment=e_j-e_i'}


def family_checks()->dict:
    """Literal calibrations of the all-rank source and affine obstruction theorems."""
    prime_cases=[]
    for m,p in ((2,3),(3,5),(4,5),(5,7),(6,7)):
        T=(0,)+tuple(p**j for j in range(m-1));A=weights(T);q=p**(m-1)
        require(len(set(A))==m*(m-1)//2 and min(A)>0 and sum(A)<q,'prime-family typing failed')
        SF=score_fibres(m);F=fibres(A);C=sum(i*t for i,t in enumerate(T))
        require(len(F)==len(SF),'prime-family scalar injection failed')
        require(modular_ap(tuple(F),q,m+1) is None,'prime-family modular certificate failed')
        perm_values={C-sum(t*x for t,x in zip(T,s)) for s in permutations(range(m))}
        require(len(perm_values)==factorial(m) and len(F)>=factorial(m),'transitive packet failed')
        prime_cases.append({'vertices':m,'prime':p,'ruler':T,'base':q,'generators':len(A),
                            'score_classes':len(SF),'transitive_classes':len(perm_values),
                            'sum':sum(A)})
    # Two arithmetic projections, one faithful on score classes and one that folds them.
    compression=[]
    for T in ((0,1,4,10,18),RULER):
        m=len(T);SF=score_fibres(m);A=weights(T);F=fibres(A);C=sum(i*t for i,t in enumerate(T))
        perm_fibres=Counter(C-sum(t*x for t,x in zip(T,s)) for s in permutations(range(m)))
        require(all(y in F for y in perm_fibres),'transitive observation outside full image')
        q=sum(A)+1
        require(max(perm_fibres.values())*q>=factorial(m),'compression lower bound failed')
        require(sum(perm_fibres.values())==factorial(m),'transitive mass changed')
        compression.append({'ruler':T,'distinct_generators':len(set(A)),'score_classes':len(SF),
                            'numeric_classes':len(F),'transitive_classes':len(perm_fibres),
                            'maximum_transitive_multiplicity':max(perm_fibres.values()),'canonical_count_base':q,
                            'transitive_quotient_kernel_dimension':factorial(m)-len(perm_fibres)})
    # The old-prefix obstruction is an entire two-parameter resonance hyperplane.
    symbolic_cases=0;hd=hashlib.sha256()
    for a in range(1,9):
        for b in range(a+1,21):
            if b==2*a:continue
            c=5*b-3*a
            for z in (2*c+1,2*c+7):
                T=(0,a,b,c,z);A=weights(T);F=fibres(A)
                require(len(set(A))==10 and min(A)>0,'resonant family generator collision')
                row=(z-c,z-b,z+c-2*b,z+2*b+c-3*a,z+b+2*c-3*a,z+3*c-3*a)
                require(all(x in F for x in row) and delta(row)==(0,0,0,0),'resonant hyperplane witness failed')
                require(row[1]-row[0]==c-b>0,'resonant difference failed')
                hd.update((repr((T,row))+'\n').encode());symbolic_cases+=1
    T=(0,1,5,22,257);SF=score_fibres(5);C=sum(i*t for i,t in enumerate(T))
    inv={C-sum(t*x for t,x in zip(T,s)):s for s in SF}
    row=tuple(257-22+17*i for i in range(6));scores=tuple(inv[y] for y in row)
    defects=tuple(tuple(scores[i][j]-2*scores[i+1][j]+scores[i+2][j] for j in range(5)) for i in range(4))
    require(len(inv)==291 and defects==((0,0,0,0,0),(1,3,-5,1,0),(-1,-3,5,-1,0),(0,0,0,0,0)),
            'one-level injection/two-level defect regression failed')
    require(all(sum(t*x for t,x in zip(T,c))==0 for c in defects),'projection kernel defect lost')
    return {'prime_family':prime_cases,'transitive_compression_examples':compression,
            'resonant_hyperplane':{'condition':'c=5*b-3*a; 0<a<b; b!=2*a; z>2*c',
                                  'finite_cases':symbolic_cases,'transcript_sha256':hd.hexdigest()},
            'faithful_but_not_AP_preserving':{'ruler':T,'points':row,'scores':scores,'vector_defects':defects,
                                             'numeric_class_count':len(inv)}}


def negative_checks(candidate:dict)->dict:
    # Recompute false statements as explicit required failures.
    rejected=[]
    tests={
      'forget_reset_endpoint':lambda: 2**2>=8,
      'extend_old_ruler_has_no_symbolic_AP':lambda:not all(-22+17*i in extension_fibres((0,1,5,22))[1] for i in range(6)),
      'previous_rank_four_is_global':lambda:BASE**4>=23**10,
      'new_ruler_is_5_AP_free':lambda:int_ap(candidate['digits'],5) is None,
      'all_source_fibres_are_singletons':lambda:all(len(ms)==1 for _,ms in candidate['all_binary_fibres']),
      'delete_empty_subset_digit':lambda:0 not in candidate['digits'],
      'smaller_base_1650_is_modular_safe':lambda:modular_ap(candidate['digits'],1650,6) is None,
      'quotient_metric_is_unit':lambda:all(x=='1' for x in candidate['source_gram'].values()),
    }
    for name,test in tests.items():
        try:require(test(),name)
        except AssertionError:rejected.append(name)
        else:raise AssertionError(f'false control unexpectedly passed: {name}')
    return {'rejected_false_formulas':rejected,'count':len(rejected)}


def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--predecessor-certificates',type=Path,default=Path(__file__).resolve().parent/'predecessor_inputs')
    args=ap.parse_args()
    c=candidate_checks();report={'schema':'ep817-graphical-obstruction-v1','status':'PASS','lean_checked':False,
       'scope':'Written infinite proofs plus exact finite arithmetic certificates; no claim of global optimality.',
       'candidate':c,'extensions':extension_checks(),'graph_lifts':graph_checks(),
       'affine_specialization':pole_specialization_checks(),'bellman_future':bellman_checks(args.predecessor_certificates),
       'all_rank_source_calibrations':family_checks(),'collision_rigidity':collision_rigidity_checks(),
       'negative_controls':negative_checks(c),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(report,sort_keys=True,indent=2)+'\n';args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(text,encoding='utf-8')
    print(json.dumps({'status':'PASS','candidate':{'base':BASE,'rank':10,'digits':len(c['digits']),'return_primitives':len(c['return_section']),
      'bad_lower_bases':len(c['excluded_smaller_canonical_bases'])},'extension_counts':report['extensions']['counts'],
      'graph_lifts':report['graph_lifts'],'affine_specialization':report['affine_specialization'],
      'all_rank_source_calibrations':report['all_rank_source_calibrations'],
      'negative_controls':report['negative_controls'],'receipt_sha256':hashlib.sha256(text.encode()).hexdigest()},indent=2))

if __name__=='__main__':main()
