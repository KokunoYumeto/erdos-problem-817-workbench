# Exact composition, finite carry certificates, and the general-k capacity

**Erdős Problem 817 — PolyClank research contribution, 14 September 2026.**

Base revision: `23c0110c95b5a2036bdc04a1f352b6e5e27742c8` of
`KokunoYumeto/erdos-problem-817-workbench`.

Status: complete ordinary proofs of the statements below, with reproducible
integer checks and explicit finite certificates; independent review is requested.
Lean coverage remains that of the existing Core/Extended modules. This work
adds no Lean declarations or replacement receipts. The conclusions below use
no conjectural block-classification lemma.

## 1. Scope and exact objects

For a finite set A of distinct positive integers, put

\[
H(A)=\{\sum_{a\in U}a:U\subseteq A\},\quad
S(A)=\sum_{a\in A}a,\quad R(A)=2S(A)+1.
\]

Let \(\mathcal A_k(n)\) be the set of such A with |A|=n and with H(A)
containing no nonconstant k-term arithmetic progression. Here k>=3. Set
\(\mathcal A_k(0)=\{\varnothing\}\), and define

\[
g_k(n)=\min_{A\in\mathcal A_k(n)}\max A\quad(n\ge1),\qquad
h_k(n)=\min_{A\in\mathcal A_k(n)}R(A)\quad(n\ge0).
\]

For a subset X of an abelian group, \(\operatorname{AP}_k(X)\) denotes the
set of ordered tuples \((x_0,\ldots,x_{k-1})\in X^k\) with
\(x_{i+2}-2x_{i+1}+x_i=0\) for every i. Constant tuples are included.
Over a cyclic group, a nonconstant progression means that its common difference
is a nonzero group element; its entries may repeat when that element has
small order. All such orders are retained in the computations.

These definitions preserve every generator, its actual value, and every
subset representation. R is an additional integer-valued observable. No gcd
is removed, no generator is rescaled to 1, and no equality of subset sums is
discarded. The original k=4 construction and signed-block proof remain credited
to the anonymous/deleted Reddit contributor. The Lean finite upper bound
remains separately credited to sneed-and-feed. Draft PR #2 supplies the earlier
variance investigation; the present proofs have no dependency on its new lemma.

The symbol lambda_k below denotes the exponential growth rate. Korsky's
Equation (1.5) uses the same letter for the polynomial-loss exponent
log_2((k-1)/(k-2)); that quantity is kept separately here. The map
log_2:(1,infinity)->(0,infinity), with inverse x->2^x, relates his
polynomial exponent to the lower exponential base d_k=(k-1)/(k-2).

The broader problem requests estimates for all k. Costa (2026) establishes
\(\liminf g_3(n)/3^n=0\), addressing the historical constant-factor question.
The present target is the full family of exponential rates and constructions.

## 2. Exact product on generators and arithmetic-progression tuples

**Theorem 2.1 (composition with explicit inverse maps).** For arbitrary finite
sets A,B of distinct positive integers, including the empty set, define

\[
A\star B=A\cup R(A)B.
\]

Then

\[
|A\star B|=|A|+|B|,\qquad
S(A\star B)=S(A)+R(A)S(B),\qquad
R(A\star B)=R(A)R(B).
\]

The maps

\[
\begin{aligned}
F_{A,B}:\mathcal P(A)\times\mathcal P(B)&\longrightarrow\mathcal P(A\star B),
 &(U,V)&\longmapsto U\cup R(A)V,\\
E_{A,B}:H(A)\times H(B)&\longrightarrow H(A\star B),
 &(x,y)&\longmapsto x+R(A)y
\end{aligned}
\]

are bijections. E induces a bijection

\[
\operatorname{AP}_k(H(A))\times\operatorname{AP}_k(H(B))
\longrightarrow \operatorname{AP}_k(H(A\star B))
\]

by componentwise evaluation. A target progression is constant exactly when
both source progressions are constant. Consequently star sends
\(\mathcal A_k(n)\times\mathcal A_k(m)\) into \(\mathcal A_k(n+m)\).
It is associative and has identity \(\varnothing\).

**Proof.** Put R=R(A). Every member of A is less than R, while each member of
RB is at least R. The two parts are disjoint, and multiplication by R is
injective. The inverse of F sends W to
\((W\cap A,\{b\in B:Rb\in W\})\). This proves the cardinality formula
and the subset representation identity.

For x in H(A), 0<=x<=S(A)<R. Thus the inverse of E is the restriction of the
Euclidean division map

\[
z\longmapsto \left(z-R\lfloor z/R\rfloor,\lfloor z/R\rfloor\right).
\]

The first and second coordinates belong to H(A),H(B) because z arose from
a subset of A star B. This proves the bijection on actual values. The
subset-sum maps commute with F and E. In particular, writing mu_A(x) for the
number of subsets of A summing to x, one has the exact fiber identity
\(\mu_{A\star B}(x+Ry)=\mu_A(x)\mu_B(y)\).

Take an arithmetic progression z_i=x_i+Ry_i in the target and put
\(e_i=x_{i+2}-2x_{i+1}+x_i\). The equation for z gives
\(e_i=-R(y_{i+2}-2y_{i+1}+y_i)\). Meanwhile
\(-2S(A)\le e_i\le2S(A)\), so \(|e_i|<R\).
Its divisibility by R forces e_i=0, and the second difference of y is then
zero as well. Conversely, evaluating two source progressions clearly gives
a target progression. The pointwise inverse of E gives the inverse on tuples.
If the target common difference is zero, its first two points have the same
E-preimage, so both source differences are zero. The reverse implication
follows by evaluation.

