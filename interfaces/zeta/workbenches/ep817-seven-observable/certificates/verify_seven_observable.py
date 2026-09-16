#!/usr/bin/env python3
"""Produce exact bounded evidence for the universal image carrier theorems.

Finite replay is corroborating evidence for the accompanying general proofs.
No new Lean elaboration is asserted. All proof checks use explicit exceptions,
so running under Python -O leaves the checks active.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb, isqrt
from pathlib import Path
import sys

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from image_carrier import (bareiss, bit_image, carrier, has_ap, identity, image,
    image_masses, is_symmetric, mm, moment_step, mv, observed, occurrences,
    polynomial_matrix, power, reflection, require, shape_basis, translated_shape,
    union_to_pattern)


def encoded(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def charpoly(M: list[list[int]]) -> list[int]:
    n = len(M); B = identity(n); out = [1]
    for k in range(1, n + 1):
        A = mm(M, B)
        tr = sum(A[i][i] for i in range(n))
        require(tr % k == 0, "characteristic coefficient lost integral divisibility")
        c = -tr // k
        out.append(c)
        B = [[x + (c if i == j else 0) for j, x in enumerate(row)] for i, row in enumerate(A)]
    require(not any(x for row in B for x in row), "Cayley-Hamilton residual")
    return out


def homogeneous_counts(M: list[list[int]], basis, length: int) -> list[int]:
    v = [len(R) for R in basis]; out = []
    for _ in range(length + 1):
        out.append(v[0]); v = mv(M, v)
    return out


def all_alphabets() -> dict:
    digest = sha256(); cases = joins = moments = symmetric = 0
    tails = [(0,), (0, 1, 3), (-2, 0, 4)]
    for q in range(2, 6):
        basis = shape_basis(q)
        for b in range(2, 5):
            W = (q - 1) * (b - 1)
            for mask in range(1 << W):
                D = (0,) + tuple(j + 1 for j in range(W) if mask >> j & 1)
                M, labels = carrier(D, b, q)
                for Y in tails:
                    old = [observed(Y, q, moment=p) for p in range(3)]
                    actual = tuple(sorted({d + b * y for d in D for y in Y}))
                    got = moment_step(labels, b, old)
                    for p in range(3):
                        target = observed(actual, q, moment=p)
                        require(got[p] == target, f"moment transfer failed: {q,b,D,Y,p}")
                        moments += 1
                    require(mv(M, old[0]) == got[0], "count/moment carrier mismatch")
                    joins += 1
                if is_symmetric(D):
                    C, _ = carrier(D, b, q, True)
                    red = shape_basis(q, True)
                    embed = [[int(min(R, reflection(R)) == Q) for Q in red] for R in basis]
                    require(mm(M, embed) == mm(embed, C), "reflection intertwiner failed")
                    for Y in ((0, 1, 3, 4), (0, 2, 5, 7)):
                        Z = {d + b * y for d in D for y in Y}
                        require(mv(C, observed(Y, q, True)) == observed(Z, q, True), "symmetric transfer failed")
                    symmetric += 1
                cases += 1
                digest.update(encoded([q,b,D,M]))
    return {"q_range":[2,5], "base_range":[2,4],
            "domain":"all D subset [0,(q-1)(b-1)] containing 0",
            "alphabets":cases, "count_joins":joins, "moment_vector_checks":moments,
            "symmetric_sources":symmetric, "transcript_sha256":digest.hexdigest()}


def original_blocks() -> dict:
    digest = sha256(); count = direct = 0
    for n in range(1, 4):
        for A in combinations(range(1, 9), n):
            for q in range(2, 7):
                D = image(A, q)
                for b in sorted({sum(A)+1, sum(A)+2, 2*sum(A)+1}):
                    M, _ = carrier(D,b,q,True)
                    initial = [len(R) for R in shape_basis(q,True)]
                    two = mv(M,mv(M,initial))[0]
                    G = tuple(A)+tuple(b*a for a in A)
                    require(len(set(G))==2*n, "scaled generator collision")
                    require(bit_image(G,q).bit_count()==two, "original generator two-level mismatch")
                    count += 1; direct += 1
                    digest.update(encoded([A,q,b,two]))
    return {"generator_domain":"all nonempty subsets of [1,8] of size at most 3",
            "q_range":[2,6],"radices":"S+1,S+2,2S+1 (duplicates removed)",
            "block_radix_cases":count,"original_two_level_counts":direct,
            "transcript_sha256":digest.hexdigest()}


def mixed_schedules() -> dict:
    dictionary = [((1,),2),((1,),3),((2,),3),((1,2),5),((1,3),7),((2,5),11)]
    digest=sha256(); cases=0; norm_checks=0
    for q in range(2,7):
        basis=shape_basis(q,True); initial=[len(R) for R in basis]
        for seed in range(28):
            length=1+seed%4
            levels=[dictionary[(seed*(j+2)+3*j+j*j)%len(dictionary)] for j in range(length)]
            product=identity(len(basis)); P=1; G=[]
            for A,b in levels:
                M,_=carrier(image(A,q),b,q,True)
                product=mm(product,M);G.extend(P*a for a in A);P*=b
            target=image(G,q); v=mv(product,initial)
            require(v==observed(target,q,True),"mixed numerical image mismatch")
            ratios=[Fraction(a,len(R)) for a,R in zip(v,basis)]
            require(max(ratios)==len(target),"exact weighted matrix norm identity failed")
            for cut in range(1,length):
                P0=1;left=[]
                for A,b in levels[:cut]:left.extend(P0*a for a in A);P0*=b
                P1=1;right=[]
                for A,b in levels[cut:]:right.extend(P1*a for a in A);P1*=b
                X=image(left,q);Y=image(right,q)
                require(len(X)*len(Y)<= (q-1)*len(target),"uniform lower product inequality failed")
                require(len(target)<=len(X)*len(Y),"upper product inequality failed")
                norm_checks+=1
            cases+=1;digest.update(encoded([q,levels,v,product]))
    return {"q_range":[2,6],"specified_schedules":cases,"macro_cut_checks":norm_checks,
            "transcript_sha256":digest.hexdigest()}


def bases_and_minimality() -> dict:
    result=[]
    for q in range(2,8):
        B=shape_basis(q);U=union_to_pattern(q)
        evals=[[len({x+r for x in P for r in R}) for R in B] for P in B]
        require(abs(bareiss(U))==1 and abs(bareiss(evals))==1,"unimodular complete observation basis failed")
        for P in B:
            C=[occurrences(P,R) for R in B]
            require(mv(U,C)==observed(P,q),"inclusion-exclusion basis identity failed")
        red=shape_basis(q,True);L=4*(q-2)+3
        Y=[tuple(sorted(set(R)|{L-r for r in R})) for R in red]
        sym=[[len({y+r for y in S for r in R}) for R in red] for S in Y]
        det=bareiss(sym);require(det!=0,"symmetric observation basis dependent")
        result.append({"q":q,"raw_dimension":len(B),"symmetric_dimension":len(red),
                       "union_to_pattern_determinant":bareiss(U),"raw_evaluation_determinant":bareiss(evals),
                       "symmetric_evaluation_determinant":det})
    B=shape_basis(5,True)
    Ys=[(0,),(0,1),(0,2),(0,1,2),(0,3),(0,1,2,3),(0,1,3,4)]
    evaluation=[observed(Y,5,True) for Y in Ys]
    require(abs(bareiss(evaluation))==1,"seven-observation integral witness failed")
    As=[(4,),(1,),(2,),(3,),(1,2),(1,6),(2,9)]
    actual=[observed(image(A,5),5,True) for A in As]
    require(all(not has_ap(image(A,2),5) for A in As),"admissible independence witness failed")
    require(bareiss(actual)!=0,"actual fifth-arity witnesses fail independence")
    prefixes=[((1,),3),((1,),4),((2,),3),((3,),4),((1,2),5),((1,3),5),((1,6),8)]
    prefix_rows=[];hankel=[]
    for A,b in prefixes:
        residues={x%b for x in image(A,2)}
        require(not any(all((x+j*d)%b in residues for j in range(5)) for x in range(b) for d in range(1,b)),"prefix modular certificate")
        M,_=carrier(image(A,5),b,5,True);prefix_rows.append(M[0])
        row=[]
        for C in As:
            G=tuple(A)+tuple(b*a for a in C)
            require(len(set(G))==len(G),"Hankel generator collision")
            require(not has_ap(image(G,2),5),"Hankel source not five-admissible")
            row.append(len(image(G,5)))
        hankel.append(row)
    require(bareiss(prefix_rows)==-120 and bareiss(hankel)==1228800,"linear realization lower bound failed")
    require(hankel==mm(prefix_rows,[list(c) for c in zip(*actual)]),"Hankel factorization failed")
    extra=(0,2,3,5)
    kernel=[0,1,-1,0,0,0,-1,1]
    packets=Ys+[extra]
    require(all(sum(c*observed(Y,5,True)[i] for c,Y in zip(kernel,packets))==0 for i in range(7)),
            "actual set-object observation kernel")
    raw=shape_basis(5);Z=(0,1,3)
    odd=len({y+r for y in Z for r in (0,1,3)})-len({y+r for y in Z for r in (0,2,3)})
    require(odd!=0,"non-symmetric reflection defect went missing")
    return {"general_dimensions":result,"seven_basis":[list(R) for R in B],
            "symmetric_sets":[list(Y) for Y in Ys],"evaluation_matrix":evaluation,
            "evaluation_determinant":bareiss(evaluation),
            "five_admissible_blocks":[list(A) for A in As],"actual_image_matrix":actual,
            "actual_image_determinant":bareiss(actual),
            "prefix_certificates":[{"generators":list(A),"base":b} for A,b in prefixes],
            "prefix_rows":prefix_rows,"prefix_determinant":bareiss(prefix_rows),
            "admissible_hankel_matrix":hankel,"admissible_hankel_determinant":bareiss(hankel),
            "set_object_observation_kernel":{"sets":[list(Y) for Y in packets],"coefficients":kernel,
                "rank":7,"kernel_rank":1},
            "non_symmetric_observation":{"Y":list(Z),"signed_difference":odd}}


def addvec(out: dict, key, amount: int) -> None:
    out[key]=out.get(key,0)+amount
    if not out[key]:del out[key]


def boundary(chain: dict) -> dict:
    out={}
    for face,c in chain.items():
        if not face:continue
        for i in range(len(face)):addvec(out,face[:i]+face[i+1:],(-1)**i*c)
    return out


def contraction(chain: dict) -> dict:
    out={}
    for face,c in chain.items():
        if 0 not in face:addvec(out,(0,)+face,c)
    return out


def chain_and_metrics() -> dict:
    identities=0
    for size in range(1,7):
        for degree in range(-1,size):
            for face in combinations(range(size),degree+1):
                b={face:1}
                lhs=boundary(contraction(b));other=contraction(boundary(b))
                for f,c in other.items():addvec(lhs,f,c)
                require(lhs==b,"augmented simplex homotopy failed")
                require(not boundary(boundary(b)),"d squared not zero")
                identities+=1
    examples=[((1,2,4),8,(1,)),((1,2,5,10),25,(1,2)),((2,5),8,(1,3)),((1,3),5,(2,7))]
    records=[];fibers=0;section_checks=0
    for q in range(2,7):
        for A,P,B in examples:
            left=image(A,q);right=image(B,q)
            require(max(left)<(q-1)*P,"macro cut example does not satisfy actual width")
            mu=image_masses(A,q);nu=image_masses(B,q)
            f=defaultdict(list)
            for x in left:
                for y in right:f[x+P*y].append((x,y))
            histogram=defaultdict(int)
            for value,pairs in f.items():
                histogram[len(pairs)]+=1
                require(len(pairs)<=q-1,"fiber bound failed")
                masses=[mu[x]*nu[y] for x,y in pairs];W=sum(masses)
                coefficients=[Fraction(w,W) for w in masses]
                require(sum(coefficients)==1,"weighted section is not a section")
                require(sum(c*c/w for c,w in zip(coefficients,masses))==Fraction(1,W),"weighted quotient Gram failed")
                for i in range(1,len(pairs)):
                    require(coefficients[i]/masses[i]==coefficients[0]/masses[0],"boundary orthogonality failed")
                section_checks+=1;fibers+=1
            records.append({"q":q,"left_generators":list(A),"cut_scale":P,"right_generators":list(B),
                            "fiber_histogram":{str(k):v for k,v in sorted(histogram.items())},
                            "domain_size":len(left)*len(right),"image_size":len(f)})
    require(any(r["q"]==5 and "4" in r["fiber_histogram"] for r in records),"sharp fourfold fiber missing")
    return {"simplex_sizes":[1,6],"all_basis_homotopy_identities":identities,
            "actual_numeric_fibers":fibers,"weighted_section_checks":section_checks,"macro_cuts":records}


def selected_matrices() -> list[dict]:
    six=(1,4,5,17,21,22);ten=(3,4,7,34,37,41,216,250,253,257)
    cases=[((1,),3,3),((1,),3,5),((3,),4,5),((1,9),27,3),((1,9),27,5),
           ((1,7,8),19,3),((1,7,8),19,5),
           (six,97,3),(six,97,5),(six,93,3),(six,93,5),
           (ten,1651,3),(ten,1651,4),(ten,1651,5),(ten,4404,5),
           ((3,10),19,5),((6,9),17,5),((7,10),19,5)]
    out=[]
    for A,b,q in cases:
        D=image(A,q);M,labels=carrier(D,b,q,True);p=charpoly(M)
        counts=homogeneous_counts(M,shape_basis(q,True),10)
        direct=[]
        raw_basis=shape_basis(q)
        _,raw_labels=carrier(D,b,q,False)
        moment_vectors=[[sum(r**p for r in R) for R in raw_basis] for p in range(3)]
        moment_records=[]
        for length in (1,2):
            G=[b**j*a for j in range(length) for a in A]
            n=bit_image(G,q).bit_count()
            require(n==counts[length],"selected original generator replay failed")
            direct.append(n)
            moment_vectors=moment_step(raw_labels,b,moment_vectors)
            require(moment_vectors[0][0]==n,"selected moment count mismatch")
            moment_records.append([v[0] for v in moment_vectors])
        record={"generators":list(A),"base":b,"q":q,"local_size":len(D),"matrix":M,
                "characteristic_polynomial_descending":p,"counts_through_length_10":counts,
                "direct_original_counts":direct,"moments_zero_one_two":moment_records,"label_sha256":sha256(encoded(labels)).hexdigest()}
        if q in (3,4,5) and (A,b) in ((six,97),(six,93),(ten,1651),((1,7,8),19)):
            require(bareiss([[b*int(i==j)-M[i][j] for j in range(len(M))] for i in range(len(M))])==0,
                    "stated full-base spectral root absent")
            record["perron_certificate"]={"root":b,"row_sum_upper":max(map(sum,M)),"det_root_minus_matrix":0}
        if A==(1,9):
            rate=9 if q==3 else 17
            require(mm(M,M)==[[rate*x for x in row] for row in M],"rank-one spectral certificate failed")
            require(counts[1]>0,"zero rank-one transfer")
            record["perron_certificate"]={"root":rate,"identity":"M^2 = root*M"}
        if A==ten and b==4404:
            require(p==[1,-4403,8796,0,0,0,0,0],"thin polynomial mismatch")
            record["perron_certificate"]={"quadratic":[1,-4403,8796],"root_interval":[4401,4402]}
        if A in ((3,10),(6,9),(7,10)):
            binary=image(A,2);residues={x%b for x in binary}
            require(not any(all((x+j*d)%b in residues for j in range(5))
                            for x in residues for d in range(1,b)),"new binary modular certificate")
            record["binary_modular_five_certificate"]={"digits":list(binary),
                "candidate_pairs":len(residues)*(b-1),"nonzero_step_witnesses":0}
        if A==(3,10):
            quartic=[1,-36,382,-1116,65]
            require(p==quartic+[0]*3,"quartic source characteristic polynomial")
            def value(x):
                ans=0
                for c in quartic:ans=ans*x+c
                return ans
            brackets=[[0,1],[4,5],[12,13],[18,19]]
            require(all(value(a)*value(b)<0 for a,b in brackets),"quartic root isolation")
            # No linear or irreducible quadratic factor modulo 3.
            rem=[]
            for linear,constant in ((0,1),(1,2),(2,2)):
                coeffs=[c%3 for c in reversed(quartic)]
                for degree in (4,3,2):
                    c=coeffs[degree]
                    coeffs[degree]=0
                    coeffs[degree-1]=(coeffs[degree-1]-c*linear)%3
                    coeffs[degree-2]=(coeffs[degree-2]-c*constant)%3
                require(any(coeffs[:2]),"quartic quadratic divisor modulo three")
                rem.append(coeffs[:2])
            require(all(value(t)%3 for t in range(3)),"quartic linear divisor modulo three")
            record["perron_certificate"]={"quartic":quartic,"root_interval":[18,19],
                "all_real_root_brackets":brackets,"irreducible_modulus":3,
                "irreducible_quadratic_remainders":rem}
            record["count_series"]={"numerator_ascending":[1,-11,43,87],
                                     "denominator_ascending":[1,-36,382,-1116,65]}
        if A==(6,9):
            require(not any(c for row in polynomial_matrix([1,-19,31,51],M) for c in row),
                    "peripheral semisimple minimal polynomial")
            record["perron_certificate"]={"root":17,"row_sum_upper":max(map(sum,M)),
                "det_root_minus_matrix":0,"squarefree_annihilator":[1,-19,31,51]}
            record["count_series"]={"numerator_ascending":[1,-1],"denominator_ascending":[1,-20,51]}
        if A==(7,10):
            v=[2,0,0,0,1,0,0];w=[-227,198,132,0,0,120,0]
            require(mv(M,v)==[13*x for x in v],"retained interior eigenvector")
            require([a-13*x for a,x in zip(mv(M,w),w)]==[462*x for x in v],"retained interior generalized eigenvector")
            record["perron_certificate"]={"root":19,"row_sum_upper":max(map(sum,M)),"det_root_minus_matrix":0}
            record["interior_jordan_chain"]={"eigenvalue":13,"eigenvector":v,
                "generalized_eigenvector":w,"multiplier":462}
            record["count_series"]={"numerator_ascending":[1,-25,243,-795],
                                     "denominator_ascending":[1,-50,888,-6526,16055]}
        if "count_series" in record:
            den=record["count_series"]["denominator_ascending"]
            num=record["count_series"]["numerator_ascending"]
            for j in range(len(counts)):
                require(sum(c*counts[j-h] for h,c in enumerate(den) if h<=j)==(num[j] if j<len(num) else 0),
                        "exact rational count-series coefficient")
        C=max(1,(max(D)+b-2)//(b-1))
        record["boundary_budget"]=C
        pc=record.get("perron_certificate",{})
        rho=pc.get("root")
        if rho is not None:
            require(all(rho**m<=counts[m]<=C*rho**m for m in range(11)),"uniform spectral prefactor")
        upper=pc.get("root",pc.get("root_interval",[None,None])[1])
        if upper is not None:
            N,M1,M2=moment_records[1]
            variance=Fraction(M2,N)-Fraction(M1,N)**2
            lower=Fraction(max(D)**2*(b*b-2)**2,(b-1)**2*C*C*upper**4)
            ceiling=Fraction(max(D)**2*(b+1)**2,4)
            require(lower<=variance<=ceiling,"variance boundary-scale bounds")
            record["second_level_variance"]={"value":str(variance),"lower":str(lower),"upper":str(ceiling)}
        out.append(record)
    return out


def prime(n: int) -> bool:
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))


def reencoding() -> list[dict]:
    out=[]
    for m in (1,2,3):
        C=tuple(sorted(w*27**j for j in range(m) for w in (1,9)))
        D3=image(C,3);D5=image(C,5);mid=2*sum(C)
        differences={x-mid for x in D5 if x>mid}
        rejected=[];p=2
        while True:
            if prime(p):
                witness=next((d for d in sorted(differences) if d%p==0),None)
                if witness is None:break
                rejected.append([p,witness])
            p+=1
        require(len({x%p for x in D3})==len(D3),"faithful prime collision")
        require(len(D5)==25*17**(m-1),"reencoding image formula failed")
        require(p<=256+2*(len(D5)-1)*(5*m+2),"prime budget failed")
        require(not has_ap(image(C,2),3),"input source is not three-admissible")
        binary=image(C,2)
        require(not any(all((x+j*d)%p in {u%p for u in binary} for j in range(3))
                        for x in range(p) for d in range(1,p)),"modular three-term witness in reencoding")
        two=image(tuple(C)+tuple(p*a for a in C),2)
        lookup={d%p:d for d in binary}
        require(len(two)==len(binary)**2,"actual binary lift cardinality")
        for y in two:
            d0=lookup[y%p];tail=(y-d0)//p
            require(tail in binary and y==d0+p*tail,"actual-digit inverse failed")
        out.append({"blocks":m,"unchanged_generators":list(C),"prime":p,
                    "two_level_binary_values":len(two),
                    "ternary_size":len(D3),"fifth_arity_size":len(D5),
                    "rejected_prime_witnesses":rejected,
                    "distinct_generator_residues":len({a%p for a in C})})
    return out


def regressions_and_nonstationary() -> dict:
    rejected=0
    for D,b,q,sym in [((0,5),2,5,False),((0,1,3),2,5,True), ((),3,5,False)]:
        try:carrier(D,b,q,sym)
        except AssertionError:rejected+=1
        else:raise AssertionError("invalid-input mutation passed")
    # Empty residue supports are missing terms, not singleton zero carries.
    M,labels=carrier((0,4),7,5,True)
    require(sum(M[0])==2<7,"absent residue distinction failed")
    # True H5 tails distinguish all seven observation functions.
    require(bases_and_minimality()["actual_image_determinant"]!=0,"minimality mutation failed")
    # Period-order matters: retain two actual fifth-arity transfers.
    A,_=carrier(image((2,9),5),23,5,True)
    B,_=carrier(image((3,8),5),29,5,True)
    require(mm(A,B)!=mm(B,A),"order regression is accidentally commuting")
    # Full matrix peripheral multiplicity does not license a nilpotent collapse.
    C,_=carrier(image((3,),5),4,5,True)
    require(polynomial_matrix([1,-5,4],C)==[[0]*7 for _ in range(7)],"semisimple peripheral control failed")
    # A nonstationary all-prefix three-admissible schedule with no entropy limit.
    # Stage j has j! copies of base 3 (odd j) or base 5 (even j), A={1}.
    levels=[];fac=1;records=[]
    for j in range(1,7):
        fac*=j;b=3 if j%2 else 5
        levels.extend([b]*fac)
        P=1;G=[]
        for a in levels:G.append(P);P*=a
        N=4*sum(G)+1
        basis=shape_basis(5,True);v=[len(R) for R in basis]
        for a in reversed(levels):
            T,_=carrier((0,1,2,3,4),a,5,True);v=mv(T,v)
        require(v[0]==N,"factorial-stage count failed")
        records.append({"stage":j,"length":len(levels),"radix":b,
                        "count_sha256":sha256(str(N).encode()).hexdigest(),"count_bit_length":N.bit_length()})
    word_mass=[]
    for m in range(1,9):
        masses=image_masses([3**j for j in range(m)],5)
        require(len(masses)==2*3**m-1 and sum(masses.values())==5**m,"original word-mass return example")
        require(max(masses.values())*len(masses)>=5**m,"original metric-return lower bound")
        word_mass.append({"length":m,"distinct_values":len(masses),"original_words":sum(masses.values()),
                          "maximum_mass":max(masses.values())})
    return {"original_word_metric_example":word_mass,
            "invalid_inputs_rejected":rejected,"absent_residue_row":M[0],
            "noncommuting_product_left":mm(A,B),"noncommuting_product_right":mm(B,A),
            "factorial_stage_replay":records}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=HERE.with_name("seven_observable_receipt.json"))
    parser.add_argument("--quick",action="store_true",help="Only selected finite certificates; not the full replay")
    args=parser.parse_args()
    report={"schema":"ep817-seven-observable-v1","status":"PASS","lean_checked":False,
            "scope":"Written general proofs plus explicitly bounded exact checks",
            "selected_matrices":selected_matrices(),"minimality":bases_and_minimality(),
            "chain_and_metrics":chain_and_metrics(),"faithful_reencoding":reencoding(),
            "regressions":regressions_and_nonstationary()}
    if not args.quick:
        report["all_alphabets"]=all_alphabets()
        report["original_blocks"]=original_blocks()
        report["mixed_schedules"]=mixed_schedules()
    report["full_replay"]=not args.quick
    report["source_sha256"]={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest()
                             for p in (HERE,ROOT/"tools"/"image_carrier.py")}
    text=json.dumps(report,sort_keys=True,indent=2)+"\n"
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text,encoding="utf-8")
    print(json.dumps({"status":"PASS","full_replay":not args.quick,"receipt":str(args.output),
                      "sha256":sha256(text.encode()).hexdigest()},sort_keys=True))

if __name__=="__main__":main()
