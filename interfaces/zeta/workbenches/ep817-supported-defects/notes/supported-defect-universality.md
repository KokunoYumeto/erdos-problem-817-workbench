# Supported zero actions, exact defect transport, and all-rank deformations

Research continuation, 15 September 2026. Ordinary mathematical proofs and exact bounded certificates; independent mathematical review pending. No new Lean elaboration or literature-priority claim is made.

## 1. Objective, original source, and conclusions

For a finite set A of distinct positive integers, retain its actual binary source, numerical image and representation multiplicities:

\[
 \Omega_A=\{0,1\}^{A},\qquad
 H(A)=\{\Phi_A(\epsilon):\epsilon\in\Omega_A\},\qquad
 \Phi_A(\epsilon)=\sum_{a\in A}\epsilon_a a,\qquad
 \mu_A(y)=|\Phi_A^{-1}(y)|.
\]

The empty binary choice is an actual source element. It has numerical value zero and is never removed. A positive-step k-progression is an ordered tuple (y,y+d,...,y+(k-1)d), d>0; negative steps are recovered by reversing the tuple. Let g_k(n) be the original EP817 maximum-generator minimum, and lambda_k its previously established nth-root limit. The new work does not improve the recorded numerical bound lambda_6 <= 1651^(1/10). It gives exact all-rank deformation and visibility results, and identifies where the unrestricted arithmetic instance survives those maps.

The inherited block is (1,7,8). Its construction and mathematical route remain attributed to the anonymous/deleted Reddit contributor; sneed-and-feed retains separate credit for the finite-upper-bound Lean extension. At EP817 main 23c0110c95b5a2036bdc04a1f352b6e5e27742c8, Core.lean contains the bounded mod-19 kernel and the all-length four-progression-free digit lift. That exact source was inspected, not rebuilt here.

The Zeta source was inspected at 58626a62cd5648e8ae7450fb54d4a4aab2330981. The used file `workbenches/splitzero-tandem/tex/support_diagrams.tex`, especially (D6)–(D8), retains the internal quotient, the receiving-boundary kernel and the distinction between fibre zero and external absence. Its original source blob is d3493f891291ee6e94dbf2c77649f7d85d240df2. No analytic zeta estimate is imported.

The principal conclusions are these.

**Theorem 1 (all signed perturbations).** Fix r>=1 and integers p_j,q_j,s_j, 0<=j<r. Put

\[
 M=\sum_{j<r}(|p_j|+|q_j|+|s_j|),\qquad L>2M,
\]

where L is an integer, and define the literal 3r-generator set

\[
 A_{L,\eta}=\bigcup_{j<r}
 \{L19^j+p_j,\ 7L19^j+q_j,\ 8L19^j+s_j\},
 \qquad d_j=p_j+q_j-s_j.
 \tag{1.1}
\]

Its generators are distinct and positive. For every k>=4,

\[
 \boxed{H(A_{L,\eta})\text{ is k-AP-free}
 \iff H(d_0,\ldots,d_{r-1})\text{ is k-AP-free}.}
 \tag{1.2}
\]

The right side is the image of the indexed binary cube, so repeated or zero d_j are retained as source coordinates. An explicit translation/reflection map relates it to the absolute-value list. Every k-AP on the left decodes to an actual k-AP in the right-hand image. Conversely, a fixed original fibre embeds every such right-hand witness back into the left side.

For k=3 the exact criterion is injectivity of the indexed ternary map sum t_j d_j, t_j in {0,1,2}. A zero defect is therefore treated differently from an absent coordinate: it prevents that injectivity.

**Theorem 2 (exact finite data transport).** For k>=4, the number ap_k of positive-step progressions, the distinct image size, and all representation multiplicities satisfy explicit subset transforms in Section 4. Two perturbations with the same entire defect vector have an explicit value-space bijection preserving those k-AP relations and the original quotient metrics. Every original parameter is retained in that map and its inverse.

**Theorem 3 (active-support rate).** For k>=4, minimize the largest generator in the special family p_j=q_j=0, s_j=h_j>=0, L>2 sum h_j, subject to exactly a positive, pairwise distinct defect amplitudes and k-admissibility. Call the result C_k(r,a). For any integers 0<=a_r<=r with a_r/r -> alpha,

\[
 \boxed{\lim_{r\to\infty} C_k(r,a_r)^{1/(3r)}
       =19^{1/3}\lambda_k^{\alpha/3}.}
 \tag{1.3}
\]

