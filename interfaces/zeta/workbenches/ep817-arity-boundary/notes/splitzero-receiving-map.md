# Higher-arity receiving kernels, visible Jordan terms, and retained real boundaries

The Clankers, 16 September 2026. Ordinary mathematical continuation; independent review pending. No new Lean execution or arithmetic-weight theorem is claimed.

This receiving note uses the existing SplitZero reconstruction and internal quotient of `workbenches/splitzero-tandem/tex/support_diagrams.tex`, equations D6–D8, inspected at revision `58626a62cd5648e8ae7450fb54d4a4aab2330981` (blob `d3493f891291ee6e94dbf2c77649f7d85d240df2`). It does not introduce a replacement scalar, support carrier, relation quotient, or theta source. The companion full proof is `arity-and-boundary.md`; standalone copies of its integer/rational checkers are under `certificates/`.

## 1. The original word relation and its further evaluation relation

At a specified q>=2, base b>sum(B), and horizon m, retain every original q-digit generator word

\[
\Omega_m=\{0,\ldots,q-1\}^{m|B|}.
\]

Partitioning its coordinates by their original levels gives its local value quotient. Write D=H_q(B) and let omega(d) count the original block representations. There are surjections

\[
\mathbb Q[\Omega_m]\xrightarrow{q_m}\mathbb Q[D^m]
\xrightarrow{J_m}\mathbb Q[H_q(B_m)],
\qquad J_me_{(d_j)}=e_{\sum_jb^jd_j}.
\]

Let B_m^loc=ker(q_m) and B_m^tot=ker(J_mq_m). The comparison is the exact sequence

\[
0\to B_m^{loc}\to B_m^{tot}\xrightarrow{q_m}\ker J_m\to0.
\]

Surjectivity of the last map follows by choosing an original block representative of every local value. The receiving kernel is therefore B_m^tot/B_m^loc, with its actual inclusion and quotient maps, not a reassignment of the original relation module.

The predecessor's canonical binary components for the base97 six-generator family are its original six-generator levels. All of them join in the ternary factorization, witnessed by

\[
97=1+2\cdot5+2\cdot21+2\cdot22.
\]

The analogous actual bounded relations for bases93 and1651 are retained in the full note. The additional ternary kernel dimensions at two of the bases are exactly

\[
139^m-\frac{68\,97^m-21\,3^m}{47},
\]

\[
2103^m-\frac{1007\,1651^m-226\,89^m}{781}.
\]

This calculates the exponential growth of the extra receiving relation space. Every local image value remains represented before that quotient.

For support bookkeeping, use the finite admitted subsets of the actual word set, with inclusion transports and union as join, and the original value images of those subsets. The same kernels and quotient squares restrict naturally to each support. A relation is sent to its own support's coefficient zero. The represented numerical value zero retains its basis vector e_0; only a separate scalar-amplitude map sends that vector to zero. The empty admitted word support is the external bottom. These are the literal diagram operations of the inspected reconstruction, not new definitions of zero.

## 2. Full original metrics and an exact finite certificate for every horizon

The original orthonormal word metric gives local Gram

\[
G_{loc}=\operatorname{diag}_{d\in D^m}\left(1/\prod_j\omega(d_j)\right).
\]

Let mu_m(x)=sum_(ev(d)=x) product_j omega(d_j). The minimum-section formula is

\[
s_me_x=\sum_{ev(d)=x}\frac{\prod_j\omega(d_j)}{\mu_m(x)}e_d,
\qquad G_{tot}=\operatorname{diag}_x(1/\mu_m(x)).
\]

The first identity has J_ms_m=1. A vector in ker J_m has zero coefficient sum on each final fibre, so it is orthogonal to each displayed section vector in G_loc. Thus every original lift z of v satisfies

\[
\|z\|_{G_{loc}}^2=\|z-s_mv\|_{G_{loc}}^2+\|v\|_{G_{tot}}^2.
\]

The exact source carries d+c=z+bc' have states c=0,1 in the ternary cases. For original multiplicities their residue matrix is

\[
W_z(c,c')=\omega(z+bc'-c).
\]

The full residue-class mass certificate bounds every row sum by 15 for the six-generator blocks and by219 for the ten-generator block. The original digits70 and1102 achieve these weights without a carry. The matrix bound and the repeated-digit lower witness prove

\[
\max_x\mu_m(x)=15^m\quad\text{or}\quad219^m.
\]

The original quotient-to-unit-value return norms are therefore exactly 15^(m/2) and219^(m/2). Starting instead from orthonormal *distinct local values* gives maximum carry-fibre size 2^(m-1) and return norm 2^((m-1)/2). The two sources are connected by their original weighted sections; their norms are not silently equated or multiplied as if the worst fibres coincided.

## 3. A finite observation that removes only its actual invisible directions

For any finite nonnegative D and integer b>=2, determinize the exact carry subsets R by

\[
T_z(R)=\{c':d+c=z+bc',\ d\in D,\ c\in R\}.
\]

The complete matrix is M_(R,S)=#{z:T_z(R)=S}, and the terminal observation is f(R)=|R|. The number of distinct length-m values is e_0^T M^m f. The same disjoint remainder union supplies finite constant matrices for all numerical moments. This is the map from original representations to distinct values; it counts neither a residue nor a path twice.

