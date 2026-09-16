#!/usr/bin/env python3
"""Independent arithmetic audit. Imports neither producer nor source library.

Reconstructs pattern coordinates by interpolation on literal finite sets,
extreme rays from small-support circulations, cycles from cyclic binary words,
and selected digit operators by their action on an actual seven-set basis.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations,product
from functools import reduce
from math import gcd,lcm
from pathlib import Path
import argparse,copy,hashlib,json

SH=((0,),(0,1),(0,2),(0,1,2),(0,3),(0,1,3),(0,1,2,3))
V=(1,2,2,3,2,3,4)

def check(t,m):
    if not t:raise AssertionError(m)
def inner(a,b):return sum(x*y for x,y in zip(a,b))
def times(A,x):return [inner(r,x) for r in A]
def trans(A):return [list(r) for r in zip(*A)]
def mul(A,B):return [[inner(r,c) for c in zip(*B)] for r in A]
def minus(A,B):return [[x-y for x,y in zip(r,s)] for r,s in zip(A,B)]
def unit(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def echelon(A):
    B=[list(map(Q,row)) for row in A];piv=[];r=0
    for j in range(len(B[0]) if B else 0):
        k=next((k for k in range(r,len(B)) if B[k][j]),None)
        if k is None:continue
        B[k],B[r]=B[r],B[k];d=B[r][j];B[r]=[a/d for a in B[r]]
        for i in range(len(B)):
            if i!=r:
                t=B[i][j]
                if t:B[i]=[a-t*b for a,b in zip(B[i],B[r])]
        piv.append(j);r+=1
        if r==len(B):break
    return B,piv

def dim(A):return len(echelon(A)[1])
def null(A,n):
    if not A:return unit(n)
    E,p=echelon(A);ans=[]
    for j in range(n):
        if j in p:continue
        x=[Q(0)]*n;x[j]=Q(1)
        for i,k in enumerate(p):x[k]=-E[i][j]
        ans.append(x)
    return ans

def solution(A,b):
    n=len(A[0]);E,p=echelon([r+[z] for r,z in zip(A,b)])
    if n in p or len(p)!=n:return None
    x=[Q(0)]*n
    for i,k in enumerate(p):x[k]=E[i][-1]
    return x

def prim(x):
    den=lcm(*[Q(a).denominator for a in x]);v=[int(Q(a)*den) for a in x];g=reduce(gcd,v)
    return tuple(a//abs(g) for a in v) if g else tuple(v)

def value_image(A,q):
    counts={0:1}
    for a in A:
        d={}
        for v,w in counts.items():
            for t in range(q):d[v+t*a]=d.get(v+t*a,0)+w
        counts=d
    return counts

def obs(S):return [len({s+r for s in S for r in R}) for R in SH]
def literal_words(S):
    S=set(S);lo,hi=(min(S),max(S)+3) if S else (0,3);out=[0]*16
    for t in range(lo,hi+1):
        e=0
        for i in range(4):
            if t-i in S:e|=1<<i
        out[e]+=1
    return out

def rev(e):
    return sum(((e>>i)&1)<<(3-i) for i in range(4))

def basis_sets():
    sets=[];rows=[]
    for width in range(1,16):
        for half in range(1,1<<((width+1)//2)):
            S={j for i in range((width+1)//2) if half>>i&1 for j in (i,width-1-i)};r=obs(S)
            if dim(rows+[r])>len(rows):rows.append(r);sets.append(sorted(S))
            if len(rows)==7:return sets,rows
    raise AssertionError('no literal seven-set interpolation basis')

def all_cycles():
    cycles=set()
    for p in range(1,9):
        for word in product((0,1),repeat=p):
            edges=tuple(sum(word[(t-i)%p]<<i for i in range(4)) for t in range(p))
            sources=[e>>1 for e in edges]
            if len(set(sources))<p:continue
            check(all((edges[i]&7)==(edges[(i+1)%p]>>1) for i in range(p)),'cyclic word encoding failed')
            cycles.add(min(edges[j:]+edges[:j] for j in range(p)))
    return cycles

def reconstruct_cone(data):
    sets,F=basis_sets();Z=[literal_words(S) for S in sets]
    N=[[0]*7]
    for e in range(1,16):
        row=solution(F,[z[e] for z in Z]);check(row is not None and all(a.denominator==1 for a in row),'pattern interpolation failed')
        N.append(list(map(int,row)))
    check(N==data['pattern_section'],'stored pattern section disagrees with literal words')
    J=[[int(any(e>>i&1 for i in R)) for e in range(16)] for R in SH]
    check(J==data['observation'] and mul(J,N)==unit(7),'stored observation changed')
    B=[[int((e&7)==i)-int((e>>1)==i) for e in range(16)] for i in range(8)]
    check(B==data['incidence'],'original boundary changed')
    eq=[r[:] for r in B]
    for e in range(16):
        if e<rev(e):eq.append([int(i==e)-int(i==rev(e)) for i in range(16)])
    check(dim(eq)==8,'cycle rank wrong')
    check(null(eq+J,16)==[[Q(int(i==0)) for i in range(16)]],'zero-loop kernel lost')
    facets=[N[e] for e in range(1,16) if e<=rev(e)]
    check(facets==data['facets'],'facet table differs from original patterns')
    # Nine reflection-orbit variables, two original balance equations.
    O=(1,2,3,5,6,7,9,11,15)
    balance=[[1,-1,-1,0,0,0,1,0,0],[0,0,1,0,-1,-1,0,1,0]]
    rays=set()
    for size in (1,2,3):
        for I in combinations(range(9),size):
            ns=null([[r[i] for i in I] for r in balance],size)
            if len(ns)!=1:continue
            x=ns[0]
            if all(a<=0 for a in x):x=[-a for a in x]
            if not all(a>0 for a in x):continue
            zz=[0]*16
            for i,a in zip(I,x):zz[O[i]]=a;zz[rev(O[i])]=a
            rays.add(prim(times(J,zz)))
    check(rays==set(map(tuple,data['rays'])) and len(rays)==10,'complete positive-flow ray enumeration failed')
    R=trans(data['rays']);K=data['ray_kernel']
    check(dim(R)==7 and dim(K)==3 and mul(R,K)==[[0]*3 for _ in range(7)],'integer kernel ranks changed')
    check({tuple(c['edges']) for c in data['cycle_decompositions']}==all_cycles(),'missing or extra simple cycle')
    for cy in data['cycle_decompositions']:
        z=[0]*16
        for e in cy['edges']:z[e]+=1;z[rev(e)]+=1
        check(times(J,z)==cy['observation'] and times(R,cy['ray_coefficients'])==cy['observation'],'cycle coefficient certificate failed')
        check(min(cy['ray_coefficients'])>=0,'negative cycle factor')
    for i,r in enumerate(data['rays']):
        f=data['ray_exposures'][i]
        check(inner(f,r)==0 and all(inner(f,s)>0 for j,s in enumerate(data['rays']) if i!=j),'ray exposure failed')
    for f in facets:check(dim([r for r in data['rays'] if inner(f,r)==0])==6,'facet exposure failed')
    return sets,F,N,J,facets


def audit_matrices(data,sets,F,facets):
    count=0;images=0
    for rec in data['selected_matrices']:
        A=rec['weights'];b=rec['base'];D=set(value_image(A,5));responses=[]
        for S in sets:responses.append(obs({d+b*y for d in D for y in S}));images+=1
        recovered=[]
        for j in range(7):
            row=solution(F,[x[j] for x in responses]);check(row is not None,'count interpolation failed');recovered.append(list(row))
        check(recovered==rec['matrix'],'matrix differs from direct numerical-set action')
        M=rec['matrix'];H=rec['positive_lift'];R=trans(data['rays']);K=data['ray_kernel']
        check(all(a>=0 and isinstance(a,int) for row in H for a in row),'lift not integral and positive')
        check(mul(R,H)==mul(M,R),'positive lift square failed')
        check(mul(H,K)==mul(K,rec['kernel_action']),'kernel action failed')
        for ray in data['rays']:check(min(times(facets,times(M,ray)))>=0,'cone preservation failed')
        # Independently check every retained numerical residue partition.
        for shape,labs in zip(SH,rec['residue_labels']):
            E={d+r for d in D for r in shape};covered=set()
            for lab in labs:
                z=lab['residue'];Qset=lab['quotients'];fiber={z+b*q for q in Qset}
                check(fiber=={x for x in E if x%b==z},'residue fibre not exact')
                check(not covered&fiber,'residue fibres overlap');covered|=fiber
                check(lab['offset']==z+b*min(Qset),'actual affine offset lost')
            check(covered==E,'residue support omitted')
        count+=1
    return dict(matrices=count,literal_basis_images=images)


def cell_vertices(facets,extra):
    H=facets+extra;out=set()
    for I in combinations(range(len(H)),6):
        x=solution([[1,0,0,0,0,0,0]]+[H[i] for i in I],[1]+[0]*6)
        if x is not None and all(inner(h,x)>=0 for h in H):out.add(tuple(x))
    return out

def expansion(rows,M,target,facets):
    ct=0
    for a in rows:
        vs=cell_vertices(facets,[[y-x for x,y in zip(a,b)] for b in rows if b!=a])
        check(bool(vs),'missing feasible potential cell')
        for x in vs:
            gx=inner(a,x);check(gx>0,'nonpositive potential')
            for b in rows:check(inner(b,times(M,x))>=target*gx,'actual cone expansion failed');ct+=1
    return ct


def check_switching(data,facets):
    z=data['switching'];X=z['X'];Y=z['Y'];P=mul(X,Y);rays=data['rays'];e=[1,0,0,0,0,0,0]
    check(P==z['product'] and P==[[t*s for s in e] for t in z['product_column']],'rank-one observation failed')
    check(z['product_column'][0]==285 and mul(P,P)==[[285*x for x in row] for row in P],'exact period cost failed')
    a=X[0];diff=[s-17*t for s,t in zip(mul([a],X)[0],a)]
    check(diff==[-28,-36,0,84,0,0,0] and min(inner(diff,v) for v in rays)>=0,'all-cone domination failed')
    check(mul([a],Y)[0]==[285,0,0,0,0,0,0] and 17**2>285 and 21**2>285,'exact two-piece argument failed')
    cols=list(rays)
    for M in (X,Y):cols.extend([[5*a-84*b for a,b in zip(times(M,r),r)] for r in rays])
    check([sum(t*cols[i][j] for t,i in zip(z['farkas_coefficients'],z['farkas_indices'])) for j in range(7)]==[0]*7,'linear-obstruction identity failed')
    check(z['farkas_indices'][0]==9 and z['farkas_coefficients'][0]>0 and all(t>0 for t in z['farkas_coefficients']),'Farkas positivity lost')
    rows=[[Q(x) for x in row] for row in z['rational_rows']];target=Q(z['rational_target'])
    inequalities=sum(expansion(rows,M,target,facets) for M in (X,Y))
    for grid in z['grid_calibrations']:
        r=[[Q(x) for x in row] for row in grid['rows']]
        inequalities+=sum(expansion(r,M,Q(grid['edge_threshold']),facets) for M in (X,Y))
        n=grid['denominator']
        check(all(0<=a-b<Q(1,n) for aa,bb in zip(rows,r) for a,b in zip(aa,bb)),'quantization inequality failed')
    # Different reduced carrier; only the three actual observations needed here.
    mats=[[[M[i][j] for j in (0,1,3)] for i in (0,1,3)] for M in (X,Y)]
    totals=0;mins={}
    def walk(v,depth):
        nonlocal totals
        check(v[0]**2>=285**depth,'independent word inequality failed');totals+=1
        mins[depth]=min(mins.get(depth,v[0]),v[0])
        if depth<13:
            for M in mats:walk(times(M,v),depth+1)
    walk([1,2,3],0)
    check({str(k):v for k,v in mins.items()}==z['minimum_counts'],'enumerated minima mismatch')
    for record in z['direct_original_words']:
        A=record['generators'];check(len(value_image(A,5))==record['fifth_values'],'original word count failed')
    return dict(all_words=totals,cone_inequalities=inequalities,original_generator_words=len(z['direct_original_words']))


def final_obstructions(data):
    z=data['obstructions'];A=z['good'];B=z['bad'];b=z['base']
    da=value_image(A,2);db=value_image(B,2)
    for start in range(b):
        for step in range(1,b):check(not all((start+j*step)%b in da for j in range(5)),'purported admissible original failed')
    check(all(v in db for v in z['bad_progression']),'original inadmissibility witness absent')
    ma=value_image(A,5);mb=value_image(B,5)
    check(set(ma)==set(mb)==set(z['common_fifth_image']),'common value image failed')
    check([max(ma.values()),max(mb.values())]==z['original_peak_masses'] and ma!=mb,'original metric difference failed')


def main():
    p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,default=Path(__file__).with_name('cone_proof.json'))
    p.add_argument('--output',type=Path,default=Path(__file__).with_name('independent_audit.json'));args=p.parse_args()
    data=json.loads(args.proof.read_text());sets,F,N,J,facets=reconstruct_cone(data)
    matrices=audit_matrices(data,sets,F,facets);switch=check_switching(data,facets);final_obstructions(data)
    local=0
    for width in range(1,17):
        for code in range(1<<((width+1)//2)):
            S={j for i in range((width+1)//2) if code>>i&1 for j in (i,width-1-i)}
            words=literal_words(S);check(times(N,obs(S))[1:]==words[1:],'literal local-pattern replay failed');local+=1
    # Mutation targets are checked by the actual proof validators.
    mutations=[]
    for tag,edit,validator in [
        ('pattern sign',lambda d:d['pattern_section'][1].__setitem__(3,1),lambda d:reconstruct_cone(d)),
        ('missing cycle',lambda d:d['cycle_decompositions'].pop(),lambda d:reconstruct_cone(d)),
        ('changed extreme ray',lambda d:d['rays'][0].__setitem__(6,5),lambda d:reconstruct_cone(d)),
        ('erased zero loop',lambda d:d['observation'][0].__setitem__(0,1),lambda d:reconstruct_cone(d)),
        ('negative lift',lambda d:d['selected_matrices'][0]['positive_lift'][0].__setitem__(0,-1),lambda d:audit_matrices(d,sets,F,facets)),
        ('changed Farkas coefficient',lambda d:d['switching']['farkas_coefficients'].__setitem__(0,127009),lambda d:check_switching(d,facets)),
        ('changed product eigenvalue',lambda d:d['switching']['product_column'].__setitem__(0,286),lambda d:check_switching(d,facets)),
        ('conflated word metric',lambda d:d['obstructions']['original_peak_masses'].__setitem__(1,19),lambda d:final_obstructions(d)),
    ]:
        d=copy.deepcopy(data);edit(d)
        try:validator(d)
        except AssertionError:mutations.append(tag)
        else:raise AssertionError('corruption was accepted: '+tag)
    out=dict(schema='ep817-independent-cone-audit-v1',status='PASS',lean_checked=False,
             proof_sha256=hashlib.sha256(args.proof.read_bytes()).hexdigest(),auditor_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             literal_interpolation_basis=sets,symmetric_cycle_dimension=8,observation_kernel_dimension=1,
             extreme_rays=10,facets=9,complete_simple_cycles=len(all_cycles()),literal_symmetric_sources=local,
             matrices=matrices,switching=switch,corruptions_rejected=mutations,
             independence='Imports no producer or source library; uses literal-set interpolation, small-support flow rays and cyclic-word enumeration.')
    text=json.dumps(out,indent=2,sort_keys=True)+'\n';args.output.write_text(text,encoding='utf-8');print(text,end='')
if __name__=='__main__':main()