This is an exact optimum within this defined deformation family, not a formula asserting that the unrestricted lambda_k has been evaluated.

**Theorem 4 (supported degeneration).** The same zero-defect construction admits a graph representation with r edge-disjoint paths between two distinct vertices having equal arithmetic marks. Its nonzero terminal boundary remains present, and its scalar image is zero. A common perturbation t changes that action to -t. At t=0 the original relation complex gains one explicitly computed specialization class. At every t>0 in the stated separated range, the actual image has a longest progression of length r+1. The common-defect classification is proved for every r, not inferred from samples.

The companion `graphic-visibility-filtration.md` gives an all-graph theorem determining exactly which integral source direction modules are visible under an arbitrary integer mark observation. It explains the graph-side infinite obstruction in Theorem 4 without requiring globally distinct vertex marks.

## 2. General separation through the original word fibres

The following argument precedes the specialized construction. Let b_1,...,b_n be distinct positive integers, let eta_i be any integers, and set

\[
 M_- =\sum_i\max\{-\eta_i,0\},\quad
 M_+=\sum_i\max\{\eta_i,0\},\quad M=M_-+M_+.
\]

Choose L>2M and set a_i=Lb_i+eta_i. Positivity follows from a_i>=L-M>0. If b_j>b_i then a_j-a_i>=L-|eta_i|-|eta_j|>=L-M>0. Thus original labels correspond to distinct actual generators without any repeated-weight convention.

On the unchanged binary source Omega={0,1}^n retain

\[
 B(\epsilon)=\sum_i b_i\epsilon_i,\quad
 E(\epsilon)=\sum_i\eta_i\epsilon_i,\quad
 \Phi_A(\epsilon)=LB(\epsilon)+E(\epsilon).
 \tag{2.1}
\]

For each original value x in H(b), let

\[
 \Omega_x=B^{-1}(x),\qquad F_x=E(\Omega_x).
\]

Then

\[
 \boxed{H(A)=\coprod_{x\in H(b)}(Lx+F_x).}
 \tag{2.2}
\]

The notation denotes a genuinely disjoint union of numerical sets. All low values lie in [-M_-,M_+], an interval of width M<L, and the exact inverse is

\[
 x=\left\lfloor\frac{y+M_-}{L}\right\rfloor,
 \qquad u=y-Lx.
 \tag{2.3}
\]

It recovers both coordinates (x,u), not just x. The word-to-joint-value map and the joint-value-to-integer map factor the original Phi_A exactly.

Suppose H(b) is k-AP-free. Write a target progression as y_i=Lx_i+u_i using (2.3). Every low second difference has absolute value at most 2M. Consequently

\[
 L\Delta x_i+\Delta u_i=0,\quad |\Delta u_i|\le2M<L
 \quad\Longrightarrow\quad\Delta x_i=\Delta u_i=0.
\]

Admissibility makes the high progression constant. The low progression is nonconstant because the full one is. Therefore

\[
 \operatorname{AP}^+_k(H(A))
 \simeq\coprod_{x\in H(b)}\operatorname{AP}^+_k(F_x),
 \quad (x,(u_i))\longmapsto(Lx+u_i)_i.
 \tag{2.4}
\]

Formula (2.3) is its inverse. This proves both existence and full tuple correspondence.

The same proof works for an integer pattern matrix P with P1=0. For row i let m_i be its positive coefficient sum, also the absolute negative coefficient sum. Then |(Pu)_i|<=m_i M. Requiring L>(max_i m_i)M proves Px=Pu=0. When H(b) has only constant solutions of that specified pattern, every target solution is in one high fibre. This is a general finite-source comparison theorem with all actual offsets retained.

## 3. The nineteen-adic source and its complete short kernel

Let

\[
 B_r=\bigcup_{j<r}19^j\{1,7,8\},\qquad
 D=\{0,1,7,8,9,15,16\}.
\]

The elementary bounded-kernel identity is

\[
 u+7v+8w\equiv0\pmod{19},\quad u,v,w\in[-2,2]\cap\mathbb Z
 \iff (u,v,w)=(t,t,-t),\quad -2\le t\le2.
 \tag{3.1}
\]

For completeness, put p=u+w and q=v+w. Then |p|,|q|<=4 and |p+7q|<=32, so a multiple of 19 is -19,0 or 19. The value 19 forces (p,q)=(-2,3). The latter q forces w>=1, whence p=u+w>=-1, a contradiction. Negation excludes -19. The value zero forces q=p=0, proving (3.1).

