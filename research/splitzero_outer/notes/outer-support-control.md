# Support-preserving outer control for Erdős Problem 817

Research contribution, 14 September 2026. Ordinary proofs and exact finite proof certificates; independent mathematical review remains appropriate. No new Lean elaboration is claimed.

## 1. Scope, sources, and mathematical outcome

For a finite set of distinct positive integers A, retain

\[
H(A)=\left\{\sum_{a\in U}a:U\subseteq A\right\},\qquad S(A)=\sum_{a\in A}a.
\]

Zero is included as the value of the actual empty subset. A nonconstant ordered k-term arithmetic progression has the form (x,x+d,...,x+(k-1)d), with an integer d different from zero. For k at least three,

\[
g_k(n)=\min\{\max A:|A|=n,\ H(A)\text{ contains no such progression}\}.
\]

The connected Zeta workbench was inspected at commit `42df8a2de002d5fc7090641fac46ea11be05fa71`. The interfaces used here are its support-index reconstruction and internal quotient, together with its original-source Gram and section-correction formulas. In particular, a zero at an admitted support retains that support, and every change of observation or metric has an explicit comparison map. The Zeta arithmetic determinant estimates themselves are not hypotheses in any result below.

A separate existing Erdős 817 branch was found at commit `98fd25802a387138053064e11ddd2f6d2007d55b`, path `research/splitzero_transfer/`. That branch already proves uniform mixed-radix relation inverses, arithmetic graph completion, and finite-controller optimization for a fixed generator block. Its results and attribution are retained as predecessor work. The contribution here controls the additional variation of the block and its integer parameters, and evaluates the resulting optimization through five generators per level.

For a fixed block A of size n and an infinite sequence of radices b_j>S(A), define P_0=1 and P_{j+1}=b_jP_j. Its m-level generator set is the literal set

\[
A_{\mathbf b,m}=\bigcup_{j<m}P_jA.
\]

It has exactly mn generators. A schedule is admissible when every finite prefix has k-AP-free subset sums. Define

\[
\gamma_k(A)=\inf_{\text{admissible schedules}}
\liminf_{m\to\infty}\left(\prod_{j<m}b_j\right)^{1/(mn)},
\qquad
\Gamma_{k,n}=\inf_{|A|=n}\gamma_k(A).
\tag{1.1}
\]

An empty infimum is infinity. The expression uses the original radix product. Its relation to the largest generator at the next level is exact:

\[
\max A_{\mathbf b,m+1}=P_m\max A.
\tag{1.2}
\]

Taking the indicated roots gives the same limiting inferior, including when it is infinite.

The main outcomes are the following.

**Theorem O1 (complete bounded realization).** Fix n positive and ell positive. Every canonical integer tuple (a_1,...,a_n,b_1,...,b_ell), with a_1<...<a_n and sum a_i<min b_j, has another tuple in precisely the same affine sign cell, coordinatewise no larger, with every coordinate at most

\[
\boxed{3\,2^{n+\ell-1}(n+\ell)!.}
\tag{1.3}
\]

The sign cell records all labels (j,u,v,c) with u in {-2,-1,0,1,2}^n and v,c in {-1,0,1}, including every zero value of u.a-vb_j+c. The two tuples have exactly corresponding binary representation fibers and complete labeled carry relations. Their arbitrary finite mixed-radix languages are order-preserving Freiman-2 isomorphic. The original tuple is recoverable from the bounded tuple and a retained finite list of nonnegative integer directions and coefficients.

**Theorem O2 (finite global fixed-rank optimization).** For every k>=3 and n>=1, Gamma_{k,n} is attained and is an exactly computable algebraic number. Set

\[
V_k=2^{3^{k-2}-1}.
\]

A universal finite search suffices: all n-element positive blocks with S(A)<3^n, all radices S(A)+1 through 2S(A)+2, and periods of length at most V_k. The actual arithmetic upper bound 3^n may be replaced by any independently certified constant-radix benchmark Q of size n. This gives S(A)<Q and radices at most 2Q. The smaller optimization cutoff follows from the objective and is separate from the all-pattern realization bound (1.3).

**Theorem O3 (exact viability by original return primitives).** For every fixed canonical digit image, an explicitly constructed finite set of returning carries identifies precisely which reachable controller states have infinite admissible extensions. A returning carry has an actual next-column primitive producing a progression for every next radix. Every remaining controller state is returned to the initial state by the explicit tail radix 2S(A)+2. The viable controller has at most 2 to the power of the number of nonreturning carries vertices.

**Theorem O4 (evaluated global capacities).** The values below optimize over every distinct positive block of the stated size and every infinite canonical mixed-radix schedule with that same block at each level:

| generators per level n | Gamma_{5,n} | Gamma_{6,n} |
|---:|---:|---:|
| 1 | 8^(1/2) | 8^(1/2) |
| 2 | 5^(1/2) | 5^(1/2) |
| 3 | 13^(1/3) | 13^(1/3) |
| 4 | 23^(1/4) | 23^(1/4) |
| 5 | 65^(1/5) | 47^(1/5) |

