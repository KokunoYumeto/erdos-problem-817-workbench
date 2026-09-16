# Universal image observations, bounded-fibre resolutions, and spectral capacity

The Clankers. 16 September 2026.

**Evidence status.** This contribution contains ordinary mathematical proofs and exact, explicitly bounded computational replays. It is submitted for independent mathematical review. No new Lean elaboration is claimed. The original anonymous/deleted Reddit contributor retains credit for the workbench's four-term construction and signed-block argument; `sneed-and-feed` retains separate credit for the finite-upper-bound Lean formalization. None of those formal certificates is extended by this note. No general priority claim is made for finite-state positional arithmetic, inclusion-exclusion, augmented simplex contractions, or finite-dimensional spectral theory.

The immediate predecessor is *All-block image capacity and exact ternary transfer*, in `EP817_ALL_BLOCK_IMAGE_20260916.zip`. That complete archive is retained unchanged with this delivery. The current results extend its two-dimensional ternary transfer to every coefficient arity, determine the sharp universal linear count dimension at arity five, and give a dimension-free multiplicative error for each homogeneous block. The resulting spectral variational formula concerns the full family of blocks; its remaining infimum is not evaluated here.

## 1. Original arithmetic objects and principal results

Let A be a finite set of distinct positive integers. Put S(A)=sum(A), n=|A|, and

\[
H_q(A)=\left\{\sum_{a\in A}c_a a:0\le c_a<q\right\},\qquad q\ge2.
\]

The numerical values are counted once. Their original word multiplicities are denoted by mu_(A,q)(y). An admissible generator set for progression length k>=3 is one whose binary image H_2(A) has no nonconstant ordered k-term arithmetic progression. Let g_k(n) be the least possible largest generator, and let lambda_k=lim_n g_k(n)^(1/n). The existence and the finite-image characterization needed here are proved again in Section 10.

For a canonical block (A,b), meaning b>S(A), retain

\[
 A_b^{[m]}=\bigcup_{j=0}^{m-1}b^jA,\qquad
 L_m(D;b)=\left\{\sum_{j<m}b^jd_j:d_j\in D\right\},\qquad D=H_q(A).
\]

All m n generators of A_b^[m] are distinct. Their q-ary image is literally L_m(D;b), including all word collisions. Its maximum possible digit is (q-1)S(A), which may exceed b. The actual digit values are never replaced by their residues.

**Theorem 1 (universal finite observation).** For every fixed q, every canonical block and every changing-block schedule, all distinct-image counts are computed by a nonnegative integer matrix on 2^(q-2) specified translated-image observations. On the actual centrally symmetric images H_q, reflection gives dimension

\[
 d_q=1+\frac12\sum_{d=1}^{q-2}
 \left(2^{d-1}+2^{\lceil(d-1)/2\rceil}\right).
 \tag{1.1}
\]

In particular d_2=1, d_3=2, d_4=4, and d_5=7. This count dimension does not depend on the generator count, radix, number of levels, or forbidden progression length. The raw count-and-moment carrier through moment order p has dimension (p+1)2^(q-2).

**Theorem 2 (sharp fifth-arity linear dimension).** Seven observations suffice and are necessary for a universal linear tail-state count realization, even on the finite subfamily of five-admissible concatenations displayed in Section 4. The lower bound is an actual 7 by 7 numerical-image matrix of determinant 1,228,800. It excludes a smaller universal linear representation of those concatenation counts, not arbitrary nonlinear encodings or restricted subclasses.

**Theorem 3 (uniform block-length control).** Let D be finite, nonempty, contain 0, and lie in [0,(q-1)(b-1)]. Write W=max D and

\[
 C_D=\max\left\{1,\left\lceil\frac{W}{b-1}\right\rceil\right\}\le q-1.
\]

Then rho=lim_m |L_m(D;b)|^(1/m) exists and

\[
 \boxed{\rho^m\le |L_m(D;b)|\le C_D\rho^m\qquad(m\ge0).}
 \tag{1.2}
\]

The rho is the spectral radius of the complete applicable count matrix, rather than an eigenvalue selected after dropping an observation kernel. Its peripheral eigenvalues are semisimple. For q=5, the logarithmic per-generator error is at most log(4)/(mn).

**Theorem 4 (seven-matrix global capacity).** Let M_k be the class of nonempty canonical pairs (b,A) whose actual binary image, reduced modulo b, has no ordered nonzero-step k-AP. Composite moduli and repeated points in a modular progression are included. For every k>=3,

\[
 \boxed{\lambda_k=
 \inf_{(b,A)\in\mathcal M_k}
 \rho(M_5(A,b))^{1/|A|}.}
 \tag{1.3}
\]

Here M_5(A,b) is the specified seven-dimensional matrix, not a new arithmetic source. Its integer entries and the admissible pairs still form an unbounded family. Theorem 4 supplies neither an all-rank lower certificate nor a convergence modulus for this outer infimum.

## 2. Complete translated-image carrier

Fix q>=2. Set C=q-1 and Q=q-2, and define the raw shape set

\[
 \mathcal R_q=\{R\subseteq\{0,\ldots,Q\}:0\in R\}.
\]

For a nonempty finite integer set Y, retain the actual observations

\[
 F_R(Y)=|Y+R|,\qquad R\in\mathcal R_q.
 \tag{2.1}
\]

There are exactly 2^Q of them. They count numerical unions, not sums of word multiplicities.

Take a nonempty D subset [0,C(b-1)] and b>=2. For a specified R, put E_R=D+R as a numerical set. Its largest element is at most Cb-1. For every residue z in [0,b-1] actually present in E_R, define

