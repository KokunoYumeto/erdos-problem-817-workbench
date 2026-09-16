# Erdős Problem 817 research workbench

## Cumulative research collection — 16 September 2026

[Read the corrected collection](editions/cumulative_20260916/latex/collected_notes.pdf) · [Twenty-nine-note index](editions/cumulative_20260916/NOTE_INDEX.md) · [LaTeX](editions/cumulative_20260916/latex/collected_notes.tex) · [Complete original delivery](https://github.com/KokunoYumeto/erdos-problem-817-workbench/releases/tag/cumulative-2026-09-16)

The workbench now includes the cumulative research notes on general-k capacity, exact carry constructions, supported arithmetic relations, graphical and recurrence sources, image-count transfer, and switching optimization. The original k=4 proof and its attribution remain below; the subsequent research is a distinct contribution.

The new [finite-period theorem](research/finite_period/notes/finite-period-control.md) gives a uniform, explicit approximation of the best infinite-schedule image rate for any specified finite canonical dictionary. For coefficient arity q≥2 and least positive generator reward n_min, the best length-m word rate U_m satisfies

```
0 ≤ log U_m − log δ_q(D) ≤ log(q−1)/(m n_min).
```

The proof uses the original numerical cut map (x,y)↦x+P_u y, whose fibres have at most q−1 elements. It retains the actual radices and generator sets. Repeating a minimizing word gives quantitative periodic approximation; exact attainment by one finite period is not assumed. Finite controllers have an explicit additional cost for a real closing path.

For the earlier radix-ten dictionary A=(10,{1,3}), B=(10,{2,4}), the continuation determines every finite fifth-arity minimum. With a_0=1 and a_1=13,

```
a_(3r)   = 893^r                 (r ≥ 1),
a_(3r+1) = 93² · 893^(r−1)       (r ≥ 1),
a_(3r+2) = 93 · 893^r            (r ≥ 0).
```

Actual words built from BA and BAA attain these values. This refines the finite endpoint calculation; the infinite per-generator rate remains 893^(1/6), rather than a new unrestricted record. The [receiving-map companion](interfaces/zeta/workbenches/ep817-finite-period/notes/splitzero-receiving-map.md) gives the original kernels, exact concatenation defect, and the separate source-metric cost.

Fresh ordinary and optimized producer and independent-auditor runs reproduce the supplied finite-period results. The publication preserves the existing seven-observation correction L>3Q and repairs formula-conversion errors in the reading edition. [Publication notes](editions/cumulative_20260916/PUBLICATION_NOTES.md) distinguish current proofs and checks from historical receipts and the unmodified source archive. The new finite-period arguments are ordinary proofs with exact finite computation; no new Lean certification is asserted.

## The original k=4 result and its attribution



## September 16 research update

[Read the new contributions, full source lineage and integration checks](integration/20260916/README.md).


This is a focused, reviewable workbench for a proof posted to
`r/LLMmathematics` by a contributor whose account was later deleted. The proof
establishes

$$
\lim_{n\to\infty} g_4(n)^{1/n}=19^{1/3},
$$

where `g_4(n)` is the least `N` for which some `n`-element subset of `[N]` has
a subset-sum set containing no nonconstant four-term arithmetic progression.

The construction and proof route belong to the anonymous/deleted Reddit
contributor. The Clankers independently reconstructed the argument, made its
compressed steps explicit, checked it computationally, and formalized its
central algebraic and base-19 components in Lean. This is a result about the
`k = 4` exponential-rate subproblem, not a solution of every part of Erdős
Problem 817 and not an Erdős-Straus artifact.

The Lean contribution by [sneed-and-feed](https://github.com/sneed-and-feed)
in [pull request #1](https://github.com/KokunoYumeto/erdos-problem-817-workbench/pull/1)
extends the formalization from the digit language to the actual finite set of
distinct positive generators. Its main theorem states the upper bound for
every positive integer `n`, including the passage from complete three-generator
blocks to an `n`-element subcollection. This is a formalization of the existing
construction; the original mathematical attribution is unchanged. The
independent build and all 44 theorem axiom checks passed; see
[verification status](STATUS.md).

## Read first

- [Complete human-readable proof](output/pdf/ep817_k4_rate.pdf).
- [TeX source](paper/ep817_k4_rate.tex).
- [Verification status](STATUS.md) - exact ordinary-proof, Lean, computation, literature, and
  novelty status.
- [Checked Lean core](formal/lean/ErdosProblem817/Core.lean).
- [Finite-generator construction and upper-bound formalization](formal/lean/ErdosProblem817/Extended.lean).
- [Pull request review](reviews/pr1-integration.md).
- [Deterministic finite checks](certificates/verify_ep817.py).
- [Public provenance records](sources/) - no private identity material.

## Credit claim

The moderators retain contemporaneous private mod-mail or notification
evidence of the original Reddit username. The contributor may request any
public attribution they prefer; that private record can be used to validate a
claimant without publishing the deleted username. A claimant can contact the
moderators of r/LLMmathematics by modmail. The proof is theirs.

## Reproduce

The Python certificate requires Python 3.10 or newer and uses only the standard
library. From the repository root:

```console
python certificates/verify_ep817.py --output certificates/certificate_fast.json
python certificates/verify_ep817.py --extended --output certificates/certificate_extended.json
python -O certificates/verify_ep817.py
```

The final command is intentionally expected to fail closed: the validator
checks that Python assertions are enabled. Lean is pinned in
`formal/lean/lean-toolchain` and
`formal/lean/lake-manifest.json`:

```console
cd formal/lean
lake exe cache get
lake build ErdosProblem817.Core
lake build ErdosProblem817.Extended
lake env lean Main.lean
lake env lean Audit.lean
```

Run the two build commands sequentially. `Audit.lean` imports the extension and
prints the axiom dependencies of every theorem in Extended. The Core and
Extended checks have separate content-addressed records in
`certificates/lean_core_receipt.json` and
`certificates/lean_extended_receipt.json`; the state validator checks both.
The written lower-bound argument and real asymptotic squeeze are not covered
by the finite-upper-bound formalization.

To rebuild the paper with a TeX distribution containing `latexmk`:

```console
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error ep817_k4_rate.tex
```

The canonical checked copy is then placed at
`output/pdf/ep817_k4_rate.pdf`. Run the machine-state validator from the
repository root after rebuilding any artifact:

```console
python scripts/validate_workbench_state.py
```

## Review posture

The ordinary proof is complete and has been independently reconstructed and
adversarially rechecked; the checkable evidence is the paper, formal modules,
and certificates above. Simone Costa's arXiv:2609.06303v1 separately answers
the historical `k = 3` lower-bound question negatively. This `k = 4` workbench
makes no novelty or priority claim. Community review, provenance corrections,
and a public credit claim from the contributor are welcome.