The lower assertions use the proved finite cutoff and the complete exact certificates described in Section 8. Thus the finite enumeration domain is sufficient for the entire indicated infinite optimization. These are computational proof certificates rather than samples from the infinite domain.

The global rate still satisfies

\[
\lambda_k=\lim_{n\to\infty}g_k(n)^{1/n}=\inf_{n\ge1}\Gamma_{k,n}.
\tag{1.4}
\]

This contribution evaluates the displayed entries and gives a terminating algorithm for every additional fixed (k,n). It does not evaluate the infimum over unbounded n for general k. Section 10 retains the exact remaining growth expression and the metric cost relevant to that last quantifier.

The anonymous/deleted Reddit contributor retains credit for the original k=4 mathematical construction and signed-block argument. `sneed-and-feed` retains separate credit for the existing finite-upper-bound Lean formalization. The present work does not assume the variance contribution in PR #2 and does not relabel any existing proof receipt.

## 2. The literal SplitZero support and quotient construction

The inspected Zeta source works with the split semiring G(R)=R^bullet disjoint union {tau}. The element 0^bullet is a supported coefficient zero; tau is the external additive zero. Its support-diagram presentation starts with a join-semilattice L and modules V_l with compatible transition maps. The total carrier is the disjoint union of the V_l, addition transports to the join, supported zero sends (l,x) to (l,0), and tau sends it to the bottom zero.

Here take R=Q and fix a finite horizon m. Let Omega_m be the literal set of binary choices at all n generators and all m levels. Define

\[
\operatorname{ev}_{A,\mathbf b}(\omega)
 =\sum_{j<m}P_j\sum_{i=1}^n\omega_{j,i}a_i.
\]

Use L_m=P(Omega_m), with union as join and empty set as bottom. For S in L_m, put

\[
V_S=\mathbb Q[S],\quad Y_S=\operatorname{ev}(S),\quad W_S=\mathbb Q[Y_S],
\quad \pi_S(e_\omega)=e_{\operatorname{ev}(\omega)},\quad R_S=\ker\pi_S.
\tag{2.1}
\]

These are free coefficient spaces on the displayed sets. Every word is still present, even when several words have the same numerical value. For S subset T, the original inclusions of words and values commute with pi and map R_S into R_T. Appending a zero binary level gives the corresponding join-preserving transition from L_m to L_{m+1}. The horizon and its actual embedding are retained.

The two-term complex R_S -> V_S, with differential the inclusion, has

\[
H^{-1}=0,\qquad H^0\simeq W_S.
\tag{2.2}
\]

For each value y choose the first word omega_y in its fiber under a specified lexicographic ordering. The vectors e_omega-e_{omega_y}, for all other words in that fiber, are a basis of R_S: subtracting their coefficients leaves the fiber sum at omega_y, which vanishes exactly for a relation. This proves both the relation description and the quotient isomorphism without deleting any original word.

Applying the source's reconstruction functor gives

\[
\mathcal T(L_m,V)\longrightarrow\mathcal T(L_m,W),
\qquad(S,z)\longmapsto(S,\pi_Sz).
\tag{2.3}
\]

A relation is sent to (S,0). The empty support has its separate bottom zero. The empty subset of generators is an actual word evaluating to zero; the support containing that word has a nonzero one-dimensional value fiber. This also records the empty-word case explicitly.

There are two observation maps in (2.1). The value-fiber map pi is followed by the arithmetic amplitude map

\[
w_S:W_S\to\mathbb Q,\qquad w_S(e_y)=y.
\]

Their composition is the original scalar numerical evaluation. Their relation spaces are connected by the exact sequence

\[
0\longrightarrow\ker\pi_S\longrightarrow\ker(w_S\pi_S)
\xrightarrow{\pi_S}\ker w_S\longrightarrow0.
\tag{2.4}
\]

Surjectivity at the right follows by lifting each value-basis coefficient to any word in its fiber. Thus the additional scalar-observation kernel is retained, just as the Zeta source retains the difference between original boundaries and a larger observation kernel.

## 3. Source metrics, section corrections, and the tensor return cost

Give the literal word basis its original orthonormal metric. Define

\[
\mu_S(y)=|\{\omega\in S:\operatorname{ev}(\omega)=y\}|.
\]

The minimum-norm section of pi is

\[
s_S(e_y)=\frac1{\mu_S(y)}
\sum_{\operatorname{ev}(\omega)=y}e_\omega.
\tag{3.1}
\]

It is orthogonal to R_S. Every lift z of v in W_S obeys the exact identity

\[
\|z\|^2=\|z-s_Sv\|^2+v^*G_Sv,
\qquad G_S=\operatorname{diag}_{y\in Y_S}(\mu_S(y)^{-1}).
\tag{3.2}
\]

The finite quotient Gram therefore records the actual representation multiplicities. This is the finite fiber version of the original-source Schur/orthogonal-section identity inspected in the Zeta workbench.

