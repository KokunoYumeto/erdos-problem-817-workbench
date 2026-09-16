# Canonical arithmetic factors and integral isolation at every clique rank

Research contribution of The Clankers, 16 September 2026. Ordinary mathematical proofs and exact finite certificates; independent mathematical review pending. No new Lean elaboration is asserted.

The original problem is Erdős 817: for fixed k>=3, minimize the largest member of an n-element set A of distinct positive integers whose set of binary subset sums contains no nonconstant k-term arithmetic progression. The original k=4 construction remains attributed to the anonymous/deleted Reddit contributor; the checked finite upper-bound Lean extension remains separately attributed to sneed-and-feed.

This contribution continues the delivered `EP817_DEFECT_CLOSURE_20260915` package. It strengthens its clique isolation to every rank and every rational observation, supplies a triangular-prism core, calculates the integral obstruction layers for K3,3, and makes the generator decomposition canonical. The all-rank results are proved below. The two finite graph statements are additionally accompanied by complete original-mask certificates, not sampled graph searches. The conformal-minimal relations used for the canonical partition are the classical Graver basis elements of the original one-row integer matrix; that terminology and method are credited to the existing literature, not introduced as a new algebraic object.

## 1. Exact statements and their scope

For a finite indexed list A=(a_i) of distinct positive integers and q>=2, retain

\[
\Phi_A:\mathbb Z^n\longrightarrow\mathbb Z,\qquad
\Phi_A(x)=\sum_i a_ix_i,
\quad H_q(A)=\Phi_A(\{0,\ldots,q-1\}^n).
\]

Write H(A)=H_2(A). Numerical values are counted once in H_q, while the multiplicity of their original digit representations is denoted mu_(A,q). No distinct-representation assumption is built into these definitions.

The main all-rank result is the following.

**Theorem CI1.** Let Sigma_m be the set of actual orientation scores of the complete graph K_m, for m>=2. For every rational linear map ell:Q^m->Q and every finite Y subset Q, if ell(Sigma_m)+Y is (m+1)-AP-free, the addition map

\[
\ell(\Sigma_m)\times Y\longrightarrow\ell(\Sigma_m)+Y
\]

is a bijection. For every nonzero r in Sigma_m-Sigma_m, the forced relation r is obtained in the original source Sigma_m union (Sigma_m+r) by at most floor(m^2/4) integral root steps. All tuple representatives and all preceding-boundary coefficients remain explicit. There is no distinctness assumption on the coordinate values of ell.

**Theorem CI2.** The triangular-prism score source and the K3,3 score source have the same isolation property at progression length five, for every rational linear observation. For the prism, every source difference is the negative sum of at most four actual first-round progression steps in the two-translate source. For K3,3, the complete proof has 94 integral first-round types, three genuine order-two first-round classes, and two types requiring a second progression-closure round.

**Theorem CI3.** Every positive distinct generator list has a unique finest partition Pi_q(A) of its literal coordinates for which

\[
\prod_{C\in\Pi_q(A)}H_q(A_C)\overset{+}{\longrightarrow}H_q(A)
\]

is bijective. Its classes are the connected components of the supports of those Graver elements g of Phi_A with norm_infinity(g)<=q-1. Increasing q can merge classes but cannot split them. The partition is a one-class partition by q=max(A)+1 whenever n>=2.

**Theorem CI4.** In a k-AP-free subset-sum set, every full K_(k-1) edge-distance core with positive distinct edge values is an entire component of Pi_2. For k=5, the same holds for full K3,3 and triangular-prism edge-distance cores. In particular any two such certified cores are disjoint or are the same set. At k=5, the three different graph types cannot have the same generator set. Removing all the certified cores therefore leaves a uniquely specified remainder, independent of a chosen packing.

These statements do not classify all components of Pi_2. Nor do they identify Pi_2 with Pi_3: Section 8 supplies an admissible seven-generator example in which a six-generator binary component and a singleton merge in the ternary image, with a calculated 84-dimensional additional receiving kernel. There is no claimed improvement to the unrestricted numerical record for lambda_5 or lambda_6 in this contribution.

## 2. A complete criterion for isolation from every finite remainder

Let S be a nonempty finite subset of a finite-dimensional rational vector space E. Say that S is universally k-isolating if, for every linear ell:E->Q and every finite Y subset Q, k-AP-freeness of ell(S)+Y forces addition ell(S) x Y -> ell(S)+Y to be injective. The factors are the actual distinct numerical images. This definition does not demand that ell be injective on S.

For any finite U subset E, let Cl_k(U) be the following rational progression closure. Start with W_0=0 and put

\[
W_{j+1}=W_j+\operatorname{span}_{\mathbb Q}
\{x_1-x_0:x\in U^k,\ x_i-2x_{i+1}+x_{i+2}\in W_j\text{ for all }i\}.
\tag{2.1}
\]