The seven digits have no nonconstant four-AP modulo 19. This finite claim is included in the inherited Lean Core and is replayed directly over all 342 start/nonzero-step pairs. A symbolic proof can also project each binary block through (a,b,c)->(a+c,b+c): (3.1) makes both projected second differences zero over the integers; four values in {0,1,2}^2 have zero common difference. This forces their original digit values to agree.

Reduce an integer four-AP in H(B_r) modulo 19. Its low digits agree; remove that exact common digit and divide by 19. Induction proves four-AP-freeness at every r. Therefore H(B_r) is also k-AP-free for every k>=4.

Apply (3.1) at the least block of any integer short relation in B_r. Its three coefficients equal (t,t,-t) and its integer block contribution is zero, not an unrecorded multiple of 19. Divide by 19 and repeat. Thus

\[
 \ker\Phi_{B_r}\cap[-2,2]^{3r}
 =\{(t_j,t_j,-t_j)_{j<r}:t_j\in[-2,2]\cap\mathbb Z\}.
 \tag{3.2}
\]

For A_(L,eta) in (1.1), a short relation c obeys

\[
 L\Phi_{B_r}(c)+\sum_i c_i\eta_i=0,
 \qquad\left|\sum_i c_i\eta_i\right|\le2M<L.
\]

The integer high relation vanishes and (3.2) applies. The exact resulting map is

\[
 \boxed{
 \{t\in[-2,2]^r\cap\mathbb Z^r:\sum_jt_jd_j=0\}
 \overset\sim\longrightarrow
 \ker\Phi_{A_{L,\eta}}\cap[-2,2]^{3r},
 \quad t\longmapsto(t_j,t_j,-t_j)_{j<r}.}
 \tag{3.3}
\]

Its inverse reads the first coefficient of each triple. This is an identity of the original integral coefficient boxes; it does not identify unrestricted scalar kernels with incidence kernels.

A positive indexed generator family is three-AP-free exactly when its ternary evaluation is injective. One direction follows by expressing a three-AP as a binary second difference. Conversely a nonzero relation in [-2,2]^n can be written coordinatewise as u-2v+w with u,v,w binary. Its three numerical values either give a nonconstant AP, or are equal. In the latter case two distinct binary representatives, after removing their common chosen indices, give disjoint nonempty subsets of equal positive value a. The original image then contains 0,a,2a. This proves the criterion without assuming distinct subset sums. Applying it to (3.3) proves the three-term statement in Theorem 1.

## 4. Every perturbation is controlled by its retained circuit defects

A high digit eight has exactly two representatives: the first two generators or the third one. The other six digits have unique representatives. For a word z=(z_0,...,z_(r-1)) in D^r, set

\[
 J(z)=\{j:z_j=8\},\quad x(z)=\sum_j19^jz_j.
\]

Choose the third generator as the specified representative at digit eight. The low anchor contribution of one digit is

| High digit | Actual low anchor |
|---:|---|
| 0 | 0 |
| 1 | p_j |
| 7 | q_j |
| 8 | s_j |
| 9 | p_j+s_j |
| 15 | q_j+s_j |
| 16 | p_j+q_j+s_j |

Let a_eta(z) be the sum of these anchors. Choosing the other representative at a digit eight adds exactly d_j=p_j+q_j-s_j. Therefore the complete fibre formula is

\[
 \boxed{
 H(A_{L,\eta})=
 \coprod_{z\in D^r}\left(Lx(z)+a_\eta(z)+H(d|_{J(z)})\right).
 }
 \tag{4.1}
\]

An original word in that fibre is specified by the unique non-eight choices and one binary choice for each eight position. Consequently, including all coincident low values,

\[
 \mu_{A_{L,\eta}}(Lx(z)+a_\eta(z)+y)
 =\mu_{d|_{J(z)}}(y).
 \tag{4.2}
\]

The map from each original subset mask to its high word and its actual low mask is a bijection; (4.2) follows from its fibres. This retains each zero d_j: both binary choices still exist when they have the same low value.

Since H(B_r) is k-free for k>=4, (2.4) applies. Every H(d|_J) is a subset of H(d). Conversely, the high word with every digit eight gives exactly the translated copy

\[
 L\,8\sum_{j<r}19^j+\sum_js_j+H(d).
 \tag{4.3}
\]