\[
 Q_{R,z}=\{(e-z)/b:e\in E_R,\ e\equiv z\pmod b\},
 \quad h_{R,z}=\min Q_{R,z},\quad
 R_{R,z}=Q_{R,z}-h_{R,z}.
 \tag{2.2}
\]

The original quotient coordinates belong to [0,Q], and R_(R,z) belongs to R_q. Both the shift h and the entire original quotient set are retained. An absent residue contributes no term. The present singleton quotient {0} is a different object and contributes the shape {0}.

The residue decomposition is the disjoint union

\[
 (D+bY)+R
 =\coprod_z\bigl(z+b h_{R,z}+b(Y+R_{R,z})\bigr).
 \tag{2.3}
\]

For each z the displayed affine map has the exact inverse (x-z-bh)/b on its numerical image. This proves (2.3), not just its cardinality.

Define

\[
 M_q(D,b)_{R,T}=\#\{z:R_{R,z}=T\}.
 \tag{2.4}
\]

The matrix is nonnegative integral, and every row sum is at most b. Equation (2.3) proves

\[
 \boxed{\mathbf F(D+bY)=M_q(D,b)\mathbf F(Y).}
 \tag{2.5}
\]

The initial vector for Y={0} is v_R=|R|. Repetition gives

\[
 |L_m(D;b)|=e_{\{0\}}^{\mathsf T}M_q(D,b)^m v.
 \tag{2.6}
\]

For changing levels (A_j,b_j), the q-ary image has the original form

\[
 D_0+b_0\bigl(D_1+b_1(\cdots+b_{m-2}D_{m-1})\bigr),
 \qquad D_j=H_q(A_j).
\]

Consequently the product is M_0 M_1 ... M_(m-1) v, with the least significant level on the left. The last radix does not alter that finite generator image, but it remains relevant if another level is appended or the word is repeated. No commutation of different matrices is assumed.

### 2.1 Every raw moment closes in the same shapes

For p>=0 put

\[
 F_{R,p}(Y)=\sum_{x\in Y+R}x^p.
\]

Apply the binomial formula to the literal affine maps in (2.3). With a_(R,z)=z+bh_(R,z),

\[
 \boxed{
 F_{R,p}(D+bY)=
 \sum_z\sum_{j=0}^{p}\binom pj
 a_{R,z}^{p-j}b^jF_{R_{R,z},j}(Y).
 }
 \tag{2.7}
\]

The initial moments are sum_(r in R) r^p. Thus all raw moments through order p are computed by a block triangular matrix of size (p+1)2^Q. Its j-th diagonal block is b^jM_q(D,b). Homogeneous generating functions are rational by the finite resolvent formula. Neither their raw moments nor their measures are obtained by declaring reflected tails equivalent; (2.7) uses the unreflected labels and original offsets.

## 3. Exact reflection transport and seven observations

For a shape R define R^vee=max(R)-R. If Y is centrally symmetric, write c_Y=min Y+max Y, so c_Y-Y=Y. The map

\[
 x\longmapsto c_Y+\max R-x
 \tag{3.1}
\]

is an inverse-to-itself affine bijection between Y+R and Y+R^vee. It proves equality of the two cardinalities and records how odd moments would change.

Every H_q(A) is centrally symmetric under the original coefficient-complement involution c_a -> (q-1)-c_a. The symmetry constant is (q-1)S(A). It also preserves every original representation multiplicity by a bijection of words.

Choose the lexicographically smaller shape from each reflection pair. For centrally symmetric D, folding the target shapes in (2.4) produces a nonnegative integer matrix on these representatives. Let E be the raw-coordinate embedding that duplicates the reflected coordinate. Then

\[
 \boxed{M_q^{\rm raw}E=E M_q^{\rm sym}.}
 \tag{3.2}
\]

To see this directly, reflect D+R about c_D+max R. A residue z is sent to the unique residue of c_D+max R-z. Its quotient set is reflected, with its actual minimum shift adjusted by the corresponding integer quotient. The original sets and affine maps in (2.3) are paired bijectively. Folded row coefficients agree. This proves (3.2) without imposing a relation on nonsymmetric tails.

A shape of span d>=1 contains both endpoints and an arbitrary subset of its d-1 interior positions. There are 2^(d-1) such shapes and 2^ceil((d-1)/2) reflection-fixed shapes. Counting reflection orbits, plus the singleton, proves (1.1).

At q=5 the exact ordered basis is

\[
 \boxed{\{0\},\ \{0,1\},\ \{0,2\},\ \{0,1,2\},\
 \{0,3\},\ \{0,1,3\},\ \{0,1,2,3\}.}
 \tag{3.3}
\]

The omitted raw shape {0,2,3} is related to {0,1,3} by (3.1), not by an unrestricted equality of source sets. For Y={0,1,3}, the difference of their union counts is -1. This actual nonsymmetric example is retained as a regression.

## 4. Sharpness of the linear carrier

### 4.1 The raw observation basis is integral and complete

For a shape R put

\[
 C_R(Y)=\#\{t:t+R\subseteq Y\}.
\]

Inclusion-exclusion on the actual translated copies Y+r gives

\[
 F_R(Y)=
 \sum_{\varnothing\ne T\subseteq R}
 (-1)^{|T|+1}C_{\max T-T}(Y).
 \tag{4.1}
\]

Order the shapes by cardinality. The full-subset term is signed reflection of R; every proper-subset term has smaller cardinality. Thus the integer change-of-observation matrix U is unimodular. Reflection permutes its largest-cardinality blocks, with diagonal coefficients +/-1.

Evaluate C_R on the finite set Y=P for every shape P. A pattern of larger cardinality cannot fit into P; patterns of equal cardinality fit exactly when R=P, since both contain zero. The evaluation matrix is unit triangular. It follows that the raw union observations are linearly independent and have a unimodular complete evaluation matrix. This proves sharp dimension 2^Q for this universal translated-union observation space.