Finally R(A star B)=2S(A)+2R(A)S(B)+1=R(A)R(B). Both bracketings of a triple
product are the same set
\(A\cup R(A)B\cup R(A)R(B)C\), and the empty set has R=1. QED.

**Concrete contrapositive.** A nonconstant k-AP in H(A star B), decoded by the
displayed division map, gives a nonconstant k-AP in at least one of H(A),H(B).
Thus a failed product construction comes with a factor witness, rather than
an unexplained failure of a heuristic.

The same product preserves the ternary image exactly. Put
\(T(A)=\{\sum_a x_a a:x_a\in\{0,1,2\}\}\).
Since 0<=x<=2S(A)=R(A)-1 for x in T(A), division by R gives a bijection
\(T(A)\times T(B)\to T(A\star B)\). Consequently the unweighted image
polynomials satisfy

\[
\sum_{t\in T(A\star B)}z^t=
\left(\sum_{x\in T(A)}z^x\right)
\left(\sum_{y\in T(B)}z^{R(A)y}\right).
\]

This supplies a direct connection to the earlier variance work while keeping
its finite sets and their measures explicit.

## 3. Existence of every fixed-k exponential rate

**Theorem 3.1.** For every integer k>=3 the following limit exists:

\[
\boxed{\lambda_k=\lim_{n\to\infty}g_k(n)^{1/n}
=\inf_{n\ge1}h_k(n)^{1/n}
=\inf_{\substack{A\in\mathcal A_k(|A|)\\ |A|>0}}
(2S(A)+1)^{1/|A|}.}
\]

Also \(1<\lambda_k\le3\), and the sequence lambda_k is nonincreasing in k.

**Proof.** Powers of 3 provide admissible sets for every n: their subset sums
use only base-3 digits 0 and 1, and reduction of a second-difference relation
modulo 3 followed by division forces each digit triple to be constant.
A k-AP would have a nonconstant initial 3-AP. Thus the displayed minima exist,
and h_k(0)=1.

Theorem 2.1 gives h_k(n+m)<=h_k(n)h_k(m). Put b_n=log h_k(n) and
L=inf_{l>=1} b_l/l. For fixed l write n=ql+r, 0<=r<l. Repeated composition
gives the exact inequality b_n<=q b_l+b_r. Division by n and passage to the
upper limit gives limsup b_n/n<=b_l/l, since the finitely many b_r are bounded.
Taking the infimum over l gives limsup<=L. The definition of L gives
b_n/n>=L for every n>=1. Therefore b_n/n tends to L.

The original maximum and the sum observable obey

\[
2g_k(n)+1\le h_k(n)\le2n g_k(n)+1.
\]

The left inequality follows from S(A)>=max A>=g_k(n). For the right one,
use a set attaining g_k(n). In particular

\[
0\le\frac{\log h_k(n)-\log g_k(n)}n
\le\frac{\log(2n+1)}n\longrightarrow0.
\]

Thus log g_k(n)/n tends to L as well. Exponentiating proves all three
expressions. The elementary construction gives lambda_k<=3. Inclusion
\(\mathcal A_k(n)\subseteq\mathcal A_{k+1}(n)\) follows by the explicit
prefix map \(\operatorname{AP}_{k+1}(X)\to\operatorname{AP}_k(X)\),
which preserves a nonzero common difference. Hence lambda is nonincreasing.
Strict positivity above 1 follows from the next calculation. QED.

For completeness, the known elementary lower mechanism can be restated
without an unproved input. Fix an ordering of an admissible A and let B be the
partial subset-sum set just before a positive generator a is added. Split B
into maximal chains with step a. A chain of length k-1 would extend in
B union (B+a) to a k-AP, so all chain lengths are at most k-2. Each chain adds
one point. Consequently

\[
|B\cup(B+a)|\ge\frac{k-1}{k-2}|B|.
\]

Iteration from {0} and |H(A)|<=S(A)+1<=n max A+1 gives

\[
g_k(n)\ge\frac{((k-1)/(k-2))^n-1}{n},\qquad
\lambda_k\ge\frac{k-1}{k-2}>1.
\]

This chain mechanism and stronger adaptive finite estimates are due to the
existing literature, in particular Korsky (2026, Section 5). It is restated
here only to close the elementary existence theorem's bounds.

## 4. The exact finite carry graph

Let b>=2 and let D be a finite nonempty subset of {0,...,b-1}. Define

\[
L_m(D;b)=\{\sum_{j=0}^{m-1}d_jb^j:d_j\in D\}.
\]

Words are written from least significant to most significant digit. The
map \(e_m:D^m\to L_m(D;b)\) is a bijection: its inverse is the m-digit
base-b expansion. No digit identification occurs in this map.

For k>=3 define the directed, labeled graph with vertices

\[
(c,f)\in\{-1,0,1\}^{k-2}\times\{0,1\}.
\]

For a digit column \(d=(d_0,\ldots,d_{k-1})\in D^k\), let
\(\Delta_i(d)=d_{i+2}-2d_{i+1}+d_i\). The column labels an edge

\[
(c,f)\xrightarrow{d}(c',f')
\]

precisely when, for every i,