Embedding a low witness in (4.3) and decoding arbitrary target witnesses by (2.3) prove (1.2). A witness in another high fibre decodes, after subtracting its anchor, to H(d|_J) and then to H(d). The resulting section/retraction is on actual numerical APs, with original mask representatives available before passing to values.

Each fixed J has 6^(r-|J|) high words. Thus

\[
 \boxed{|H(A_{L,\eta})|
   =\sum_{J\subseteq[r]}6^{r-|J|}|H(d|_J)|,}
 \tag{4.4}
\]

and for every k>=4,

\[
 \boxed{\operatorname{ap}_k(H(A_{L,\eta}))
   =\sum_{J\subseteq[r]}6^{r-|J|}
      \operatorname{ap}_k(H(d|_J)).}
 \tag{4.5}
\]

These count distinct values and positive-step numerical tuples. The full representation profile is the disjoint union of the profiles in (4.2). In particular

\[
 \boxed{\max_y\mu_{A_{L,\eta}}(y)=\max_y\mu_d(y).}
 \tag{4.6}
\]

For the upper inequality, a subset-family representation injects into the full defect family by fixing all other choices to zero. Equality occurs in (4.3).

Negative defects have the explicit cube involution: flip the chosen bit at every negative coordinate. It satisfies

\[
 \sum_jd_j\epsilon_j
 =-\sum_{d_j<0}|d_j|+\sum_j|d_j|(\kappa\epsilon)_j.
 \tag{4.7}
\]

It preserves every representation multiplicity and is its own inverse on the indexed cube. Zero coordinates are fixed, not deleted.

### 4.1 Same-defect perturbations and the exact isomorphism they induce

Let (L,eta) and (L',eta') satisfy their respective separation inequalities and have the same literal defect vector d. For y in the first image, recover its high word z by (2.3) followed by its base-19 digits, and put

\[
 \Psi(y)=L'x(z)+a_{\eta'}(z)+
          (y-Lx(z)-a_\eta(z)).
 \tag{4.8}
\]

The inverse uses the primed division data and exchanges the parameters. Formula (4.1) proves both inverse laws. On each fibre this is a translation, so (2.4) proves preservation and reflection of all k-AP tuples for every k>=4. Formula (4.2) shows that the representation multiplicities and quotient metrics are retained exactly.

No global linearity on all integers is asserted. Its domain is the actual finite value image; its complete high-label decomposition is part of the map. In particular the kernels and offsets of the original arithmetic parameters are not discarded.

For the parameter homomorphism

\[
 D:\mathbb Z^{3r}\to\mathbb Z^r,
 \quad (p,q,s)\mapsto(p_j+q_j-s_j)_j,
\]

one literal section is d->(0,0,-d). Subtracting this section from eta produces the retained element of ker D. Equations (4.8) and its inverse explain exactly what is preserved along that parameter fibre. The supported circuit action descends through the old high-value quotient precisely when every d_j=0. Indeed the old fibre differences are generated, as word relations, by the choice of the two representatives of each high digit eight, and their low observation is d_j.

### 4.2 The defect vector is the full original relative cohomology class

There is a geometric identification of D, not only a parameter analogy. Let Theta_r have terminals u,v and, for each j, a path with two new vertices a_j,b_j. Orient its three edges as

\[
 u\to a_j,\qquad a_j\to b_j,\qquad v\to b_j.
\]

Take the original integral relative cochain complex for the pair (Theta_r,{u,v}). A relative vertex potential vanishes at both terminals. In its actual internal-vertex coordinates (alpha_j,beta_j), the coboundary is

\[
 \delta^0(\alpha_j,\beta_j)_{j<r}
       =(\alpha_j,\beta_j-\alpha_j,\beta_j)_{j<r}.
\]

There are no two-cells. Therefore the entire relative cohomology sequence is

\[
 \boxed{0\longrightarrow\mathbb Z^{2r}
 \xrightarrow{\delta^0}\mathbb Z^{3r}
 \xrightarrow D H^1(\Theta_r,\{u,v\};\mathbb Z)
       \cong\mathbb Z^r\longrightarrow0.}
\tag{4.9}
\]

Indeed D delta^0=0. If p_j+q_j-s_j=0, the unique relative potential primitive is alpha_j=p_j, beta_j=s_j. Surjectivity of D is witnessed by the section (0,0,-d_j). For an arbitrary eta, its retained decomposition is