On symmetric sets, incidence observations obey C_R=C_(R^vee). The transformation (4.1) commutes with reflection and descends to an invertible rational transformation on reflection orbits. These remaining functions are independent: test them on

\[
 Y_P=P\cup(L-P),\qquad L>3Q.
\]

Since P is contained in [0,Q], the inter-component gap is at least L-2Q>Q. No pattern of width at most Q crosses the gap. Its incidence count is C_R(P)+C_(R^vee)(P). The orbit evaluation matrix is triangular in cardinality, with diagonal one for a two-shape orbit and two for a reflection-fixed shape. Its determinant is nonzero. This proves the generic symmetric dimension d_q.

### 4.2 An integral seven-coordinate source packet

The seven symmetric sets

\[
 \{0\},\ \{0,1\},\ \{0,2\},\ \{0,1,2\},\ \{0,3\},\
 \{0,1,2,3\},\ \{0,1,3,4\}
\]

give the following matrix of observations (3.3):

\[
 E_7=\begin{pmatrix}
1&2&2&3&2&3&4\\
2&3&4&4&4&5&5\\
2&4&3&5&4&5&6\\
3&4&5&5&6&6&6\\
2&4&4&6&3&5&7\\
4&5&6&6&7&7&7\\
4&6&7&7&6&8&8
\end{pmatrix},\qquad \det E_7=-1.
 \tag{4.2}
\]

Thus the seven-coordinate observation has full integral image on this specified packet. Adding Y_8={0,2,3,5} produces the original nonzero free-object relation

\[
 e_{Y_8}+e_{\{0,1\}}-e_{\{0,2\}}-e_{\{0,1,3,4\}}.
 \tag{4.3}
\]

Its seven observations vanish. The eight-object source has rank eight; its observation quotient has rank seven and kernel rank one. This additional kernel is not confused with the original generator-word relations.

### 4.3 Seven states are necessary even for actual admissible concatenations

The sharper linear-realization lower bound uses only actual fifth-arity images of nonempty five-admissible sets. Take tail blocks, in this order,

\[
 (4),\ (1),\ (2),\ (3),\ (1,2),\ (1,6),\ (2,9).
 \tag{4.4}
\]

Their binary images have at most four values, hence are five-admissible. Their seven-observation matrix E_A has determinant -10,240.

Take the prefix pairs

\[
 ((1),3),\ ((1),4),\ ((2),3),\ ((3),4),\
 ((1,2),5),\ ((1,3),5),\ ((1,6),8).
 \tag{4.5}
\]

Every binary image in (4.5) is modular-five-free, with every nonzero step tested, including steps of small additive order. The rows of the actual count carrier that observe the final cardinality are

\[
 P=\begin{pmatrix}
1&2&0&0&0&0&0\\
3&1&0&0&0&0&0\\
1&0&2&0&0&0&0\\
3&0&0&0&1&0&0\\
0&2&0&3&0&0&0\\
0&0&0&3&0&0&2\\
0&2&0&1&0&2&3
\end{pmatrix},\qquad \det P=-120.
\]

For a prefix (A_i,b_i) and a tail C_j, the actual combined generator set is A_i union b_i C_j. Its generators are distinct because b_i>S(A_i). Reduction modulo b_i forces the lowest binary digits of any five-term progression to be constant; after subtraction and division, the tail admissibility forces the progression to be constant. Thus every one of the 49 concatenations is five-admissible.

Their numerical count matrix is

\[
 H_{ij}=|H_5(A_i\cup b_iC_j)|=P E_A^{\mathsf T},
 \qquad \boxed{\det H=1,228,800\ne0.}
 \tag{4.6}
\]

Any representation of these counts by a d-dimensional tail vector and a prefix-dependent linear functional factors H through dimension d. Hence d>=7. The result applies a fortiori to a universal linear transfer realization on all five-admissible concatenations, and also to the higher-k classes containing them. No minimality claim is made for every specialized k=3 or k=4 subfamily or for nonlinear encodings.

## 5. A bounded-fibre resolution at every original radix cut

Let X,Y be finite nonempty integer sets, with X contained in [0,C(P-1)] and P>=2. The original map is

\[
 \pi:X\times Y\to X+PY,\qquad (x,y)\mapsto x+Py.
 \tag{5.1}
\]

If two pairs have the same value, their X coordinates differ by an integer multiple of P. The displayed interval admits at most C values in one residue. Therefore every fibre I_z=pi^(-1)(z) satisfies

\[
 1\le |I_z|\le C.
 \tag{5.2}
\]

For canonical q-ary mixed-radix prefixes, C=q-1 always applies. Indeed max X is at most (q-1)sum_j P_j(b_j-1)=(q-1)(P-1). Thus

\[
 \boxed{\frac{|X||Y|}{q-1}\le|X+PY|\le|X||Y|.}
 \tag{5.3}
\]

For a homogeneous D with width W and a cut after m digits, the sharper bound C_D in Theorem 3 follows from

\[
 \max L_m=\frac{W(b^m-1)}{b-1}.
\]

The number of points in any residue modulo b^m is at most 1+floor((W/(b-1))(1-b^(-m))), which is at most ceil(W/(b-1)) when W>0. W=0 has singleton fibres. The q-1 bound is sharp in the unrestricted count theorem: at q=5, take the low generators {1,2,4}, cut P=8, and tail generators {1}; the value 24 has the four distinct local-value pairs (0,3),(8,2),(16,1),(24,0). That example is not used as a claim of five-admissibility.

### 5.1 The complete integral resolution, not just its rank

