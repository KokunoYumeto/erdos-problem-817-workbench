#!/usr/bin/env python3
"""Independent finite audit: does not import producer or local_flow.

Uses direct numerical output windows rather than residue masks, reconstructs
coordinate identities by exact interpolation, and enumerates balanced pattern
flows independently of the producer's circuit decomposition.
"""
from __future__ import annotations
import argparse,copy,hashlib,json
from collections import Counter,deque
from fractions import Fraction
from itertools import combinations,permutations,product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SH=((0,),(0,1),(0,2),(0,1,2),(0,3),(0,1,3),(0,1,2,3))
ORB=(1,2,3,5,6,7,9,11,15)

def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def dg(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def mul(X,Y):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*Y)] for r in X]
def act(M,x):return [sum(a*b for a,b in zip(r,x)) for r in M]
def I(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def tr(X):return [list(r) for r in zip(*X)]
def powm(M,n):
    P=I(len(M))
    for _ in range(n):P=mul(P,M)
    return P

def rr(M):
    M=[[Fraction(x) for x in r] for r in M];p=[];j=0
    if not M:return M,p
    for c in range(len(M[0])):
        s=next((s for s in range(j,len(M)) if M[s][c]),None)
        if s is None:continue
        M[j],M[s]=M[s],M[j];v=M[j][c];M[j]=[x/v for x in M[j]]
        for i in range(len(M)):
            if i!=j:
                v=M[i][c];M[i]=[x-v*y for x,y in zip(M[i],M[j])]
        p.append(c);j+=1
        if j==len(M):break
    return M,p

def rk(M):return len(rr(M)[1])
def inverse(M):
    R,p=rr([r+e for r,e in zip(M,I(len(M)))])
    ck(p[:len(M)]==list(range(len(M))),'singular interpolation')
    return [r[len(M):] for r in R]

def det(M):
    M=[r[:] for r in M];n=len(M);old=1;sign=1
    for i in range(n-1):
        s=next((j for j in range(i,n) if M[j][i]),None)
        if s is None:return 0
        if s!=i:M[s],M[i]=M[i],M[s];sign=-sign
        v=M[i][i]
        for j in range(i+1,n):
            for k in range(i+1,n):
                a=M[j][k]*v-M[j][i]*M[i][k]
                ck(a%old==0,'determinant divisibility');M[j][k]=a//old
            M[j][i]=0
        old=v
    return sign*M[-1][-1]

def check_char(M,coeff):
    n=len(M);ck(len(coeff)==n+1 and coeff[0]==1,'char polynomial degree')
    for x in range(n+1):
        v=0
        for a in coeff:v=v*x+a
        ck(v==det([[x*int(i==j)-M[i][j] for j in range(n)] for i in range(n)]),
           'characteristic determinant interpolation')

def reverse(e,width):return int(format(e,'0'+str(width)+'b')[::-1],2)
def obs(Y):return [len({x+s for x in Y for s in S}) for S in SH]
def windows(Y,q=5):
    Y=set(Y);width=q-1;out=[0]*(1<<width)
    for t in range(min(Y),max(Y)+width):
        w=''.join('1' if t-i in Y else '0' for i in range(width))
        out[int(w[::-1],2)]+=1
    return out

def digits(A,q):
    co={0}
    for a in A:
        n=set()
        for c in range(q):n.update(x+c*a for x in co)
        co=n
    return tuple(sorted(co))
def dbits(A,q):
    p=1
    for a in A:
        s=p
        for c in range(1,q):s|=p<<(c*a)
        p=s
    return p

def direct_substitution(D,b,q):
    w=q-1;nv=1<<(w-1);L=[[0]*(2*nv) for _ in range(2*nv)]
    paths=[];vertices={}
    for e in range(2*nv):
        input_set={-i for i in range(w) if e>>i&1}
        output={d+b*y for d in D for y in input_set}
        path=[]
        for z in range(b):
            a=sum(int(z-i in output)<<i for i in range(w))
            path.append(a);L[a][e]+=1
        start=path[0]>>1;end=path[-1]&(nv-1)
        for old,new in ((e>>1,start),(e&(nv-1),end)):
            ck(old not in vertices or vertices[old]==new,'inconsistent boundary vertex action')
            vertices[old]=new
        ck(all(path[j]&(nv-1)==path[j+1]>>1 for j in range(b-1)),'output path broken')
        paths.append(path)
    vertex=[vertices[i] for i in range(nv)]
    V=[[int(vertex[j]==i) for j in range(nv)] for i in range(nv)]
    return L,V,vertex,paths


def symsets(spanmax):
    yield (0,)
    for n in range(1,spanmax+1):
        pairs=[{j,n-j} for j in range(1,n//2+1)]
        for mask in range(2**len(pairs)):
            Y={0,n}
            for i,p in enumerate(pairs):
                if mask>>i&1:Y|=p
            yield tuple(sorted(Y))


def audit_static(data,characteristic=True):
    cone=data['cone'];AA=cone['A'];BB=cone['B'];C=cone['conservation']
    ys=((0,),(0,1),(0,2),(0,1,2),(0,3),(0,1,2,3),(0,1,3,4))
    F=[obs(Y) for Y in ys];Z=[[windows(Y)[e] for e in ORB] for Y in ys]
    reconstructed=tr(mul(inverse(F),Z))
    ck(reconstructed==AA,'original-set interpolation of nine counts')
    ck(mul(BB,AA)==I(7) and mul(C,AA)==[[0]*7]*2,'integer inverse and conservation')
    # Original symmetric cycle module and observation kernel.
    boundary=[[0]*16 for _ in range(8)]
    for e in range(16):boundary[e&7][e]+=1;boundary[e>>1][e]-=1
    revrows=[[int(j==i)-int(j==reverse(i,4)) for j in range(16)] for i in range(16)]
    O=[[int(any(e>>r&1 for r in R)) for e in range(16)] for R in SH]
    ck(rk(boundary)==7 and rk(boundary+revrows)==8 and rk(boundary+revrows+O)==15,
       'cycle/symmetric-cycle/observation dimensions')
    rays=cone['rays'];ck(len(rays)==10,'missing cone ray')
    zs=[r['defect_ray'] for r in rays]
    ck(all(min(z)>=0 and act(C,z)==[0,0] for z in zs),'invalid circulation ray')
    ck(len({tuple(z) for z in zs})==10,'duplicate ray')
    # Every 0/1 circulation is a sum of the claimed integer generators.
    reachable={(0,)*9};todo=deque(reachable)
    while todo:
        x=todo.popleft()
        for z in zs:
            y=tuple(a+b for a,b in zip(x,z))
            if max(y)<=2 and y not in reachable:reachable.add(y);todo.append(y)
    allfeasible={z for z in product(range(3),repeat=9) if act(C,z)==[0,0]}
    ck(reachable==allfeasible,'independent bounded integral semigroup equality')
    ck(rk([r['count_ray'] for r in rays])==7,'seven-dimensional cone')
    for r in rays:
        ck(r['count_ray']==act(BB,r['defect_ray']),'ray observation')
        f=r['count_ray'];word=r['period'];h=word.count('1');p=len(word)
        for row in r['approximants']:
            N=row['repetitions'];Y={j*p+i for j in range(N) for i,x in enumerate(word) if x=='1'}
            L=2*N*p+4;Y|={L-y for y in tuple(Y)}
            ck(obs(Y)==row['observations'] and len(Y)==row['size'],'actual periodic approximant')
            ck(all(abs(row['observations'][j]*f[0]-2*N*h*f[j])<=12*f[0] for j in range(7)),
               'retained periodic boundary')
    ck(len(cone['facets'])==9,'missing facet')
    for i,row in enumerate(cone['facets']):
        ck(row['row']==AA[i] and row['pattern']==format(ORB[i],'04b'),'changed pattern facet')
        ck(rk([r['count_ray'] for r in rays if not r['defect_ray'][i]])==6,'facet dimension')
    # Independently enumerate simple cycles by all distinct-vertex permutations.
    cyc=set()
    for size in range(1,9):
        for nodeset in combinations(range(8),size):
            first=nodeset[0]
            for tail in permutations(nodeset[1:]):
                nodes=(first,)+tail;edges=[];ok=True
                for a,b in zip(nodes,nodes[1:]+nodes[:1]):
                    e=(a<<1)|(b&1)
                    if e&7!=b:ok=False;break
                    edges.append(e)
                if ok:cyc.add((nodes,tuple(edges)))
    actual={(tuple(r['vertices']),tuple(r['edges'])) for r in cone['simple_cycles']}
    ck(cyc==actual and len(cyc)==19,'independent complete cycle enumeration')
    for r in cone['simple_cycles']:
        counts=Counter(r['edges']);c=[counts[e]+counts[reverse(e,4)] for e in range(16)]
        ck(c==r['symmetric_current'],'cycle multiplicity')
        z=[c[e] for e in ORB]
        ck([sum(a*b for a,b in zip(r['circuit_coefficients'],col)) for col in zip(*zs)]==z,
           'cycle circuit coefficients')
    for ent in data['selected_matrices']:
        D=digits(ent['weights'],5);ck(list(D)==ent['digits'],'original fifth-arity digit image')
        L,V,phi,_=direct_substitution(D,ent['base'],5)
        ck(L==ent['edge_matrix'] and V==ent['vertex_matrix'] and phi==ent['vertex_function'],
           'original output-window lift')
        # Interpolate the count map from seven original sets, not from residues.
        values=[obs({d+ent['base']*y for d in D for y in Y}) for Y in ys]
        M=tr(mul(inverse(F),values))
        ck(M==ent['count_matrix'],'independent count matrix interpolation')
        embed=[[int(e!=0 and min(e,reverse(e,4))==o) for o in ORB] for e in range(16)]
        K=mul([L[o] for o in ORB],embed)
        ck(K==ent['pattern_matrix'] and mul(K,AA)==mul(AA,M),'positive-pattern quotient')
        section=mul(embed,AA);gram=mul(tr(section),section)
        ck(gram==ent['quotient_gram'] and det(gram)>0,'original unit-current quotient Gram')
        lam=[ent['base']*int(j==6)-M[6][j] for j in range(7)]
        ck(lam==ent['section_defect'],'section correction row')
        Q=mul(L,section);P=mul(section,M)
        ck([[x-y for x,y in zip(a,b)] for a,b in zip(Q,P)]==[lam]+[[0]*7 for _ in range(15)],
           'section defect is the actual zero loop')
        lhs=mul(tr(Q),Q);rhs=mul(tr(M),mul(gram,M))
        ck(lhs==[[rhs[i][j]+lam[i]*lam[j] for j in range(7)] for i in range(7)],
           'Gram correction retained')
        if characteristic:
            check_char(ent['count_matrix'],ent['count_charpoly'])
            check_char(L,ent['edge_charpoly'])
    sw=data['switching'];Ma=sw['A']['matrix'];Mb=sw['B']['matrix']
    Ablock=(1,3);Bblock=(2,4);Cblock=(1,3,10,30,200,400)
    ck(sw['macro_weights']==list(Cblock) and sw['macro_base']==1000,'original macro block')
    ck(sw['macro_matrix']==mul(mul(Ma,Ma),Mb),'period ordered composition')
    ck(act(sw['macro_matrix'],[1,2,2,3,2,3,4])[0]==2301,'period first image')
    for row in sw['run_values']:
        a,b,val=row;ck(9*val==8*10**(a+b)+4*10**b-3,'run arithmetic formula')
    ck(sw['exact_comparisons']['93_cubed']==93**3 and sw['exact_comparisons']['893_squared']==893**2,
       'exact minimizing comparison')
    return {'integral_flow_cube_cases':len(allfeasible),'independent_simple_cycles':len(cyc),
            'matrices_checked':len(data['selected_matrices'])}


def audit_domains(data):
    transcripts=[];count=0;edge_paths=0
    tails=((0,),(0,1),(0,2,4),(-2,0,2),(0,1,4,5))
    joins=0
    for q in range(2,7):
        for b in range(2,7):
            for D in symsets(min(8,(q-1)*(b-1))):
                L,V,phi,paths=direct_substitution(D,b,q)
                for Y in tails:
                    X={d+b*y for d in D for y in Y};pred=act(L,windows(Y,q))
                    pred[0]-=(q-1)*(b-1)-max(D)
                    ck(pred==windows(X,q),'independent complete source replay')
                    joins+=1
                transcripts.append([q,b,D,phi,dg(paths)]);count+=1;edge_paths+=len(paths)
    sr=data['substitution_replay']
    ck((count,joins,edge_paths)==(sr['complete_symmetric_digit_cases'],sr['actual_joins'],sr['entire_edge_paths'])
       and dg(transcripts)==sr['transcript_sha256'],'complete replay binding')
    wordrows=[];products={():I(7)};Ma=data['switching']['A']['matrix'];Mb=data['switching']['B']['matrix'];direct=0
    for n in range(1,11):
        for word in product((0,1),repeat=n):
            M=mul(products[word[:-1]],(Ma,Mb)[word[-1]]);products[word]=M
            N=act(M,[1,2,2,3,2,3,4])[0]
            radius=sum(M[i][i] for i in range(7)) if len(set(word))==2 else 10**n
            ck(radius**3>=893**n and radius<=N<=4*radius,'all word lower estimate')
            if n<=5:
                weights=[];P=1
                for i in word:weights.extend(P*a for a in ((1,3),(2,4))[i]);P*=10
                ck(dbits(weights,5).bit_count()==N,'independent generator DP for switched word');direct+=1
            wordrows.append([list(word),N,radius])
    ck(dg(wordrows)==data['switching']['word_transcript_sha256'],'word transcript binding')
    sat=data['saturation'];ms=[]
    for ent in sat['blocks']:
        b=ent['base'];D=digits(ent['weights'],3)
        ck(len(D)==ent['ternary_values'] and {d%b for d in D}==set(range(b)),'actual residue saturation')
        # Stored selected entry identified by both original generators and base.
        row=next(r for r in data['selected_matrices'] if r['weights']==ent['weights'] and r['base']==b)
        M=row['count_matrix'];ck(act(M,[1]*7)==[b]*7,'common ray identity');ms.append(M)
    for i,j,n,N in sat['direct_two_level_cases']:
        a,b=sat['blocks'][i],sat['blocks'][j];G=a['weights']+[a['base']*x for x in b['weights']]
        ck(len(G)==n and dbits(G,5).bit_count()==N,'saturated literal macro image')
        P=a['base']*b['base'];bits=dbits(G,3);mask=(1<<P)-1
        ck((bits|(bits>>P))&mask==mask,'saturated original ternary residues')
    # Every small integral row is either positively certified or has an actual finite tail violation.
    dual=data['linear_dual'];cases=dual['cases']
    ck([x['row'] for x in cases]==[list(w) for w in product((-1,0,1),repeat=7)],'complete dual row domain')
    true_rows=false_rows=0
    for row in cases:
        w=row['row'];c=row['certificate']
        if c['nonnegative']:
            alpha=c['pattern_coefficients'];ck(min(alpha)>=0 and act(tr(data['cone']['A']),alpha)==w,
                                               'nonnegative original pattern certificate')
            p=c['potential'];r=act(tr(data['cone']['B']),w)
            ck(alpha==[r[j]-sum(p[i]*data['cone']['conservation'][i][j] for i in range(2)) for j in range(9)],
               'two-potential conservation correction');true_rows+=1
        else:
            word=c['period'];N=c['repetitions'];p=len(word)
            Y={p*j+i for j in range(N) for i,s in enumerate(word) if s=='1'}
            L=2*N*p+4;Y|={L-y for y in tuple(Y)};F=obs(Y)
            ck(len(Y)==c['size'] and F==c['observations'] and sum(a*b for a,b in zip(w,F))<0,
               'actual finite symmetric violation');false_rows+=1
    ck((true_rows,false_rows)==(dual['nonnegative_rows'],dual['actual_finite_violations']),
       'dual classification counts')
    return {'complete_symmetric_digit_cases':count,'joins':joins,'edge_paths':edge_paths,
            'dual_nonnegative_rows':true_rows,'dual_actual_counterexamples':false_rows,
            'switch_words':len(wordrows),'direct_switched_generator_images':direct,
            'direct_saturated_macro_images':len(sat['direct_two_level_cases'])}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--receipt',type=Path,default=ROOT/'certificates/local_flow_receipt.json')
    p.add_argument('--output',type=Path,default=ROOT/'certificates/independent_audit.json')
    args=p.parse_args();data=json.loads(args.receipt.read_text())
    ck(data['status']=='PASS' and data['lean_checked'] is False,'receipt status')
    static=audit_static(data);domains=audit_domains(data)
    def mutate(i):
        x=copy.deepcopy(data)
        if i==0:x['cone']['A'][0][0]+=1
        if i==1:x['cone']['rays'].pop()
        if i==2:x['cone']['facets'][0]['row'][3]*=-1
        if i==3:x['cone']['simple_cycles'].pop()
        if i==4:x['selected_matrices'][0]['edge_matrix'][0][0]+=1
        if i==5:x['selected_matrices'][0]['vertex_function'][0]=1
        if i==6:x['selected_matrices'][0]['pattern_matrix'][0][0]+=1
        if i==7:x['switching']['macro_base']=893
        return x
    rejected=0
    for i in range(8):
        try:audit_static(mutate(i),characteristic=False)
        except AssertionError:rejected+=1
        else:raise AssertionError('corrupted certificate was accepted')
    result={'schema':'ep817-local-flow-independent-audit-v1','status':'PASS','lean_checked':False,
            'method':'Direct output windows, original-set interpolation, rational matrix ranks, determinant evaluations, full balanced-pattern enumeration; no producer imports.',
            'static':static,'domains':domains,'corrupted_certificates_rejected':rejected,
            'receipt_sha256':hashlib.sha256(args.receipt.read_bytes()).hexdigest(),
            'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