\[
 \eta=\delta^0(p_j,p_j+q_j)_{j<r}+(0,0,-d_j)_{j<r}.
\tag{4.10}
\]

Both summands and the original coordinates are recoverable; the first summand is an actual relative coboundary with its specified primitive.

The nineteen-adic high cochain itself is the relative coboundary of the potential (L19^j,8L19^j). Thus the actual generator cochain A_(L,eta) has relative class exactly d, with all original integer edge values retained. Theorems 1–2 say that, within this explicitly separated family, k-AP-freeness for k>=4 is determined exactly by this complete relative H^1 class. Formula (4.8) gives the numerical and metric comparison for changes by relative coboundaries. The proof uses the full constrained binary source; an abstract isomorphism of free groups alone is not substituted for that feasible-set comparison.

The absolute H^1 is the further quotient

\[
 0\longrightarrow\mathbb Z\xrightarrow{t\mapsto(t,\ldots,t)}
 H^1(\Theta_r,\{u,v\};\mathbb Z)
 \xrightarrow{d\mapsto(d_j-d_0)_{1\le j<r}}
 H^1(\Theta_r;\mathbb Z)\cong\mathbb Z^{r-1}
 \longrightarrow0.
\tag{4.11}
\]

To verify the map, the original absolute cycles are c_j-c_0, where c_j has edge coefficients (1,1,-1) along its path; evaluation gives exactly d_j-d_0. Its kernel is the diagonal terminal-action line and its surjectivity is explicit by choosing d_0=0. A common nonzero defect therefore has zero absolute H^1 class but a nonzero relative class. It is exactly the terminal-action component that creates the long arithmetic progression in Section 6. Forgetting it would lose an actual obstruction, despite leaving the absolute cohomology unchanged.

For inclusions of path supports, extension by zero on internal vertices, edges and defects commutes with (4.9)–(4.10). These are original support-diagram maps, with no assumed injectivity of an unrelated observation. The componentwise formulas work over any coefficient ring; the arithmetic statements retain Z, while the parameter specialization below uses the displayed Q[t].

## 5. Original supported quotient, relative kernel, and metric

Fix the original word set Omega and any admitted word support S subset Omega. Use the original base ring Q and its split semiring G(Q). Define

\[
 V_S=\mathbb Q[S],\quad
 W_S=\mathbb Q[B(S)],\quad
 Z_S=\mathbb Q[(B,E)(S)].
\]

The maps send basis words to their actual high values or joint values:

\[
 q_S:V_S\to W_S,\quad p_S:V_S\to Z_S,
 \quad f_S:Z_S\to W_S,\qquad q_S=f_Sp_S.
\]

All maps commute with inclusions of admitted word supports. Set R_S=ker q_S and R'_S=ker p_S. The actual exact sequences are

\[
 0\to R'_S\to R_S\xrightarrow{p_S}\ker f_S\to0,
 \tag{5.1}
\]

\[
 0\to\ker f_S\to V_S/R'_S\longrightarrow V_S/R_S\to0.
 \tag{5.2}
\]

Surjectivity in (5.1) follows by lifting a joint-value vector whose high observation vanishes. Its kernel is exactly R'_S. The two-term relation complexes therefore have a chain map from the refined to the original coarser complex, and (5.2) calculates the induced quotient kernel. A nonzero low defect has not been asserted to kill an old boundary; (5.1) retains its failure to do so.

Under the inspected SplitZero reconstruction, a relation maps to (S,0). External absence is the bottom support with its zero coefficient. The empty subset word belongs to every full binary source and remains an active basis vector e_0. Its final numerical-amplitude observation may vanish; that is a further specified map, with its own kernel.

Give the word basis its original orthonormal metric. For a high value x, let M_x be the number of its words, and m_(x,u) the size of its joint-value cells. Then

\[
 G^{\rm high}_{x,x}=1/M_x,\qquad
 G^{\rm joint}_{(x,u),(x,u)}=1/m_{x,u}.
 \tag{5.3}
\]

The minimum-norm section of f_S is

\[
 e_x\longmapsto\sum_u\frac{m_{x,u}}{M_x}e_{x,u},
\]

and its squared norm is

\[
 \sum_u\left(\frac{m_{x,u}}{M_x}\right)^2\frac1{m_{x,u}}
 =\frac1{M_x}.
 \tag{5.4}
\]

Thus the quotient of the refined metric is exactly the original coarse metric. On word space the two averaging projectors satisfy