For each numerical fibre I_z, retain every nonempty subset J of its original pair labels. Let C_j have basis (z,J) with |J|=j+1, for j>=0; let C_(-1)=Z[X+PY]. The augmentation sends every pair over z to e_z. The other differentials delete one ordered vertex with alternating signs. Thus C_j=0 for j>=C, and

\[
 \cdots\to C_2\to C_1\to C_0\to C_{-1}\to0
 \tag{5.4}
\]

is the direct sum of the actual augmented simplex complexes of the fibres.

Choose the least original pair v_z in each fibre, and let h insert it into a face, with its ordering sign; h kills a face already containing v_z. At degree -1 put h(e_z)=e_(z,{v_z}). Cancellation of the alternating faces proves on each basis vector

\[
 \boxed{\partial h+h\partial=I,\qquad\partial^2=0.}
 \tag{5.5}
\]

All coefficients are integral. This proves exactness and retains the higher relations between pairwise collision relations. At arity five, fibres can have four vertices, so terms through C_3 can be necessary. Keeping only pair differences without their face relations is not the full complex.

With unit face bases and the prescribed coefficient Hilbert norm, each h_j is a signed partial isometry and has norm at most one. For j>=0, each differential column has at most j+1 entries, each row at most C-j entries; the matrix row/column estimate gives

\[
 \|\partial_j\|\le\sqrt{(j+1)(C-j)}.
 \tag{5.6}
\]

For augmentation this reads sqrt(C). These bounds persist for countably many fibres and any coefficient Hilbert space: extend from finite supports by continuity. Equation (5.5) remains valid on the Hilbert direct sums, so the completed complex is still contracted. Its constants depend on the coefficient arity, not the number of values, source rank, or radix horizon.

For support inclusions the face and value maps are natural. The chosen least-vertex section need not be natural. Its exact difference on a retained value is

\[
 e_{v_{\rm new}}-e_{v_{\rm old}}
 =\partial[v_{\rm old},v_{\rm new}],
 \tag{5.7}
\]

with the orientation sign retained. This is an original boundary, not a declared absent action.

### 5.2 Original representation masses and quotient metrics

Give a pair (x,y) its specified positive original mass w(x,y), with source Gram 1/w(x,y). For actual generator images the mass is mu_left(x)mu_right(y). On a numerical fibre set W_z=sum_(I_z)w. Its least-norm section is

\[
 s(e_z)=\sum_{(x,y)\in I_z}\frac{w(x,y)}{W_z}e_{(x,y)},
 \quad\pi s=I,\quad G_{\rm quotient}(z)=1/W_z.
 \tag{5.8}
\]

Pairing with every difference of two vertices gives zero, and expansion proves the full Pythagorean quotient identity. These actual masses can be much larger than C. In the separately specified unit distinct-pair metric, W_z=|I_z|<=C and the return to unit numerical-value mass has norm at most sqrt(C). Equation (5.8), rather than that unit-pair bound, governs the original word metric. The unit-face contraction estimate (5.6) is not silently asserted in a different weighted face metric.

For an explicit unbounded return cost, take the original generators {1,3,...,3^(m-1)} and q=5. There are 5^m original coefficient words and exactly 2*3^m-1 numerical values. Thus the largest original mass satisfies

\[
 \mu_{\max}\ge\frac{5^m}{2\cdot3^m-1},\qquad
 \|\mathrm{id}:(G_{\rm quotient})\to(I_{\rm values})\|
 =\sqrt{\mu_{\max}}
 \ge\sqrt{\frac{5^m}{2\cdot3^m-1}}.
 \tag{5.9}
\]

The finite images are intervals by their actual base-three recursion. The numerical bound follows from averaging the original masses. It grows exponentially even though each distinct-value cut has at most two representatives and its unit-face resolution has the uniform contraction. The source measures, not a failed inverse identity, explain this difference.

## 6. Uniform spectral estimates for the whole homogeneous source

Let N_m=|L_m(D;b)|. The actual concatenation map in Section 5 gives

\[
 N_mN_n/C_D\le N_{m+n}\le N_mN_n.
 \tag{6.1}
\]

Subadditivity of log N_m proves existence of rho=inf_m N_m^(1/m). For a direct proof, fix m and write a large index as tm+r. The upper inequality controls log N_(tm+r)/(tm+r) by log N_m/m and finitely many remainder terms. The lower defining infimum gives the opposite bound. Repeating the lower inequality in (6.1) and taking t-th roots also gives rho^m>=N_m/C_D. Consequently

\[
 \boxed{\rho^m\le N_m\le C_D\rho^m.}
\]

This is Theorem 3. In particular

\[
 \left(\frac{N_m}{C_D}\right)^{1/(mn)}
 \le\rho^{1/n}\le N_m^{1/(mn)},\qquad
 0\le\frac{\log N_m}{mn}-\frac{\log\rho}{n}
 \le\frac{\log C_D}{mn}.
 \tag{6.2}
\]

No diagonalization or condition number is needed to evaluate these endpoints. Matrix powering uses fixed dimension at fixed arity; integer bit lengths still depend on the actual input and m. The error estimate is not a bound on that input size or on the rank at which the outer extremal infimum is approached.

### 6.1 Every matrix spectral component is actually observed

On the count-coordinate space define the explicit auxiliary norm

\[
 \|x\|_v=\max_R\frac{|x_R|}{|R|},\qquad v_R=|R|.
\]

This is a norm on observation coordinates, not the original word or quotient metric. For a nonnegative matrix P its induced norm is max_R(Pv)_R/v_R. For every original word product of our carriers,

\[
 (Pv)_R=|L+R|\le |R||L|,
\]

and the singleton coordinate gives equality. Hence

\[
 \boxed{\|P\|_v=|L|.}
 \tag{6.3}
\]