A strict step increases dimension. Let W_* be the resulting fixed space. An observation whose image of U is k-AP-free annihilates every W_j: apply it to each actual tuple in (2.1), and use the fact that an admitted progression must be constant.

Conversely, in E/W_* every vector-valued k-AP of the image of U is constant by the fixed-point equation. Given z outside W_*, choose a rational functional on that quotient avoiding the finitely many hyperplanes attached to nonzero pair differences, nonzero second differences, and z. Such a functional exists because a finite union of proper rational hyperplanes does not exhaust the rational dual. It detects z and its numerical image of U is k-AP-free. Thus

\[
\operatorname{Cl}_k(U)=
\bigcap_{\ell(U)\ k\text{-AP-free}}\ker\ell.
\tag{2.2}
\]

The quotient map E->E/W_* and every new subspace W_(j+1)/W_j remain part of this construction. An integral tuple certificate can be stronger than the rational conclusion (2.2); later sections state explicitly when integer multiples rather than the original vector are derived.

**Proposition 2.1 (two-translate criterion).**

\[
\boxed{S\text{ is universally }k\text{-isolating}
\iff r\in\operatorname{Cl}_k(S\cup(S+r))\quad\text{for every }r\in S-S.}
\tag{2.3}
\]

**Proof.** Suppose the right side holds and ell(s_1)+y_1=ell(s_2)+y_2 is a collision with distinct factor pairs. Then d=ell(s_1-s_2)=y_2-y_1 is nonzero. Put r=s_1-s_2. A translate of ell(S union (S+r)) is contained in ell(S)+Y. Formula (2.2) forces ell(r)=0, a contradiction.

Conversely, suppose r lies outside the indicated closure. The separating observation constructed after (2.1) has ell(r) nonzero and ell(S union (S+r)) k-AP-free. Set Y={0,ell(r)}. The two source representatives realizing r give a collision of factor pairs, so universal isolation fails. Both directions construct the actual maps and, in the failure direction, the entire finite numerical counterexample. QED.

Universal isolation is preserved by specified linear images: compose any receiving observation with the given source map. It is also preserved by finite Cartesian products. For the product, apply isolation of the first factor with all other numerical factors and Y as its finite remainder; then repeat for the next factor. Every resulting addition bijection is the restriction of the original sum map.

## 3. Integral clique packets and the all-rank proof

### 3.1 Original orientation sources and their cut criterion

An orientation assigns each edge of a loopless multigraph to one endpoint. The score is the vector of the numbers assigned to each vertex. For a target integer score d, an orientation exists precisely when

\[
\sum_vd_v=|E|,\qquad d(U)\ge |E(U)|\quad\text{for every vertex set }U.
\tag{3.1}
\]

The equivalent upper inequality is d(U)<=|E|-|E(V\U)|. This is the classical generalized Landau criterion; see Kolesnik and Sanchez (2024), Corollary 4.2. A direct integral construction suffices here: make a bipartite network with one unit-capacity node for each original edge, arcs to its two endpoints, and prescribed endpoint capacities d_v. The cut inequalities give a flow of |E|. Integral augmenting paths give a zero-one assignment of every original edge. No random orientations are substituted for actual masks.

For K_m, coordinate scores lie in [0,m-1]. Their differences are exactly

\[
\mathcal R_m=\{r\in\mathbb Z^m:\sum r_i=0,
\quad r(U)\le |U|(m-|U|)\text{ for every }U\}.
\tag{3.2}
\]

Necessity follows from the width of the score cut interval. For sufficiency, orient the doubled graph 2K_m with score r+(m-1)1 using (3.1). Split its two copies into scores s,t. Reversing the second copy has score (m-1)1-t, so r=s-((m-1)1-t) is an actual difference. This supplies both original orientation masks.

### 3.2 A packet with one retained terminal defect

Take nonzero r in R_m. Choose i with maximal r_i and j with minimal r_j, and put

\[
\alpha=e_j-e_i.
\]

Then r_i>=1 and r_j<=-1. Let I=V\{i,j}; define b_i=0, b_j=m-1 and b_h=m-2 for h in I. Form the literal multigraph M consisting of one K_m plus another K_(m-2) on I. Its prescribed score is

\[
d=r+\alpha+b.
\tag{3.3}
\]

We verify every cut in (3.1). Put w=r+alpha and a=|U|. In upper form, the required inequalities are

| Membership of i,j in U | Required upper bound on w(U) |
|---|---|
| neither | a(m-a)-a |
| i only | a(m-a) |
| j only | a(m-a)-(m-1) |
| both | a(m-a)-(m-a) |