\[
 P_{\rm high}P_{\rm joint}=P_{\rm joint}P_{\rm high}=P_{\rm high}.
\]

Their difference is the orthogonal projector onto the restored relative classes and has rank |(B,E)(S)|-|B(S)|. Orthogonality is proved by these projectors, not inferred from different support labels.

If exactly a of the r defects are nonzero, (4.6) and the retained zero bits give

\[
 \mu_{\max}(A)=2^{r-a}\mu_{\max}(d_{\rm active}),
 \qquad
 \|I:(\text{quotient metric})\to(\text{unit value metric})\|
 =2^{(r-a)/2}\sqrt{\mu_{\max}(d_{\rm active})}.
 \tag{5.5}
\]

This is the original metric return cost. In particular sublinear active support does not make the many zero-action representation choices disappear.

## 6. Zero terminal actions, actual graph homology, and specialization

Take a graph with terminals u,v and r internally disjoint paths of length three. For path j use vertices a_j,b_j and edges (u,a_j),(a_j,b_j),(v,b_j), with these displayed incidence orientations. Let c_j be the edge chain (1,1,-1) on that path. Its original boundary is

\[
 \partial c_j=e_v-e_u=:z\ne0.
 \tag{6.1}
\]

Assign marks t_u=t_v=0, t_(a_j)=L19^j and t_(b_j)=8L19^j. The actual positive edge weights are L19^j,7L19^j,8L19^j, all distinct. The nonzero source vector z has numerical observation zero. For all r, this is exactly the inherited four-AP-free arithmetic set L B_r.

Identifying u and v gives a bouquet of r triangles. The map on edge chains is the identity and the vertex map sends e_u and e_v to the same basis vector. The relative homology calculation is

\[
 0\longrightarrow H_1(\Theta_r;\mathbb Z)
 \longrightarrow H_1(\text{triangle bouquet};\mathbb Z)
 \xrightarrow{\partial}\mathbb Zz\longrightarrow0.
 \tag{6.2}
\]

The bouquet cycles are the c_j. Their linear combination has original theta boundary (sum alpha_j)z. Hence the first kernel is the free span of c_j-c_0, and the last map is their augmentation. This proves exactness and all generators explicitly. The vertex identification is licensed by equality of their actual marks, so every original edge value and every binary source mask is unchanged.

Choosing the positive or negative part of each c_j gives 2^r distinct subset masks of the common value 8L sum_j19^j. A supported zero action thus retains a fibre of size 2^r. Choosing neither part, one part, or both parts also gives an explicitly represented ternary image in the disjoint supports. No such choices are external absence.

Now change only the terminal mark to t_v=-t. The edge weights become

\[
 L19^j,\quad7L19^j,\quad8L19^j+t,
 \qquad\Phi_t(c_j)=-t.
 \tag{6.3}
\]

For fixed integer t>0 choose L>2rt. Formula (4.3) gives the actual progression

\[
 8L\sum_j19^j,\quad8L\sum_j19^j+t,\quad\ldots,\quad
 8L\sum_j19^j+rt.
 \tag{6.4}
\]

For r>=3, (1.2) applied at k=r+2 proves there is no longer progression, since the defect image is the r+1-point interval {0,t,...,rt}. At r=2 the same argument excludes four-APs and (6.4) has length three. At r=1, (3.3) has no nonzero short relation, so the image is three-AP-free and its longest progression has length two. Thus the longest progression has exactly r+1 terms for every r>=1 and t>0 in the stated separated range. At t=0 it has exactly three terms: the original block gives 0,8L,16L, and the inherited theorem excludes four terms.

For any epsilon>0 and k>=4, choose r=k-1 and L>max(2r,1/epsilon). Perturbing only each third weight by one changes every weight relatively by less than epsilon, but changes a k-admissible original family into a family containing (6.4). All original masks and all common-progression second-difference equations are retained; the terminal action changes from supported zero to a nonzero difference. This is an exact arithmetic statement about the effect of the perturbation, not an obstruction to studying the source by its full quotient data.

### 6.1 The specialization class and its first-order detector

Let R=Q[t]. Restrict to the original path-chain span U_J=R^J for a finite nonempty active path support J. Its differential to the scalar action is

\[
 d_t=-t\varepsilon_J,
 \qquad\varepsilon_J(x)=\sum_{j\in J}x_j.
 \tag{6.5}
\]

