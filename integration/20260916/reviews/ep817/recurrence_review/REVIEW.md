# Recurrence-control intake review

Primary verdict: **proved as written**, for the explicit statements R1, R2,
R3, R4, R5, R5u, R5c, R6, and R6p in the recovered recurrence note. This is a
bounded independent agent review of those written arguments and their finite
certificates, not peer review, Lean verification, or a priority determination.
No substantive proof defect was found. The payload is safe to integrate at
its stated scope without changing the intake.

## Exact target

Delivered root:
`intake/ep817_recurrence/EP817_RECURRENCE_CONTROL_20260915/`.
The entire EP817 `notes/recurrence-control.md`, the entire Zeta receiving
`notes/splitzero-receiving-map.md`, both `source_and_claims.json` records, and
both certificate programs were read. The main note SHA-256 is
`8f389209ad2fec65f7a5498c26fc3c78cbb68a6b3bf5b8629fa22c74e43b8346`;
the receiving note SHA-256 is
`a99ec2576fc0a2b69f96761920d8781ff48add647973b11723c498dab2082ef6`.

The mathematical objects are positive integral generator sequences satisfying
the exact displayed gap inequalities, their full binary subset-sum sources,
the original integer relation matrices, their Hilbert completions with the
arithmetic observation retained separately, and explicitly indexed finite
carry automata. No altered generator scale, source domain, or quotient is used.

## Dependency and proof checks

| Claim | Dependency and decisive check | Verdict |
|---|---|---|
| R1 | Strict superincreasing evaluation gives unique binary words. A progression crossing the largest differing coordinate has step greater than the lower-fibre width; pigeonhole among the `2^r` top-word fibres gives the opposite inequality. | Passed for all stated positive integral gaps and all finite prefix lengths. |
| R2 | Coordinatewise induction makes every integral gap at least one; subtracting successive unit gaps gives the stated recurrence. Initial dyadic weights supply the exact longest progression. Positive recurrence comparison with the characteristic root proves the exponential rate. | Passed, including `r=1` and prefixes shorter than `r`. |
| R3 | Actual unit-pivot columns eliminate the largest coordinate, leaving `Phi(z)e_0`; the same elimination is a unique integral primitive. | Passed over the integers, including `n=1`. |
| R4 | With `m=r-1`, `D=-2I+S-(S*)^m` has negative real quadratic form equal to half the two displayed shift energies. Their lower bound is `2/m^2`. The adjoint has the same real form, giving dense as well as closed range. Truncated constant/plane-wave tests give the stated lower bounds; the semigroup integral follows from the same coercivity estimate. | Passed on each stated Hilbert coefficient space; lower/equality bounds correctly exclude the zero space. |
| Quotient/metric comparison | High-coordinate vectors have vanishing Hilbert norm and fixed arithmetic observation. The graph closure is the direct sum, with the written contraction and kernel. Least-norm sections give the two Grams and their exact determinant difference. | Passed; no claim that raw completion preserves the arithmetic class. |
| R5 | Two conjugate-embedding bounds force precisely the five stated integral carry coordinates. Scalar-zero terminals include the nonzero algebraic kernel. The first-two-word flag is valid because binary evaluation is injective. | Passed; both nonzero scalar-zero states are necessary and retained. |
| R5c | The complete graph counts oriented tuples and reversal divides by two. The 22-dimensional recurrence residual has 22 zero outputs, sufficient by Cayley–Hamilton. | Passed; the displayed 8-state restriction was also checked separately. |
| R5u | Rouche root count has no unit-circle endpoint root; the roots are simple. The unit-circle coercivity bound and derivative bound give the explicit stable-root gap. Exact observation weights control the expanding embedding, and Lagrange interpolation returns to the original integer basis. | Passed with the stated degree-dependent cutoff, not a degree-uniform box. |
| R6 | The seven masks evaluate directly to `x+j(b+c)`; the six delayed-recurrence indices are distinct for `r>=3`. At `r=2` the fourth mask has coefficient two after pushforward and exits the binary source. | Passed for the stated strictly increasing positive initial seeds and the first `2r+1` generators. |
| R6p | Disjoint actual motif supports let the `s` indices independently range over `0..6`, giving every total `0..6s`. | Passed with disjointness and equal positive difference retained. |