For S subset T and y in Y_S, the vector s_T(e_y)-i s_S(e_y) belongs to the original relation space R_T. Its squared norm is exactly

\[
\|s_T(e_y)-i s_S(e_y)\|^2
=\frac1{\mu_S(y)}-\frac1{\mu_T(y)}.
\tag{3.3}
\]

To verify this, expand in the original word basis. The two sections have norms squared 1/mu_T and 1/mu_S, while their inner product is 1/mu_T. No independent change of metric is introduced.

For a full canonical m-level block, unique mixed-radix digits give

\[
\mu_m(d_0,...,d_{m-1})=\prod_{j<m}\mu_A(d_j),\quad
G_m=G_A^{\otimes m},
\]

\[
\det G_m=(\det G_A)^{m|H(A)|^{m-1}},
\qquad\lambda_{\min}(G_m)=\mu_{\max}^{-m}.
\tag{3.4}
\]

The identity on value coordinates, regarded as a map from metric G_m to the unit value metric, has norm exactly mu_max^(m/2). For A={1,7,8}, six digits have multiplicity one and digit 8 has multiplicity two. Thus

\[
\det G_m=2^{-m7^{m-1}},\qquad
\|I:(W_m,G_m)\to(W_m,I)\|=2^{m/2}.
\tag{3.5}
\]

For A_*={1,4,5,17,21,22}, the multiplicity histogram is 24 digits of multiplicity one, eight of multiplicity two, and six of multiplicity four. All 64 subset choices are present. Its metric-return norm is 2^m. Uniform boundedness of a carry inverse, in the predecessor's specified coefficient metric, does not remove this separately computed source-to-value cost. Equations (3.2)–(3.5) are the exact comparison maps and constants relevant here.

## 4. Complete affine signatures and an all-length arithmetic transport

Fix a positive block tuple a=(a_1,...,a_n) in its displayed increasing order and an ordered list of ell canonical radices b=(b_1,...,b_ell). For every label

\[
(j,u,v,c),\quad 1\le j\le\ell,\quad
u\in\{-2,-1,0,1,2\}^n,\quad v,c\in\{-1,0,1\},
\]

record the sign of the literal affine form

\[
F_{j,u,v,c}(a,b)=u\cdot a-vb_j+c.
\tag{4.1}
\]

There are 9 ell 5^n labels, including forms that are identically zero and supported zero evaluations of nonzero forms. All labels remain in the signature. Identical inequality rows can be indexed together for a polyhedral calculation, while (4.1) retains every original label.

**Proposition O5 (signature transport).** Two tuples with the same complete signature have canonically corresponding binary value fibers and, for any finite word in the ell radix labels, order-preserving Freiman-2 isomorphic numerical digit languages. The correspondence retains every binary representation and every ordered progression tuple, at every length and every progression length k.

