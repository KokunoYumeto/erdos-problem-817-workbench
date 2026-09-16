# Exact local-pattern quotients and switching image capacity

The Clankers. 16 September 2026.

**Evidence and lineage.** This is an additive continuation of *Universal image observations, bounded-fibre resolutions, and spectral capacity*, delivered in `EP817_SEVEN_OBSERVABLE_20260916.zip`. The preceding archive is retained byte-for-byte. The statements below have ordinary proofs; the listed finite inputs have exact computational certificates and a separately implemented arithmetic audit. No new Lean elaboration or outside mathematical review is claimed. The original anonymous/deleted contributor retains credit for the four-term construction and signed-block proof; `sneed-and-feed` retains separate credit for the finite upper-bound Lean extension. Standard circulation decomposition and local-pattern polytopes are background, not claimed inventions. No general literature-priority claim is made.

The main progression problem keeps the original distinct positive generators. Write

\[
H_q(A)=\left\{\sum_{a\in A}c_a a:0\le c_a<q\right\},\qquad S(A)=\sum_{a\in A}a.
\]

Here q is coefficient arity. Progression length is denoted k. Admissibility always concerns the actual binary image H_2(A). The present contribution proves a complete positivity description of the seven fifth-arity observations, lifts every arithmetic carrier to a chain map on original local binary words, and solves an actual two-block changing-schedule image optimization. It also proves that arbitrary mixtures of the preceding residue-saturated record blocks cannot benefit from faithful ternary re-encoding. No new unrestricted upper record or full determination of the general rate is asserted.

## 1. Original numerical sets, observations, and local words

For a nonempty finite centrally symmetric set Y of integers, retain the seven original observations, in this order:

\[
 f(Y)=\bigl(|Y+R|\bigr)_{R\in\mathcal R},\qquad
 \mathcal R=(0,01,02,012,03,013,0123).
 \tag{1.1}
\]

For example, 013 means the actual shift set {0,1,3}, not a digit word. We write the corresponding coordinates as f_0,f_1,...,f_6. The symmetry assumption means c-Y=Y for c=min(Y)+max(Y). Every H_q(A) has this symmetry by the original coefficient-complement involution.

For each integer t from min(Y) through max(Y)+3, define the binary four-position word

\[
 e(t)=\sum_{j=0}^3 2^j\mathbf1_Y(t-j).
 \tag{1.2}
\]

Let c_e(Y) count its occurrences. These are occurrences in the characteristic function of the *distinct numerical image*. They are not counts of the original coefficient representations of a value.

Use the directed overlap graph with vertex set {0,...,7} and edge set {0,...,15}; edge e has source floor(e/2) and target e mod 8. Scanning (1.2) starts and ends at vertex 000. Thus the integral edge current c(Y) is a cycle:

\[
 \partial c(Y)=0,\qquad
 \partial e=e_{e\bmod8}-e_{\lfloor e/2\rfloor}.
 \tag{1.3}
\]

There are span(Y)+4 edges, where span(Y)=max(Y)-min(Y). Reflection of Y proves c_e=c_rev(e), with rev reversing all four bits. The zero word 0000 can occur in an actual gap. It is retained as an ordinary edge and cycle.

### 1.1 Nine nonnegative pattern coordinates and two exact relations

Select one original count from each nonzero reversal orbit, ordered as

\[
 z=(c_{0001},c_{0010},c_{0011},c_{0101},c_{0110},
       c_{0111},c_{1001},c_{1011},c_{1111}).
 \tag{1.4}
\]

A selected count is not the sum of the two reversed counts. For a palindromic word its orbit has one element. Direct expansion of each union indicator, followed by (1.3), gives

\[
\begin{array}{ll}
z_0=f_6-f_3,&z_1=f_6-f_5,\\
z_2=-f_1+f_3+f_5-f_6,&z_3=-f_2+f_3+f_5-f_6,\\
z_4=-f_4+2f_5-f_6,&z_5=-f_0+f_1+f_2-f_3+f_4-2f_5+f_6,\\
z_6=-f_1+2f_3-f_6,&z_7=-f_0+2f_1+f_2-2f_3-f_5+f_6,\\
z_8=4f_0-3f_1-2f_2+2f_3-f_4+2f_5-f_6.&
\end{array}
\tag{1.5}
\]

Write this integral map as z=A f. The complete conservation equations on the nine coordinates are

\[
 z_0-z_1-z_2+z_6=0,\qquad z_2-z_4-z_5+z_7=0.
 \tag{1.6}
\]