The Zeta receiving note faithfully retains the coefficient-module source,
free binary-word source, scalar observation, and support-index changes as
separate objects with explicit maps. Its interface does not establish an
analytic zeta/RH estimate. The parent review's exact source check and
`../topic_route.json` cover the cited support-diagram source and contextual
Korsky benchmark. This subreview does not independently authenticate those
external source passages, and the new recurrence proofs do not rely on a
Pisot-automaton theorem imported from an unread paper. No novelty claim is
made.

The abstract's broader wording about positive seeds is harmless for infinite
constructions: arbitrary positive seeds become strictly increasing after the
initial delay, and one can shift the motif there. The explicit first-`2r+1`
bound in R6 is correctly stated for increasing seeds; do not remove that
hypothesis when summarizing the bounded-index result.

## Executable checks

Both programs use only Python standard-library exact integers and rational
arithmetic. They do not start child processes, access the network, modify
input files, or execute archive-supplied shell commands. The only writes are
the requested result JSON. The fresh producer and auditor were run through
the parent's reviewed `run_bounded.run`, with a 5,000,000,000-byte direct-tree
working-set watcher and 180-second limit. No Lean process was started.

- `../recurrence_producer/manifest.json`: exit zero, 1.389 seconds,
  peak working set 23,175,168 bytes.
- `../recurrence_auditor/manifest.json`: exit zero, 2.818 seconds,
  peak working set 23,588,864 bytes.
- Both manifests pass the Mathbox manifest validator with their stated
  legacy-v1 provenance limitations. The runner separately records source
  hashes before/after and the effective watcher settings.
- All four carry graphs were re-enumerated independently: `(k,states,edges)`
  = `(3,8,26)`, `(4,22,46)`, `(5,27,28)`, `(6,49,50)`.
- Producer direct arithmetic covers Pell prefixes through 13; the separately
  implemented direct-pair auditor covers 33 counts through prefix 11.
- The auditor rechecks 2,186 gap sequences, 175 relation matrices, 97,655
  literal coefficient words (687 scalar-zero words, 3,589 prefix remainders),
  the seven-point motif and its alias failure, and rejects eight deliberate
  corruptions.
- `check_displayed_matrix.py` reconstructs coaccessibility from the fresh full
  graph, verifies all entries of the displayed 8-by-8 matrix, initial index
  3, and accepting indices 0, 4, 7. All four checks pass.

Fresh producer receipt SHA-256:
`9b1d814f75662fdba860af1845d7b3003300c9d7842308de39b5e6dd82bfb8a6`.
Fresh auditor receipt SHA-256:
`bd6e31db8adc936fac13c93e8b16f66a3a77a2422aa7dc3d8f7cee2d2ffb23ad`.

The fresh producer JSON is semantically identical to the delivered receipt.
Its different byte hash is entirely Windows CRLF versus delivered LF. The
fresh auditor JSON differs only in its correctly rebound producer receipt
hash (and line endings at byte level). Keep the original receipts unchanged;
do not describe the fresh runs as byte-identical reproductions. No
mathematical normalization or changed input is involved.

## Integration scope and route addition

Include the complete recovered `research/recurrence_control` contribution as
browsable source, retaining its code, original receipts, proof note, claims,
and attribution. The Zeta payload is a concrete receiving contribution worth
notifying the Zeta task about. The uniform inverse and finite algebraic
carrier are proved results in the stated recurrence model, not proofs of the
unrestricted EP817 extremal rate or of analytic-zeta arithmetic estimates.

Add source ID `DELIVERY-EP817-RECURRENCE-CONTROL-20260915` to the parent topic
route, with the two exact note locators above; reading status is full content
read. Relevant main-note sections are 1–10 and receiving sections 1–7. Its
dependency is `SPLITZERO-SUPPORT-DIAGRAMS-58626a6` for the named receiving
interface; the recurrence proofs themselves are written internally.