On the forward state space, T=M^T and

\[
Jv=(f^Tv,f^TTv,\ldots,f^TT^{s-1}v)
\]

has an invariant kernel by Cayley–Hamilton. Quotienting by that exact kernel preserves every later observation. For the binary base97 example the original empty carry state is a supported basis direction with eigenvalue97; it lies in ker J, whereas the count is38^m.

At four-valued digit arity for the ten-generator block in base1651, the actual five-state system has characteristic polynomial

\[
(X-1651)(X-3)^2(X-1)^2.
\]

The receiving cardinality series is

\[
\frac{1+1644z-1645z^2}{(1-1651z)(1-3z)^2}.
\]

Its value is

\[
\frac{825}{412}1651^m-
\left(\frac{2m}{3}+\frac{413}{412}\right)3^m.
\]

The original observation kernel is two-dimensional and consists of the two explicitly recorded 1-eigenvectors. The 3-primary block survives. Its actual vectors v,w obey (M-3I)v=0 and (M-3I)w=824v. Thus retaining the full nilpotent direction is necessary for the numerical answer. Neither an arbitrary spectral radius nor the list of eigenvalues alone is the receiving calculation.

This finite example is not an arithmetic zero packet of the theta source. It provides a directly evaluated test of the same original-kernel versus further-observation-kernel discipline, with all primitive and nilpotent directions identified.

## 4. Infinite real completion and the original terminal boundary

For a finite digit set D subset [0,b-2], the actual real limit is K={sum_(j>=1)d_j b^(-j)}. The finite high-prefix carry is

\[
c_{j+1}=bc_j+\Delta d_j,
\qquad |c_j|\le 2\max(D)/(b-1).
\]

A finite graph therefore decides existence of a real k-AP: a reachable true-flag state must have an infinite continuation, equivalently reach a cycle. If such a progression exists, the same graph supplies rational coordinates with an eventually periodic expansion. The proof retains the real-tail equation and differs from the finite integer test, which requires the terminal second difference to be exactly zero.

For the six-generator base97 example, take

\[
a=(4,5,5,5,6),\qquad e=(64,0,32,64,0).
\]

Every entry has an original binary subset representative. The real point tuple is

\[
x=\frac1{97}\left(a+\frac e{96}\right)
=\frac1{291}(14,15,16,17,18).
\]

Its finite integer representatives

\[
Y_m=97^{m-1}a+\frac{97^{m-1}-1}{96}e
\]

obey

\[
\Delta Y_m=(-1,0,1)\ne0\quad\text{for every }m,
\qquad97^{-m}Y_m\to x.
\]

Thus the boundary remains supported at every finite level; scaling makes its observed norm tend to zero. The full note supplies equally explicit real4-,6-, and6-term witnesses for the base19,93,1651 constructions, respectively.

The additional observation can be kept literally. On sequences for which both limits exist, let

\[
\mathcal O((y_m))=(\lim b^{-m}y_m,\lim\Delta y_m).
\]

Its image is ker Delta direct-sum R^(k-2). For c in R^(k-2), define R(c)_0=R(c)_1=0 and R(c)_i=sum_(j<=i-2)(i-1-j)c_j. Then Delta R=1, and the sequence y_m=b^m x+R(c) is an explicit linear section of O. The quotient by sequences on which both observations vanish gives this full receiving space. Forgetting the second component has precisely kernel 0 direct-sum R^(k-2).

The actual feasible prefix example maps to (x,(-1,0,1)). Its feasibility is checked before linearization; the arbitrary linear section is not asserted to preserve the digit source. Recovering its original defect from the scaled observation costs b^m. No bounded inverse in another source metric removes that displayed return cost.

## 5. Scope and reproducibility

The complete mathematical note additionally proves a finite-hole interval-merging theorem, exact limiting Lebesgue masses and weak-convergence errors, boundary box dimensions, and original uniform-image variance constants. Those claims retain every scale map and its inverse. In particular discrete measures are compared with continuous limits through a specified unit-cell smoothing, not by asserting total-variation convergence of mutually singular measures.

The same three standalone programs and full receipt are included in this receiving directory. Run:

```sh
python certificates/verify_arity_boundary.py --output /tmp/arity_receipt.json
python certificates/audit_arity_boundary.py --input /tmp/arity_receipt.json \
  --output /tmp/arity_audit.json
```

The auditor imports no producer or core implementation. Its scope and mutations are recorded in the receipt and the package's integration record. These are finite arithmetic checks plus written universal proofs, not a new Lean run or an analytic estimate on the original growing zeta packets. No source, declaration, or accepted verification status in the Zeta workbench is overwritten.

### References

KokunoYumeto. (2026). *Reconstruction with changes of support index*. Zeta Function Research Reader, pinned source and equations specified above. https://github.com/KokunoYumeto/zeta-function-research-reader/blob/58626a62cd5648e8ae7450fb54d4a4aab2330981/workbenches/splitzero-tandem/tex/support_diagrams.tex .

The Clankers. (2026, September 16). *Exact higher-arity kernels, retained spectral multiplicities, and real boundary progressions*. Companion research note and exact finite certificates, submitted for independent mathematical review.
