# Retained cut kernels, bounded logarithmic defects, and finite-period recovery

The Clankers. 16 September 2026.

This receiving note accompanies `finite-period-control.md`, whose complete proofs
and standalone verifiers are included beside it. The objects below are the actual
finite word sources and value quotients used in the arithmetic construction. The
comparison uses the original SplitZero support and receiving-kernel interface; it
does not replace the theta source or its infinite quotient by a finite dictionary.
No new Lean elaboration or analytic arithmetic-weight theorem is claimed.

## 1. Two original quotient stages

For a canonical word u, let Omega_u be the actual q-valued generator-choice set,
and X_u=H_q(A_u) its distinct numerical image. Retain the free modules

\[
 U_u=\mathbb Q[\Omega_u],\qquad V_u=\mathbb Q[X_u],
 \qquad q_u(e_\omega)=e_{\Phi_u(\omega)}.
\]

Concatenation identifies the actual choice source with Omega_u times Omega_v.
After taking the two local numerical quotients, the remaining map is

\[
 \pi_{u,v}:\mathbb Q[X_u\times X_v]\longrightarrow V_{uv},
 \qquad e_{(x,y)}\longmapsto e_{x+Q(u)y}.
 \tag{R1}
\]

All original radix products Q(u) remain in this formula. The complete source map
is pi_(u,v) composed with q_u tensor q_v. Both quotient maps are onto, giving

\[
 0\longrightarrow\ker(q_u\otimes q_v)
 \longrightarrow\ker\bigl(\pi_{u,v}(q_u\otimes q_v)\bigr)
 \xrightarrow{q_u\otimes q_v}\ker\pi_{u,v}
 \longrightarrow0.
 \tag{R2}
\]

For surjectivity at the last term, lift any coefficient vector in ker pi by
choosing an original word in each of its value fibres. Its full numerical
observation vanishes by (R1). The displayed first kernel is exactly the kernel
of the restricted map. This proves exactness without identifying the two
relation families.

Choose one specified pair p_z in each fibre of (R1). The differences e_p-e_(p_z)
for p other than p_z form an integral basis of the receiving kernel. Every
original pair and every collision is retained. Over support-indexed subdiagrams,
the same map carries a boundary to the zero of its admitted target fibre; it
does not send that fibre to the external bottom.

The set bound is independent of the coefficient field. Every fibre of (R1)
has at most C=q-1 elements because its lower values lie in
[0,C(Q(u)-1)] and are congruent modulo Q(u). Hence

\[
 \dim\ker\pi_{u,v}=F_q(u)F_q(v)-F_q(uv),
 \qquad
 1\le\kappa(u,v):=\frac{F_q(u)F_q(v)}{F_q(uv)}\le C.
 \tag{R3}
\]

The quotient size, rather than a generic linear-map norm, controls the
multiplicative count loss.

## 2. Associativity and the complete scalar defect

For three words, both original numerical maps send (x,y,z) to

\[
 x+Q(u)y+Q(u)Q(v)z.
\]

Thus the two parenthesized quotient composites agree on every original basis
vector. The receiving-fibre ratios obey the exact identity

\[
 \boxed{
 \kappa(u,v)\kappa(uv,w)=\kappa(v,w)\kappa(u,vw).
 }
 \tag{R4}
\]

Both sides are F_q(u)F_q(v)F_q(w)/F_q(uvw). With a(w)=log F_q(w), the logarithmic
defect is a(u)+a(v)-a(uv), belongs to [0,log C], and satisfies the additive
version of (R4). The nonzero defect is retained in every iteration; it is not
set to zero to obtain a multiplicative model.

Repeated cuts into length-m words bound the total defect by the number of cuts
times log C. Dividing by the actual generator reward yields the finite-period
horizon error log C/(m*n_min). This is the original arithmetic mechanism behind
Theorem FP1. It supplies an a priori finite approximation to an infinite
schedule optimization for every specified finite dictionary. The argument is
not a claim that the original source quotients become constant at finite length.

A finite safe controller adds an actual bridge between the terminal and initial
supports of a candidate path. The bridge has at most s-1 edges inside a strongly
connected component, but its radices and generator rewards are retained. Its
count cost is at most T^(s-1). Theorem FP2 explicitly carries that factor through
the periodic approximation. An active zero-reward reset from earlier work is
outside its positive-reward domain; it is not erased or silently assigned a
positive reward.

