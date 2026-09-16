# EP817 PR2 and PR3 integration review — 16 September 2026

## Verdict and integration recommendation

Both are **proved as written**, at ordinary mathematical proof plus explicitly bounded exact certificate scope. Recommend integrating the exact reviewed revisions as additive research notes. No new Lean coverage, human peer review, or global priority finding is implied. No blocking defect found.

| PR | Exact head | Diff | Live merge check |
|---|---|---|---|
| 2 | `612020848e4bbec5f5a723a64c5fdc85636b5e83` | 3 new files, 752 additions, 0 deletions | open, draft, mergeable=true, clean |
| 3 | `a4ac40a60a91a45ab364f882904e07039b7ede27` | 4 new files, 1739 additions, 0 deletions | open, draft, mergeable=true, clean |

Observed base: `23c0110c95b5a2036bdc04a1f352b6e5e27742c8`. Each diff is disjoint from the other and from PR4/PR5. Fresh checks must still re-resolve the exact head before merging. No remote mutation was performed by this reviewer.

## PR2 claim and proof dependencies

For distinct positive generators A, n>=1, whose binary subset-sum image has no nonconstant four-term integer progression, let M be the number of **distinct** ternary sums and Q=sum(a²). With n=3q+r, 0<=r<3, the note proves M>=19^q·3^r and 19(M²−1)<=192Q. Thus the finite maximum-generator lower bound has denominator sqrt(n), rather than n in the earlier interval argument.

Read the entire 327-line note and 250-line checker, and the raw base manuscript's relation-splitting, disjoint minimal-block, signed decomposition, complete short-kernel and product-cardinality proofs. The new dependency chain is:

1. The coefficient layers of a short relation split into signed relations by an explicit four-progression witness.
2. Minimal signed relations have disjoint supports; the full short kernel is their unique bounded-coefficient sum.
3. Reflecting negative coordinates and subtracting the minimum produces one representative per diagonal class. The excluded representatives have generating polynomial z^(S_B/2) product(1+z^a).
4. The product of these local sections maps bijectively to the **distinct image**, so uniform image measure is genuinely a product measure.
5. Subtracting unnormalized moments gives kappa_m=(8·3^m−3·2^m)/(12(3^m−2^m))<=16/19 for m>=3.
6. The pairwise-distance identity gives Var(uniform M distinct integers)>=(M²−1)/12.
7. The exact residue-sensitive class count and integer finite constraints yield the stated bound.

Each implication passed. Empty block collections, free coordinates, n=1 and n=2, and M=1 in the general spacing lemma are handled. No inference from ternary cube multiplicity measure to uniform distinct-image measure is made.

## PR3 claim and proof dependencies

For every fixed k>=3 the maximum-generator nth-root rate exists. It equals the infimum of q^(1/|B|) over finite distinct-positive blocks with sum(B)<q and no ordered nonzero-step modular k-progression in their actual binary image. Composite moduli and repeated residues in modular progressions are included. A separate finite automaton decides all-length freeness for arbitrary nonnegative digit alphabets containing0, including digits>=q and signed carries. The displayed six-generator block gives all-n upper constructions at bases97 for k=5 and93 for k=6.

Read the entire 580-line note and 401-line checker. Dependencies checked:

- The exact product H(A)×H(B)→H(A∪(2S(A)+1)B) and mod/div inverse, distinctness, second-difference decomposition, and multiplicative sum cost.
- The written submultiplicative limit proof and its nth-root squeeze to the maximum-generator rate; remainder indices include0.
- Both directions between modular certificates and integer constructions. The second-difference bound excludes nonzero multiples of2S+1.
- Carry recurrence signs and telescoping; invariant signed box; terminal nonzero flag; reverse-path construction with zero padding for noncanonical digits; finite shortest witness bound.
- Separation by exact q-divisibility coordinates even for composite q; longer-prefix modular certificates converge to the carry-certified rate.
- All five finite modular examples, generator/image maps, and direct two-level constructions.
- Correlated six-column example and rectangular column-mass count use the stated domains. Neither replaces actual scalar/modular arithmetic tests.

Each implication passed. No general numerical evaluation of the infimum, finite stopping bound, sharp large-k theorem, or global novelty conclusion is claimed.

## External source check

Canonical corpus queried for `Korsky` in both layers (no hits) and `subset sums` (unrelated routing hits not used). Then authenticated the exact primary arXiv:2606.24139v1 HTML, title/author/version, definitions and Theorems1.2–1.3. Its upper-rate formula gives the cited comparison values at k=5,6; the new blocks' improvements reduce to integer-power comparisons. This is a scoped benchmark check, not re-refereeing the external paper or surveying subsequent priority. See `topic_route.json`.

## Fresh bounded computation

Command: `powershell -File run_bounded_checks.ps1` (run from any directory using the full file path).

Python3.13.9; standard library; actual runtime1.1043917s; observed peak working set23,146,496bytes. Watcher: 5,000,000,000-byte ceiling, 90-second timeout. Reviewed Python imports have no subprocess, network, checkout or remote-write behavior. All outputs remain in this private review folder.

Fresh PASS:

- PR2: all159 admissible subsets of[1,12] of size at most4;3 targeted multi-block/free-coordinate examples; exact abstract partition checks through n=200, coefficient checks through m=256, canonical cubes through dimension8, and6 negative/regression checks.
- PR3: all5 published modular blocks, each direct one- and two-level image;56 canonical alphabets at q=2..4 and k=3..6 with168 direct language comparisons;738 compositions from246 admissible left instances; the three-state carry-only example and a negative-carry witness.

This does **not** claim to replay the historical full PR2 domain[1,24] or PR3 exhaustive searches. No Lean run.

Raw receipt `fresh_bounded_checks.json` SHA256:
`49b3af156c22edb4f2f0a294c19c4286c1ef8f7c02d036b834a3670f0b83b7ff`.

Checker SHA256 values:

- PR2: `0dc30dd50e6040d0fc257df10cb28fd0aa43175d7d8391504d182a0263bc04d7`
- PR3: `bad43ea413381f1d1ce1635bd12bf20740b2ec75feeb8f3c789e4404bc5c1d20`

## Remaining boundaries

The finite code audit cannot itself establish universal proofs; those were separately read above. The new claims remain unformalized. Existing contributors' distinct mathematical/formalization credits should remain intact. Archive-era statements that remote publication had not yet occurred are historical provenance, not current repository status. No zeta-function theorem is asserted by these two PRs; carry-history tracking is reusable machinery but not an independently proved arithmetic zeta connection.