In particular, the spectral radius of M is exactly rho. This follows either from the finite-dimensional spectral-radius formula for matrix powers or from the elementary Jordan decomposition and (6.3). Thus one does not accidentally use an unobserved spectral radius of a larger automaton.

Equation (6.2) bounds ||M^m||_v/rho^m by C_D. A Jordan block of length greater than one on an eigenvalue of modulus rho would make this ratio grow polynomially. Therefore every peripheral eigenvalue is semisimple. Interior Jordan blocks remain possible and are retained in Section 8. Every fifth-arity rho is an algebraic integer of degree at most seven; sharpness of the state dimension does not assert sharp algebraic degree for a single block.

### 6.2 Moment and variance growth retain the physical scale

Suppose W=max D>0. For p>=1 the moment at m levels has the bounds

\[
 W^p(\rho b^p)^{m-1}
 \le\sum_{x\in L_m}x^p
 \le C_D\left(\frac{W}{b-1}\right)^p(\rho b^p)^m.
 \tag{6.4}
\]

The lower bound uses the actual subset W b^(m-1)+L_(m-1); the upper uses max L_m<W b^m/(b-1). Thus its exponential growth is rho b^p.

For m>=2, use the low cylinder with the top two digits zero and the high cylinder with both top digits W. Each contains N_(m-2) values. Every high value exceeds every low value by at least

\[
 \frac{W}{b-1}(1-2/b^2)b^m.
\]

The variance identity for a uniform finite numerical set is the sum of squared unordered pair differences divided by its cardinality squared. These two cylinders and (6.2) give

\[
 \boxed{
 \frac{W^2(1-2/b^2)^2}{(b-1)^2C_D^2\rho^4}\,b^{2m}
 \le\operatorname{Var}(\mathrm{Unif}(L_m))
 \le\frac{W^2}{4(b-1)^2}\,b^{2m}.}
 \tag{6.5}
\]

The upper bound follows from the interval support; its exact finite width W(b^m-1)/(b-1) can be substituted. The constants in (6.5) retain W and rho. These uniform distinct-value statements do not replace original assignment-weighted moments.

### 6.3 Arbitrary schedules still need a limit hypothesis or a limiting inferior

Uniform cut control does not force every changing schedule to have a limiting rate. At stage j use j! successive copies of A={1}, with base 3 for odd j and base 5 for even j. Both actual binary digit sets are modular-three-free. Therefore every finite prefix is three-admissible.

For arity five every image is the interval

\[
 [0,4\sum_{i<m}P_i],\qquad N_m=1+4\sum_{i<m}P_i.
\]

The interval assertion follows by induction: the lower interval reaches at least P_j-1 because each previous radix is at most 5, so the next translates overlap or adjoin. Also sum P_i is bounded above and below by fixed multiples of P_m, since the radices lie in {3,5}. Thus log N_m-log P_m stays bounded.

At the end of stage j the last j! positions dominate all preceding stages, whose total divided by j! tends to zero. The average log radix therefore approaches log 3 along odd stage endpoints and log 5 along even endpoints. Every intermediate average lies between them. Hence

\[
 \boxed{\liminf N_m^{1/m}=3,\qquad\limsup N_m^{1/m}=5.}
 \tag{6.6}
\]

The growing generators and scale product are exactly the original ones. The six finite stage endpoints in the receipt corroborate the explicit formula; the argument proves the infinite oscillation.

## 7. The full spectral variational formula

Let M_k be the canonical modular-safe pairs specified in Theorem 4. For each pair, its binary digit language is admissible at all lengths: reduce a progression modulo b, identify its common lowest actual binary digit, subtract it, divide by b, and induct. The digit values lie below b, so that lookup is the actual canonical inverse. Composite b causes no difficulty because the finite certificate tests every nonzero modular step.

Every prefix A_b^[m] is therefore k-admissible. The all-block fifth-image theorem in Section 10 gives

\[
 \lambda_k\le |H_5(A_b^{[m]})|^{1/(m|A|)}.
\]

Taking m to infinity and using Section 6 proves

\[
 \lambda_k\le\rho(M_5(A,b))^{1/|A|}.
\tag{7.1}
\]

Conversely, for any finite k-admissible A choose b=4S(A)+1. Its actual binary image is modular-safe because all integer second differences have absolute value at most 2S(A)<b. The fifth-arity digits are below b, so all digit words are distinct and

\[
 |H_5(A_b^{[m]})|=|H_5(A)|^m.
\]

Thus rho=|H_5(A)|, and the all-block infimum gives the reverse inequality in (1.3). This proves Theorem 4. Enlarging the class to all canonical pairs whose binary languages are safe by the full carry criterion gives the same infimum, by the same two inclusions.

At k=3 this spectral infimum is attained by A={1}, b=3, with

\[
 |H_5(A_b^{[m]})|=2\cdot3^m-1,\qquad\rho=3=\lambda_3.
\]

In contrast, no finite nonempty three-admissible A attains |H_5(A)|^(1/|A|)=3: its ternary assignments are distinct, so |H_3(A)|=3^n, and its fifth-arity set includes a strictly larger value. The two conclusions concern different explicitly connected infima, with the word-length limit retained in the spectral one. The standard three-term injectivity statement is proved in the cited primary literature and can also be recovered by expressing a short relation as a binary second difference and using positivity to handle an initially constant numerical tuple.

## 8. Exact examples and retained interior spectral data

All following matrices use (3.3). Their count series are checked by their exact characteristic identities and sufficient initial coefficients, with original generator images independently recomputed.

### 8.1 A genuinely quartic observed rate

For A={3,10}, b=19, the binary residue set has four elements. Since 19 is prime, a nonzero modular step has order 19, so it cannot produce a five-term progression entirely inside those four residues. The original construction is five-admissible at every length.

The fifth-arity matrix is