Over R, H^(-1)=ker epsilon_J and H^0=R/(t). On specialization t=0, the differential is zero, so H^(-1)=Q^J and H^0=Q. The exact additional class is

\[
 0\to\ker\varepsilon_J\to\mathbb Q^J
 \xrightarrow{-\varepsilon_J}\mathbb Q\to0.
 \tag{6.6}
\]

The rightmost Q is the Tor_1 contribution calculated by the literal free resolution R --t--> R of R/(t). Its sign in (6.6) is the actual -t in (6.5). A source lift x satisfies d_t x/t=-epsilon_J(x); this is the connecting map. Thus the first parameter derivative detects exactly the new class. The statements use a computed resolution, not an unspecified derived-functor comparison.

For J subset K, source inclusion and identity on the receiving scalar commute with augmentation. All maps and the added class therefore form the original type of support diagram. One may index by the finite active supports with a separately adjoined external bottom. At the active empty path set, U is zero but the receiving scalar remains R; it is not assigned the nonempty-support cokernel R/(t). Its map to a nonempty receiving quotient is the actual reduction R->R/(t). This retains the empty action chart and global absence separately.

The actual edge-chain norm of c_j is squared norm three, and different paths have disjoint supports. The quotient of Q^J by ker epsilon_J consequently has Gram 3/|J|, attained by the section with every coefficient 1/|J|. Its change with |J| remains in the comparison; no uniform Euclidean norm is substituted for it. At the word-fibre level the corresponding common-value Gram at t=0 is 2^(-|J|), consistent with the independently counted 2^|J| representatives.

## 7. Unbounded active-support control and its exact extremal cost

Consider the special deformation

\[
 A_{L,h}=\bigcup_{j<r}\{L19^j,7L19^j,8L19^j+h_j\},
 \quad h_j\ge0,\quad L>2\sum_jh_j.
 \tag{7.1}
\]

There are r active generator triples even when some actions h_j are zero. Let exactly a entries of h be positive and pairwise distinct; retain their positions and the zero entries. For k>=4, (1.2) says exactly that the positive active set is k-admissible.

Let C_k(r,a) minimize the largest generator among (7.1) with these conditions. At a=0,

\[
 C_k(r,0)=8\,19^{r-1}.
\]

For a>=1, the original definition of g_k(a) gives the exact comparison

\[
 8(2g_k(a)+1)19^{r-1}\le C_k(r,a)
 \le8(2a g_k(a)+1)19^{r-1}+g_k(a).
 \tag{7.2}
\]

For the lower bound, sum h >= max h >= g_k(a), and the last high triple has generator at least 8L19^(r-1). For the upper bound choose an actual minimizing active set for g_k(a), put it in any a distinct positions, and choose L=2 sum h+1. The separation and distinctness statements have already been proved, and the last perturbation is at most g_k(a). Thus (7.2) is a bound on the actual original integers, uniform in the positions of the active support.

For completeness, lambda_k exists by the exact composition A star B=A union (2S(A)+1)B. Euclidean division identifies the distinct subset-sum product. The low second difference is smaller than the radix, so every progression decodes to one in each factor. The cost 2S+1 is multiplicative. Its minimum F_k(n) is submultiplicative; writing n=qm+s and dividing its logarithm by n proves convergence to its infimum. Finally 2g_k(n)+1<=F_k(n)<=2n g_k(n)+1 transfers that limit to g_k. Powers of three give existence and the bound g_k(a)<=3^(a-1).

Take a_r/r -> alpha. When a_r tends to infinity, log g_k(a_r)=a_r log lambda_k+o(a_r). When it stays bounded its contribution divided by r is zero; if alpha=0, the uniform powers-of-three bound handles any sublinear unbounded subsequence. Taking logarithms in (7.2), retaining the O(log(a_r+1)) error, proves

\[
 \lim_{r\to\infty}\frac{\log C_k(r,a_r)}{3r}
 =\frac{\log19}{3}+\frac{\alpha\log\lambda_k}{3}.
\]

This proves (1.3), including alpha=0 and alpha=1. Infinitely many nonzero defect actions are therefore explicitly controlled even when their support grows; their density determines the precise additional exponential cost in this family.

The formula is a reduction to the original lambda_k, not a calculation of its value. At every alpha>0 the unknown arithmetic rate is still present with its stated exponent. The exact source-to-quotient return norm (5.5) also remains. The new theorem neither asserts an improved unrestricted upper record nor a matching general lower bound.