Their matrix is C. The explicit inverse on ker C is f=Bz, where

\[
 B=\begin{pmatrix}
1&0&1&1&0&1&1&2&1\\
1&1&1&2&1&2&1&2&1\\
1&1&2&1&1&2&1&2&1\\
1&2&2&2&1&2&1&2&1\\
2&0&2&2&0&2&1&2&1\\
2&1&2&2&1&2&1&2&1\\
2&2&2&2&1&2&1&2&1
\end{pmatrix}.
\tag{1.7}
\]

In particular BA=I_7, CA=0, and ABz=z for Cz=0. One way to check all identities directly is to let E insert z into the original sixteen coordinates, duplicating a reversal pair, and to let O_R(e)=1 when at least one bit indexed by R is one. Then B=OE and the vertex conservation relations on E are exactly the two rows of C. Solving those equations gives (1.5). This proves both directions over the integers, not merely equality of real ranks.

Every inequality z_i>=0 is therefore an exact original-pattern count. For example,

\[
4f_0-3f_1-2f_2+2f_3-f_4+2f_5-f_6=c_{1111}(Y)\ge0.
\]

Equality says that no four consecutive integers occur in Y. A coefficient-zero count at a supported word label remains separate from a word absent from an admitted source support.

The omitted gap count is also exact:

\[
 \boxed{c_{0000}(Y)=\operatorname{span}(Y)+4-f_6(Y).}
 \tag{1.8}
\]

For Y={0,4} and Y'={0,5}, all seven observations agree, but