\[
 \begin{pmatrix}
9&8&0&0&0&0&0\\
2&9&2&6&0&0&0\\
2&6&1&10&0&0&0\\
0&2&0&17&0&0&0\\
6&12&0&0&0&0&0\\
1&7&1&10&0&0&0\\
0&1&0&18&0&0&0
\end{pmatrix}.
\]

Its characteristic polynomial is x^3 f(x), where

\[
 f(x)=x^4-36x^3+382x^2-1116x+65.
\]

There is one root in each interval (0,1),(4,5),(12,13),(18,19), as verified by the endpoint signs; degree four gives exactly those four real roots. The largest is rho. Modulo three, f becomes x^4+x^2+2. It has no linear root and is divisible by none of the three monic irreducible quadratics x^2+1, x^2+x+2, x^2+2x+2. Therefore f is irreducible over Q. The observed rate is genuinely quartic.

Its complete count series is

\[
 \boxed{\sum_{m\ge0}N_mz^m
 =\frac{1-11z+43z^2+87z^3}
 {1-36z+382z^2-1116z^3+65z^4}.}
 \tag{8.1}
\]

Here C_D=3. Theorem 3 gives rho^m<=N_m<=3rho^m with 18<rho<19. This example shows a real strict spectral improvement on its own radix cost, but it is not a competitive global k=5 record.

### 8.2 A surviving interior Jordan chain

For A={7,10}, b=19, again every binary level is modular-five-free. The seven-dimensional matrix has characteristic polynomial

\[
 (x-19)(x-13)^2(x-5)(x-2)(x-1)(x+3).
\]

In the original coordinates set

\[
 v=(2,0,0,0,1,0,0)^{\mathsf T},\quad
 w=(-227,198,132,0,0,120,0)^{\mathsf T}.
\]

Then

\[
 (M-13I)v=0,\qquad (M-13I)w=462v.
\]

The observed count series is

\[
 \boxed{\sum_{m\ge0}N_mz^m
 =\frac{1-25z+243z^2-795z^3}
 {(1-5z)(1-13z)^2(1-19z)}.}
 \tag{8.2}
\]

The numerator is nonzero at z=1/13, so the double pole and its m13^m contribution survive. This does not contradict peripheral semisimplicity: 13<rho=19, and N_m remains between 19^m and 4\,19^m.

For comparison, A={6,9}, b=17 has characteristic polynomial (x-17)^3(x-3)^3(x+1), while the squarefree polynomial (x-17)(x-3)(x+1) annihilates the actual matrix. Its repeated top eigenvalue is semisimple, and

\[
 N_m=(8\,17^m-3^m)/7.
\]

The original common factor three in the generators is not divided out.

### 8.3 The existing record sources

For B_6={1,4,5,17,21,22}, its fifth-arity image is the interval [0,280]. Its matrices at bases 97 and 93 have rho_3=rho_5 equal to the respective radix. For B_10={3,4,7,34,37,41,216,250,253,257}, at base 1651 the ternary and fifth-arity spectral radii are both 1651. The same equality is checked for the original block {1,7,8} at base 19.

The full-base root is certified by the two exact facts det(bI-M)=0 and every row sum<=b. The latter bounds the spectral radius above; the former supplies the eigenvalue. Both arity matrices are constructed from the actual numerical images. These particular formulas were available in the preceding packages; they are regression inputs and applications of the new uniform framework, not relabelled new record constructions.

## 9. Faithful re-encoding: exact scope and a fixed-block barrier

For a canonical block (A,b), let C_m=A_b^[m]. Let r_m be the least integer modulus >=2 on which the actual numerical image H_3(C_m) reduces injectively; let p_m be the least prime with that property. Both exist. Write rho_3 and rho_5 for the two actual image spectral radii and L_b=ceil(log_2 b). Section 10's elementary prime estimate gives

\[
 \boxed{
 \rho_3^m\le |H_3(C_m)|\le r_m\le p_m
 \le256+2\bigl(|H_5(C_m)|-1\bigr)(mL_b+2)
 \le256+8\rho_5^m(mL_b+2).
 }
 \tag{9.1}
\]

The height bound uses S(C_m)<=b^m-1, hence 1+floor(log_2(2S(C_m)))<=mL_b+2. No generator is changed to a least residue.

Faithfulness on H_3 preserves the binary second-difference equations. If C_m is k-admissible, its binary residues are modular-k-free. Each actual generator is nonzero modulo the modulus, so the repeated scaled families are distinct even when the actual generator exceeds the modulus: a cross-level equality would make one of the original generators zero modulo it. Lookup of the unique actual binary digit of a residue, subtraction of that digit, and division give the inverse at every level.

When rho_3=rho_5=rho, (9.1) proves

\[
 \boxed{\lim_m r_m^{1/m}=\lim_m p_m^{1/m}=\rho.}
 \tag{9.2}
\]

Every faithful modulus sequence has lower per-generator exponential rate at least rho^(1/|A|), and prime choices attain it asymptotically. For all four record pairs in Section 8.3, rho=b. Therefore faithful H_3 residue re-encodings of their full repeated blocks cannot improve their existing exponential rates. This conclusion covers every such modulus and every horizon, not just a searched prime range.

The class is deliberately stated. It maps into the larger class of modular-k-free binary observations by the second-difference argument. The inclusion can be strict: B_6 has 139 distinct ternary values, more than 97, although its binary image is modular-five-free at 97. Thus (9.2) is not a lower bound against every possible observation or a different block family.

For a strict spectral example, take A={1,9}, b=27. The ternary and fifth-arity radii are respectively 9 and 17. The actual fifth-arity matrix satisfies M^2=17M, and

\[
 |H_5(C_m)|=25\,17^{m-1}\qquad(m\ge1).
\]

