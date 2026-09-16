# All-block image capacity and exact ternary transfer

[Full mathematical proof](notes/all-block-image-capacity.md) · [Exact producer](certificates/verify_all_block_image.py) · [Separate auditor](certificates/audit_all_block_image.py) · [Observed audit](certificates/independent_audit.json).

This add-only contribution continues the unbounded-block question in Erdős Problem 817. It proves that for every fixed k >= 3 the global exponential rate equals the infimum of |H_5(A)|^(1/|A|) over all admissible distinct positive generator sets. The same infimum is obtained at every fixed arity q >= 5. Here H_q counts each actual numerical value once and allows coefficients from 0 through q-1. No claim of attaining that infimum at a finite block is made; a complete k=3 example proves nonattainment.

The converse from small image cardinality to a cheap infinite construction is explicit. A prime retaining every necessary bounded arithmetic equation is selected with an elementary bound involving the original height. Tensor amplification is performed on the original weights before proving that its logarithmic height cost has vanishing exponential contribution. Digits exceeding the new prime remain actual digits. The construction does not replace a block by selected representatives or divide out a common factor.

For every canonical block, the entire ternary distinct-image count and its number of integer runs are governed by a two-by-two nonnegative integer matrix, independent of block size. Matrix products handle changing blocks and radices. A complete fixed-block collision dichotomy and a higher-arity witness horizon are proved. An actual five-admissible sparse schedule gives polynomial rather than exponential accumulated collision loss; its exact exponent and finite rational enclosures are included, so the fixed-block theorem is not overextended to varying schedules.

The quotient sequence, original pair fibres, section and reciprocal-multiplicity Gram are kept separately from the count vector. The Zeta companion generalizes the cardinality theorem to every specified binary-rigid translation-invariant integer pattern matrix, at an arity determined by its actual coefficient radius.

## Reproduce

From the repository root:

```sh
python research/all_block_image/certificates/verify_all_block_image.py
python research/all_block_image/certificates/audit_all_block_image.py
```

Only Python's standard library is required. `--output` writes an alternative receipt. The auditor also accepts `--receipt`. Both tools use explicit error checks, retained under `python -O`. The auditor imports neither the producer nor its helper library: it uses a four-state residue-subset automaton for cardinality, direct joins for the run statistic and kernel, and independent polynomial evaluation for the prime witnesses.

The complete finite replay covers 1,364 small digit alphabets, 5,456 joins, 3,171 generator/radix cases, 160 mixed schedules, 720 higher-arity collision cases, 191 prime records, 24 rational weighted quotient cases, and all 1,024 specified sparse-schedule prefixes. The independent audit has 9,548 finite-state length counts and separately recomputes eleven large sparse prefixes. Eight deliberately corrupted records are rejected. The note states every domain and distinguishes these tests from the general proofs.

## Scope and provenance

Ordinary mathematical proofs and exact finite checks; independent mathematical review pending. No new Lean elaboration, external human review, remote commit, PR, or merge is asserted by these files. The contribution provides no new best numerical upper rate and does not determine the unrestricted rate at general k. The unbounded rank remains in the exact cardinality infimum.

Erdős 817 main was inspected at `23c0110c95b5a2036bdc04a1f352b6e5e27742c8`. The actual SplitZero receiving interface is the source's equations D6--D8 in `support_diagrams.tex`, pinned to `58626a62cd5648e8ae7450fb54d4a4aab2330981`. The source and claim inventory retains their precise roles. No theta arithmetic estimate or old Lean receipt is silently extended to this work.

The anonymous/deleted Reddit contributor retains credit for the original k=4 construction and signed-block proof. sneed-and-feed retains separate credit for the checked finite-upper-bound Lean extension. The new global capacity argument does not assume that signed-block classification.
