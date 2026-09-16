#!/usr/bin/env python3
"""Exact finite proofs for the cone/dual continuation; standard library only."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import exact_cone as c

def pack(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):pack(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [pack(v) for v in x]
    return x

def prove_cone():
    U,N=c.pattern_map();J=c.observation_map();B=c.incidence();E=c.symmetric_equations();R=c.transpose(c.RAYS)
    c.require(c.mm(J,N)==c.eye(7),'section inverse failed')
    c.require(c.mm(B,N)==[[0]*7 for _ in range(8)],'section is not a cycle')
    c.require(c.rank(E)==8,'symmetric cycle dimension failed')
    ker=c.nullspace(E+J)
    c.require(ker==[[F(int(i==0)) for i in range(16)]],'wrong observation kernel')
    c.require(c.rank(R)==7 and c.rank(c.KERNEL)==3 and c.mm(R,c.KERNEL)==[[0]*3 for _ in range(7)],'ray relation sequence failed')
    for z in c.nullspace(E):
        dz=[a-b for a,b in zip(z,c.mv(N,c.mv(J,z)))];c.require(not any(dz[1:]),'zero-loop splitting failed')
    cy=[]
    for e in c.cycles():
        x=c.cycle_vector(e);cy.append(dict(edges=e,observation=x,ray_coefficients=c.greedy_coordinates(x)))
    c.require(len(cy)==19,'incomplete cycle domain')
    per=[]
    for p,r in zip(c.PERIODS,c.RAYS):
        c.require(c.periodic_vector(p)==list(r),'periodic ray failed')
        for m in (1,2,5,17,64):
            word=p*m;n=len(word);P={i for i,b in enumerate(word) if b=='1'};Y=P|{3*n+3-i for i in P}
            x=c.observe(Y);err=[a-2*m*b for a,b in zip(x,r)]
            c.require(c.symmetric(Y) and all(0<=a<=6 for a in err),'periodic approximation bound failed')
            per.append([p,m,x,err])
    fs=c.facets();expos=[]
    for i,r in enumerate(c.RAYS):
        act=[f for f in fs if c.dot(f,r)==0];h=[sum(f[j] for f in act) for j in range(7)]
        c.require(c.rank(act)==6 and all(c.dot(h,s)>0 for j,s in enumerate(c.RAYS) if i!=j),'extreme-ray certificate failed');expos.append(h)
    for f in fs:c.require(c.rank([r for r in c.RAYS if c.dot(f,r)==0])==6,'redundant facet')
    return dict(shapes=c.SHAPES,union_incidence_matrix=U,pattern_section=N,observation=J,incidence=B,
                symmetric_equations=E,facets=fs,facet_words=[f'{e:04b}' for e in range(1,16) if e<=c.reverse(e)],
                rays=c.RAYS,periods=c.PERIODS,ray_kernel=c.KERNEL,cycle_decompositions=cy,
                ray_exposures=expos,periodic_approximation=per)

def finite_sources():
    cases=0;dig=hashlib.sha256()
    for width in range(1,19):
        half=(width+1)//2
        for mask in range(1<<half):
            Y={j for i in range(half) if mask>>i&1 for j in (i,width-1-i)};v=c.observe(Y)
            z=c.word_counts(Y);zp=c.word_counts(Y,7)
            c.require(c.mv(c.observation_map(),z)==v and c.mv(c.incidence(),z)==[0]*8,'literal window square failed')
            c.require(c.mv(c.pattern_map()[1],v)[1:]==z[1:],'pattern reconstruction failed')
            c.require(zp[0]==z[0]+14 and zp[1:]==z[1:],'padding loop failed')
            c.greedy_coordinates(v);cases+=1;dig.update((repr((width,mask,v,z))+'\n').encode())
    flows=0;orbit=(1,2,3,5,6,7,9,11,15)
    for vals in product(range(3),repeat=9):
        u,v,w,d,e,f,g,h,i=vals
        if u+g!=v+w or w+h!=e+f:continue
        z=[0]*16
        for k,a in zip(orbit,vals):z[k]=a;z[c.reverse(k)]=a
        x=c.mv(c.observation_map(),z);coeff=c.greedy_coordinates(x)
        c.require(all(isinstance(a,int) for a in coeff) and c.mv(c.pattern_map()[1],x)==z,'integral Hilbert-basis check failed');flows+=1
    return dict(widths=[1,18],sources=cases,transcript_sha256=dig.hexdigest(),orbit_coordinate_range=[0,2],balanced_flows=flows)

def matrices():
    count=0;direct=0;dig=hashlib.sha256();fs=c.facets();tails=((0,),(0,2,7,9),(0,1,4,5))
    for size in range(1,4):
        for A in combinations(range(1,13),size):
            D=c.image(A);S=sum(A)
            for b in sorted({S+1,S+2,2*S+1,4*S+1}):
                M,_=c.matrix(D,b)
                for r in c.RAYS:c.require(min(c.mv(fs,c.mv(M,r)))>=0,'actual block cone invariance failed')
                for Y in tails:
                    c.require(c.mv(M,c.observe(Y))==c.observe({d+b*y for d in D for y in Y}),'literal transfer failed');direct+=1
                count+=1;dig.update((repr((A,b,M))+'\n').encode())
    digits=0
    for b in range(2,6):
        for W in range(4*(b-1)+1):
            atoms=[(i,W-i) for i in range(1,(W+1)//2)]
            if W>0 and W%2==0:atoms.append((W//2,))
            for bits in range(1<<len(atoms)):
                D={0,W}
                for j,atom in enumerate(atoms):
                    if bits>>j&1:D.update(atom)
                M,_=c.matrix(D,b)
                for r in c.RAYS:c.require(min(c.mv(fs,c.mv(M,r)))>=0,'symmetric digit cone invariance failed')
                digits+=1
    chosen=[((1,),3),((2,),3),((1,2),5),((1,3,4),13),((1,3,4,7),23),((3,10),19),((7,10),19),
            ((3,13),23),((1,4),23),((1,4,5,17,21,22),97),((3,4,7,34,37,41,216,250,253,257),1651)]
    records=[];ms=[]
    for A,b in chosen:
        M,labels=c.matrix(c.image(A),b);H=c.positive_lift(M);action=c.kernel_action(H)
        c.require(c.mm(c.transpose(c.RAYS),H)==c.mm(M,c.transpose(c.RAYS)),'integral lift square failed')
        c.require(c.mm(H,c.KERNEL)==c.mm(c.KERNEL,action),'relation action failed')
        records.append(dict(weights=A,base=b,matrix=M,residue_labels=labels,positive_lift=H,kernel_action=action));ms.append(M)
    pairs=0;nonzero=0;triples=0
    for M,N in product(ms[:6],repeat=2):
        D=c.defect(M,N);pairs+=1;nonzero+=any(any(r) for r in D)
        c.require(c.mm(c.KERNEL,D)==c.subtract(c.mm(c.positive_lift(M),c.positive_lift(N)),c.positive_lift(c.mm(M,N))),'composition primitive failed')
    for M,N,P in product(ms[:4],repeat=3):
        L=c.mm(c.defect(M,N),c.positive_lift(P));d=c.defect(c.mm(M,N),P)
        L=[[x+y for x,y in zip(r,s)] for r,s in zip(L,d)]
        R=c.mm(c.kernel_action(c.positive_lift(M)),c.defect(N,P));d=c.defect(M,c.mm(N,P))
        R=[[x+y for x,y in zip(r,s)] for r,s in zip(R,d)]
        c.require(L==R,'associative defect cocycle failed');triples+=1
    return records,dict(original_blocks=count,original_transfer_comparisons=direct,block_transcript_sha256=dig.hexdigest(),
                        arbitrary_symmetric_digits=digits,integral_lifts=len(records),composition_pairs=pairs,
                        nonzero_composition_defects=nonzero,cocycle_triples=triples)

def switching():
    X=c.matrix(c.image((3,13)),23)[0];Y=c.matrix(c.image((1,4)),23)[0];e=[1,0,0,0,0,0,0];a=X[0]
    P=c.mm(X,Y);w=[r[0] for r in P]
    c.require(P==[[z*t for t in e] for z in w] and w[0]==285,'rank-one product failed')
    c.require(c.mm(P,P)==[[285*x for x in r] for r in P],'product recurrence failed')
    aa=c.mm([a],X)[0]
    c.require([x-17*y for x,y in zip(aa,a)]==[-28,-36,0,84,0,0,0],'X potential identity failed')
    c.require(c.mm([a],Y)[0]==[285,0,0,0,0,0,0],'Y potential identity failed')
    for A in ((3,13),(1,4)):c.require(c.modular_witness(c.image(A,2),23,5) is None,'actual binary modular certificate failed')
    X3=[[X[i][j] for j in (0,1,3)] for i in (0,1,3)];X2=c.mm(X3,X3);X3pow=c.mm(X2,X3)
    c.require([[X3pow[i][j]-31*X2[i][j]+190*X3[i][j]+56*int(i==j) for j in range(3)] for i in range(3)]==[[0]*3 for _ in range(3)],'cubic matrix identity failed')
    rows=[[F(t) for t in e],[F(5*t,84) for t in a]]
    certs=[c.certify_min_expansion(rows,M,F(84,5)) for M in (X,Y)]
    inds=[9,18,19,21,23,24,27];coeff=[127008,81900,1475712,44725,126840,251855,327960]
    columns=list(c.RAYS)
    for M in (X,Y):columns += [[5*z-84*r for z,r in zip(c.mv(M,v),v)] for v in c.RAYS]
    c.require([sum(t*columns[i][j] for t,i in zip(coeff,inds)) for j in range(7)]==[0]*7,'positive Farkas identity failed')
    wc=0;mins={};dig=hashlib.sha256()
    def visit(v,depth):
        nonlocal wc
        n=v[0];c.require(n*n>=285**depth,'uniform switching lower bound failed');wc+=1
        mins[depth]=min(mins.get(depth,n),n);dig.update((repr((depth,v))+'\n').encode())
        if depth<13:visit(c.mv(X,v),depth+1);visit(c.mv(Y,v),depth+1)
    visit(list(c.V0),0)
    direct=[]
    for length in range(1,4):
        for word in product(range(2),repeat=length):
            A=tuple(sorted(23**j*t for j,z in enumerate(word) for t in ((3,13),(1,4))[z]));v=list(c.V0)
            for z in reversed(word):v=c.mv((X,Y)[z],v)
            D=c.image(A);c.require(c.observe(D)==v and c.ap_witness(c.image(A,2),5) is None,'direct original switching check failed')
            direct.append(dict(word=word,generators=A,fifth_values=len(D)))
    macro=(3,13,23,92)
    c.require(len(c.image(macro))==285 and max(c.image(macro))==524 and sum(macro)==131,'original macroblock failed')
    c.require(c.modular_witness(c.image(macro,2),529,5) is None,'macroblock certificate failed')
    grids=[]
    for Ngrid in (137,211,1000):
        approx=[[F((t*Ngrid).__floor__(),Ngrid) for t in row] for row in rows]
        th=F(Ngrid-68,Ngrid)*F(84,5)
        cert=[c.certify_min_expansion(approx,M,th) for M in (X,Y)]
        for old,new in zip(rows,approx):c.require(all(0<=x-y<F(1,Ngrid) for x,y in zip(old,new)) and sum(new)<=1,'rational grid bound failed')
        grids.append(dict(denominator=Ngrid,rows=approx,edge_threshold=th,certificates=cert))
    return dict(X=X,Y=Y,product=P,product_column=w,step_row=a,rational_rows=rows,rational_target=F(84,5),
                potential_checks=certs,farkas_indices=inds,farkas_coefficients=coeff,farkas_positive_term=127008,
                word_horizon=13,all_words=wc,word_transcript_sha256=dig.hexdigest(),minimum_counts=mins,
                direct_original_words=direct,macroblock=macro,macrobase=529,grid_calibrations=grids)

def obstructions():
    good=(1,3,4,7);bad=(1,2,4,8);D1=c.image(good);D2=c.image(bad);M=c.matrix(D1,31)[0]
    c.require(D1==D2==tuple(range(61)) and M==c.matrix(D2,31)[0],'same-matrix arithmetic test failed')
    c.require(c.modular_witness(c.image(good,2),31,5) is None,'good source failed')
    witness=c.ap_witness(c.image(bad,2),5);c.require(witness==[0,1,2,3,4],'bad source witness failed')
    masses=[c.masses(A) for A in (good,bad)];c.require(masses[0]!=masses[1],'word metrics conflated')
    box=(1,1,1,1,1,1,2);c.require(min(c.mv(c.facets(),box))<0,'box relaxation test failed')
    mutants=0
    for thunk in (
        lambda:c.greedy_coordinates(box),
        lambda:c.require(c.pattern_map()[1][15]==[0]*7,'supported all-one word erased'),
        lambda:c.require(c.word_counts({0},3)[0]==c.word_counts({0})[0],'padding loop erased'),
        lambda:c.require(masses[0]==masses[1],'equal count maps identify word metrics'),
        lambda:c.require(c.modular_witness(c.image(bad,2),31,5) is None,'count matrix decides admissibility'),
        lambda:c.certify_min_expansion([[F(1),0,0,0,0,0,0]],c.matrix(c.image((3,13)),23)[0],F(84,5)),
    ):
        try:thunk()
        except AssertionError:mutants+=1
        else:raise AssertionError('false formula was accepted')
    return dict(good=good,bad=bad,base=31,common_matrix=M,common_fifth_image=D1,bad_progression=witness,
                original_peak_masses=[max(x.values()) for x in masses],coarse_box_vector=box,
                coarse_box_pattern_values=c.mv(c.pattern_map()[1],box),false_formulas_rejected=mutants)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).with_name('cone_receipt.json'))
    ap.add_argument('--proof',type=Path,default=Path(__file__).with_name('cone_proof.json'));a=ap.parse_args()
    proof=prove_cone();print('cone proof complete',file=sys.stderr,flush=True)
    finite=finite_sources();print('finite sources complete',file=sys.stderr,flush=True)
    selected,mat=matrices();print('matrix/lift checks complete',file=sys.stderr,flush=True)
    sw=switching();print('switching checks complete',file=sys.stderr,flush=True);ob=obstructions()
    proof.update(selected_matrices=selected,switching=sw,obstructions=ob)
    text=json.dumps(pack(proof),indent=2,sort_keys=True)+'\n';a.proof.write_text(text,encoding='utf-8')
    receipt=dict(schema='ep817-cone-dual-v1',status='PASS',lean_checked=False,
                 scope='Exact finite certificates and replays; unbounded statements have the accompanying ordinary proofs.',
                 finite_sources=finite,matrix_checks=mat,switching=dict(words=sw['all_words'],horizon=13,
                 direct_original_words=len(sw['direct_original_words']),transcript_sha256=sw['word_transcript_sha256']),
                 false_formulas_rejected=ob['false_formulas_rejected'],proof_sha256=hashlib.sha256(text.encode()).hexdigest(),
                 source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                'exact_cone.py':hashlib.sha256(Path(c.__file__).read_bytes()).hexdigest()})
    text=json.dumps(pack(receipt),indent=2,sort_keys=True)+'\n';a.output.write_text(text,encoding='utf-8');print(text,end='')
if __name__=='__main__':main()