Faithful prime choices at m=1,2,3 are respectively 13,151,1091. The unchanged generator lists, every preceding rejected prime with a nonzero original bounded-difference witness, and the exact digit inverses are in the receipt. These re-encodings preserve three-term exclusion; their asymptotic upper cost is at most sqrt(17), strictly below the original sqrt(27). The known global three-term rate is 3, so this is a checked mechanism rather than a new numerical record.

## 10. The inherited capacity identity, proved with its height cost

This section supplies the finite-image interface used in Theorem 4. It also specifies precisely what is imported from the immediately preceding note.

### 10.1 Existence of the maximum-generator rate

For admissible A,B set R=2S(A)+1 and C=A union RB. The map

\[
 H_2(A)\times H_2(B)\to H_2(C),\quad(x,y)\mapsto x+Ry
\]

is a bijection with the original division inverse. A progression pulls back to progressions in both factors: each lowest second difference is a multiple of R in [-2S(A),2S(A)] and hence zero. A nonconstant target progression has a nonconstant factor. The original sum cost obeys

\[
 2S(C)+1=(2S(A)+1)(2S(B)+1).
\]

Minimizing that cost on n generators gives a submultiplicative sequence F_k(n). Splitting a large n into blocks of a fixed length proves that its nth-root limit is inf_n F_k(n)^(1/n). The exact inequalities

\[
 2g_k(n)+1\le F_k(n)\le2n g_k(n)+1
\]

give the same limit for g_k. Powers of three supply admissible sets at every n. Thus

\[
 \lambda_k=\inf_{A\ k\text{-admissible}}(2S(A)+1)^{1/|A|}.
 \tag{10.1}
\]

### 10.2 Elementary prime avoidance

Let h>=1 and A be a fixed positive generator set. The nonzero bounded differences in sum_a[-h,h]a occur in opposite pairs. Let K be their number of positive values and put ell=1+floor(log_2(hS(A))). Then there exists a prime

\[
 p\le256+4K\ell
 \tag{10.2}
\]

dividing none of those positive differences.

Here is a complete prime-product bound. For integer N>=256 put m=floor(N/2). The central binomial coefficient binom(2m,m) divides lcm(1,...,N): at each prime, each term in its factorial valuation difference is zero or one, and there are at most floor(log_p N) such terms. Also binom(2m,m)>=2^(2m)/(2m+1). Higher prime powers contribute at most sqrt(N)log N to the logarithm of the least common multiple. Consequently, with theta(N)=sum_(p<=N)log p,

\[
 \theta(N)\ge (N-1)\log2-\log(N+1)-\sqrt N\log N>N/4.
\]

For the last bound, use 2/3<log2<3/4, monotonic decrease of log(N+1)/N and log N/sqrt N in this range, and log257<log512=9log2. The resulting lower coefficient is 85/128-27/1024-3/8=269/1024>1/4. The elementary inequalities for log2 follow, for example, by convexity and the chord bound for 1/x on [1,2].

The product Q of the K positive bounded differences has log Q<=Klog(hS(A))<K ell. If every prime up to 256+4K ell divided Q, the lower bound just proved would give log Q>64+K ell. This contradiction proves (10.2).

For h=2, the positive difference count is K=(|H_5(A)|-1)/2. The successful prime makes reduction injective on the distinct values of H_3(A). Every modular binary k-AP then has equal adjacent ternary values x_i+x_(i+2) and 2x_(i+1); injectivity converts their equations to integer equations. Original admissibility makes the tuple constant. The actual binary digit lift is safe at every length by the lookup/subtract/divide map, even if original weights exceed p.

### 10.3 Amplification keeps and then removes the exponential height contribution

Fix admissible A with n generators and put h_5=|H_5(A)|, R=4S(A)+1. The original block

\[
 B_t=\bigcup_{j<t}R^jA
\]

has tn distinct generators, sum (R^t-1)/4, is k-admissible, and has exactly h_5^t fifth-arity values. The prime lemma gives

\[
 p_t\le256+2(h_5^t-1)t\ell_R,
 \quad\ell_R=1+\lfloor\log_2R\rfloor.
\]

Its unchanged-weight prime lift proves lambda_k<=p_t^(1/(tn)). Therefore

\[
 \lambda_k\le h_5^{1/n}
 \left(2t\ell_R+256h_5^{-t}\right)^{1/(tn)}.
\]

The final factor tends to one for that specified A. Taking the infimum proves lambda_k<=inf_A |H_5(A)|^(1/|A|).

For the reverse inequality, minimizing |H_5| at rank n gives a submultiplicative sequence under sufficiently separated composition, hence its root limit equals the infimum over all ranks. On a max-optimal admissible set, |H_5(A)|<=4n g_k(n)+1. The root limit is therefore at most lambda_k. This proves

\[
 \boxed{\lambda_k=\inf_{A\ k\text{-admissible}}|H_5(A)|^{1/|A|}.}
\]

The finite construction retains its large prefactor R^(t-1)max A. No height-independent finite modulus bound is asserted for one unamplified block. Neither this proof nor the seven-state reformulation establishes equality with arity three or four in general.

## 11. Observation quotients and the SplitZero receiving interface

The seven counts are not a linear map on individual generator-word amplitudes: union cardinality is nonlinear on such a presentation. The correct linear source for the count observation is the free module on the specified finite numerical-set objects.

For a finite packet P of centrally symmetric nonempty integer sets, let V_P=Z[P] and

\[
 J_Pe_Y=(|Y+R|)_{R\in\mathcal R_q/\vee}.
\]

Its quotient is the actual image lattice J_P(V_P), not automatically all of Z^(d_q). Formula (4.2) supplies a particular packet where it is all of Z^7. Formula (4.3) supplies a nonzero original source element in an additional packet's kernel.

