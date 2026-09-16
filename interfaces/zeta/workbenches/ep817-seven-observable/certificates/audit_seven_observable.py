#!/usr/bin/env python3
"""Independent integer audit of the seven-observable contribution.

Imports neither the producer nor its carrier library. Count matrices are
recovered by interpolation on literal finite-set joins rather than by carry
fibers. Original large-generator moments use bytewise bit-image moments.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations,product
import json
from math import comb,isqrt
from pathlib import Path

HERE=Path(__file__).resolve();ROOT=HERE.parents[1]


def require(ok,msg):
    if not ok:raise AssertionError(msg)


def serial(x):return (json.dumps(x,sort_keys=True,separators=(",",":"))+"\n").encode()


def basis(q,red=False):
    sets=[tuple(i for i in range(q-1) if mask>>i&1) for mask in range(1,1<<(q-1),2)]
    if red:sets=list({min(R,tuple(sorted(R[-1]-r for r in R))) for R in sets})
    return sorted(sets,key=lambda R:(R[-1],len(R),R))


def inverse(A):
    n=len(A);M=[[Fraction(x) for x in row]+[Fraction(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        p=next(i for i in range(j,n) if M[i][j]);M[j],M[p]=M[p],M[j]
        v=M[j][j];M[j]=[x/v for x in M[j]]
        for i in range(n):
            if i!=j:
                a=M[i][j];M[i]=[x-a*y for x,y in zip(M[i],M[j])]
    return [row[n:] for row in M]


def det(A):
    if not A:return 1
    M=[[Fraction(x) for x in row] for row in A];r=Fraction(1);n=len(A)
    for j in range(n):
        p=next((i for i in range(j,n) if M[i][j]),None)
        if p is None:return 0
        if p!=j:M[j],M[p]=M[p],M[j];r=-r
        x=M[j][j];r*=x
        for i in range(j+1,n):
            ratio=M[i][j]/x
            M[i]=[u-ratio*v for u,v in zip(M[i],M[j])]
    require(r.denominator==1,"determinant integrality")
    return int(r)


def join(X,R):return {x+r for x in X for r in R}


def interpolate(D,b,q,red=False):
    B=basis(q,red);Q=q-2;L=4*Q+3
    tests=[set(P)|{L-p for p in P} for P in B] if red else [set(P) for P in B]
    E=[[len(join(Y,R)) for R in B] for Y in tests]
    # Cache no source carrier: this inverse depends only on literal test sets.
    key=(q,red)
    if key not in INV:INV[key]=inverse(E)
    V=INV[key]
    targets=[[len(join({d+b*y for d in D for y in Y},R)) for R in B] for Y in tests]
    rows=[]
    for r in range(len(B)):
        row=[]
        for j in range(len(B)):
            value=sum(V[j][i]*targets[i][r] for i in range(len(B)))
            require(value.denominator==1,"interpolated count matrix is nonintegral")
            row.append(int(value))
        require(all(v>=0 for v in row),"interpolated count matrix is negative")
        rows.append(row)
    return rows
INV={}


def mult(M,v):return [sum(x*y for x,y in zip(row,v)) for row in M]


def original_image(A,q):
    masses={0:1}
    for a in reversed(A):
        nxt=Counter()
        for value,mass in masses.items():
            for c in range(q):nxt[value+c*a]+=mass
        masses=dict(nxt)
    return masses


def raw_bits(A,q):
    bits=1
    for a in reversed(A):
        original=bits
        for c in range(1,q):bits|=original<<(a*c)
    return bits
BYTE=[(x.bit_count(),sum(i for i in range(8) if x>>i&1),sum(i*i for i in range(8) if x>>i&1)) for x in range(256)]


def bit_moments(bits):
    totals=[0,0,0]
    for j,byte in enumerate(bits.to_bytes((bits.bit_length()+7)//8,"little")):
        a,b,c=BYTE[byte];offset=8*j
        totals[0]+=a;totals[1]+=offset*a+b;totals[2]+=offset*offset*a+2*offset*b+c
    return totals


def pvalue(coeffs,t):
    value=0
    for c in coeffs:value=value*t+c
    return value


def validate_selected(data):
    expected=[([1],3,3),([1],3,5),([3],4,5),([1,9],27,3),([1,9],27,5),
              ([1,7,8],19,3),([1,7,8],19,5),
              ([1,4,5,17,21,22],97,3),([1,4,5,17,21,22],97,5),
              ([1,4,5,17,21,22],93,3),([1,4,5,17,21,22],93,5),
              ([3,4,7,34,37,41,216,250,253,257],1651,3),
              ([3,4,7,34,37,41,216,250,253,257],1651,4),
              ([3,4,7,34,37,41,216,250,253,257],1651,5),
              ([3,4,7,34,37,41,216,250,253,257],4404,5),
              ([3,10],19,5),([6,9],17,5),([7,10],19,5)]
    require([(r['generators'],r['base'],r['q']) for r in data]==expected,"selected domain mismatch")
    counts=moments=0
    for row in data:
        A,b,q=row['generators'],row['base'],row['q'];D=set(original_image(A,q));B=basis(q,True)
        M=interpolate(D,b,q,True)
        require(M==row['matrix'],"selected matrix interpolation mismatch")
        require(len(D)==row['local_size'],"local image size")
        v=[len(R) for R in B]
        for j in range(11):
            require(v[0]==row['counts_through_length_10'][j],"selected iterate mismatch")
            require(max(Fraction(x,len(R)) for x,R in zip(v,B))==v[0],"weighted observation norm")
            v=mult(M,v)
        cp=row['characteristic_polynomial_descending'];n=len(M)
        require(len(cp)==n+1 and cp[0]==1,"characteristic polynomial degree")
        for t in range(n+1):
            require(det([[t*int(i==j)-M[i][j] for j in range(n)] for i in range(n)])==pvalue(cp,t),"characteristic polynomial interpolation failed")
        for m in (1,2):
            G=[a*b**j for j in range(m) for a in A]
            value=bit_moments(raw_bits(G,q))
            require(value==row['moments_zero_one_two'][m-1],"original bit-image moments mismatch")
            require(value[0]==row['direct_original_counts'][m-1],"original count mismatch")
            counts+=1;moments+=3
        C=max(1,(max(D)+b-2)//(b-1))
        require(C==row['boundary_budget'],"actual boundary budget")
        if 'second_level_variance' in row:
            V=row['second_level_variance'];N,a,c=row['moments_zero_one_two'][1]
            variance=Fraction(c,N)-Fraction(a,N)**2
            require(variance==Fraction(V['value']) and Fraction(V['lower'])<=variance<=Fraction(V['upper']),"variance enclosure")
        pc=row.get('perron_certificate',{})
        if pc.get('det_root_minus_matrix')==0:
            root=pc['root'];require(max(map(sum,M))<=root,"claimed row-sum spectral bound")
            require(pvalue(cp,root)==0,"claimed spectral eigenvalue")
        if pc.get('identity'):
            root=pc['root']
            require(all(sum(M[i][t]*M[t][j] for t in range(n))==root*M[i][j] for i in range(n) for j in range(n)),"rank-one identity")
        if pc.get('quadratic'):
            f=pc['quadratic'];lo,hi=pc['root_interval']
            require(pvalue(f,lo)<0<pvalue(f,hi),"strict spectral interval")
            require(cp==f+[0]*5,"quadratic factorization")
        if "binary_modular_five_certificate" in row:
            D2=set(original_image(A,2));mod=row["binary_modular_five_certificate"]
            require(sorted(D2)==mod["digits"],"new original binary digits")
            residues={x%b for x in D2}
            require(not any(all((x+i*d)%b in residues for i in range(5)) for d in range(1,b) for x in residues),"new modular witness")
            require(mod["candidate_pairs"]==len(residues)*(b-1),"modular domain count")
        if pc.get("quartic"):
            f=pc["quartic"];require(cp==f+[0]*3,"quartic source degree")
            require(all(pvalue(f,a)*pvalue(f,b)<0 for a,b in pc["all_real_root_brackets"]),"all real root brackets")
            require(pc["root_interval"]==[18,19],"largest real root bracket")
            # Direct trial division by every monic linear or quadratic over F3.
            for degree in (1,2):
                for c in product(range(3),repeat=degree):
                    divisor=list(c)+( [1] );work=list(reversed([v%3 for v in f]))
                    for j in range(4,degree-1,-1):
                        scale=work[j]
                        for h,v in enumerate(divisor):work[j-degree+h]=(work[j-degree+h]-scale*v)%3
                    require(any(work[:degree]),"quartic has a factor modulo 3")
        if pc.get("squarefree_annihilator"):
            coeff=pc["squarefree_annihilator"];zero=[[0]*n for _ in range(n)]
            for c in coeff:
                zero=[[sum(zero[i][t]*M[t][j] for t in range(n))+c*int(i==j) for j in range(n)] for i in range(n)]
            require(not any(x for r in zero for x in r),"squarefree annihilator failed")
        if "interior_jordan_chain" in row:
            J=row["interior_jordan_chain"];v=J["eigenvector"];w=J["generalized_eigenvector"];a=J["eigenvalue"]
            require(mult(M,v)==[a*x for x in v],"interior eigenvector")
            require([x-a*y for x,y in zip(mult(M,w),w)]==[J["multiplier"]*x for x in v],"interior generalized vector")
        if "count_series" in row:
            series=row["count_series"];N=row["counts_through_length_10"]
            num,den=series["numerator_ascending"],series["denominator_ascending"]
            require(all(sum(c*N[j-h] for h,c in enumerate(den) if h<=j)==(num[j] if j<len(num) else 0) for j in range(len(N))),"count-series coefficients")
    return counts,moments


def validate_minimality(d):
    R=basis(5,True);require(d['seven_basis']==[list(r) for r in R],"seven basis changed")
    M=[[len(join(Y,r)) for r in R] for Y in d['symmetric_sets']]
    require(M==d['evaluation_matrix'] and det(M)==d['evaluation_determinant']==-1,"unimodular seven witness")
    N=[[len(join(set(original_image(A,5)),r)) for r in R] for A in d['five_admissible_blocks']]
    require(N==d['actual_image_matrix'] and det(N)==d['actual_image_determinant']==-10240,"actual fifth-image independence")
    H=[]
    for pre in d['prefix_certificates']:
        A,b=pre['generators'],pre['base'];D=set(original_image(A,2));res={x%b for x in D}
        require(not any(all((x+j*t)%b in res for j in range(5)) for x in res for t in range(1,b)),"prefix modular check")
        H.append([raw_bits(A+[b*a for a in C],5).bit_count() for C in d['five_admissible_blocks']])
    require(H==d['admissible_hankel_matrix'] and det(H)==d['admissible_hankel_determinant']==1228800,"actual admissible Hankel rank")
    require(det(d['prefix_rows'])==d['prefix_determinant']==-120,"prefix observer rank")
    for row in d['general_dimensions']:
        q=row['q'];B=basis(q);Y=basis(q,True);L=4*(q-2)+3
        V=[[len(join(P,R)) for R in B] for P in B]
        require(det(V)==row['raw_evaluation_determinant'],"raw independence determinant")
        S=[set(P)|{L-x for x in P} for P in Y]
        V=[[len(join(P,R)) for R in Y] for P in S]
        require(det(V)==row['symmetric_evaluation_determinant'],"symmetric independence determinant")
        require(len(B)==row['raw_dimension'] and len(Y)==row['symmetric_dimension'],"dimension count")
    K=d['set_object_observation_kernel']
    E=[[len(join(Y,r)) for r in R] for Y in K['sets']]
    require(all(sum(c*row[j] for c,row in zip(K['coefficients'],E))==0 for j in range(7)),"set-object observation kernel")
    require(det(E[:7])!=0 and K['rank']==7 and K['kernel_rank']==1,"finite observation quotient dimension")
    Y=d['non_symmetric_observation']['Y']
    defect=len(join(Y,(0,1,3)))-len(join(Y,(0,2,3)))
    require(defect==d['non_symmetric_observation']['signed_difference']!=0,"reflection kernel mutation")


def validate_primes(rows):
    require(len(rows)==3,"prime source domain")
    for rec in rows:
        A=rec['unchanged_generators'];p=rec['prime'];m=rec['blocks']
        require(A==sorted(a*27**j for j in range(m) for a in (1,9)),"weights were changed in reencoding")
        T=set(original_image(A,3));F=set(original_image(A,5));mid=2*sum(A)
        require(len(T)==rec['ternary_size'] and len(F)==rec['fifth_arity_size'],"prime image sizes")
        require(all(p%d for d in range(2,isqrt(p)+1)),"nonprime retained modulus")
        require(len({x%p for x in T})==len(T),"prime observation not injective")
        rejected=rec['rejected_prime_witnesses'];expected=[q for q in range(2,p) if all(q%d for d in range(2,isqrt(q)+1))]
        require([r[0] for r in rejected]==expected,"omitted earlier prime")
        require(all(w>0 and w+mid in F and w%q==0 for q,w in rejected),"false rejected-prime witness")
        B=set(original_image(A,2)); residues={x%p for x in B}
        require(not any((2*y-x)%p in residues for x in residues for y in residues if x!=y),"modular three-term obstruction")
        lifted=set(original_image(A+[p*a for a in A],2))
        require(len(lifted)==rec['two_level_binary_values']==len(B)**2,"prime lift image")
        look={x%p:x for x in B}
        require(all((z-look[z%p])//p in B for z in lifted),"actual-digit inverse")


def audit_alphabets(expected):
    digest=sha256();n=extra=0
    for q in range(2,6):
        B=basis(q)
        for b in range(2,5):
            W=(q-1)*(b-1)
            for mask in range(1<<W):
                D=(0,)+tuple(i+1 for i in range(W) if mask>>i&1)
                M=interpolate(D,b,q,False)
                Y={-3,0,2,7};Z={d+b*y for d in D for y in Y}
                actual=[len(join(Z,R)) for R in B]
                require(mult(M,[len(join(Y,R)) for R in B])==actual,"out-of-interpolation-domain count check")
                digest.update(serial([q,b,D,M]));n+=1;extra+=1
    require(n==expected['alphabets']==5050 and digest.hexdigest()==expected['transcript_sha256'],"complete alphabet replay digest")
    return {"independently_interpolated_matrices":n,"additional_literal_tails":extra,"transcript_sha256":digest.hexdigest()}


def audit_blocks(expected):
    digest=sha256();count=0
    for size in range(1,4):
        for A in combinations(range(1,9),size):
            for q in range(2,7):
                for b in sorted({sum(A)+1,sum(A)+2,2*sum(A)+1}):
                    n=raw_bits(list(A)+[b*a for a in A],q).bit_count()
                    digest.update(serial([A,q,b,n]));count+=1
    require(count==expected['block_radix_cases']==1375 and digest.hexdigest()==expected['transcript_sha256'],"complete generator domain")
    return {"original_generator_cases":count,"transcript_sha256":digest.hexdigest()}


def audit_fibers(d):
    total=0
    for rec in d['macro_cuts']:
        A,B,q,P=rec['left_generators'],rec['right_generators'],rec['q'],rec['cut_scale']
        m=original_image(A,q);n=original_image(B,q);counts=Counter(x+P*y for x in m for y in n)
        histogram=Counter(counts.values())
        require({str(k):v for k,v in sorted(histogram.items())}==rec['fiber_histogram'],"fiber histogram")
        require(max(counts.values())<=q-1,"too many cut representatives")
        require(len(counts)==rec['image_size'] and sum(counts.values())==rec['domain_size'],"cut exact sequence dimensions")
        total+=len(counts)
    require(total==d['actual_numeric_fibers']==2828,"fiber total")
    # Different contraction: cone to the LAST vertex, with its insertion sign.
    checked=0
    for size in range(1,7):
        top=size-1
        def add(out,k,c):
            out[k]=out.get(k,0)+c
            if not out[k]:del out[k]
        def boundary(x):
            o={}
            for F,c in x.items():
                for i in range(len(F)):add(o,F[:i]+F[i+1:],c*(-1)**i)
            return o
        def h(x):
            o={}
            for F,c in x.items():
                if top not in F:add(o,F+(top,),c*(-1)**len(F))
            return o
        for j in range(-1,size):
            for F in combinations(range(size),j+1):
                x={F:1};lhs=boundary(h(x))
                for f,c in h(boundary(x)).items():add(lhs,f,c)
                require(lhs==x,"independent last-vertex contraction")
                checked+=1
    require(checked==d['all_basis_homotopy_identities']==126,"simplex domain")
    return total,checked


def mutations(data):
    # Bind each modified object to its own callable.
    tests=[]
    def add(obj,key,validator):tests.append(lambda obj=obj,key=key,validator=validator:validator(obj[key]))
    x=deepcopy(data);x['selected_matrices'][0]['matrix'][0][0]+=1;add(x,'selected_matrices',validate_selected)
    x=deepcopy(data);x['selected_matrices'][0]['moments_zero_one_two'][0][1]+=1;add(x,'selected_matrices',validate_selected)
    x=deepcopy(data);x['selected_matrices'][0]['characteristic_polynomial_descending'][-1]+=1;add(x,'selected_matrices',validate_selected)
    x=deepcopy(data);x['selected_matrices'].pop();add(x,'selected_matrices',validate_selected)
    x=deepcopy(data);x['minimality']['actual_image_determinant']=0;add(x,'minimality',validate_minimality)
    x=deepcopy(data);x['minimality']['non_symmetric_observation']['signed_difference']=0;add(x,'minimality',validate_minimality)
    x=deepcopy(data);x['faithful_reencoding'][0]['prime']=3;add(x,'faithful_reencoding',validate_primes)
    x=deepcopy(data);x['faithful_reencoding'][0]['rejected_prime_witnesses'].pop();add(x,'faithful_reencoding',validate_primes)
    failures=0
    for t in tests:
        try:t()
        except (AssertionError,ValueError,IndexError,StopIteration):failures+=1
        else:raise AssertionError("corrupted certificate admitted")
    return failures


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path,default=HERE.with_name('seven_observable_receipt.json'))
    parser.add_argument('--output',type=Path,default=HERE.with_name('independent_audit.json'))
    args=parser.parse_args();data=json.loads(args.receipt.read_text())
    require(data['status']=='PASS' and data['full_replay'] is True and data['lean_checked'] is False,"receipt status/scope")
    for path,expected in data['source_sha256'].items():require(sha256((ROOT/path).read_bytes()).hexdigest()==expected,"source identity")
    for row in data['regressions']['original_word_metric_example']:
        m=row['length'];mass=original_image([3**j for j in range(m)],5)
        require(len(mass)==row['distinct_values']==2*3**m-1,"word-metric distinct count")
        require(sum(mass.values())==row['original_words']==5**m,"word-metric original mass")
        require(max(mass.values())==row['maximum_mass'],"word-metric maximum mass")
    counts,moments=validate_selected(data['selected_matrices'])
    validate_minimality(data['minimality']);validate_primes(data['faithful_reencoding'])
    alphabets=audit_alphabets(data['all_alphabets']);blocks=audit_blocks(data['original_blocks'])
    fibers,homotopies=audit_fibers(data['chain_and_metrics']);bad=mutations(data)
    out={'schema':'ep817-seven-observable-independent-audit-v1','status':'PASS','lean_checked':False,
         'imports_producer_or_library':False,'selected_original_counts':counts,'selected_original_moments':moments,
         'alphabet_replay':alphabets,'generator_replay':blocks,'actual_cut_fibers':fibers,
         'independent_contraction_identities':homotopies,'original_word_metric_cases':len(data['regressions']['original_word_metric_example']),'corruptions_rejected':bad,
         'producer_receipt_sha256':sha256(args.receipt.read_bytes()).hexdigest(),
         'auditor_sha256':sha256(HERE.read_bytes()).hexdigest()}
    text=json.dumps(out,sort_keys=True,indent=2)+'\n';args.output.write_text(text,encoding='utf-8')
    print(json.dumps({'status':'PASS','audit':str(args.output),'sha256':sha256(text.encode()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