For neither, maximality gives r_i>=r(U)/a when a>0. Apply (3.2) to U union {i} to get r(U)<=a(m-a-1). The empty case is immediate. Applying the same calculation to -r and the complement of U proves the both case. The i-only case follows from w(U)=r(U)-1 and (3.2).

For j only, the cases a=1 and a=m-1 follow from r_j<=-1 and r_i>=1. For 2<=a<=m-2, let P_a be the sum of the largest a entries of r. Replacing the minimum by the maximum gives

\[
r(U)\le P_a-r_i+r_j,
\quad r_i\ge P_a/a,
\quad r_j\le-P_a/(m-a).
\]

Since a(m-a)>=m in this range,

\[
r(U)\le\left(1-\frac m{a(m-a)}\right)P_a
\le a(m-a)-m.
\]

Adding the one contributed by alpha proves the last required bound. The total in (3.3) equals the number of edges of M, so (3.1) now supplies an actual orientation.

Let t be its score on K_m, and t' the score on the extra K_(m-2). Put s=b-t'. This is an actual K_m score: vertex j wins every incident edge, vertex i loses every incident edge, and the internal edges are the reverse of the extra orientation. We have

\[
t-s=r+\alpha.
\tag{3.4}
\]

Reverse first the direct j-to-i path and then the m-2 edge-disjoint two-edge paths through I. Every reversal decreases the score by alpha. Reversing this ordered list of orientations gives the actual source tuple

\[
s-(m-1)\alpha,\ldots,s-\alpha,s,t.
\tag{3.5}
\]

Its first difference is alpha, all second differences except the final one are zero, and the final one is r. Equivalently, with sigma=(0,...,0,1), it has rows a+l alpha+sigma_l r. This proves the packet for every r, including m=2. All edges, orientations and signs are specified by the construction.

### 3.3 Root contraction stays inside the feasible difference source

Set r'=r+alpha. It is still in R_m. Only a cut containing j but not i can increase. If that cut had attained its original upper bound, replacing j by i would increase its sum by at least two without changing its size, contradicting (3.2). Thus its original integral slack is at least one. All other cuts decrease or stay unchanged.

The positive-coordinate mass decreases exactly by one:

\[
\sum_h(r_h')_+=\sum_h(r_h)_+-1.
\tag{3.6}
\]

The positive-coordinate set itself is an admitted cut, so initially this mass is at most floor(m^2/4). Repeating the operation terminates at zero in at most that many steps. No coefficient vector is divided or replaced by a primitive representative.

### 3.4 Every implication uses the same original two-translate source

Fix the ORIGINAL r and U_r=Sigma_m union (Sigma_m+r). At step t the residual is

\[
r_t=r+\alpha_0+\cdots+\alpha_{t-1}.
\]

Construct its packet x_l=a+l alpha_t+sigma_l r_t by (3.5), and set

\[
z_l=x_l+(1-\sigma_l)r.
\tag{3.7}
\]

The first m rows lie in Sigma_m+r, and the final row in Sigma_m. The source never changes to a quotient representative set. The first difference of z is alpha_t and its only possible nonzero second difference is

\[
r_t-r=\sum_{h<t}\alpha_h.
\tag{3.8}
\]

It is an integral combination of previously derived steps. Starting with t=0, (2.1) therefore derives every alpha_t using original masks. At termination

\[
\boxed{r=-\sum_t\alpha_t.}
\tag{3.9}
\]

This proves an integral closure certificate in at most floor(m^2/4) steps, and Proposition 2.1 proves Theorem CI1.

If an arithmetic observation detects the original r, at least one derived alpha has nonzero image. Choose the first such step. Every preceding defect in (3.8) has zero image, and the actual tuple (3.7) evaluates to a nonconstant progression. This is the explicit failure-witness procedure, not merely an implication between abstract dimensions.

The progression-length threshold is sharp for arbitrary observations. Projection to one vertex maps Sigma_m onto {0,...,m-1}. Adding Y={0,1} gives {0,...,m}, with collisions but no (m+2)-term progression. This map displays why universal (m+1)-isolation does not become universal (m+2)-isolation.

## 4. Two cubic sources, and the difference between integer torsion and a new implication

The proof data retain all 512 orientation masks for each nine-edge graph, each score fibre, every nonzero source difference, the full graph automorphism group, and every source row used below. An automorphism permutes original vertices and edge masks; reversal of all edges sends scores s to 3*1-s and differences to their negatives. These explicit bijections justify the orbit reduction.

For a difference r, a recorded binary-switch packet consists of

\[
x_l=a+lv+\sigma_lr\in\Sigma(G),\quad 0\le l\le4,
\quad\sigma_l\in\{0,1\},\quad\sigma_0=0.
\tag{4.1}
\]

The rows x_l+(1-sigma_l)r form an actual vector progression in Sigma(G) union (Sigma(G)+r), with step v. Thus every k=5-admissible observation of this union kills v. This fact uses the numerical image of the two translates and does not assume that ell(r)=0.

### 4.1 The triangular prism

The vertex set is {0,...,5} and the edge list is

\[
01,02,03,12,14,25,34,35,45.
\]

Its actual score source has 314 values and 4,994 nonzero differences. There are 255 orbits under its 12 graph automorphisms and simultaneous sign reversal. For each representative r, the complete certificate supplies t packets with

\[
\boxed{r=-\sum_{h=1}^{t}v_h,\qquad1\le t\le4.}
\tag{4.2}
\]

The orbit counts by t are 4,39,202,10 for t=1,2,3,4 respectively. Every coefficient in (4.2) is the literal integer -1. Membership of every packet row is verified against its retained orientation mask. Equation (4.2), the finite complete orbit cover, and Proposition 2.1 prove universal five-isolation for the prism without a condition on ell.

A second finite certificate addresses source faithfulness when graph marks actually define positive distinct generators. For every r, recorded packet steps span an original vertex root. If ell(r)=0 and ell(Sigma(G)) is five-AP-free, those packets force the observed root to vanish. For the prism, any two vertices are adjacent or share a neighbour. Equal marks would therefore give either a zero edge or two equal absolute edge values. Under the actual-generator hypotheses all marks are distinct, and the root cannot vanish. Hence ell is injective on the 314 source scores.

An implementation initially restricted this root search to adjacent vertex pairs. The broader root certificate is valid for the stated diameter-two reason, and the corrected file retains all vertex pairs. No proof statement or supported source row was weakened by the correction.

### 4.2 K3,3: three first-round torsion classes

Use left vertices 0,1,2 and right vertices 3,4,5. The score source has 328 values, 5,298 nonzero differences and 99 symmetry orbits. In 94 orbits, certificates of the form (4.2) apply directly.

Three representatives require the retained multiplier two:

\[
\begin{split}
r_1&=(-3,-3,1,1,2,2),\\
r_2&=(-3,-2,2,1,1,1),\\
r_3&=(-2,-2,1,1,1,1).
\end{split}
\]

For each, the complete first-round direction lattice has generators

\[
\begin{array}{ll}
v_1=(0,1,-1,0,0,0),&v_2=(1,0,-1,0,0,0),\\
v_3=(1,1,0,0,-1,-1),&v_4=(1,1,0,-1,0,-1),\\
v_5=(1,1,0,-1,-1,0).
\end{array}
\]

The exact identities are

\[
\begin{split}
2r_1&=-v_1-v_2-3v_3-v_4-v_5,\\
2r_2&=-v_1-3v_2-v_3-v_4-v_5,\\
2r_3&=-v_1-v_2-v_3-v_4-v_5.
\end{split}
\tag{4.3}
\]

Every v has even pairing with eta=(1,1,1,0,0,0), while each eta*r is odd. The class of r in the integer quotient by the first-round step lattice has order exactly two. The auditor independently enumerates all vector five-term progressions in the original two-translate union, confirming that no omitted first-round step removes this parity certificate.

The quotient class is retained. A rational or integer numerical observation that kills the first-round steps also kills 2r; its torsion-free codomain then forces ell(r)=0. Equivalently, the map from the original integer quotient to its rationalization kills precisely the relevant torsion class. No scalar division is assigned to an original binary source point.

### 4.3 K3,3: two second-round classes

The other representatives are

\[
r_4=(-3,1,1,-1,0,2),\qquad
r_5=(-2,-1,0,1,1,1).
\]

For r_4, the first-round steps are

\[
v_1=e_0-e_5,\quad v_2=e_0-e_2,\quad v_3=e_0-e_1.
\]

Coordinate 3 annihilates all three and detects r_4. Thus r_4 survives even the rational first-round quotient. A second original-source tuple has step w=e_3-e_0 and defects

\[
v_3,\qquad v_2-v_3,\qquad2v_1+v_3,
\]

all in the already established first-round lattice. The final integer identity is

\[
r_4=-2v_1-v_2-v_3-w.
\tag{4.4}
\]

For r_5, the first-round steps are v_1=e_0-e_5, v_2=e_0-e_4, v_3=e_0-e_3. Coordinate 1 detects the surviving class. The second tuple has w=e_1-e_3, with defects v_2-v_3, v_1-v_2, v_2+v_3. Now

\[
r_5=-v_1-v_2-w.
\tag{4.5}
\]

All five rows of each second-round tuple are actual orientations with a retained shift bit, and remain in the original Sigma union (Sigma+r). Their original-mask data and the displayed coefficients are checked independently. These two cases require a new progression implication; rational saturation of the first-round lattice alone does not supply it.

Together, the 94+3+2 cases prove universal five-isolation of K3,3 for every rational observation. This strengthens the predecessor's isolation statement, which used distinct marks and local alternatives to expose a nonzero numerical step. Source faithfulness for positive distinct K3,3 edges is separately certified by original-source closure from ell(r)=0 to an observed vertex root. K3,3 also has diameter two, so those actual-generator hypotheses make every such root nonzero.

## 5. From the source theorem to exact arithmetic factors

For a graph with vertex marks T, orient an edge in a mask toward its selected endpoint and define L_T(s)=sum_v t_vs_v. Put C_T=sum_(uv in E) max(t_u,t_v). Select the corresponding distance generator when the mask chooses the smaller marked endpoint. The exact original evaluation is

\[
\Phi_A(\text{subset mask})=C_T-L_T(\text{score}).
\tag{5.1}
\]

This is a bijection between edge masks and subsets. It retains all score fibres and their multiplicities.

If A=C disjoint-union B is k-admissible and C is a certified critical core, apply universal isolation to its score image with Y=H(B), using the affine translation in (5.1). It gives

\[
\boxed{H(C)\times H(B)\overset{+}{\simeq}H(A).}
\tag{5.2}
\]

No magnitude separation or order of the numerical generators is required. The theorem also has an explicit contrapositive. Two distinct value pairs with the same sum determine an observed nonzero source difference r and place the two-translate image in H(A). The first derived step having nonzero numerical observation yields an actual forbidden progression. Source masks give subsets of the original core; its shift bit chooses one of the two original remainder subsets. No sum uses a generator twice.

Applying (5.2) successively to disjoint certified cores proves exact factorization with an arbitrary remainder. For k=5, if there are a K4 cores, b K3,3 cores and c prism cores, then

\[
|H(A)|=38^a328^b314^c|H(B)|.
\tag{5.3}
\]

This identity preserves numerical collisions inside each factor and excludes only additional collisions among the factor values. Section 6 proves that the possible core sets themselves are canonical components; no choice of a maximal packing remains in (5.3).

## 6. Canonical q-ary arithmetic components

A vector h is conformal to g, written h preceq g, when h_i g_i>=0 and |h_i|<=|g_i| for every i. A Graver element of the original row Phi_A is a nonzero integer kernel vector with no distinct nonzero conformally smaller integer kernel vector. This is the established Graver definition, e.g. Onn (2024), Section 1.3. The following argument keeps the literal coefficient boxes throughout.

For q>=2, take the hypergraph on the original generator indices whose edges are the supports of the Graver elements with norm_infinity<=q-1. Denote its component partition by Pi_q(A).

**Proposition 6.1 (canonical factorization).** Addition

\[
\prod_{C\in\Pi_q(A)}H_q(A_C)\longrightarrow H_q(A)
\tag{6.1}
\]

is bijective, and Pi_q is the unique finest coordinate partition with this property.

**Proof.** Every nonzero integer relation g decomposes conformally into Graver elements. Indeed, when it is not minimal, choose a nonzero proper h preceq g in the kernel; both h and g-h have smaller l1 mass, so induction terminates. If g is in the q coefficient box, every summand stays in that box.

Suppose two q-ary digit vectors have the same value. Their difference is such a bounded relation. Every Graver summand lies within one Pi_q component. Restricting the decomposition to each component shows that the two digit vectors have the same numerical value on that component. This proves injectivity in (6.1); surjectivity is the literal choice of component words.

For any other partition with injective addition, take a bounded Graver element g. Its positive and negative parts are actual q-ary words with equal value. Injectivity forces its restriction to each part of that partition to be a kernel vector. A nonzero proper restriction would be conformally smaller, contrary to minimality. Hence supp(g) lies entirely in one part of every independent partition. Therefore Pi_q refines every such partition, establishing uniqueness. QED.

The proof does not introduce new integer relations by taking rational spans. In particular it preserves which bounded boxes contain the primitive relation witnesses.

### 6.1 Exact arity filtration and a finite full primitive description

The admitted primitive set increases with q, so Pi_(q+1) is a coarsening of Pi_q. Equivalently each Graver support is retained with the threshold label

\[
q(g)=1+\|g\|_\infty.
\tag{6.2}
\]

At each q, the original generator set is partitioned by the supports whose thresholds have actually been reached.

There is also an elementary finite bound for the full one-row Graver family. Let M=max(A), and let g be a Graver element. Make the signed multiset having |g_i| copies of sign(g_i)*a_i. Let P be its largest positive term and N its largest absolute negative term. Starting at zero, choose a remaining positive term when the partial sum is nonpositive and a remaining negative term otherwise. Such a term exists because the remaining total is the negative of the current partial sum.

Every proper partial sum is nonzero, and no two proper partial sums coincide: a coincidence would give a nonempty proper zero-sum submultiset and a conformal subrelation of g. All proper partial sums lie in [1-N,P]. Consequently

\[
\|g\|_1\le P+N\le2M-1.
\tag{6.3}
\]

The final inequality uses distinct positive original weights: P and N belong to different signed indices and are distinct values. The order of the signed terms and all partial sums are retained; no generator is scaled.

Thus all Graver elements can be enumerated within a stated finite l1 ball. A sharper bound for complete merging needs only the two-coordinate primitives

\[
\frac{a_j}{\gcd(a_i,a_j)}e_i-
\frac{a_i}{\gcd(a_i,a_j)}e_j.
\tag{6.4}
\]

They are conformally minimal and have infinity norm at most M. Hence Pi_q has one component for every q>=M+1 when n>=2. This finite bound depends on the actual maximum generator; it does not supply a uniform all-rank extremal estimate.

### 6.2 Certified cores are whole canonical components

By (5.2), the bipartition into a core C and its complement is independent at q=2. Proposition 6.1 therefore puts each canonical component entirely on one side. Inside a critical clique, every triangle supplies an actual signed relation with three supported generator coordinates. Inside K3,3, the four-cycles connect the edges; inside the prism, the two triangles and its rectangular four-cycles connect every edge.

All of these short cycle relations are binary Graver elements. A nonzero signed relation on distinct positive weights has at least three supported coordinates. A conformal decomposition of a three- or four-coordinate signed relation would have disjoint supports, each of size at least three, which is impossible. The short-cycle supports therefore join all coordinates of a core inside Pi_2.

Combining the two facts, C is exactly one Pi_2 component. Any two certified cores must be disjoint or identical as generator sets. For k=5, K4 has six coordinates while the cubic cores have nine. A set simultaneously realized as a K3,3 and prism core would have, by faithfulness, both 328 and 314 binary values. Thus those graph types cannot have the same actual set in a five-admissible ambient set.

This proves a canonical decomposition into all certified cores and the remaining Pi_2 components. It does not assert that every remaining component has one of those graph forms.

## 7. Exact prism moments, original multiplicities, and finite bounds

The prism source has the multiplicity distribution

| Original masks per score | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| Distinct scores | 204 | 66 | 24 | 2 | 12 | 6 |

The counts sum to 314 scores and 512 masks. For the uniform distribution on DISTINCT scores, the mean is (3/2)1. Its covariance in the original vertex coordinates has denominator 628, diagonal 573, off-diagonal within either triangle -195, matching cross-pair entries -181, and all other cross entries -1.

Let L_P be the graph Laplacian. Let u=(1,1,1,-1,-1,-1), P_part=uu^T/6, and let P_anti,0 be the orthogonal projector onto {(x,-x):sum x_i=0}. In the displayed order, its entries are

\[
(P_{\rm anti,0})_{ij}=\frac{\operatorname{sgn}(i,j)}2
\left(\mathbf1_{i\bmod3=j\bmod3}-\frac13\right),
\]

where sgn is +1 in the same triangle and -1 otherwise. The complete matrix identity is

\[
\boxed{\operatorname{Cov}(s)=
\frac{49}{157}L_P-\frac{13}{314}P_{\rm part}
-\frac8{157}P_{\rm anti,0}.}
\tag{7.1}
\]

All entries of this identity are independently checked from the actual 314 source values. For marks T, put Q=sum_edges(t_i-t_j)^2, D=sum_(i<3)t_i-sum_(i>=3)t_i, and delta_i=t_i-t_(i+3). Then

\[
\operatorname{Var}(L_T(s))=
\frac{49}{157}Q-
\frac{13}{1884}D^2-
\frac4{157}\sum_{i=0}^2(\delta_i-D/3)^2.
\tag{7.2}
\]

The negative terms and all cross coordinates are retained. These are moments of the unweighted image, not of the uniform orientation masks. The latter has covariance L_P/4; the map from 512 masks to 314 score values has the displayed nonuniform fibres.

For any canonical value factorization, original word multiplicities satisfy

\[
\mu_{A,q}(\sum_C y_C)=\prod_C\mu_{A_C,q}(y_C).
\tag{7.3}
\]

Hence the original quotient Gram diag(1/mu) tensorizes. The identity from this metric to the unit numerical-value metric has norm sqrt(max mu), retaining every factor. For a partition into a K4 cores, b K3,3 cores, c prism cores and remainder B, that norm is

\[
4^{a/2}6^{(b+c)/2}\sqrt{\max_y\mu_B(y)}.
\tag{7.4}
\]

Uniform measure on the DISTINCT global value image is the product measure by (6.1), so its variances add. If a five-admissible set is partitioned into h prism cores, M=314^h and Q=sum_(a in A)a^2. For M distinct integers, spacing gives Var >= (M^2-1)/12. Equation (7.2) therefore yields

\[
\boxed{157(314^{2h}-1)\le588Q.}
\tag{7.5}
\]

The retained correction terms give the stronger version before their removal. With N=max A and Q<=9hN^2,

\[
N\ge\left\lceil\sqrt{\frac{157(314^{2h}-1)}{5292h}}\right\rceil.
\tag{7.6}
\]

For h=1,2,3, the integer bounds are 55, 12009, and 3078707. Distinctness permits the further exact inequality Q<=nN^2-n(n-1)N+n(n-1)(2n-1)/6. These are bounds for the stated family, not new unrestricted values of g_5.

The prism claim is nonvacuous. The marks T=(0,1,5,25,125,625) give the nine generators

\[
A_P=\{1,4,5,25,100,124,500,600,620\},\quad S(A_P)=1979.
\]

Its 314 actual subset sums are five-AP-free modulo 3125. The producer checks this by exact rotations of the residue support; the separate auditor tests all 314 starts in the digit set and all 3124 nonzero steps, including nonunits. All other starting residues fail membership immediately. Since 1979<3125, ordinary digit lifting proves an infinite admissible family. This construction supplies an example, not a better global exponential rate.

## 8. The actual ternary merger and its additional kernel

Take

\[
C=\{1,4,5,17,21,22\},\qquad A=C\cup\{97\}.
\]

The existing base-97 modular certificate makes A five-admissible. Direct checking is also included. Its canonical binary partition is {C,{97}} and

\[
|H(A)|=38\cdot2=76.
\]

At q=3 the whole seven-generator set is one component. An actual admitted relation is

\[
\boxed{97=1+2\cdot5+2\cdot21+2\cdot22.}
\tag{8.1}
\]

The exact addition map on ternary factor values is

\[
J:\mathbb Q[H_3(C)\times\{0,97,194\}]
\longrightarrow\mathbb Q[H_3(A)],\quad
 e_{(x,y)}\longmapsto e_{x+y}.
\tag{8.2}
\]

Its source dimension is 139*3=417, its receiving dimension is 333, and it is onto. Thus

\[
\dim\ker J=84.
\tag{8.3}
\]

On the original ternary word module V=Q[{0,1,2}^7], let q_loc be the quotient to the source of (8.2), and q_full=J q_loc. The comparison sequence is

\[
0\longrightarrow\ker q_{\rm loc}
\longrightarrow\ker q_{\rm full}
\xrightarrow{q_{\rm loc}}\ker J\longrightarrow0.
\tag{8.4}
\]

Lifting each factor value to an original word proves surjectivity at the right. This is the exact additional receiving kernel; it is not identified with the old local relation module. Every zero digit, repeated representation, and support label remains present.

For comparison, adjoining the generator 6 to C gives the actual five-term progression (0,6,12,18,24), with masks in the receipt. That direct overlap witness and the admissible addition of 97 distinguish binary coupling from ternary coupling in the original arithmetic.

## 9. Transfer to the supported quotient and remaining objective

At an admitted support U of original digit words, use V_U=Q[U] and the map to the free module on its actual numerical image. Its kernel is the original value-representation relation subspace, with basis differences of words in one fibre. These maps commute with support inclusions. The reconstruction of this diagram through the original SplitZero functor sends a relation to its support-labelled zero; it does not delete U.

For a further value observation J, the original quotient and the receiving quotient are related by (8.4). The three K3,3 order-two examples additionally retain the integer class before scalar extension. The two second-round examples retain an original free class before adding an actual new progression consequence. These are different comparison kernels and are recorded separately.

The all-rank clique construction derives every new relation with an integer coefficient and an actual tuple in one fixed two-translate source. Its original boundary history is the list of alpha_h in (3.8), and its terminal identity is (3.9). Under any support-preserving receiving map the first nonzero observed step still produces the same arithmetic obstruction. No theorem about the Zeta source's unevaluated analytic weight is used to infer an arithmetic bound.

The new canonical components sharpen the remaining extremal problem. Efficient constructions can be organized by their actual binary components; certified clique and cubic cores cannot overlap or couple to the remaining binary values. But |H(A)|<=2^n for every n-generator set. Binary cardinality alone cannot prove an exponential lower base greater than two, whereas the present sharp k=4 base and several current upper records lie above two. The natural higher-arity observations introduce precisely the receiving kernels illustrated in (8.4). Their controlled arithmetic size, or another source invariant retaining them, remains necessary for a sharp general result.

No theorem here bounds the canonical remainder by a fixed list of graph types, bounds all arity-merger kernels uniformly in n, or evaluates the global infimum defining lambda_k. The cutoff (6.3) depends on max(A); this is an exact finite description for each original set rather than an estimate uniform in the unknown extremal height.

Exploratory cube calculations suggest additional cubic sources may admit multi-round certificates, but this release does not promote them to a complete theorem: its exported finite proof domains are precisely the prism and K3,3. A separate bounded search for improved prism modular marks found no improvement and is not used to exclude other constructions.

## 10. Reproducibility and exact evidence scope

Run from this contribution's repository root:

```sh
python research/canonical_isolation/certificates/build_certificate.py
python research/canonical_isolation/certificates/audit_certificate.py
python research/canonical_isolation/certificates/verify_arity_filtration.py
```

The first program uses the accompanying `exact_source.py`; the independent auditor imports neither file. The auditor reconstructs orientation fibres by dynamic edge extension, checks every original mask and relation coefficient, independently enumerates all graph automorphisms and their orbit cover, directly computes the exceptional first-round progression directions, and recovers the canonical partition by numerical image-cardinality splitting rather than by Graver support enumeration.

The complete clique replay covers all 3300 nonzero differences through m=5 and 15020 original root steps. Eighty-four actual orientation-pair examples at m=6,...,12 are separately labelled samples. The infinite theorem is Section 3, not an extrapolation from those samples.

The prism proof covers every one of its 4994 differences via 255 complete disjoint orbits. K3,3 covers all 5298 differences via 99 orbits, including all three integer-torsion and both second-round classes. Every local source point retains at least one actual mask, while the entire mask fibre is also stored. The literal modular prism audit checks 980936 possible starts-in-D/nonzero-step pairs.

Canonical factorization is cross-checked on all nonempty subsets of [1,12] of size at most five at q=2 (1585 cases), and all nonempty subsets of [1,10] of size at most four at q=3 (385 cases). All 385 shared arity transitions and four larger specified targets are replayed. Primitive counts are independently checked by proper conformal-subvector enumeration.

A further exact script checks all 154 subsets of [1,8] of size two through four. It retains 4180 signed one-row Graver elements with their literal alternating-word witnesses, and 1050 arity comparisons against independently split numerical images. The all-Graver coverage outside the finite enumeration bound is supplied by the proof of (6.3).

Nine deliberate corruptions are rejected by the independent auditor: altered source mask, altered root, missing orbit, nonbinary switch, erased multiplier two, false old-boundary coefficient, omitted covariance term, omitted canonical input, and false overlap mask. The scripts use explicit checks that remain active with `python -O`. Exact final replay and archive statuses are bound by the integration receipt; this note does not substitute a written command for an observed run.

No new Lean source or receipt is introduced. Mathematical novelty is not asserted for the classical orientation criterion, Graver bases, conformal decomposition, or discrete variance spacing inequality. The theorem-specific contribution is the integral all-rank clique derivation, universal two-translate isolation application, exact prism and K3,3 proof layers, and their canonical arithmetic-factor and receiving-kernel consequences.

## References and inspected source roles

Kolesnik, B., & Sanchez, M. (2024). The geometry of random tournaments. *Discrete & Computational Geometry, 71*, 1343–1351. DOI: 10.1007/s00454-023-00571-4. Inspected: the primary HTML body, especially Corollary 4.2. Role: classical integral orientation-score cut criterion. The specialized multigraph, cut bounds and root derivation are proved in Section 3 above.

Onn, S. (2024). *Circuit and Graver walks and linear and integer programming* (arXiv:2410.00656v1). Inspected: primary HTML, Section 1.3 and the discussion of conformal decomposition. Role: established definitions and literature context for Graver elements. No oracle complexity result is imported into this contribution.

Onn, S. (2010). *Nonlinear discrete optimization: An algorithmic theory*. European Mathematical Society. DOI: 10.4171/093. Publisher metadata and abstract inspected; no unread book theorem is cited as a proof input.

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1). Primary HTML inspected for problem conventions and general-bound context. No new global bound is asserted here against that benchmark.

KokunoYumeto. (2026). *Reconstruction with changes of support index*. `workbenches/splitzero-tandem/tex/support_diagrams.tex` at revision `58626a62cd5648e8ae7450fb54d4a4aab2330981` in `KokunoYumeto/zeta-function-research-reader`. Exact blob `d3493f891291ee6e94dbf2c77649f7d85d240df2`; equations D6–D8 reread. Role: original support quotient and receiving-kernel interfaces, not an analytic arithmetic estimate.

The Clankers. (2026, September 15). *Defect closure, synchronized witnesses, and isolated graphical cores*. Delivered `EP817_DEFECT_CLOSURE_20260915` research package. Role: immediate predecessor, containing finite closure and the earlier K4/K3,3 isolation route. Preserved unchanged in this release's lineage.