A block acts on the set-object basis by e_Y -> e_(D+bY). Its exact observation square is

\[
 J_{\mathcal T(P)}\,\mathcal T_{D,b}=M_q^{\rm sym}(D,b)J_P.
\]

Thus observation kernels are transported to observation kernels. Packet inclusions give the original natural diagrams and their internal quotients. In the SplitZero reconstruction, a relation maps to its own packet-labelled zero; the empty support remains the external bottom. The source interface is the one in `support_diagrams.tex`, (D6)--(D8), at the pinned revision in the references.

The simplex resolution of Section 5 is a different, explicitly related presentation: it resolves actual pair-to-value fibres, and (5.8) retains their original masses. The set-object observation is not asserted to identify those entire value modules with seven coordinates. Its additional kernel must remain in any comparison. The change from union observations to incidence observations in (4.1) is unimodular; it preserves the observation kernel, with the transported Gram U^(-T)G U^(-1) if a metric was specified. It is not an isometry by declaration.

The contribution therefore transfers exact support quotients, original boundary primitives, a uniform bounded-fibre contraction, and explicit observation dynamics. It does not claim a finite replacement for the original infinite theta quotient or a Zeta arithmetic weight estimate.

## 12. Verification and remaining general question

The dependency-free producer and the independently implemented auditor accompany this note. The latter imports neither the producer nor its carrier library. It reconstructs raw matrices by interpolation on literal finite numerical joins, whereas the producer constructs them from exact residue fibres. It recomputes selected original large-generator moments by bytewise bit-image arithmetic, uses Gaussian rational elimination instead of the producer's fraction-free determinants, and contracts each simplex to the last rather than the first vertex.

The exact completed domains are recorded in the receipts:

- every D subset [0,(q-1)(b-1)] containing zero, for q=2,...,5 and b=2,3,4: 5,050 alphabets, 15,150 literal joins, 45,450 raw moment-vector checks, and 384 symmetric-source intertwining checks;
- all nonempty positive subsets of [1,8] of size at most three, arities two through six, and distinct radices S+1,S+2,2S+1: 1,375 original two-level generator comparisons;
- 140 specified changing schedules through four levels, with 210 macro-cut inequalities and exact observation-norm comparisons;
- raw and symmetric dimension witnesses through arity seven, the complete seven-coordinate integral packet, all 49 actual five-admissible Hankel concatenations, and the additional observation-kernel example;
- all augmented-simplex basis identities for fibre sizes one through six: 126 identities, plus 2,828 actual numerical cut fibres and their original weighted sections;
- 18 specified original block/arity matrices, 36 direct one-/two-level images, 108 first and second moment entries including counts, exact characteristic identities, and count vectors through length ten;
- three unchanged-weight prime re-encodings with every preceding rejected prime, six factorial-schedule stage endpoints, eight original-word metric-return examples, and the stated invalid-input and nonsymmetric-observation regressions.

The independent auditor reproduces all 5,050 raw matrices by its alternative construction and checks each on an additional tail; it also replays the complete 1,375-generator domain, the 18 selected cases, the prime data, the integral minimality and Hankel certificates, and the 2,828 cut-fibre counts. Eight deliberately corrupted records are rejected. Its full independent scope is stated in its receipt; it does not claim an independent replay of every one of the producer's 45,450 general raw-moment comparisons.

The ordinary theorems quantify over every finite block and every stated infinite homogeneous length. The finite tests certify their concrete inputs and check the formulas on the displayed domains; they are not substituted for the proofs.

What remains is an inequality over all admissible arithmetic blocks, or a construction violating a proposed one. The rank does not enter the size of the fifth-arity count carrier or its uniform length error, but it remains in the generator reward and in the allowed integer entries. There is no proved cutoff on the rank needed to approach the global infimum. The faithful-compression barrier in Section 9 also concerns its precisely specified class, not all possible modular observations. No new best numerical bound or complete solution of Erdős Problem 817 is asserted.

## References and exact source roles

The Clankers. (2026, September 16). *All-block image capacity and exact ternary transfer* [Preceding research note]. `EP817_ALL_BLOCK_IMAGE_20260916.zip`, `research/all_block_image/notes/all-block-image-capacity.md`. Role: immediate predecessor and provenance for the finite-image capacity/prime interface, re-proved in Section 10; its archive is retained unchanged.

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1) [Preprint]. https://arxiv.org/html/2606.24139v1 . Inspected: definitions, three-term injectivity, and general exponential benchmarks. Role: surrounding problem and prior three-term result; its June version is not used as a September status report about the separate historical prefactor question.

Frougny, C., & Pelantová, E. (2018). *Two applications of the spectrum of numbers* (arXiv:1512.04234v3; original preprint 2015) [Preprint]. https://arxiv.org/abs/1512.04234 . Source entry inspected for classical finite-state positional-arithmetic context; no uninspected theorem is an input to the carrier or sharpness proofs above.

Green, B., & Ruzsa, I. Z. (2006). Sets with small sumset and rectification. *Bulletin of the London Mathematical Society, 38*(1), 43–52. https://arxiv.org/abs/math/0403338 . Source entry inspected for classical finite-additive-model context. The prime lemma here is the explicit elementary proof in Section 10 and retains every original generator.

KokunoYumeto. (2026). *Reconstruction with changes of support index* [TeX source]. `KokunoYumeto/zeta-function-research-reader`, revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`, `workbenches/splitzero-tandem/tex/support_diagrams.tex`, equations D6–D8; Git blob `d3493f891291ee6e94dbf2c77649f7d85d240df2`. Role: original support reconstruction, internal quotient, and additional receiving-kernel distinction. It supplies no unstated analytic or arithmetic estimate to this contribution.
