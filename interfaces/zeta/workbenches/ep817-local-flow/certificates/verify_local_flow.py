#!/usr/bin/env python3
"""Exact finite certificates for the local-flow and switching theorems.

The general statements are proved in the accompanying note. Bounded replay
counts are explicit; no output is a Lean elaboration or an all-rank search.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from local_flow import (A,B,CONSERVATION,ORBITS,PERIODS,RAY_SUPPORTS,SHAPES,
    bit_image,charpoly,cone_rays,count_carrier,decompose,dual_certificate,eye,image,incidence,
    integer_ap,mm,modular_safe,mv,observations,power,rank,require,reverse_bits,
    simple_cycles,substitution,symmetric,symmetric_period,transpose,window_counts)


def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def symmetric_sets(max_span):
    yield (0,)
    for span in range(1,max_span+1):
        pairs=[]
        for i in range(1,span//2+1):pairs.append({i,span-i})
        for mask in range(1<<len(pairs)):
            Y={0,span}
            for i,p in enumerate(pairs):
                if mask>>i&1:Y|=p
            yield tuple(sorted(Y))


def symmetric_digits(q,b,max_width=8):
    for D in symmetric_sets(min(max_width,(q-1)*(b-1))):yield D


def cone_certificate():
    require(mm(B,A)==eye(7),'integer inverse BA')
    require(mm(CONSERVATION,A)==[[0]*7]*2,'conservation inverse')
    circuits=cone_rays()
    expected=[[int(j in s) for j in range(9)] for s in RAY_SUPPORTS]
    require(sorted(circuits)==sorted(expected),'complete ray enumeration')
    rays=[]
    for z,word in zip(expected,PERIODS):
        f=mv(B,z);circ=[0]*16;p=len(word)
        for t in range(p):
            e=sum(int(word[(t-i)%p])<<i for i in range(4));circ[e]+=1
        sym=[circ[e]+circ[reverse_bits(e,4)] for e in range(16)]
        zz=[sym[e] for e in ORBITS]
        require(mv(CONSERVATION,zz)==[0,0],'period balance')
        require(all(zz[j]*f[0]==z[j]*mv(B,zz)[0] for j in range(9)),'period does not realize ray')
        approximants=[]
        for N in (1,2,4,8,16):
            Y=symmetric_period(word,N);F=observations(Y)
            require(symmetric(Y),'symmetric period construction')
            h=word.count('1')
            # Exact scaled bound, avoiding fractions.
            require(all(abs(F[i]*f[0]-2*N*h*f[i])<=12*f[0] for i in range(7)),
                    'period boundary estimate')
            approximants.append({'repetitions':N,'size':len(Y),'observations':F})
        rays.append({'defect_ray':z,'count_ray':f,'period':word,'approximants':approximants})
    require(rank([r['count_ray'] for r in rays])==7,'cone dimension')
    facets=[]
    for i in range(9):
        on=[r['count_ray'] for r in rays if r['defect_ray'][i]==0]
        require(rank(on)==6,'facet was redundant')
        facets.append({'pattern':format(ORBITS[i],'04b'),'row':A[i],'zero_face_rank':6})
    cycles=[]
    for nodes,edges in simple_cycles():
        c=[0]*16
        for e in edges:c[e]+=1
        c=[c[e]+c[reverse_bits(e,4)] for e in range(16)]
        z=[c[e] for e in ORBITS]
        cycles.append({'vertices':list(nodes),'edges':list(edges),'symmetric_current':c,
                       'circuit_coefficients':decompose(z)})
    require(len(cycles)==19,'directed simple-cycle count')
    # Arbitrary integral flows in a stated coefficient domain.
    tested=0
    for coeff in product(range(3),repeat=6):
        z=[sum(coeff[i]*expected[i][j] for i in range(6)) for j in range(9)]
        decompose(z);tested+=1
    for coeff in product(range(3),repeat=4):
        z=[sum(coeff[i]*expected[i+6][j] for i in range(4)) for j in range(9)]
        decompose(z);tested+=1
    return {'A':A,'B':B,'conservation':CONSERVATION,'rays':rays,'facets':facets,
            'simple_cycles':cycles,'integral_decompositions_tested':tested}


def original_set_replay():
    count=0;hashes=[]
    for Y in symmetric_sets(16):
        c=window_counts(Y);f=observations(Y);z=[c[e] for e in ORBITS]
        require(mv(incidence(5),c)==[0]*8,'original cycle boundary')
        require(all(c[e]==c[reverse_bits(e,4)] for e in range(16)),'reversal current')
        require(mv(A,f)==z and mv(B,z)==f,'local counts inverse')
        require(mv(CONSERVATION,z)==[0,0] and min(z)>=0,'local positive constraints')
        require(c[0]==max(Y)-min(Y)+4-f[-1],'zero-loop gap count')
        decompose(z);hashes.append([Y,c,f]);count+=1
    nonsymmetric=0
    for bits in range(1,1<<9):
        Y={i for i in range(9) if bits>>i&1}
        c=window_counts(Y);require(mv(incidence(5),c)==[0]*8,'nonsymmetric boundary')
        # The actual reflection-double source, with a retained separating gap.
        Z=Y|{24-y for y in Y}
        require(symmetric(Z),'reflection-double source')
        f=observations(Z);require(mv(A,f)==[x for e,x in enumerate(window_counts(Z)) if e in ORBITS],
                                 'reflection-double local identities')
        nonsymmetric+=1
    Y1=(0,4);Y2=(0,5)
    require(observations(Y1)==observations(Y2),'gap example counts')
    dif=[y-x for x,y in zip(window_counts(Y1),window_counts(Y2))]
    require(dif==[1]+[0]*15,'retained gap kernel')
    return {'symmetric_max_span':16,'symmetric_sources':count,'nonsymmetric_masks':nonsymmetric,
            'transcript_sha256':digest(hashes),'gap_example':{'sources':[Y1,Y2],
             'common_observations':observations(Y1),'current_difference':dif}}


def substitution_replay():
    tested=0;joins=0;edge_paths=0;records=[]
    tails=((0,),(0,1),(0,2,4),(-2,0,2),(0,1,4,5))
    for q in range(2,7):
        for b in range(2,7):
            for D in symmetric_digits(q,b):
                out=substitution(D,b,q);L=out['edges']
                for Y in tails:
                    X={d+b*y for d in D for y in Y}
                    predicted=mv(L,window_counts(Y,q));predicted[0]-=out['zero_padding']
                    require(predicted==window_counts(X,q),'exact zero-padding action')
                    if q==5:
                        require(mv(out['counts'],observations(Y))==observations(X),'seven transfer on sets')
                        z=[window_counts(Y)[e] for e in ORBITS]
                        require(mv(out['patterns'],z)==[window_counts(X)[e] for e in ORBITS],
                                'nine transfer on sets')
                    joins+=1
                tested+=1;edge_paths+=len(out['paths'])
                records.append([q,b,D,out['vertex_function'],digest(out['paths'])])
    return {'arity_range':[2,6],'base_range':[2,6],'maximum_digit_width':8,
            'complete_symmetric_digit_cases':tested,'actual_joins':joins,
            'entire_edge_paths':edge_paths,'transcript_sha256':digest(records)}


def selected_matrices():
    blocks=[((1,),3),((3,10),19),((7,10),19),((1,3),10),((2,4),10),
            ((1,7,8),19),((1,4,5,17,21,22),97),((1,4,5,17,21,22),93),
            ((3,4,7,34,37,41,216,250,253,257),1651)]
    out=[]
    for weights,b in blocks:
        D=image(weights,5);s=substitution(D,b)
        entry={'weights':weights,'base':b,'digits':D,'count_matrix':s['counts'],
               'pattern_matrix':s['patterns'],'edge_matrix':s['edges'],
               'vertex_function':s['vertex_function'],'vertex_matrix':s['vertices'],
               'zero_padding':s['zero_padding'],
               'count_charpoly':charpoly(s['counts']),
               'edge_charpoly':charpoly(s['edges'])}
        emb=[[int(e!=0 and min(e,reverse_bits(e,4))==o) for o in ORBITS] for e in range(16)]
        section=mm(emb,A);gram=mm(transpose(section),section)
        lam=[b*int(j==6)-s['counts'][6][j] for j in range(7)]
        diff=[[x-y for x,y in zip(a0,b0)] for a0,b0 in zip(mm(s['edges'],section),mm(section,s['counts']))]
        require(diff==[lam]+[[0]*7 for _ in range(15)],'original zero-loop section defect')
        lhs=mm(transpose(mm(s['edges'],section)),mm(s['edges'],section))
        rhs=mm(transpose(s['counts']),mm(gram,s['counts']))
        rhs=[[rhs[i][j]+lam[i]*lam[j] for j in range(7)] for i in range(7)]
        require(lhs==rhs,'original pattern-current Gram correction')
        entry.update({'section_defect':lam,'quotient_gram':gram})
        out.append(entry)
    return out


def switching_certificate():
    Ma=count_carrier(image((1,3),5),10);Mb=count_carrier(image((2,4),5),10)
    require(modular_safe((1,3),10) and modular_safe((2,4),10),'modular source certificate')
    u=[17,18,19,19,20,20,20];v=[0,2,0,3,0,0,0]
    require(mm(Ma,Mb)==[[x*y for y in v] for x in u],'rank-one AB identity')
    Au=mv(Ma,u)
    require(mv(mm(Ma,Ma),u)==[11*x-10*y for x,y in zip(Au,u)],'A recurrence on u')
    vB=mv(transpose(Mb),v)
    require(mv(transpose(mm(Mb,Mb)),v)==[11*x-10*y for x,y in zip(vB,v)],'B recurrence on v')
    tests=[]
    for a in range(1,13):
        for b in range(1,13):
            val=sum(x*y for x,y in zip(v,mv(mm(power(Mb,b-1),power(Ma,a-1)),u)))
            target=(8*10**(a+b)+4*10**b-3)//9
            require(val==target,'all-run scalar formula')
            require(val**3>=893**(a+b),'run lower bound')
            tests.append([a,b,val])
    require(93**3>893**2 and 80000>9*93**2 and 933**2>93**3,
            'exact all-length minimizing comparisons')
    word_rows=[];products={():eye(7)};initial=[len(R) for R in SHAPES]
    for length in range(1,11):
        for word in product((0,1),repeat=length):
            M=mm(products[word[:-1]],(Ma,Mb)[word[-1]]);products[word]=M
            N=mv(M,initial)[0]
            radius=sum(M[i][i] for i in range(7)) if 0 in word and 1 in word else 10**length
            require(radius**3>=893**length and radius<=N<=4*radius,'full-word lower certificate')
            if length<=4:
                P=1;weights=[]
                for e in word:
                    weights.extend(P*a for a in ((1,3),(2,4))[e]);P*=10
                require(bit_image(weights,5).bit_count()==N,'direct switched numerical image')
                require(integer_ap(image(weights,2),5) is None,'switched binary witness')
            word_rows.append([list(word),N,radius])
    P=mm(mm(Ma,Ma),Mb)
    require(charpoly(P)==[1,-893,0,0,0,0,0,0],'AAB characteristic polynomial')
    counts=[]
    for m in range(1,13):
        N=mv(power(P,m),initial)[0]
        require(N==2301*893**(m-1),'period image formula');counts.append(N)
    return {'A':{'weights':[1,3],'base':10,'matrix':Ma},
            'B':{'weights':[2,4],'base':10,'matrix':Mb},
            'AB_factor_u':u,'AB_factor_v':v,'run_values':tests,
            'words_through_length':10,'word_instances':len(word_rows),
            'word_transcript_sha256':digest(word_rows),
            'attaining_period':[0,0,1],'macro_weights':[1,3,10,30,200,400],
            'macro_base':1000,'macro_matrix':P,'period_counts':counts,
            'exact_comparisons':{'93_cubed':93**3,'893_squared':893**2,
              'lower_for_length_at_least_4':[80000,9*93**2],
              'wrong_three_run':[933**2,93**3]}}


def saturation_certificate():
    blocks=[((1,7,8),19),((1,4,5,17,21,22),97),
            ((1,4,5,17,21,22),93),((3,4,7,34,37,41,216,250,253,257),1651)]
    ms=[];records=[]
    for A0,b in blocks:
        D3=image(A0,3);require({d%b for d in D3}==set(range(b)),'record ternary residue coverage')
        M=count_carrier(image(A0,5),b);require(mv(M,[1]*7)==[b]*7,'common occupied ray')
        ms.append(M);records.append({'weights':A0,'base':b,'ternary_values':len(D3),
                                    'covered_residues':b})
    direct=[]
    for i,(A0,b) in enumerate(blocks):
        for j,(A1,c) in enumerate(blocks):
            G=tuple(A0)+tuple(b*a for a in A1);N=bit_image(G,5).bit_count()
            require(mv(mm(ms[i],ms[j]),[len(R) for R in SHAPES])[0]==N,'saturated direct pair')
            require(b*c<=N<=4*b*c-3,'saturated bound')
            require({d%(b*c) for d in image(G,3)}==set(range(b*c)),
                    'saturated product residue transport')
            direct.append([i,j,len(G),N])
    rows=[]
    for word in product(range(4),repeat=4):
        M=eye(7);cost=1
        for i in word:M=mm(M,ms[i]);cost*=blocks[i][1]
        N=mv(M,[len(R) for R in SHAPES])[0]
        require(cost<=N<=4*cost-3 and mv(M,[1]*7)==[cost]*7,'changing saturated block')
        rows.append([word,N,cost])
    return {'blocks':records,'direct_two_level_cases':direct,
            'four_level_word_instances':len(rows),'word_transcript_sha256':digest(rows)}


def dual_replay():
    cases=[]
    for w in product((-1,0,1),repeat=7):
        cert=dual_certificate(w);cases.append({'row':list(w),'certificate':cert})
    return {'coefficient_domain':[-1,0,1],'rows_tested':len(cases),
            'nonnegative_rows':sum(row['certificate']['nonnegative'] for row in cases),
            'actual_finite_violations':sum(not row['certificate']['nonnegative'] for row in cases),
            'cases':cases}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=ROOT/'certificates/local_flow_receipt.json')
    args=ap.parse_args()
    report={'schema':'ep817-local-flow-v1','status':'PASS','lean_checked':False,
            'scope':'Proved all-rank statements in companion note; only listed domains exhaustively replayed.',
            'cone':cone_certificate(),'original_sets':original_set_replay(),
            'substitution_replay':substitution_replay(),'selected_matrices':selected_matrices(),
            'switching':switching_certificate(),'saturation':saturation_certificate(),
            'linear_dual':dual_replay(),
            'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (Path(__file__),ROOT/'tools/local_flow.py')}}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':report['status'],'output':str(args.output),
                     'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
                     'substitution_replay':report['substitution_replay']},indent=2))

if __name__=='__main__':main()