\[
 c(Y')-c(Y)=e_{0000}.
 \tag{1.9}
\]

These are two actual symmetric numerical sets, so this receiving kernel has a concrete source witness.

## 2. The complete feasible cone: nine facets and ten primitive rays

Let K be the closed conical hull of all f(Y) for nonempty finite centrally symmetric integer sets. Then

\[
 \boxed{K=\{f\in\mathbb R^7:Af\ge0\}.}
 \tag{2.1}
\]

The nine inequalities in (1.5) are all facets. The cone has dimension seven and precisely ten extreme rays.

Here is the full integral structure. The nonnegative integral solutions of Cz=0 are generated, without denominators, by

\[
\begin{gathered}
e_3,\ e_8,\ e_0+e_1,\ e_6+e_1,\ e_4+e_7,\ e_5+e_7,\\
e_0+e_2+e_4,\ e_0+e_2+e_5,\ e_6+e_2+e_4,\ e_6+e_2+e_5.
\end{gathered}
\tag{2.2}
\]

The same list generates the nonnegative real solutions as a cone. For a direct decomposition, remove the e_3 and e_8 components first. Equations (1.6) read

\[
 z_0+z_6=z_1+z_2,\qquad z_4+z_5=z_2+z_7.
\]

Allocate z_2 units from the available pair (z_0,z_6) to the available pair (z_4,z_5), using their actual minimum at each allocation. These are the four triple generators. The remaining supplies sum to z_1 and z_7 and give the four pair generators. This is exact for real, rational, and integer data. No coefficient vector is divided by a common factor to change an original arithmetic relation.

The ten observed rays f=Bz, with their original integral scale retained, are:

| Period word | Integral count ray |
|---|---|
| 10 | (1,2,1,2,2,2,2) |
| 1 | (1,1,1,1,1,1,1) |
| 1000 | (1,2,2,3,2,3,4) |
| 001 | (1,2,2,3,1,2,3) |
| 011 | (2,3,3,3,2,3,3) |
| 1011 | (3,4,4,4,4,4,4) |
| 11000 | (2,3,4,4,4,5,5) |
| 111000 | (3,4,5,5,6,6,6) |
| 1001 | (2,3,4,4,3,4,4) |
| 11001 | (3,4,5,5,5,5,5) |

The period words refer to their actual occupied residue positions, not coefficient digits of a generator set. To realize a ray asymptotically, let P_N be N literal copies of its period support and put

\[
 Y_N=P_N\cup(2N p+4-P_N),
 \tag{2.3}
\]

where p is the period length. The two supports have a gap greater than three, so their translated union counts add. Y_N is centrally symmetric. If h is the number of ones in one period and g is its displayed count ray, then |Y_N|=2Nh and

\[
 \left|f_i(Y_N)-\frac{2Nh}{g_0}g_i\right|\le12
 \quad(0\le i\le6).
 \tag{2.4}
\]

Only the first and last three positions of one periodic segment can disagree with the periodic union count; applying this separately to both reflected copies proves the bound. For the displayed primitive periods h=g_0, but (2.4) keeps the scale explicitly.

Thus every ray belongs to the closed cone generated by actual sets. Conversely every actual set satisfies (1.5), and the decomposition (2.2) proves the opposite inclusion in (2.1). Each generator in (2.2) is a minimal positive dependence among the two-dimensional columns of C; hence it is extreme. The rays with z_i=0 span dimension six for each i, proving all nine facet assertions. The finite certificate checks these ranks exactly.

There is also an exact integer semigroup statement:

\[
 \{f\in\mathbb Z^7:Af\ge0\}
 =\sum_{g\text{ in the table}}\mathbb Z_{\ge0}g.
 \tag{2.5}
\]

It follows from (1.5)--(1.7) and the integral allocation proof. Equation (2.5) describes local circulation coordinates. It does not assert that each such integer vector is the count vector of one finite numerical set. For example, the ray vector (1,1,1,1,1,1,1) cannot be the observation of a one-point set, whose |Y+{0,1}| is two. Its actual source realization is the periodic limit (2.3). The scale parameter and the endpoint data are not erased by that comparison.

The finite graph has nineteen directed simple cycles, one of them the zero loop. Symmetrizing their integral currents and decomposing by (2.2) is an independent complete certificate for the cone. Local-pattern circulation polytopes are classical in symbolic dynamics; the particular integral nine-to-seven comparison, ten generators, and arithmetic action below are the specialized calculations here (Ziemian, 1995).

## 3. An exact two-potential test for every linear bound

Let w be a rational row on the seven original observations. The following are equivalent:

\[
\begin{split}
&w f(Y)\ge0\quad\text{for every finite symmetric numerical }Y;\\
&w g\ge0\quad\text{for the ten displayed count rays};\\
&w=\alpha A\quad\text{for some rational row }\alpha\ge0.
\end{split}
\tag{3.1}
\]

There is an explicit construction requiring no linear-programming oracle. Put r=wB and retain

\[
 p_1=\min(r_0,r_6),\qquad p_2=-\min(r_4,r_5),
 \qquad\alpha=r-(p_1,p_2)C.
 \tag{3.2}
\]

The ten ray inequalities are exactly

\[
 r_3,r_8\ge0,
\quad r_0+r_1,r_6+r_1\ge0,
\quad r_4+r_7,r_5+r_7\ge0,
\]

and the four inequalities r_i+r_2+r_j>=0 for i in {0,6}, j in {4,5}. Substitution in (3.2) proves every component of alpha is nonnegative. Since BA=I and CA=0, alpha A=w. This proves the last implication directly. The other implications follow from the original pattern counts and the actual periodic approximation.

Thus a successful linear estimate has the literal decomposition

\[
 \boxed{w f(Y)=\sum_{i=0}^8\alpha_i c_{\omega_i}(Y),}
 \tag{3.3}
\]

with all original nonnegative terms visible. The correction (p_1,p_2)C is zero on the original conserved current. Equality is exactly absence of every counted pattern whose coefficient alpha_i is positive.

A failed ray test also produces a numerical source, not just an abstract vector. If w g=-epsilon<0, choose the period in the table and any integer

\[
 N>\frac{6g_0\|w\|_1}{h\epsilon}.
 \tag{3.4}
\]

The symmetric set (2.3) then has w f(Y_N)<0 by (2.4). The verifier evaluates the resulting actual set. This is an obstruction to the stated universal-tail inequality; a periodic binary support is not automatically the fifth-arity image of a positive-generator block. That further arithmetic realizability constraint remains separate.

For an arithmetic count matrix M and a proposed rational growth inequality ell M f>=c ell f, apply (3.1) to the actual row w=ell M-c ell. The result is either a complete certificate on every finite symmetric tail or an explicit periodic finite-tail obstruction. If ell is positive on the cone, multiplying certified edge inequalities gives a lower bound for every changing schedule in the specified dictionary. No assertion is made that one linear potential always gives the optimal rate.

## 4. The arithmetic action is a literal graph-path substitution

This construction works at every coefficient arity q>=2. Put d=q-2. Vertices are binary words of length d; edges are binary words of length d+1, with the same overlapping source and target convention as in (1.3). For q=2 there is one vertex and the convention has its literal meaning.

Let b>=2 and 0 in D subset [0,(q-1)(b-1)]. An input edge a=(a_0,...,a_d) is replaced by b consecutive output edges. At residue z=0,...,b-1, its r-th output bit is

\[
 o_r^{(z)}=\bigvee_{\substack{0\le h\le d\\ bh+z\in D+r}}a_h,
 \qquad0\le r\le d.
 \tag{4.1}
\]

This is the literal membership test for bt+z-r in D+bY when a_h=1_Y(t-h). The range bound ensures all required h lie in [0,d]. Every actual digit remains in the membership test; no digit is replaced by its residue alone.

The vertex map is

\[
 \phi(s)_r=\bigvee_{\substack{1\le h\le d\\bh-1\in D+r}}s_{h-1},
 \qquad0\le r<d.
 \tag{4.2}
\]

Adjacent output edges overlap because o_(r+1)^(z+1)=o_r^z. The first source is phi(input source), and the final target is phi(input target), by (4.2). Hence every input edge is sent to a specified path with those endpoints.

Let L be the integral matrix counting the entire output path of each edge, and V the matrix of phi. The exact chain square is

\[
 \boxed{\partial L=V\partial.}
 \tag{4.3}
\]

Every column of L sums to b, and the actual zero loop satisfies

\[
 Le_{0^{q-1}}=b e_{0^{q-1}}.
 \tag{4.4}
\]

For a finite numerical input Y, scanning one full input edge cell produces some additional terminal zero words. The exact number is

\[
 g=(q-1)(b-1)-\max D\ge0.
\]

Consequently the original finite-set current obeys

\[
 \boxed{c(D+bY)=Lc(Y)-g e_{0^{q-1}}.}
 \tag{4.5}
\]

Indeed the input scan has span(Y)+q-1 cells, each of b output positions. The actual output scan has b span(Y)+max(D)+q-1 positions. Their difference is g, and all omitted terminal words are zero. This proves both the amount and the support of the correction.

The correction is tied to the presence of a nonempty finite source. On the free space of finite-set objects, let epsilon([Y])=1 and Psi([Y])=c(Y). Then

\[
 \Psi\mathsf S_{D,b}=L\Psi-g e_0\epsilon,
 \qquad \mathsf S_{D,b}[Y]=[D+bY].
 \tag{4.6}
\]

Adjoining epsilon makes this a genuine linear augmented action. It is not valid to apply the affine finite-boundary correction to an arbitrary stationary ray without its presence and endpoint data.

### 4.1 The seven-dimensional quotient and its positive nine-coordinate lift

At q=5 let Z_1^+ be the reversal-invariant cycle subspace in Q^16. It has dimension eight. The original union observations J give the exact sequence

\[
 \boxed{0\longrightarrow\mathbb Qe_{0000}
 \longrightarrow Z_1^+\xrightarrow{J}\mathbb Q^7\longrightarrow0.}
 \tag{4.7}
\]

Explicitly, the section r(f)=EAf has zero 0000 coefficient, where E duplicates the reversal pairs from (1.4). Equations (1.5)--(1.7) give Jr=I and

\[
 c-rJc=c_{0000}e_{0000}.
 \tag{4.8}
\]

This proves exactness without choosing an eigenbasis. The section is a coefficient-current representative, not a claim that every represented vector is itself one finite binary support.

For symmetric D, let K be the nine-by-nine nonnegative integer matrix obtained by expanding a selected reversal count into its actual input edges, applying L, and reading the nine selected output counts. Let M be the original seven-count carrier. Then

\[
 \boxed{KA=AM.}
 \tag{4.9}
\]

On the original invariant subspace Cz=0, this is exactly z(D+bY)=Kz(Y). Its conservation relations remain in that subspace; the nine entries are not treated as independent new variables. One can prove (4.9) from (4.1) and (1.5), or by applying the actual operator to seven finite symmetric source sets whose observation matrix has determinant minus one. Those seven original sets are listed in the certificate.

Every matrix M preserves the full cone (2.1). This follows either from (4.9), K>=0, and the two conservation relations, or from the direct count identity followed by the periodic-limit construction. The nine-coordinate lift is positive and integral; no linear-programming extension of M is needed.

### 4.2 The section defect and metric return are exact

The section difference is entirely in the retained zero-loop line:

\[
 \boxed{Lr-rM=e_{0000}\lambda,
 \qquad\lambda=b e_6^{\mathsf T}-e_6^{\mathsf T}M.}
 \tag{4.10}
\]

The sum of the nonzero input edge coordinates is f_6. Column sums of L equal b, and the nonzero output mass is (Mf)_6. Their difference proves (4.10).

Give the original sixteen edge-current basis vectors the specified orthonormal metric. In the nine selected coordinates its restriction is

\[
 W=\operatorname{diag}(2,2,2,2,1,2,1,2,1).
\]

The quotient metric is the full positive form

\[
 G=A^{\mathsf T}WA.
\]

The zero-loop axis is orthogonal to r(Q^7), so r is the actual minimum-norm section in this metric. Orthogonality proves

\[
 \boxed{(Lr)^{\mathsf T}(Lr)=M^{\mathsf T}GM+\lambda^{\mathsf T}\lambda.}
 \tag{4.11}
\]

For an original finite current c=r(f)+z_0e_0, the complete receiving norm after (4.5) is

\[
 \|c(D+bY)\|^2
 =(Mf)^{\mathsf T}G(Mf)
 +\bigl(bz_0+\lambda f-g\bigr)^2.
 \tag{4.12}
\]

The current metric is not the original coefficient-word metric of H_q(A). On that separate source the value quotient still has Gram diag(1/mu(y)), with its original weighted section. The passage from a whole numerical set to its local-pattern counts is linear only after forming the free module on finite-set objects. In particular, it is not a context-free linear map sending each individual value basis vector to a fixed local pattern.

The previous word-to-value quotient and the additional local observation kernel therefore remain separate. On the free finite-set source, (1.9) proves that the added zero-loop line in ker(JPsi)/ker(Psi) is actually reached. Supported zero and external absence are not interchanged.

### 4.3 A larger operator can have the wrong numerical growth rate

Since every column of L sums to b and (4.4) holds, rho(L)=b. That number is not automatically the numerical image radius rho(M).

For A={3,10}, b=19, the actual fifth-image matrix has characteristic polynomial

\[
 X^3(X^4-36X^3+382X^2-1116X+65).
\]

Its largest root lies in (18,19), approximately 18.911324463. The full edge operator has characteristic polynomial

\[
 X^{10}(X-19)(X-1)
 (X^4-36X^3+382X^2-1116X+65).
\]

The 19-eigenvector e_0000 is present in the original cycle space and killed by the precise quotient (4.7). Thus the source-to-receiving spectral discrepancy is explained by an actual kernel, not by selecting a preferred root after discarding unspecified information. The full matrices and determinant checks are in the receipt.

## 5. An exact changing-block minimum that beats both homogeneous images

Use two original level types, both with radix ten:

\[
 \mathsf A=(10,\{1,3\}),\qquad
 \mathsf B=(10,\{2,4\}).
 \tag{5.1}
\]

Their binary digit images are respectively {0,1,3,4} and {0,2,4,6}. A nonzero modular step of order at least five would require at least five distinct points; a step of order two differs by five and neither set contains such a pair. Thus both are modular-five-free. Every finite prefix of every changing schedule is five-admissible by the original lowest-digit induction. There are exactly two distinct generators per level.

In the coordinate order (1.1), their fifth-image actions are

\[
 M_Af=(3f_0+7f_1,\ 2f_0+8f_1,\ f_0+9f_1,\ f_0+9f_1,
                10f_1,\ 10f_1,\ 10f_1),
\]

\[
 M_Bf=(2f_1+3f_3,\ 4f_1+6f_3,\ f_1+4f_3,\ 3f_1+7f_3,
           4f_1+6f_3,\ 3f_1+7f_3,\ 2f_1+8f_3).
 \tag{5.2}
\]

Both have characteristic polynomial X^5(X-10)(X-1). Their homogeneous image counts are

\[
 N_A(m)=\frac{16\,10^m-7}{9},\qquad
 N_B(m)=\frac{4\,10^m-1}{3}.
 \tag{5.3}
\]

The actual stable local current for A is the all-occupied periodic ray. For B it is the parity ray (1,2,1,2,2,2,2). Both have homogeneous growth ten, but they retain different original numerical supports.

### 5.1 Run factorization and complete optimization

Retain

\[
 u=(17,18,19,19,20,20,20)^{\mathsf T},\qquad
 v=(0,2,0,3,0,0,0).
\]

Direct integer multiplication proves

\[
 M_AM_B=uv.
 \tag{5.4}
\]

For a,b>=1 define U_a=M_A^{a-1}u and V_b=vM_B^{b-1}. Then M_A^aM_B^b=U_aV_b. The exact scalar crossing of consecutive runs is

\[
 \boxed{V_bU_a=\theta(a,b)
 =\frac{8\,10^{a+b}+4\,10^b-3}{9}.}
 \tag{5.5}
\]

For a direct all-length verification of (5.5), the vectors u and row v satisfy the respective recurrences with polynomial (X-1)(X-10). The four values at a,b in {1,2} determine the displayed two-variable expression. This proves it for every a,b, beyond the listed finite replay.

For a cyclic word with runs A^(a_1)B^(b_1)...A^(a_s)B^(b_s), cyclically rotating the matrix product to expose (5.4) proves that its only possible nonzero eigenvalue is

\[
 \prod_{i=1}^s\theta(a_{i+1},b_i),\qquad a_{s+1}=a_1.
 \tag{5.6}
\]

A change of cyclic starting position preserves the nonzero eigenvalues. The scalar in (5.6) is positive and is the radius. Pure words have radius 10^m.

Let r=893^(1/3). For fixed L=a+b, the expression (5.5) is minimized by b=1. For L=2 it equals 93, and

\[
93^3=804357>797449=893^2.
\]

For L=3 the minimum is theta(2,1)=893. For L>=4,

\[
\theta(a,b)^{1/L}>10(8/9)^{1/L}\ge10(8/9)^{1/4}>\sqrt{93},
\]

where the last comparison is 80000>9*93^2. The remaining length-three pair has theta(1,2)=933 and 933^2>93^3. Therefore

\[
 \boxed{\theta(a,b)\ge r^{a+b},}
 \tag{5.7}
\]

with equality exactly at (a,b)=(2,1).

For any finite word w, let N(w) be its actual fifth-arity image cardinality and P_w its ordered count matrix. Its literal aggregate generator block has radix 10^|w|. At a cut of a repeated aggregate, a numerical value has at most four original distinct-value pairs. Thus

\[
 \boxed{\rho(P_w)\le N(w)\le4\rho(P_w).}
 \tag{5.8}
\]

For completeness, if N_t is the image of t repetitions, then N_t<=N(w)^t and N_t>=N(w)^t/4^(t-1). Applying the same inequalities to larger concatenations yields the root limit and its factor-four bound. To identify that limit with the full radius of P_w, retain the auxiliary weighted coordinate norm

\[
 \|x\|_v=\max_i|x_i|/|R_i|,\qquad v_i=|R_i|.
\]

For every actual nonnegative word matrix P, its induced norm is max_i(Pv)_i/v_i. The numerical meaning of Pv gives

\[
 \|P\|_v=\max_i |L+R_i|/|R_i|=|L|.
\]

The upper inequality counts the original translated copies, and the singleton coordinate gives equality. Thus \|P_w^t\|_v=N_t and the radius is the same root limit. This proves (5.8) without discarding an unobserved spectral component. The auxiliary coordinate norm is not substituted for an original word or current metric.

Equations (5.6)--(5.8) prove N(w)>=r^|w| for every word. The period AAB attains the rate. Its actual six-generator aggregate and radix are

\[
 C=\{1,3,10,30,200,400\},\qquad Q=1000.
 \tag{5.9}
\]

The period matrix has rank one, radius 893, and

\[
 \boxed{|H_5(C_Q^{[t]})|=2301\,893^{t-1}\quad(t\ge1).}
 \tag{5.10}
\]

Consequently the exact optimization over all infinite schedules in this two-block dictionary is

\[
 \boxed{
 \inf_{\mathbf w\in\{A,B\}^{\mathbb N}}
 \liminf_{m\to\infty}|H_5(G_m(\mathbf w))|^{1/(2m)}
 =893^{1/6}\approx3.1031914962.
 }
 \tag{5.11}
\]

Alternation AB has the slightly larger image rate 93^(1/4), approximately 3.1054227991. Homogeneous image rates are sqrt(10), approximately 3.1622776602.

All the original radices in this dictionary are still ten. Their original maximum-generator rate is sqrt(10), for every schedule. Equation (5.11) is an image-capacity improvement. The preceding arity-five prime-observation theorem converts it into a new re-encoded construction rate, retaining the original finite prefactor and prime height. It is not a better global record than the existing workbench bound 97^(1/6) for k=5.

### 5.2 Quantitative stability of the optimizing pattern

For a mixed cyclic word, call a crossed run pair (a_(i+1),b_i) good when it equals (2,1), and let L_bad be the total length of all other crossed pairs. For a pure word set L_bad=|w|. The proof above gives theta(a,b)>=93^((a+b)/2) for every bad pair, while theta(a,b)<=10^(a+b) always. With L=|w|,

\[
 \boxed{
 r^L(\sqrt{93}/r)^{L_{bad}}
 \le N(w)
 \le4r^L(10/r)^{L_{bad}}.
 }
 \tag{5.12}
\]

In particular, for any sequence of words with lengths tending to infinity,

\[
 \lim N(w)^{1/|w|}=r
 \quad\Longleftrightarrow\quad
 L_{bad}(w)/|w|\longrightarrow0.
\]

For the limiting inferior alone, the corresponding exact criterion is

\[
 \liminf N(w)^{1/|w|}=r
 \quad\Longleftrightarrow\quad
 \liminf L_{bad}(w)/|w|=0.
\]

Both implications follow from the two strictly positive logarithmic gaps in (5.12); no limit is presumed to exist for an arbitrary schedule. These are proved stability statements, not conclusions drawn from checking a finite list of periods.

## 6. A common occupied ray controls arbitrary mixtures of the record blocks

For any original canonical digit set D, the following are equivalent:

\[
 D\bmod b=\mathbb Z/b\mathbb Z,
 \qquad M\mathbf1=b\mathbf1.
 \tag{6.1}
\]

The first row of M counts the occurring residues of D. If all occur, every D+R also has every residue, so all row sums equal b. This proves both implications. In the positive local-pattern coordinates this is precisely preservation of the pure 1111 ray with multiplier b.

For a changing schedule whose fifth images all satisfy (6.1), put P_m=product_(j<m)b_j. The initial vector v_R=|R| satisfies v>=1, so

\[
 |H_5(G_m)|\ge P_m.
\]

The actual image interval has width at most 4(P_m-1). Consequently

\[
 \boxed{P_m\le|H_5(G_m)|\le4P_m-3.}
 \tag{6.2}
\]

This holds even with unbounded, changing generator counts and radices. It requires no existence of an average log radix. Per total generator count N_m, the image and product costs differ by at most log(4)/N_m.

The preceding record blocks have the stronger property that their *ternary* images cover all residues:

\[
\begin{array}{c|c}
A&b\\\hline
\{1,7,8\}&19\\
\{1,4,5,17,21,22\}&97\\
\{1,4,5,17,21,22\}&93\\
\{3,4,7,34,37,41,216,250,253,257\}&1651.
\end{array}
\tag{6.3}
\]

The finite certificate checks each complete residue set. Ternary coverage implies fifth coverage by inclusion. It also composes in the original residue groups: first choose the lower digit for the desired residue modulo b, then choose the next digit for its actual quotient residue, and continue. Hence every changing aggregate of these blocks has at least P_m distinct ternary values.

Every injective residue observation of those ternary values must therefore use modulus at least P_m. Thus faithful ternary re-encoding cannot improve the exponential product cost of *any mixture* of the sources in (6.3). The admissibility length still belongs to the actual block: for k=5 use only the five-admissible entries; for k=6 all four entries are available.

The conclusion also covers any canonical generator block whose modular edge weights arise from one of these by multiplication by a unit and independent sign choices, provided positivity, distinctness, and sum(A)<b hold for its actual chosen lifts. Indeed coefficient complementation on a sign-changed coordinate translates its H_3 residue image by the original twice-weight, and unit multiplication is a residue-group automorphism. Both preserve full coverage and binary modular progression-freeness. The actual lifts and their finite costs remain separate data.

This identifies why the switching example behaves differently. Its A block has the occupied integer ray, but B has only even fifth residues modulo ten and a different parity eigenprofile. Full homogeneous spectral growth by itself does not imply the common-ray condition (6.1). The exact local observation detects the phase difference.

## 7. General target and precise limits of this contribution

The earlier all-block theorem is

\[
 \lambda_k=
 \inf_{A\text{ k-admissible}}|H_5(A)|^{1/|A|}
 =\inf_{(b,A)\in\mathcal M_k}\rho(M_5(A,b))^{1/|A|},
\]

where M_k consists of original canonical modular-safe binary blocks. It is the interface used here; none of the present local-cone arguments assumes a numerical value for that infimum.

The cone theorem gives all linear inequalities valid on every finite symmetric numerical tail, together with an exact positive pattern decomposition or an explicit family of counterexamples. The graph lift gives an original current complex, its receiving kernel, and its full section and metric defects. The switching result solves one infinite arithmetic dictionary exactly, while (6.2) excludes faithful re-encoding improvements over the entire saturated record-block family.

The remaining arithmetic domain is narrower than all symmetric finite sets: it consists of actual H_5 images of positive distinct blocks satisfying binary k-admissibility. The ten periodic extremal tails need not all have such a generator realization. A failed universal-tail inequality is therefore a counterexample to that proposed inequality, not automatically a counterexample to an Erdős lower bound. Conversely, a successful ten-test inequality applies to every admissible tail but need not be optimal on that smaller domain.

No rank cutoff for the global infimum is proved. The large-k gap in the inspected general bounds remains between logarithmic rates of order 1/k and log(k)/k (Korsky, 2026). The present matrices keep the generator reward |A| and every original radix; fixed local dimension does not bound the bit length or rank of the arithmetic inputs.

## 8. Reproducibility and exact checked scopes

Run from the contribution directory:

```sh
python certificates/verify_local_flow.py
python certificates/audit_local_flow.py
```

Both programs use Python's standard library only. The audit imports neither the producer nor its helper library. It derives edge substitutions by evaluating actual finite numerical output windows, rather than using the producer's residue masks. It reconstructs the nine-count identity by exact interpolation on seven original symmetric sets; it checks characteristic polynomials by determinant evaluations rather than the producer's trace recurrence.

The complete finite scopes are:

* all 19 directed simple cycles of the four-position overlap graph, all 10 cone generators and 9 facet ranks, 810 producer integral decompositions, and all 1,089 balanced flows in the auditor's [0,2]^9 domain;
* all 766 symmetric finite supports of span at most 16 in the specified construction, and all 511 nonempty masks on [0,8] through their actual separated reflection doubles;
* all 722 symmetric digit sources containing zero, with q=2,...,6, b=2,...,6, and digit width at most min(8,(q-1)(b-1)); 3,610 direct source joins and all 11,352 complete input-edge paths;
* all 2,187 seven-coordinate rows with coefficients in {-1,0,1}: 990 exact nonnegative certificates and 1,197 actual finite symmetric counterexamples;
* nine selected arithmetic graph lifts, their count and edge matrices, full quotient Grams, and zero-loop section defects;
* all 2,046 two-letter words through length ten, 144 run-formula instances, and the exact attaining period; the auditor also checks 62 direct switched original-generator images through five levels;
* all sixteen direct two-level mixtures of the saturated record blocks and all 256 four-level matrix words, with their complete common-ray and product bounds.

Eight corrupted proof records are deliberately rejected. Normal and optimized Python outputs are compared byte-for-byte. Those checks corroborate the written infinite proofs; they are not presented as enumeration of all blocks or all infinite schedules. All reported runs have finished. No background work is asserted.

## References and source roles

Ziemian, K. (1995). Rotation sets for subshifts of finite type. *Fundamenta Mathematicae, 146*(2), 189–201. DOI: 10.4064/fm-146-2-189-201. The publisher's abstract and bibliographic record were inspected for the established finite-pattern/polytope context. The circulation decomposition, integral coordinate maps, and complete specialized cone proof are given above; no uninspected theorem body is imported.

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1). Inspected HTML source: https://arxiv.org/html/2606.24139v1 . Role: original problem conventions and the benchmark large-k gap, not the source of the current local-flow formulas or switching classification.

Frougny, C., & Pelantová, E. (2018). *Two applications of the spectrum of numbers* (arXiv:1512.04234v3; original preprint 2015). Role: established positional finite-state context; no new general automata-priority claim.

KokunoYumeto. (2026). *Reconstruction with changes of support index* [TeX source]. `workbenches/splitzero-tandem/tex/support_diagrams.tex` in `KokunoYumeto/zeta-function-research-reader`, inspected revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`, source blob `d3493f891291ee6e94dbf2c77649f7d85d240df2`, equations D6–D8. Role: the original internal quotient and additional observation-kernel interface. No analytic theta estimate is imported or claimed proved.

The Clankers. (2026, September 16). *Universal image observations, bounded-fibre resolutions, and spectral capacity* [Predecessor research contribution]. The complete preceding delivery `EP817_SEVEN_OBSERVABLE_20260916.zip` is retained unchanged. The original k=4 construction and signed-block proof remain attributed there to the anonymous/deleted Reddit contributor, and the Lean upper-bound extension separately to sneed-and-feed.