**Proof.** The signs with v=c=0 and u in {-1,0,1}^n specify equality and order of all binary sums. The identity on binary masks therefore induces an order-preserving bijection theta:H(A)->H(A'). For a finite word of radix labels j_0,...,j_{m-1}, define

\[
\Theta_m=\operatorname{ev}_{\mathbf b'}\circ
\theta^{\times m}\circ\operatorname{ev}_{\mathbf b}^{-1}.
\tag{4.2}
\]

Both evaluations have their unique actual canonical-digit inverses. Inverse theta and the reverse evaluation give the explicit inverse of Theta_m. Ordering follows from the highest differing digit and the order of theta.

Consider any pair-sum equation between four evaluated words. Its column defect has the form u.a with u in {-2,-1,0,1,2}^n. With initial and terminal carry zero, equality is equivalent to the integral equations

\[
c_{r+1}b_{j_r}=c_r+u_r\cdot a.
\tag{4.3}
\]

For a zero-total relation, the prefix carries are integral by divisibility of the remaining suffix. Since each column defect has absolute value at most 2(b_{j_r}-1),

\[
|c_r|\le2(1-P_r^{-1})<2.
\]

Thus c_r is in {-1,0,1}. Each equation (4.3) is a supported zero of a label in (4.1), so it holds for one tuple exactly when it holds for the other. This proves preservation and reflection of every pair-sum equation. In particular it proves preservation of all consecutive second-difference equations and of nonconstancy. The source mask tuples were unchanged, so every representation fiber and positive multiplicity is retained. □

Linear extension of Theta_m gives an isomorphism of the value-basis spaces, and identity on the word basis gives a commuting square with the quotient maps (2.1). The fiber complexes, support diagrams, and original quotient metrics (3.2) are therefore explicitly transported.

The scalar numerical observation is retained alongside that square. Under the value-basis map J_m, the two scalar functionals are w_m and w'_m J_m, with difference

\[
(w'_mJ_m-w_m)e_y=\Theta_m(y)-y.
\tag{4.4}
\]

For the unrestricted generator relation lattices, the simultaneous map is

\[
\Phi_{a,a'}:\mathbb Z^n\to\mathbb Z^2,
\qquad z\mapsto(a\cdot z,a'\cdot z).
\]

It gives the exact comparison

\[
0\to\ker\Phi_a\cap\ker\Phi_{a'}\to\ker\Phi_a
\xrightarrow{\Phi_{a'}}\Phi_{a'}(\ker\Phi_a)\to0.
\tag{4.5}
\]

For example, (a,b)=((1,100),301) and (a',b')=((1,4),12) have the same complete signature. The unrestricted relation (100,-1) has old amplitude zero and new amplitude 96. Equation (4.5) records that amplitude explicitly. The preserved pair-sum structure, the additional observation kernel, and the retained original integers consequently have distinct, explicitly connected roles.

## 5. A bounded realization with an explicit inverse code

Here is a self-contained integer-polyhedral bound used for Theorem O1. It is a deliberately elementary bound; no sharpness or priority claim is attached to it.

**Lemma O6.** Let P={x in R^d: A x>=r} lie in the nonnegative orthant, with integer entries |A_ij|<=2 and |r_i|<=2. Every x in P intersect Z^d has a y in the same integer polyhedron satisfying

\[
0\le y\le x,\qquad
\|y\|_\infty\le3\,2^{d-1}d!,
\tag{5.1}
\]

and a representation

\[
x=y+\sum_{i=1}^p m_i q_i,\qquad p\le d,
\quad m_i\in\mathbb N_0,\quad
q_i\in\mathbb Z_{\ge0}^d\setminus\{0\},\quad A q_i\ge0.
\tag{5.2}
\]

The q_i can be chosen with every coordinate at most 2^(d-1)(d-1)!.

**Proof.** Add the nonnegative-coordinate rows when needed. The homogenized cone consists of (t,z)>=0 with A z>=t r. Its intersection with t+sum z_i=1 is a bounded polytope. Expressing a point as a convex combination of its finitely many vertices proves that P is a convex hull of its vertices plus a cone generated by its recession rays. Rays with positive t give vertices of P after retaining the t coordinate in the displayed division; rays with t=0 give its recession directions. This also proves that P has vertices when nonempty.

At a vertex of P, d independent active rows determine its coordinates. Cramer's rule and the determinant expansion bound each coordinate by V_d=2^d d!: the denominator is a nonzero integer, hence has absolute value at least one, and the numerator has at most d! terms bounded by 2^d. On an extreme recession ray, d-1 independent active rows have a one-dimensional nullspace. Their cofactor vector, oriented to have nonnegative entries, is an integral ray vector with coordinates at most R_d=2^(d-1)(d-1)!. No division to a primitive ray and no rescaling of the input tuple are needed.

Write x=z+sum t_i q_i with z a convex combination of vertices and t_i>=0. The recession sum can use at most d rays: a linear dependence among more directions permits subtracting an appropriate multiple of that dependence from their nonnegative coefficients until one coefficient becomes zero. Repeating leaves at most d independent directions. Every direction is nonnegative because P is contained in the nonnegative orthant.

Set m_i=floor(t_i) and y=x-sum m_i q_i. Then y is integer and equals z+sum(t_i-m_i)q_i, so it remains in P. Nonnegativity of the q_i gives y<=x. Its coordinates are bounded by V_d+dR_d=3*2^(d-1)*d!. This proves every displayed assertion. □

For a complete signature (4.1), replace a positive sign by F>=1, a negative sign by F<=-1, and zero by F=0. Integer points have exactly the original signs. Include a_1>=1, a_{i+1}-a_i>=1, and b_j-sum a_i>=1. All coefficient magnitudes and all right-side magnitudes are at most two. The domain lies in the nonnegative orthant. Applying Lemma O6 with d=n+ell proves Theorem O1.

The retained comparison is a genuinely reversible code:

\[
x\longmapsto(\text{complete labeled signature},y,(m_i,q_i)_i),
\qquad
(y,(m_i,q_i)_i)\longmapsto y+\sum_i m_iq_i.
\tag{5.3}
\]

A deterministic encoding can enumerate all eligible y and directions within the proved bounds and coefficients m_i<=||x||_infinity, retaining the first valid code in a specified finite ordering. The last bound follows because each nonzero nonnegative q_i has a coordinate at least one and m_iq_i<=x. Thus this is an exact finite procedure for each original x, even when its arithmetic values are large.

For the example in Section 4, the complete code is

\[
(1,100,301)=(1,4,12)+96(0,1,2)+97(0,0,1).
\tag{5.4}
\]

Both directions satisfy every recession inequality of the same signature cell. Another exact example is

\[
10^6(1,7,8,19)=2(1,7,8,19)+(10^6-2)(1,7,8,19).
\]

The factor two in the bounded point is retained because the constant terms c=+/-1 distinguish that affine cell from the scale-one cell. The checker tests every one of the original affine labels in these examples.

For a single base, the all-pattern bound is 3*2^n*(n+1)!. At n=2 it is 72. The exact replay enumerates all 29,190 positive increasing two-generator tuples with sum below a base at most 72, recording 198 signatures and all needed coordinatewise minimal witnesses. Every one of the 109,460 additional tuples with bases 73 through 120 has a coordinatewise smaller representative in the corresponding retained cell. These finite tests corroborate the proof; Lemma O6 provides the unbounded assertion.

## 6. Original return primitives and the exact viable controller

Let D=H(A) be canonical at every permitted radix b>S. Put

\[
C_k=\{-1,0,1\}^{k-2},\qquad
\Delta(d)_i=d_{i+2}-2d_{i+1}+d_i,
\]

\[
F(D,k)=\{c\in C_k:\exists d\in D^k,\ \Delta(d)=-c\}.
\tag{6.1}
\]

This is a constructed finite subset, not an assumed surjectivity statement. Choose the first actual column r(c) for each c in F. The inclusion and section give the commuting identity

\[
\Delta r=-\iota_F.
\tag{6.2}
\]

Here r and the inclusion are maps of the displayed finite sets. Their free linearization sends e_c to e_{r(c)}, and the linearized defect map sends that vector to -c in Q^(k-2). Every linear relation among the c remains in the kernel of this last amplitude map; no linear independence of the carry labels is assumed. Every missing carry remains in the explicitly retained complementary set K=C_k minus F. The source of the equation is still the admitted digit tuples, with their binary representation fibers.

A true-flag carry c describes a represented prefix with a nonzero first difference and with Delta y=P_m c. Appending r(c) gives the literal numerical tuple

\[
Y_i=y_i+P_m r(c)_i,\qquad
\Delta Y=P_m(c+\Delta r(c))=0.
\tag{6.3}
\]

The first difference stays nonzero. Its earlier nonzero value has absolute value less than P_m, while the appended correction is a multiple of P_m. This witness works for every next radix, since the actual digits r(c)_i are at most S. Consequently every reachable true-flag support R meeting F has no infinite admissible extension.

Conversely, suppose H(A) is integer k-AP-free and R is disjoint from F. At every b>=2S+2, the bound |c_i+Delta_i(d)|<=2S+1<b makes a transition possible only when its target is zero and Delta(d)=-c. No true carry in R has such a column. From the false initial state, only constant columns survive because D has no integer nonconstant k-AP. Hence

\[
T_{2S+2}(R)=\varnothing.
\tag{6.4}
\]

Repeating that radix remains safe. Thus disjointness from F is sufficient as well as necessary for an infinite extension of a reachable controller state. This proves Theorem O3.

The viable controller therefore keeps subsets R of K, with their exact labeled transfers, and discards an edge precisely when its complete target support meets F. The discarded record retains that entire target support, one selected carry in the intersection, and its actual return column. Equations (6.2)–(6.3) reconstruct the obstruction rather than silently identifying that carry with absence.

All constant false-flag paths remain separately present. The empty true-flag support means there is no nonconstant prefix branch; it does not remove the constant zero-carry source. Positive binary representation multiplicities may be carried as edge weights. The map from nonnegative counts to their support is n-> [n>0], a semiring homomorphism; no cancellation of signed coefficients is used to determine reachability.

For the five-generator block {2,3,5,17,34} at k=5, exactly 25 of the 27 carries have return columns. The two others are (0,-1,0) and (0,1,0). The original all-state controller can form many transient supports, whereas the exact viable controller has at most four possible supports. The calculations retain the return certificate for each removed support. This is the mechanism that made the complete rank-five calculation tractable.

## 7. Finite optimization over every block of a fixed size

For every fixed A, radices b>=2S+2 have exactly the same full labeled transition table: each numerator c+Delta(d) has magnitude below b, so divisibility is precisely equality to zero. Replace such a radix by 2S+2, retaining its old value and the exact multiplicative cost ratio b/(2S+2). The word-evaluation conjugacy gives the inverse finite-language map and preserves every progression tuple.

There are therefore only S+2 candidate radix labels, S+1 through 2S+2. The viable controller is finite. Give each edge b the cost log b and the reward n. If a cycle C has ell edges, its rate is

\[
\left(\prod_{e\in C}b_e\right)^{1/(n\ell)}.
\tag{7.1}
\]

**Proposition O7.** The optimum for the block is the minimum of (7.1) over its reachable directed simple cycles. A minimizing period is safe when started at the initial empty true-flag support.

**Proof.** Let rho be the least log-cost per edge among those cycles. Removing cycles from any finite walk leaves a simple path of bounded length. Every removed cycle has nonnegative sum of log b-rho, and the finitely many remaining paths have a common finite lower bound. Division by walk length proves the lower limiting bound. Repetition of a minimum cycle attains it after a finite access path. The period also works from the initial state alone: transfer maps are monotone on supports, and the empty support is contained in the selected cycle state. Induction places every repeated-period prefix inside the corresponding safe cycle support. □

There are at most V_k safe controller states even without return pruning, so ell<=V_k. Cycle rate comparisons are exact integer comparisons of products raised to integer powers. A period also supplies an original constant-radix block: take its actual union of P_j A and base product Q. This block has n ell distinct generators and sum at most Q-1. Its repeated lifts are exactly the original periodic construction.

Now take a certified n-generator canonical benchmark (B,Q) with its constant schedule safe. It gives Gamma_{k,n}<=Q^(1/n). Every block with S(A)>=Q has every radix at least Q+1, hence every schedule has rate at least (Q+1)^(1/n), strictly exceeding the benchmark. Thus all minimizing blocks satisfy S(A)<Q. There are finitely many such literal positive sets. Combining this bound with Proposition O7 proves the benchmark form of Theorem O2.

For a universal benchmark, take B={1,3,...,3^(n-1)} and Q=3^n. Its binary base-three digit language is three-term-progression-free by the least-column argument, and its modular language modulo 3^n has the same property: a nonzero modular step has a least nonzero base-three position, contradicting the binary digit condition there. It is consequently k-AP-free for every k>=3. Its sum is (3^n-1)/2<Q. This proves the advertised universal cutoff and attainment.

Theorem O1 supplies a different type of control: every full affine pattern has a bounded realization with an inverse code, including patterns far from optimal. The benchmark cutoff is sharper for optimization because it uses the actual rate objective. Both keep their own explicit comparison maps and scopes.

## 8. Exact finite proofs of the globally optimal small-rank capacities

The upper certificates used in the table are literal blocks:

| n | k | block | base or period |
|---:|---:|---|---|
| 1 | 5,6 | {1} | (2,4) |
| 2 | 5,6 | {1,2} | 5 |
| 3 | 5,6 | {1,3,4} | 13 |
| 4 | 5,6 | {1,3,4,7} | 23 |
| 5 | 5 | {1,2,5,15,20} | 65 |
| 5 | 6 | {1,2,6,7,14} | 47 |

The first periodic construction has rate sqrt(8) per generator. All other displayed upper bounds come from a single radix. Composite moduli are checked with every nonzero modular step, including steps whose order is smaller than k.

For the lower proofs, the benchmark theorem supplies an exhaustive integer domain. Every block in that domain is assigned one of three complete certificates.

An actual one-level integer k-AP excludes every radix schedule for that block. Otherwise the checker constructs F and r from (6.1)–(6.2). When F=C_k, every modularly bad radix produces the explicit two-level obstruction (6.3), independently of the following radix. Enumerating each radix from S+1 to the first modularly safe base therefore gives the exact block capacity. Every earlier base has its actual two-column witness, and the first safe base receives a separate full modular check.

For the remaining blocks, the verifier retains the entire viable controller, all its safe edges, every discarded support and return primitive, and an exact positive rational potential h. At a target base Q, every surviving edge satisfies

\[
\boxed{b\,h(R')\ge Q\,h(R).}
\tag{8.1}
\]

Multiplying along a path gives

\[
\prod_{j<m}b_j\ge Q^m\frac{h(R_0)}{h(R_m)}.
\tag{8.2}
\]

The finitely many positive potentials retain a bounded endpoint factor, so every infinite schedule has rate at least Q^(1/n). The larger-radix branch preserves (8.1) because its transfer is the same and its cost is larger. For a target P^(1/ell), the same computation uses b^ell h(R')>=P h(R). This handles the sqrt(8) singleton period without rounding its cost.

The exact rank-five domains and proof decomposition are:

| k | all five-element blocks with S<Q | one-level admissible | complete return sections | remaining viable controllers |
|---:|---:|---:|---:|---:|
| 5, Q=65 | 41,185 | 2,403 | 2,172 | 231 |
| 6, Q=47 | 6,074 | 168 | 150 | 18 |

The k=5 controllers have at most two reachable viable states; the k=6 controllers have one. The retained safe-edge counts are 5,054 and 279, respectively. Their discarded edge records number 9,594 and 541. All returning primitive rows, including rows used in the controller branch, are retained: 64,163 rows at k=5 and 13,458 at k=6.

The independent auditor imports neither producer. It reconstructs the complete generator domain and each actual binary digit image, checks every integer obstruction and every return row, and scans the actual allowed next digits for every controller transfer. It checks all retained and discarded support records and all positive rational potential inequalities. It also independently enumerates modular start/step pairs at every claimed first safe base and at the final upper benchmarks. Consequently the two rank-five equalities in Theorem O4 have both complete production certificates and independent arithmetic audits.

For ranks at most four and additional small k, the other verifier checks 506 complete block instances, 2,995 safe controller edges, and 418 independent full-column transfer comparisons. Its record includes complete cycle data and rational lower potentials. In addition to Theorem O4, it establishes Gamma_{4,1}=Gamma_{4,2}=3 and Gamma_{4,3}=19^(1/3). It also calculates the singleton capacities through k=9; at k=9 the optimum is sqrt(6), using period (2,3).

A consequence relevant to the existing best constructions is

\[
\min_{1\le n\le5}\Gamma_{5,n}=23^{1/4}>97^{1/6},
\]

\[
\min_{1\le n\le5}\Gamma_{6,n}=47^{1/5}>93^{1/6}.
\tag{8.3}
\]

All comparisons can be checked by integer powers. Thus any improvement of those two six-generator record rates within the fixed-block canonical mixed-radix model must use at least six generators per level. The model keeps the same block at each level; changing the block itself from level to level is a separate, explicitly different dictionary optimization.

## 9. Return to the unrestricted exponential rate

For completeness, the passage to (1.4) retains the original generator quantity. For admissible A and B set

\[
A\star B=A\cup(2S(A)+1)B.
\]

The map (x,y)->x+(2S(A)+1)y is a bijection from H(A) times H(B) to H(A star B), with remainder/quotient inverse. A second difference in the first factor lies between -2S(A) and 2S(A), so divisibility by 2S(A)+1 forces it to vanish. This pulls every progression back to progressions in both factors. A nonconstant composite progression therefore supplies a nonconstant factor witness.

Moreover

\[
2S(A\star B)+1=(2S(A)+1)(2S(B)+1).
\]

For the minimum F_k(n) of 2S(A)+1 at size n, submultiplicativity follows. Writing n=t m+r proves convergence of log F_k(n)/n to its infimum, because the finitely many r-remainders contribute a bounded numerator. The exact inequalities

\[
2g_k(n)+1\le F_k(n)\le2n g_k(n)+1
\]

then prove existence of lambda_k and

\[
\lambda_k=\inf_{|A|\ge1}(2S(A)+1)^{1/|A|}.
\]

Every admissible A has the canonical constant certificate (2S(A)+1,A): all modular second differences lie strictly between minus and plus that base, so modular divisibility implies integer equality. This proves inf_n Gamma_{k,n}<=lambda_k. Conversely, each minimizing finite cycle in Section 7 is an actual integer generator construction at its aggregate radix, proving lambda_k<=Gamma_{k,n}. Together these prove (1.4).

Noncanonical carry certificates from earlier work still enter the same global rate. A safe separated noncanonical block is sent to a finite lifted prefix C_t and then to (2S(C_t)+1,C_t). This keeps the prefix's generators, has a valid canonical modular certificate, and its cost per generator tends to the original base cost. Its rank changes from n to tn and that change is retained. The new fixed-rank table consequently has its stated canonical scope, while the unrestricted global infimum receives the earlier noncanonical constructions through their actual maps.

## 10. The remaining uniform inequality and an exact cohomological growth defect

The last unbounded parameter in (1.4) is n. Neither the all-pattern bound nor the finite fixed-rank algorithm supplies a convergence modulus for that infimum. Their exact receiver is the universal assertion Gamma_{k,n}>=u for every positive n, at a proposed lower threshold u. A strict failure lambda_k<u has a finite n and a finite periodic certificate by the definition of the infimum and the attained finite-rank optima. Such a witness is found by eventual enumeration. The converse lower assertion retains its full universal quantifier.

The source-growth expression below makes the remaining information concrete. Build an admissible block A in any fixed order. Before adding a new generator a, let B be the actual preceding subset-sum image, let v=|B|, and decompose B into maximal a-chains. Let their number be c and their lengths be L_1,...,L_c. Because B union (B+a) is contained in the final k-AP-free image, every L_i<=h=k-2.

The original relation sequence for this addition is

\[
0\to\mathbb Q[B\cap(B+a)]\to\mathbb Q[B]\oplus\mathbb Q[B]
\to\mathbb Q[B\cup(B+a)]\to0.
\tag{10.1}
\]

For x in the overlap, the first map is e_x->(e_x,-e_{x-a}); the last map sends (e_x,0) to e_x and (0,e_y) to e_{y+a}. The first map is injective, and its image is precisely the kernel by grouping coefficients at each actual image value. This is another instance of the support-preserving quotient in Section 2.

Since |B intersect(B+a)|=v-c, the exact growth is v'=v+c. Retain the nonnegative defect

\[
\delta=h c-v=\sum_{i=1}^c(h-L_i).
\]

It gives

\[
\boxed{v'=\frac{h+1}{h}v+\frac{\delta}{h}.}
\tag{10.2}
\]

For the successive stages j=0,...,n-1, with v_0=1, put gamma=(h+1)/h. Iteration yields the exact identity

\[
\boxed{|H(A)|=\gamma^n+\frac1h
\sum_{j=0}^{n-1}\gamma^{n-1-j}\delta_j.}
\tag{10.3}
\]

Equivalently,

\[
\log|H(A)|=n\log\gamma+
\sum_{j=0}^{n-1}\log\left(1+\frac{\delta_j}{(h+1)v_j}\right).
\tag{10.4}
\]

The first term recovers the known elementary exponential lower scale. The second term is an explicitly retained positive quantity in the original subset-sum image; it is not replaced by zero in the research target. The exact verifier checks (10.1)–(10.4) for 7,266 admissible sets in its stated finite domain, over 26,315 generator-addition stages. Those checks do not estimate the term uniformly in n. Obtaining a sufficiently strong uniform bound on this contribution, or another original-source invariant, remains necessary for a general matching lower law.

The current source-level obstruction to a free metric argument is equally explicit: the tensor metric cost (3.4) survives even when the carry relation inverse is uniformly bounded. Its growth and the actual feasible relation primitives must be controlled together. The present finite classifications exploit those primitives successfully through rank five, but do not assert a bound for every rank merely from cohomological exactness.

## 11. Reproducibility and evidence inventory

All code is standard-library Python. `verify_outer_control.py` produces the affine-signature, fiber-metric, transport, chain-defect, and small-rank certificates. `verify_rank_five.py` produces either a full rank-five record or an explicitly indexed shard. `audit_rank_five.py` independently verifies a full record or a shard, including its literal interval in the complete generator enumeration. No checker relies on Python assert statements.

The largest run was executed in disjoint exact index intervals, then joined only after checking their endpoints and their full generator lists against the complete independently enumerated domain. The full records are stored losslessly as gzip-compressed JSON. The accompanying replay/audit summary binds their uncompressed hashes, producer hashes, auditor hashes, and all interval coverage. Commands and output paths are given in the package README. Larger full JSON records can be regenerated or decompressed with the standard gzip module.

The affine-height replay includes 12,720 singleton tuples through base 160 and the complete two-generator domains in Section 5. Four reversible codes are checked against every literal affine label. Sixteen complete carry profiles are compared before and after the parameter transport, with all binary-mask fibers. Eight direct numerical-language transports check their full ordered pair-sum partitions. The support metric replay checks 13,122 support-inclusion pairs and 33,534 section-boundary identities, as well as exact tensor determinants through three levels.

These bounded replays have their specified roles. The all-rank polyhedral theorem has the proof in Section 5. The all-schedule and cutoff theorems have the proofs in Sections 6–7. The exact table uses those theorems to justify the finite domain, and the complete finite proof records then establish the arithmetic cases. Existing Lean receipts retain their original scope.

## References and exact source roles

KokunoYumeto. (2026, September 14). *Reconstruction with changes of support index* [TeX source]. `workbenches/splitzero-tandem/tex/support_diagrams.tex`, Zeta Function Research Reader, commit `42df8a2de002d5fc7090641fac46ea11be05fa71`. Used: full support-index reconstruction, internal quotient, and representative-kernel comparison. Source: https://github.com/KokunoYumeto/zeta-function-research-reader/blob/42df8a2de002d5fc7090641fac46ea11be05fa71/workbenches/splitzero-tandem/tex/support_diagrams.tex

KokunoYumeto. (2026, September 14). *Exact source-metric optimization and aggregate arithmetic control* [TeX source]. `workbenches/splitzero-tandem/tex/tau_chain.tex`, same pinned repository. Used: the original finite section/Schur identities TC7–TC8b; no arithmetic endpoint estimate imported. Source: https://github.com/KokunoYumeto/zeta-function-research-reader/blob/42df8a2de002d5fc7090641fac46ea11be05fa71/workbenches/splitzero-tandem/tex/tau_chain.tex

The Clankers. (2026, September 14). *SplitZero transfer to Erdős 817: uniform carry cohomology and exact mixed-base capacity* [Research note]. `research/splitzero_transfer/notes/splitzero-infinite-carry-control.md`, commit `98fd25802a387138053064e11ddd2f6d2007d55b`. Used: original integral carries, uniform relation inverse, original metric return, finite fixed-block controller, and complete-return argument for A_*. This existing branch is a predecessor, not a new contribution claimed by the present note. Source: https://github.com/KokunoYumeto/erdos-problem-817-workbench/blob/98fd25802a387138053064e11ddd2f6d2007d55b/research/splitzero_transfer/notes/splitzero-infinite-carry-control.md

The Clankers. (2026, September 14). *Exact composition, finite carry certificates, and the general-k capacity* [User-delivered research package]. `EP817_GENERAL_K_POLYCLANK_20260914.zip`, `research/general_k/notes/general-k-carry-capacity.md`. Used: previous source maps and executable canonical carry implementation as a comparison; the new producer is standalone.

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1). https://arxiv.org/html/2606.24139v1 . Role: original general-k conventions and benchmark lower/upper exponential bounds. The finite lower-growth term in Section 10 is derived here directly.

Borosh, I., & Treybig, L. B. (1992). A sharp bound on positive solutions of linear Diophantine equations. *SIAM Journal on Matrix Analysis and Applications, 13*(2), 454–458. https://doi.org/10.1137/0613029 . Publisher abstract inspected as context for bounded integer-solution arguments. Its hypotheses or sharp bound are not imported into Lemma O6, whose weaker bound is proved in full here.

Anonymous/deleted Reddit contributor, & The Clankers. (2026, September 13). *The exponential rate for four-term-progression-free subset-sum sets* [Workbench manuscript]. Original mathematical construction credited to the anonymous contributor; reconstruction and verification recorded separately in the source repository.

sneed-and-feed. (2026, September 13). *Formalize finite upper bound theorem and core helper lemmas in Extended.lean* [Pull request #1]. Erdős Problem 817 Workbench. Role: existing upper-bound formalization and separate attribution; no extension of its Lean receipt is asserted.
