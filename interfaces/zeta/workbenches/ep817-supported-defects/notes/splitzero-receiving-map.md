# Relative defect classes and the retained infinite visibility filtration

15 September 2026. Additive receiving contribution for the Zeta SplitZero
workbench. The full new proof bodies and standalone integer/rational
verification programs accompany this note. No arithmetic theta estimate,
Riemann-hypothesis conclusion, or new Lean elaboration is claimed.

## 1. Original source and the exact transferred statement

The receiving source is `workbenches/splitzero-tandem/tex/support_diagrams.tex`
at Zeta revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`, blob
`d3493f891291ee6e94dbf2c77649f7d85d240df2`. Equations (D6)–(D8) give the
original internal quotient, the additional receiving-observation kernel and
the supported-zero versus global-absence comparison. They are used here as
stated, with ordinary integer or rational module fibres and the original
reconstruction over G(R). No substitute scalar or homology definition is
introduced. The existing source file and all its verification records stay
unchanged.

The new calculation identifies an actual relative cohomology class controlling
an unbounded family of finite arithmetic sources. It also computes a complete
infinite graphical-direction filtration with its support-changing map and
original observation ideals. All statements have proofs in the two copied
companion notes; their bodies are byte-identical in the EP817 and Zeta payloads.

## 2. Relative cochains, original primitives and arithmetic feasible sets

Let Theta_r have terminals u,v and r paths of length three, with internal
vertices a_j,b_j and oriented edges u->a_j, a_j->b_j, v->b_j. Relative vertex
potentials vanish at u,v. The actual relative cochain sequence is

\[
0\to R^{2r}\xrightarrow{\delta^0}R^{3r}
\xrightarrow D H^1(\Theta_r,\{u,v\};R)\cong R^r\to0,
\]

where

\[
\delta^0(\alpha_j,\beta_j)
=(\alpha_j,\beta_j-\alpha_j,\beta_j),\qquad
D(p_j,q_j,s_j)=p_j+q_j-s_j.
\]

The inverse on the boundary image reads alpha_j=p_j and beta_j=s_j. The
specified class section is d->(0,0,-d), and the exact decomposition is

\[
\eta=\delta^0(p_j,p_j+q_j)_j+(0,0,-d_j)_j.
\]

The original high cochain consisting of L19^j,7L19^j,8L19^j is itself a relative
coboundary. When L>2 sum_j(|p_j|+|q_j|+|s_j|), every perturbed edge value stays
positive and distinct. The full original binary source then satisfies, for
k>=4,

\[
H\!\left(\bigcup_{j<r}
 \{L19^j+p_j,7L19^j+q_j,8L19^j+s_j\}\right)
\text{ is k-free}
\iff H(d_0,\ldots,d_{r-1})\text{ is k-free}.
\]

This uses more than an abstract cohomology isomorphism. The proof partitions
the original words by their exact high digits, retains all low anchors and
representation counts, and constructs inverse numerical maps for representative
changes. Every defect progression embeds in the high fibre whose digits are
all eight; every full progression decodes to an actual defect progression.
These are explicit constrained-source maps. For three terms, the separate
criterion is injectivity of the indexed ternary defect evaluation.

On the original absolute cycles c_j-c_0, restriction sends d to d_j-d_0.
Consequently there is the exact sequence

\[
0\to R\xrightarrow{t\mapsto(t,\ldots,t)}H^1(\Theta_r,\{u,v\};R)
\to H^1(\Theta_r;R)\to0.
\]

The common-action line is therefore visible in relative cohomology even when
its absolute class vanishes. This is the precise class producing the long
arithmetic progression under a common terminal perturbation.

## 3. Supported specialization and first-order detection

The actual path chains c_j have boundary e_v-e_u. Pairing an edge cochain with
these chains is precisely the defect row d. For the common third-edge change
t, the pairing is -t times augmentation. Over R=Q[t] and a nonempty admitted
path support J, retain the complex

\[
R^J\xrightarrow{-t\varepsilon_J}R,
\qquad\varepsilon_J(x)=\sum_{j\in J}x_j.
\]

Its cohomology is ker epsilon_J in the source degree and R/(t) in the receiving
degree. At t=0 the source kernel becomes Q^J. The exact additional class is
computed from the literal principal-ideal resolution:

\[
0\to\ker\varepsilon_J\to\mathbb Q^J
\xrightarrow{-\varepsilon_J}\mathbb Q\to0.
\]

The last Q is Tor_1^R(R/(t),Q), and the displayed map is obtained by dividing
the actual differential by t before specializing. It is the first-order
detector, not an assumed spectral or analytic comparison.

Zero extension on the admitted path supports and identity on the receiving
scalar give the original support diagram. At the active empty path support,
the receiving fibre is still R and the source is zero. Its receiving quotient
is R, not the nonempty-support R/(t). Global absence is an additional bottom
label. The nonzero terminal chain with zero arithmetic pairing remains in its
own admitted fibre throughout.

The edge-chain norm of each c_j has square three. The augmentation quotient
Gram is therefore 3/|J|. The common binary word fibre instead has 2^|J|
representatives and quotient Gram 2^(-|J|). These are separate original
presentations, with their computed metrics retained.

## 4. Infinite graphical filtration and finite receiving support

For any finite loopless multigraph G, write Sigma(G) for its actual orientation
scores. The integral span of directions of (q+1)-term source progressions is

\[
K_q(G)=\{z\in\mathbb Z^V:\sum_{v\in C}z_v=0
\text{ for every q-edge-connected class }C\}.
\]

The proof uses the classical Gomory–Hu cut-tree theorem. Low cut capacities
force the indicated zero charges, and edge-disjoint paths supply actual
progressions for every class-root generator. Integral-span combinations are
not declared feasible directions without their original source witnesses.

For an actual mark observation L_T, its image is the ideal

\[
I_{q,T}=a_q\mathbb Z,\qquad
 a_q=\gcd\{|t_u-t_v|:u,v\text{ belong to the same q-class}\}.
\]

The original exact sequence is

\[
0\to K_q\cap\ker L_T\to K_q\xrightarrow{L_T}a_q\mathbb Z\to0.
\]

A nonconstant visible source progression exists exactly when a_q>0. When
all its source directions have zero observed action, the source K_q remains;
it has not become an absent support.

The entire q-family is reconstructed on the semilattice of positive integers
with reverse order, together with bottom infinity and join min. The fibre at
infinity is zero; a zero fibre at any finite q remains supported. There is a
finite support map q->P_q, with infinity sent to a separately adjoined bottom.
It preserves joins and uses the identity on each coefficient lattice. Its
support coalescences are exactly the equal cut partitions. Thus every q value
and original coefficient is retained on the source while a finite target
controls all changes of the filtration.

When actual edge weights are positive and distinct, identifying only vertices
with equal arithmetic marks preserves every edge and creates a simple quotient
graph. Its relative cycle sequence is

\[
0\to H_1(G;\mathbb Z)\to H_1(\bar G;\mathbb Z)
\xrightarrow{\partial_G}\operatorname{im}\partial_G\cap\ker p_*\to0.
\]

The observation vanishes on the displayed relative module. The source masks
are unchanged and the quotient score masses are summed over their actual
p_* fibres. The induced minimum-section metric is the original weighted
quotient metric, not unit mass on the coarser score values.

## 5. Original word quotients and what still requires arithmetic control

For any admitted word support S, define V_S=Q[S], its high-value image W_S,
and its joint high/defect-value image Z_S. The maps q_S=f_S p_S commute with
all support inclusions. Their original relation families satisfy

\[
0\to\ker p_S\to\ker q_S\xrightarrow{p_S}\ker f_S\to0.
\]

The high quotient Gram is 1/M_x and the joint quotient Gram is 1/m_(x,u).
The minimum section has coefficients m_(x,u)/M_x. In particular representative
changes and the additional quotient kernel have exact source metrics.
For r path defects, with a nonzero active actions, the return to unit mass on
numerical values has norm

\[
2^{(r-a)/2}\sqrt{\mu_{\max}(d_{\mathrm{active}})}.
\]

This factor is not discarded. The companion active-support theorem gives
an exact asymptotic within its defined separated family,
19^(1/3) lambda_k^(alpha/3), for active density alpha. The unrestricted
arithmetic lambda_k remains in that formula; no general EP817 solution follows
merely from an unconstrained module equivalence or finite dimension count.

The present construction is a worked transfer of original supported quotient,
relative cohomology, specialization and observation-kernel techniques. It does
not replace the Zeta workbench's infinite theta quotient by a finite graph,
and it imports no unevaluated arithmetic weight estimate.

## 6. Sources and checking scope

The complete proofs, their primary references and exact finite domains are in
`supported-defect-universality.md` and `graphic-visibility-filtration.md`.
The cut-tree theorem is attributed to Gomory and Hu (1961) and Gusfield (1990).
The original nineteen construction remains credited to the anonymous/deleted
Reddit contributor, and the separate Lean upper-bound extension to sneed-and-feed.

The standalone producer and separate auditor are copied unchanged into this
receiving workbench, along with their complete compressed proof records and
receipts. A second independently implemented pair checks the faithful graph
quotient with original masks and relative cycle classes. Their exact source
hashes and evidence boundaries are in `polyclank/verification.json`.
No existing Zeta file or formal verification record is modified by this addition.