\[
\boxed{b c'_i=c_i+\Delta_i(d),\qquad
f'=f\mathbin{\lor}[d_0\ne d_1].}
\]

The initial vertex is (0,0), and the accepting vertex is (0,1).

**Theorem 4.1 (all-length decision and witness bound).** For every b,D,k as
above, the following are equivalent:

(a) Some L_m(D;b), m>=1, contains a nonconstant k-AP.

(b) The accepting vertex is reachable from the initial vertex.

Every such instance has a witness using at most \(3^{k-2}\) digit columns.
A finite vertex set containing the initial vertex, excluding the accepting
vertex, and closed under every labeled transition certifies k-AP-freeness
for every m. When 0 belongs to D, it also certifies the union over all m,
since leading zero padding places any finite tuple in one common L_m.

**Proof.** A matrix of digit columns d^(0),...,d^(m-1) determines numbers
\(y_i=\sum_{j<m}b^j d_i^{(j)}\). Starting at c^(0)=0, the edge equations
say \(\Delta(d^{(j)})=b c^{(j+1)}-c^{(j)}\). Hence, exactly,

\[
\sum_{j<m}b^j\Delta(d^{(j)})=b^m c^{(m)}.
\]

Ending with c^(m)=0 is equivalent to all second differences of y vanishing.
The flag is 1 exactly when the first two digit words differ; uniqueness of
base-b expansion makes this equivalent to y_0!=y_1. Thus any accepting
labeled path evaluates to a nonconstant k-AP.

Conversely, take a k-AP in L_m and use the unique base-b expansion of each
term. Set

\[
c^{(j)}=b^{-j}\sum_{t<j}b^t\Delta(d^{(t)}).
\]

The full second difference is zero, so the prefix sum is divisible by b^j;
each c^(j) is an integer vector. Since |Delta_i|<=2(b-1),

\[
|c_i^{(j)}|\le2(1-b^{-j})<2\quad(j>0).
\]

It lies in {-1,0,1}. These carries satisfy the transition equations and end
at zero. The nonconstant progression makes the flag 1. This is the inverse
map from progressions, through their unique digits, to labeled paths.

The only reachable flag-0 vertex is (0,0). Indeed, from zero with d_0=d_1,
the congruence for d_2 forces d_2=d_1 because both are in [0,b); successive
congruences force all entries equal, and then every carry stays zero.
The graph therefore has at most one reachable flag-0 vertex and
3^(k-2) reachable flag-1 vertices. A shortest accepting path repeats no
vertex, so its length is at most 3^(k-2). Closure of a proposed safe vertex
set keeps every finite path inside that set, proving the last assertions.
QED.

The graph may be explored using only |D|^2 starting digit pairs at each
vertex. Having chosen d_0,d_1, each subsequent digit is forced by

\[
d_{i+2}\equiv 2d_{i+1}-d_i-c_i\pmod b,
\qquad 0\le d_{i+2}<b.
\]

An edge exists exactly when all these forced digits belong to D. This is an
exact enumeration of D^k columns satisfying the divisibility conditions.
The checker also compares it with direct column enumeration on a smaller,
fully specified domain. Parent edges retain actual digit columns so that
negative results contain concrete integer witnesses.

### 4.2 Retaining digits above the base and every representation collision

The preceding canonical-digit map has a complete extension to arbitrary finite
D contained in [0,S], with S allowed to exceed b. Keep the same evaluation
surjection e_m:D^m -> L_m(D;b), and retain its entire fibers. For example,
when D={0,7,8,15,19,26,27,34} and b=19, the words (19,7) and (0,8)
both belong to D^2 and evaluate to 152. Both are retained. Tracking whether two digit words differ would flag
these equal values incorrectly. The map to actual differences is therefore
made explicit below.

Set

\[
C_0=\left\lceil\frac{2S}{b-1}\right\rceil,\qquad
H_0=\left\lceil\frac{S}{b-1}\right\rceil.
\]

The full graph has vertices

\[
(c,h,f)\in\{-C_0,\ldots,C_0\}^{k-2}
\times\{-H_0,\ldots,H_0\}\times\{0,1\}.
\]

For a column d in D^k require the exact transition equations

\[
bc'_i=c_i+\Delta_i(d),\quad
h+d_1-d_0=r+bh',\quad 0\le r<b,\quad
f'=f\lor[r\ne0].
\]

Thus h' and r are respectively the Euclidean quotient and remainder of
h+d_1-d_0; negative values are handled by the floor quotient. Start at
(0,0,0). A vertex is accepting exactly when c=0 and either f=1 or h!=0.

**Theorem 4.2 (full carry equivalence).** For every b>=2, k>=3, and nonempty
finite D contained in the nonnegative integers, an L_m(D;b) contains a
nonconstant k-AP exactly when this full graph has a reachable accepting
vertex. A shortest witness has at most

\[
2(2C_0+1)^{k-2}(2H_0+1)-1
\]

columns. A finite transition-closed set of vertices containing the initial
vertex and excluding every accepting vertex certifies all word lengths.

**Proof.** For a labeled path of length m let
\(y_i=\sum_{j<m}b^j d_i^{(j)}\). The second-difference transitions telescope
exactly as before to \(\Delta(y)=b^m c^{(m)}\). Meanwhile the extra carry
transitions give the separate identity

\[
\boxed{y_1-y_0=\sum_{j<m}b^j r_j+b^m h^{(m)}.}
\]

The sum of remainders lies in [0,b^m). Consequently this difference vanishes
exactly when all r_j vanish and h^(m)=0. This is precisely the complement
of the stated acceptance test at c^(m)=0. Thus every accepting path gives
an actual nonconstant progression, with no assumption about uniqueness of
word representations.

Conversely, take any progression in L_m and any digit word representing each
of its terms. For each j define the second-difference carry from the prefix
formula in Theorem 4.1. It is integral because the full second difference
vanishes. Its magnitude is at most
\(2S(1-b^{-j})/(b-1)\), hence at most C_0. Starting with h^(0)=0,
perform the displayed quotient-remainder recursion. If
\(p_j=\sum_{t<j}b^t(d_1^{(t)}-d_0^{(t)})\), induction gives
\(h^{(j)}=\lfloor p_j/b^j\rfloor\) and a remainder in [0,b^j).
Since \(|p_j|/b^j\le S(1-b^{-j})/(b-1)\), one has
\(-H_0\le h^{(j)}\le H_0\). These data define a full-graph path.
The actual nonzero difference guarantees its accepting endpoint.

This construction is a bijection between labeled accepting paths and
matrices of digit words whose evaluated rows form nonconstant progressions.
Evaluation of the rows maps these matrices surjectively to the progression
set, with exactly the original representation fibers. A shortest accepting
path has no repeated vertex, proving the finite bound. Closure proves the
all-length assertion. QED.

For canonical D, forgetting h gives a graph morphism on reachable states
from this graph to the graph of Theorem 4.1: (c,h,f) -> (c,f). Before the
first differing canonical digit, h=0; at the first such digit the difference
has magnitude less than b and gives a nonzero remainder. Hence both flags
become true on exactly the same column. This proves preservation of the
transition labels and the acceptance condition on reachable vertices.

An explicitly checked positive full certificate uses b=19,
A={7,8,19}, and D=H(A)={0,7,8,15,19,26,27,34}. Its full graph has 15
reachable states and 288 labeled transitions. Direct D^4 enumeration verifies
closure. There is also an exact independent generator-set explanation:

\[
\bigcup_{j<m}19^j\{7,8,19\}
\ \subseteq\ \bigcup_{j\le m}19^j\{1,7,8\}.
\]

The terms 7 and 8 stay at their original levels, while each 19 at level j
is the original 1-generator at level j+1. The subset-sum inclusion sends
any progression witness to one in the original certified construction.
This example uses digits above the base without replacing the input block.

## 5. Modular reduction, carry compatibility, and explicit contrapositives

Reduction \(\rho_b:\mathbb Z\to\mathbb Z/b\mathbb Z\) is a group
homomorphism. Applied coordinatewise to a digit column, it maps zero-start
carry transitions to modular arithmetic progressions, since
\(\Delta(d)=bc'\). The target carry records the exact integer second
difference divided by b. A sequence of such columns lifts to an integer
progression precisely when the carries match and eventually return to zero,
as proved by Theorem 4.1.

In particular, a modularly k-AP-free D has only constant zero-start columns;
{(0,0)} is then a closed safe certificate. This proves the usual modular
digit lifting argument with no assumption that b is prime.

Two explicit examples retain the additional information carried by the graph.
For b=4, D={0,2}, k=3, the complete reachable set is

\[
\{(0,0),(-1,1),(1,1)\}.
\]

The modular tuple (0,2,0) labels an edge from (0,0) to (-1,1). The vertex
(-1,1) has no outgoing edge: every integer second difference of D-digits is
even, so adding -1 cannot be divisible by 4. The same holds at (1,1).
Consequently the whole digit language avoids 3-APs even though that modular
tuple exists. This uses the original digits {0,2} exactly as given.

For b=8, D={0,1,3,4}, k=5, the complete reachable set is

\[
\{((0,0,0),0),((-1,1,-1),1),((1,-1,1),1)\}.
\]

Only constant columns occur as zero-to-zero transitions. The other two
reachable vertices have no outgoing edge; their closure can be checked by
the 16 possible first digit pairs at each vertex. The reduction map sends
(0,4,0,4,0) to a modular progression, and the exact carry (-1,1,-1) records
its terminal incompatibility. Thus arbitrary nonzero carries are retained
rather than excluded by assumption.

The opposite outcome is equally explicit. For the four-generator block
{1,3,4,7} in base 16, the digit columns

\[
(0,4,8,12,0),\qquad(0,0,0,0,1)
\]

form an accepting path and evaluate to (0,4,8,12,16). For the original
{1,7,8} block in base 18, columns (0,9,0,9),(0,0,1,1) evaluate to
(0,9,18,27). These are witnesses against those exact smaller-base lifts.
They leave the valid base-23 and base-19 constructions intact.

## 6. A capacity formula covering every admissible generator set

A **modular certificate** is a pair (b,A) with b>=2, nonempty A a finite set
of distinct positive integers, S(A)<b, and H(A) modularly k-AP-free.
A **carry certificate** has the same data, replacing the last property by
absence of an accepting path in the graph of Section 4 for D=H(A).
Call their classes \(\mathcal M_k\) and \(\mathcal C_k\).

**Theorem 6.1 (exact certificate capacity).** For every k>=3,

\[
\boxed{\lambda_k
=\inf_{(b,A)\in\mathcal M_k}b^{1/|A|}
=\inf_{(b,A)\in\mathcal C_k}b^{1/|A|}.}
\]

Both classes admit finite exact verification of each member.

**Proof.** From either certificate form
\(A^{[m]}=\bigcup_{j=0}^{m-1}b^jA\). Its members are distinct: each a in A
is in [1,b), so two members at different levels have disjoint magnitude
ranges. Thus |A^[m]|=m|A| and max A^[m]=b^(m-1) max A.

The blockwise subset-sum map
\(\{0,1\}^{m\times |A|}\to H(A)^m\) is surjective, with fiber
cardinality \(\prod_j\mu_A(d_j)\). Composing with e_m gives exactly
H(A^[m])=L_m(H(A);b). The actual subset collisions therefore persist with
known multiplicities, while the value-word map is bijective. Section 4 or 5
proves k-AP-freeness at every m. Deleting generators gives, for every n>=1,

\[
\boxed{g_k(n)\le(\max A)\,b^{\lceil n/|A|\rceil-1}.}
\]

Taking roots and using Theorem 3.1 proves lambda_k<=b^(1/|A|), for either
certificate class.

Conversely, for every nonempty admissible A, take b=2S(A)+1. Any modular
k-AP in the integer digit set H(A) has second differences divisible by b
and of absolute value at most 2S(A)=b-1. They therefore vanish over the
integers. Admissibility makes the progression constant. Thus
A -> (2S(A)+1,A) is an explicit map from every admissible set to a modular
certificate. Theorem 3.1 makes the infimum of the resulting costs exactly
lambda_k. Since every modular certificate is also a carry certificate, the
opposite inequalities are proved. QED.

**Finite countercertificate equivalence.** For every positive real u,

\[
\lambda_k<u\quad\Longleftrightarrow\quad
\exists(b,A)\in\mathcal M_k\;[b<u^{|A|}].
\]

The same equivalence holds with C_k. This follows from the two infimum
identities, including the strict inequality on both sides. It is a proved
witness statement, without an unproved extension premise. For an algebraic
threshold u=c^(1/t), positive integers c,t, the comparison is the exact
integer inequality b^t<c^|A|.

There is a concrete monotone sequence approaching lambda_k from above:
minimize b^(1/|A|) over certificates with 2<=b<=B. For each B this domain is
finite, because A is a subset of [1,b-1] with S(A)<b and
|A|(|A|+1)/2<b. For B>=3 it is nonempty. Exhausting B exhausts all
certificates, so its limit equals lambda_k. The theorem supplies convergence;
this contribution supplies no effective error bound for that convergence.

### 6.2 Full certificates and exact generator distinctness

A finite positive set A is **b-separated** when no two of its elements have
ratio b^t for an integer t>=1. This is a finite decidable predicate: for each
a, multiply successively by b until exceeding max A, checking membership at
each step. The map

\[
q_m:\{0,\ldots,m-1\}\times A\longrightarrow
\bigcup_{j<m}b^jA,\qquad q_m(j,a)=b^ja
\]

is surjective. It is injective for every m exactly when A is b-separated.
Indeed, equality b^i a=b^j a' either gives i=j and a=a', or, after taking
the smaller index, gives precisely a power ratio. Conversely, a'=b^t a
gives the explicit collision q_(t+1)(0,a')=q_(t+1)(t,a).

A **full certificate** consists of b>=2 and a nonempty b-separated set A of
distinct positive integers, together with a safe full graph for D=H(A).
There is no restriction S(A)<b in this definition. Write its class as F_k.

**Theorem 6.2.** For every k>=3,

\[
\boxed{\lambda_k=\inf_{(b,A)\in\mathcal F_k}b^{1/|A|}.}
\]

Every full certificate gives, for all n>=1,
\(g_k(n)\le(\max A)b^{\lceil n/|A|\rceil-1}\).

**Proof.** Injectivity of q_m gives exactly m|A| distinct generators.
The map from subsets of these generators to their block digit words is
surjective, and evaluation gives their actual subset-sum image. Because
word evaluation may now have multiple fibers, the full multiplicity identity
is

\[
\mu_{A^{[m]}}(y)=
\sum_{\substack{d\in H(A)^m\\\sum_j b^j d_j=y}}
\prod_{j<m}\mu_A(d_j).
\]

This follows directly by partitioning the binary generator choices according
to their block sums. Theorem 4.2 certifies the actual value image. The maximum
is (max A)b^(m-1), and deletion gives the stated finite bound. Therefore
lambda_k<=b^(1/|A|) for each full certificate. Every canonical carry certificate
is a full certificate, because its generators lie in [1,b) and its digit
language has the same progression property under the full equivalence.
Theorem 6.1 provides the reverse infimum inequality. QED.

The separation check is retained even when a digit-language check is available.
For b=19 and A={1,7,8,19}, q_m has m-1 duplicate pairs, and its image has
3m+1 elements, compared with 4m indexed generator positions. For instance,
q_2(0,19)=q_2(1,1)=19. The actual image embeds in the indexed system by
choosing, for each image value, its least-level preimage; the resulting
injection of finite subsets preserves their sums. It need not cover arbitrary
indexed selections. The verifier detects this power alias before accepting
a generator-cardinality certificate; it never silently deletes a generator
and retains the original cardinality claim.

## 7. Explicit applications beyond k=4

The small certificates are

\[
(k,b,A)=(5,23,\{1,3,4,7\}),\qquad
(6,47,\{1,2,6,7,14\}).
\]

Their digit sets are respectively

\[
D_{23}=\{0,1,3,4,5,7,8,10,11,12,14,15\}
\]

and

\[
D_{47}=\{0,1,2,3,6,7,8,9,10,13,14,15,16,17,20,21,22,23,24,27,28,29,30\}.
\]

To make the finite modular fact inspectable, for each positive step up to
half the prime modulus the maximum number of consecutive terms in D is:

| b | steps d in order | maximum run lengths in that order |
|---|---|---|
| 23 | 1,...,11 | 3,4,4,4,4,2,3,4,3,4,4 |
| 47 | 1,...,23 | 5,3,4,4,3,5,5,4,3,4,3,3,3,3,3,2,4,2,4,4,4,3,4 |

Each row is verified by starting at every residue and iterating the stated
step until leaving D. The reversal bijection
\((x_0,...,x_{k-1})\mapsto(x_{k-1},...,x_0)\) exchanges d and -d,
so the table covers every nonzero step. The executable additionally checks
all b(b-1) ordered start/step pairs directly, without using that reduction.

A larger exact search gives the six-generator block

\[
A_* = \{1,4,5,17,21,22\},\qquad S(A_*)=70.
\]

Its 38 distinct subset sums are

\[
\begin{split}
D_* =\{&0,1,4,5,6,9,10,17,18,21,22,23,25,26,27,28,30,31,32,\\
       &38,39,40,42,43,44,45,47,48,49,52,53,60,61,64,65,66,69,70\}.
\end{split}
\]

This is modularly 5-AP-free at b=97 and modularly 6-AP-free at b=93.
The second check includes all nonzero steps of the composite modulus,
including steps of order 3 and 31. In each case the complete reachable carry
certificate consists of the initial vertex alone. The exhaustive finite
arithmetic is included in the checker and receipt.

**Theorem 7.1 (new explicit upper constructions).** For every n>=1,

\[
\boxed{g_5(n)\le22\,97^{\lceil n/6\rceil-1},\qquad
       g_6(n)\le22\,93^{\lceil n/6\rceil-1}.}
\]

Consequently \(\lambda_5\le97^{1/6}\) and
\(\lambda_6\le93^{1/6}\). These statements follow by applying the fully
proved lift to the displayed finite certificates. The smaller certificates
also give g_5(n)<=7*23^(ceil(n/4)-1) and
 g_6(n)<=14*47^(ceil(n/5)-1), useful for some finite n.
The minimum of the corresponding finite upper expressions may be used.


The target progression length is retained in the certificate. At base 93,
the same block's two-level subset sums contain the five-term progression

\[
9,\ 990,\ 1971,\ 2952,\ 3933
\]

with difference 981. Its digit columns are
(9,60,18,69,27) and (0,10,21,31,42), all entries in D_*.
The prefix map from six-term progression tuples to five-term tuples is the
restriction of Z^6 -> Z^5. It preserves the common difference. This particular
five-term tuple has no preimage: its forced sixth term is 4914, whose residue
78 modulo 93 is absent from D_*. Thus the base-93 result is certified for k=6,
while base 97 supplies the stated k=5 construction.

For a sharper remainder-sensitive version, list a certificate's generators
as a_1<...<a_s, write n=sq+r with 0<=r<s, and retain q complete levels and
then the first r generators at level q. When r>0 the maximum is a_r b^q;
when r=0 it is a_s b^(q-1). Positivity and disjoint level ranges prove the
cardinality and the bound exactly.

The comparisons with Korsky's stated general graph bound are exact:
for k=5 its rate is sqrt(5), and 97<5^3; for k=6 its rate is 7^(2/5), and
93^5<7^12. These comparisons identify improvement over that retrieved bound,
without a claim of global literature priority.

## 8. An explicit correlated cube behind the six-generator block

Let the six columns in Z^3 be

\[
v_1=(1,0,0),\ v_2=(0,1,0),\ v_3=(1,1,0),\
v_4=(0,0,1),\ v_5=(0,1,1),\ v_6=(1,1,1).
\]

Let C be the image of the binary cube under \(\varepsilon\mapsto
\sum_i\varepsilon_i v_i\). It lies in [0,3] x [0,4] x [0,3].

**Proposition 8.1.** C has no nonconstant five-term arithmetic progression
over Z^3.

**Proof.** In a five-term progression, the first and third coordinates have
integer common differences and span at least 4 times their absolute values.
Their ranges have width 3, so both common differences are zero. A remaining
nonzero middle difference must be +/-1 and use both middle levels 0 and 4.
Middle level 0 forces the choices for columns 2,3,5,6 all to vanish; its
first coordinate is at most 1. Middle level 4 forces all four of those
choices to be present; its first coordinate is at least 2. They cannot share
the required first coordinate. Thus every common difference is zero. QED.

The homomorphism
\(L:\mathbb Z^3\to\mathbb Z\), L(x,y,z)=x+4y+17z, maps these columns
to A_*. Direct enumeration gives |C|=38 and |L(C)|=38, so its restriction
C -> H(A_*) is a bijection. However the second-difference equations after
projection require their own verification: |C+C|=201 whereas
|L(C+C)|=139. The exact surjection L:C+C -> T(A_*) retains this distinction;
its fibers are included in the executable checks. The modular certificate
in Section 7 verifies the required progression property after projection.
The three-dimensional argument motivates the construction without silently
asserting a Freiman equivalence that the sumset cardinalities contradict.

## 9. Overlapping relations of arbitrary extent already occur at k=5

**Theorem 9.1.** For every r>=2 the set

\[
A_r=\{5^i:0\le i<r\}\cup\{5^i+5^{i+1}:0\le i<r-1\}
\]

has 2r-1 distinct positive generators, has 5-AP-free subset sums, and has
minimal signed relations whose intersection graph contains a path of r-1
vertices. Consequently the relation interaction has arbitrarily large
connected extent for every k>=5.

**Proof.** Label generators v_i=5^i and e_i=5^i+5^{i+1}. Their standard
base-5 digit vectors are respectively the unit vector u_i and u_i+u_(i+1),
which proves distinctness. The exact column homomorphism from
Z^{2r-1} to Z^r sends the generator labels to those columns; evaluation
\(\eta(x)=\sum_i x_i5^i\) gives the actual integer weights.
Each subset contributes at most three units at each position, one from its
vertex and at most two from incident edges. Thus H(A_r) lies in the
base-5 language with digits {0,1,2,3}, which is modularly 5-AP-free and
hence safe by Section 5.

The signed relation q_i has coefficients +1 on v_i,v_(i+1), -1 on e_i,
and zero elsewhere. It is minimal: a relation supported on a proper nonempty
subset would have one or two coordinates, incompatible with positivity
and distinctness of the weights. Consecutive q_i share v_(i+1), producing
the claimed path. The map
\(\Gamma:\mathbb Z^{r-1}\to\ker(\Phi_{A_r})\),
\(\Gamma(t)=\sum_i t_iq_i\), is injective because its e_i coordinate
is -t_i. This is an explicit linear embedding of the entire path relation
system into the actual generator kernel. Admissibility for larger k follows
from the prefix map on progression tuples. QED.

The old four-term splitting algebra remains visible. For adjacent edges,
q_i+q_(i+1) has magnitude-two layer consisting of the single nonzero weight
v_(i+1). It gives the actual four-term progression

\[
v_i+v_{i+2},\quad v_i+v_{i+1}+v_{i+2},\quad
e_i+e_{i+1},\quad e_i+e_{i+1}+v_{i+1},
\]

with common difference v_(i+1). At r=3 these values are 26,31,36,41 in
H({1,5,25,6,30}). The restriction of the coordinate projection Z^5 -> Z^4 gives the prefix map
\(\operatorname{AP}_5(H(A_r))\to\operatorname{AP}_4(H(A_r))\)
preserves common differences; the displayed 4-AP lies outside its image.
Its witness and the 5-AP-free proof identify exactly which step of a
four-term-only decomposition cannot be imposed on the general-k domain.

## 10. A proved boundary for all positive interval-digit column models

**Proposition 10.1 (full positive-column budget).** Let M be an r by n
nonnegative integer matrix with distinct nonzero columns. Let every row sum
be at most tau. Then

\[
\boxed{2n\le r(\tau+1).}
\]

**Proof.** At most r columns have coordinate sum 1, since they must be
unit vectors. Every other column has coordinate sum at least 2. The total
column mass is therefore at least 2n-r and is exactly the total row mass,
which is at most r tau. Combining the exact counts proves the inequality.
QED.

The column map M:Z^n -> Z^r and the evaluation homomorphism
\(\eta_b(x)=\sum_{i=0}^{r-1}x_i b^i\) give the integer generators.
When tau<b, evaluation is injective on the full subset-coordinate box;
its inverse is the actual base-b digit expansion. For prime b and
 tau=min(b,k)-2 this is the positive interval-digit construction. The
budget forces r>=ceil(2n/(min(b,k)-1)). With r active positions, some
generator has value at least b^(r-1). Thus, for each fixed prime b, that entire column class has
exponential rate at least b^(2/(min(b,k)-1)); the graph construction attains
that rate asymptotically. This is a statement about the precisely displayed
column domain and maps.

An explicit failure of a proposed universal passage into that domain is
supplied by A={1,3,4,7}. For any assignment of nonzero nonnegative columns
w_1,w_3,w_4,w_7 preserving its subset equalities,

\[
w_4=w_1+w_3,\qquad w_7=w_3+w_4,
\qquad \sum_{a\in A}w_a=3w_1+4w_3.
\]

Some coordinate of w_3 is at least 1, and that row load is at least 4.
Hence every such assignment violates a row-load bound of 3. The typed
relation-preserving map M:Z^4 -> Z^r has to send the two displayed relation
vectors to zero; those equations prove the obstruction in every dimension.
The actual scalar map (coefficients 1,3,4,7) and the modular projection to
Z/23 are exhibited in Section 7 and produce a valid 5-AP-free construction.
Thus the carried and correlated digit route has a concrete mathematical
reason to be pursued beyond positive interval boxes.

## 11. What has been established and what remains to be evaluated

The proved all-k conclusions are the exact product, the existence of each
lambda_k, the complete certificate-capacity formulas, and the finite
canonical and full carry decisions with an explicit witness-length bound. The explicit k=5 and
k=6 certificates improve the retrieved general upper estimates. The path
construction and positive-column count prove two precise structural
boundaries for possible lower-bound arguments.

The exact numerical values of lambda_k for general k>=5, and the sharp
large-k behavior of log lambda_k, remain unevaluated here. The current lower
and upper mechanisms leave a gap between order 1/k and order log(k)/k.
The new capacity identity identifies the exact optimization across all
finite certificates, including every admissible integer set through its
explicit map A -> (2S(A)+1,A). A bounded search supplies exact finite data
and decreasing upper bounds; it supplies no lower certificate for unsearched
bases. Independent review should focus on Sections 2,4,6 before using the
capacity theorem, and on the modular transcripts before citing new constants.

## 12. Reproducible verification and exact search domains

The standalone command, run from this contribution's directory, is

```sh
python certificates/verify_general_k.py --output certificates/general_k_receipt.json
```

The resulting receipt reports PASS for the following completely specified
finite domains. The general implications are proved in Sections 2--6; these
checks independently test their finite maps, graph transitions, and witnesses.

| Check | Domain and result |
|---|---|
| Primary modular certificates | Every start and nonzero step: 342 pairs for base 19; 506 for base 23; 2,162 for base 47; 9,312 for base 97; 8,556 for base 93 |
| Canonical carry graph | All D subset [0,b) containing zero, 2<=b<=8, 3<=k<=6: 1,016 instances; 415 safe and 601 with explicit witnesses |
| Independent canonical closure | Direct enumeration of digit columns verifies 1,433 transitions across the safe certificates |
| Full carry graph | All D subset [0,6] containing zero, b=2,3,4, k=3,4: 384 instances; 30 safe and 354 with explicit witnesses |
| Independent full closure | 122 transitions across the small safe cases, plus 288 transitions for the noncanonical {7,8,19} example |
| Direct finite languages | All graph-domain cases at word lengths 1,2,3: 4,200 comparisons with separately generated integer sets |
| Exact composition | 256 ordered pairs of empty, singleton, or two-element subsets of [1,5]; 1,024 full AP-tuple comparisons for k=3,4,5,6 |
| Associativity | All 4,096 ordered triples from the same 16-set domain |
| Primary generator lifts | Two levels for each of five primary certificates; complete binary fiber multiplicities and remainder-sensitive deletions |
| Structural maps | The 38-point correlated cube, all 201 points in its sumset and all 139 projected values; path-relation family r=2,3,4,5 |
| Regressions | Two modular/carry bridge examples, five decoded failed-base/progression-length constructions, power-alias cardinalities, and nine rejected invalid inputs or mutations |

The canonical and full graph outputs are additionally compared on every
canonical input with b<=6 and k<=5. Two independent transition generators are
used: the search solver builds columns recursively by congruences, while the
closure checker directly enumerates D^k. Negative outputs retain digit columns,
which the checker evaluates independently to the displayed integer progression.

The constructive search is exhaustive over every positive generator set
with sum strictly less than its base for k=5,6 and bases 3 through 160.
A second search uses modular certificates for k=7 through 12 and bases 3
through 80. These are 784 base/length parameter records. The generic search
has a depth cap of eight, but its largest returned generator counts are six
in the first domain and seven in the second. The cap therefore leaves no
larger admissible set hidden: any such set would have an admissible eight-
element subset. The verifier separately rechecks all 784 recorded witnesses.
It does not replay the entire maximality search by default.

The exhaustive-search pruning has explicit justifications. Generators are
visited in strictly increasing order. For a partial tuple, the minimum sum
needed to exceed the current best cardinality is an arithmetic-series sum;
branches exceeding the base budget are rejected. A failed partial digit set
cannot become safe after adding generators, because its progression word
remains in every larger alphabet. The search retains the actual generators
and only caches the progression property of an already computed digit set.
No multiplication by units, gcd removal, or re-centering of an input set is
used. All comparisons of exponential costs are exact cross-power integer
comparisons.

The search can be replayed with

```sh
python search_carry.py --mode carry --min-base 3 --max-base 80 --k 5 6
python search_carry.py --mode carry --min-base 81 --max-base 160 --k 5 6
python search_carry.py --mode modular --min-base 3 --max-base 80 --k 7 8 9 10 11 12
```

A further retained full-carry probe fixes A_* and tests bases 23 through 70
for both k=5 and k=6. All 96 instances produce two-level progression
witnesses. The complete witnesses are in
`logs/noncanonical_fixed_block.json`; this is a failure of those precise
base/block pairs, with the map to integer progressions supplied by Theorem
4.2. It provides no obstruction to different blocks at the same bases.

A repeated verifier run with Python's optimization flag `-O` gives the same
receipt bytes. The program uses explicit exception-raising requirements,
so optimization cannot remove its checks. Source and transcript SHA-256
hashes identify exact inputs and outputs. Lean elaboration was not run in
this contribution; its certificate type is an ordinary mathematical proof
plus finite exact verification, and existing Lean artifacts are preserved.

## References, inspected sources, and contribution lineage

Costa, S. (2026). *A negative answer to the Erdős–Sárkőzy question* (Version 1)
[Preprint]. arXiv:2609.06303. Source: https://arxiv.org/html/2609.06303v1. Inspected HTML, especially abstract and Section 1;
used solely for the current historical k=3 question.

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (Version 1)
[Preprint]. arXiv:2606.24139. Source: https://arxiv.org/html/2606.24139v1. Inspected HTML, Sections 1,5,6; used for the
problem definition, known chain mechanism, and the comparison upper bound.

Anonymous/deleted Reddit contributor, & The Clankers. (2026, September 13).
*The exponential rate for four-term-progression-free subset-sum sets*
[Workbench manuscript]. `paper/ep817_k4_rate.tex` at the base revision above.
The original construction and proof route belong to the anonymous contributor.

sneed-and-feed. (2026, September 13). *Formalize finite upper bound theorem and
core helper lemmas in Extended.lean* [Pull request #1]. Same workbench.

The Clankers. (2026, September 14). *An unweighted ternary-variance refinement
of the k=4 lower bound* [Draft pull request #2], commit
`612020848e4bbec5f5a723a64c5fdc85636b5e83`. Parallel predecessor contribution;
its separate review and Lean status are retained.

PolyClank methodology: `erdos-straus-foundation/POLYCLANK.md` (inspected) and
`yang-mills-interacting-workbench/docs/polyclank/RESEARCH_STATE.md` at
`7ba7ea5a5dab84d88934477de93dda71f6af0662` (inspected). These supply the public
research-record convention, with claim-local evidence and source lineage;
they supply no additional mathematical theorem used in this note.