## 8. Mathematical implication for the general programme

Every indexed nonnegative defect list appears in the fixed high fibre (4.3). For positive distinct defect lists, this embeds every original EP817 instance. For k>=4 the correspondence has a witness decoder in the other direction; for k=3 the exact short-kernel map gives the same freeness equivalence for positive lists. Thus the full arithmetic problem is present inside separated deformations of one fixed, verified nineteen-adic source.

The successful infinite-family statement is not just an estimate for finitely many horizons. Sections 2–7 quantify over every r, every admitted integer perturbation, all original word fibres, and every k in the stated range. The common action t=0 versus t!=0 is completely classified, and its new class, derivative, and metrics are computed. The companion cut-tree theorem controls all integral graphical direction modules and their observation ideals.

The remaining general EP817 obligation is to control the actual defect images uniformly as the arithmetic input varies. A purely unconstrained linear identification is insufficient to perform that step, and its exact reason is visible rather than asserted: the row action (1,3,9) equals the augmentation row composed with diag(1,3,9), but that invertible rational map takes the binary box to {0,1} times {0,3} times {0,9}. The different original boxes are retained. The defect lists (1,1,1) and (1,3,9) have rational row complexes of the same ranks, while the first gives a four-AP and the second does not. Their literal feasible source fibres distinguish them.

This identifies the part on which a stronger all-rank inequality must act: the constrained arithmetic image and its original metric, together with the explicitly retained supported classes. It does not rule out such an inequality or claim a complete resolution of the general extremal problem.

## 9. Checks and exact evidence boundaries

The standalone producer and separate auditor use Python integers and Fraction. The auditor does not import or execute the producer. Both rebuild original source words. All new infinite statements rest on the written proofs; finite computations are corroboration and certificates for displayed finite constants.

The finite suite checks 43 full deformations through three triples, including all defect lists in {0,1,2}^r for r=1,2,3 and four stated additional lists; 4,002 admitted general separation instances; all 756 signed perturbations in {-1,0,1}^{3r}, r=1,2; all 256 word supports and 6,561 inclusions for the one-triple refinement; the parameter complex and actual path incidences; and the original 125-coefficient, 342-progression mod-19 checks. The separate auditor reconstructs 14,562 distinct deformation values and 162 positive-step APs in its 43 displayed cases. Its signed-perturbation scope is reported separately in the final receipt.

The companion graph suite covers all 1,099 labelled simple graphs on 1 through 5 vertices, 40,398 source-score values, 1,391,037 endpoint pairs, 1,152 explicitly checked component cut trees, 8,493 observations, 23,118 image-ideal calculations, and 15,147 original root-direction witnesses. The original graph cut theorem is classical; the full source visibility argument and exact observation filtration are provided in the companion note.

Corrupted source counts, missing supports, zeroed witnesses, false cut capacities, and false metric/zero-action assertions are required to fail. Source and receipt hashes and the normal/optimized replay results are in the delivery manifest. No earlier large arithmetic search was silently rerun or assigned a new verification label. No inherited Lean source or receipt is changed.

## References and exact roles

Anonymous/deleted Reddit contributor, & The Clankers. (2026, September 13). *The exponential rate for four-term-progression-free subset-sum sets* [Workbench manuscript]. EP817 main 23c0110c95b5a2036bdc04a1f352b6e5e27742c8. Role: original (1,7,8) construction and mathematical attribution.

sneed-and-feed. (2026, September 13). *Formalize finite upper bound theorem and core helper lemmas in Extended.lean* [Pull request #1]. Role: inherited formal upper-bound coverage; not verification of this continuation.

KokunoYumeto. (2026). *Reconstruction with changes of support index* [TeX source]. Zeta Function Research Reader, `workbenches/splitzero-tandem/tex/support_diagrams.tex` at 58626a62cd5648e8ae7450fb54d4a4aab2330981. Role: original reconstruction, internal quotient, and additional receiving-kernel interfaces, especially (D6)–(D8).

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1). https://arxiv.org/html/2606.24139v1 . Role: problem conventions and the general upper/lower benchmark, not a source of the new perturbation or specialization formulas.

The Clankers. (2026, September 15). *Graphical obstruction propagation and a stronger six-term construction* [Predecessor contribution supplied in this conversation]. Role: disjoint-path witness map, complete-graph rigidity and the retained base-1651 upper record. Its exact package is retained unchanged in the new delivery; its full audit was not rerun here.