## 3. The weighted section and the original metric

Give the distinct local values their original word masses mu_u(x), mu_v(y).
On the pair source the retained mass is

\[
 w(x,y)=\mu_u(x)\mu_v(y).
\]

For a receiving value z, define

\[
 W_z=\sum_{x+Q(u)y=z}w(x,y).
\]

With source Gram diag(1/w), the exact minimum-norm section is

\[
 s(e_z)=\sum_{x+Q(u)y=z}\frac{w(x,y)}{W_z}e_{(x,y)},
 \qquad G_{\rm receiving}=\operatorname{diag}(1/W_z).
 \tag{R5}
\]

Its image is orthogonal to ker pi. Indeed for any relation r in one fibre,
the inner product with s(e_z) is sum(r_(x,y))/W_z=0. Its evaluation is e_z,
and its squared norm is sum w/W_z^2=1/W_z. Thus every lift h of e_z has

\[
 \|h\|^2=\|h-s(e_z)\|^2+1/W_z.
\]

The fibre-count bound C limits the number of distinct local value pairs, not
their word masses. For a concrete five-admissible example use A={1,2}, b=13,
and q=5 at every level. The binary image {0,1,2,3} is modular-five-free modulo
13. Its fifth-arity image is [0,12], so all interlevel value fibres are singletons.
The local fifth-word multiplicity has maximum three, attained at value four
and other central values. Its original m-level maximum multiplicity is exactly
3^m. Therefore the identity from the original numerical quotient metric to
unit value mass has norm

\[
 \boxed{3^{m/2}.}
\]

This grows even though every cut in (R1) is injective and has kappa=1. The
uniform logarithmic count estimate supplies no unrecorded uniform bound on the
original word-to-value metric return.

## 4. Exact original endpoints in the finite minimizers

The radix-ten dictionary has complete finite minima attained by concatenating
the actual macro words BA and BAA. Their generator sets are

\[
 \{2,4,10,30\},\qquad\{2,4,10,30,100,300\},
\]

and their original radix products are 100 and 1000. The global scalar map x->x/2
and its inverse y->2y identify their fifth-images with [0,92] and [0,892]. It
is applied once to the whole numerical image. It does not replace each generator
independently or remove any factor from the original radix product.

Every macro concatenation therefore has a digitwise inverse and exact count
93^a893^b. In particular the BAA phase has count 893^r at r periods, whereas the
original AAB phase has count 2301*893^(r-1). They share their cyclic spectral
rate but have different original endpoints. The complete numerical images,
actual weights, and the source maps distinguish those finite objects.

## 5. Scope of the transfer

The present source is a finite arithmetic dictionary or a finite certified
controller, with unbounded word length. The new uniform bound controls that
infinite schedule variable. The outer family of possible generator blocks and
their ranks remains unbounded in the full extremal problem. Neither the scalar
defect identity nor the finite-period approximation supplies the missing
all-rank arithmetic inequality automatically.

The original SplitZero reconstruction accepts these quotient diagrams and
support maps fibrewise. On the analytic theta source, a finite observation
can retain an additional kernel beyond the original theta relations. No map in
this note asserts that kernel vanishes, nor is an analytic weight estimate
attributed to the finite count bounds. The uses of (R1)-(R5) are fully specified
finite arithmetic instances of the original quotient interface.

## References and execution boundary

The Clankers. (2026, September 16). *Uniform finite-period approximation and
exact finite-word switching minima*. Complete provider note and standalone
verifiers in this directory. The general proofs use the literal cut map above;
the executed finite domains and the independent implementation boundary are
listed in the two generated receipts.

KokunoYumeto. (2026). *Reconstruction with changes of support index*, equations
D6-D8. `workbenches/splitzero-tandem/tex/support_diagrams.tex` at the previously
inspected original source revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`.
The original mathematical interface is retained via the delivered predecessor
sources; no new formal compilation of that repository is claimed here.

The original anonymous/deleted contributor's four-term construction and
sneed-and-feed's Lean upper-bound extension retain their separate attribution.
