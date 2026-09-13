# Verification status

Last updated: 2026-09-13 (Europe/Berlin)

## Mathematical claim

The written proof establishes the finite bounds

\[
\frac{19^{n/3}-1}{2n}\le g_4(n)\le
8\,19^{\lceil n/3\rceil-1}
\]

for every positive integer `n`, and therefore determines the `k = 4`
exponential rate as `19^(1/3)`.

## Evidence layers

| Layer | Status | Exact scope |
|---|---|---|
| Written proof | complete, independently reconstructed | Entire finite bound and nth-root squeeze |
| Lean Core | passing, freshly rechecked 13 September | Bounded mod-19 kernel, digit rigidity, recursive all-length base-19 lifting, binary-block digit image, relation-splitting algebra |
| Lean Extended (PR #1) | passing; all 44 theorem axiom reports checked | Exact finite-generator/subset-sum bridge, distinctness and positivity of all generators, hereditary 4-AP-freeness, and the finite upper bound for every positive `n` |
| Lean not yet covered | open formalization work | Minimal signed-block decomposition, exact ternary quotient product, real asymptotic squeeze |
| Python certificate | passing | Exhaustive finite kernel, digit/AP, lifting, deletion, and bounded stress tests |
| Literature crosswalk | bounded, primary-source based | Erdős-Sárközy 1992, Erdős Problems #817, Korsky 2026, Costa 2026 |
| Novelty/priority | not claimed | Absence from checked sources does not prove novelty |

The theorem resolves the exponential-rate question for the `k = 4` subcase of
Problem 817. It does not address all of Problem 817 or determine every finite
value. Costa's arXiv:2609.06303v1 separately answers the historical `k = 3`
lower-bound question negatively.

## Finite upper-bound formalization

[sneed-and-feed](https://github.com/sneed-and-feed) contributed
[`Extended.lean`](formal/lean/ErdosProblem817/Extended.lean) in
[PR #1](https://github.com/KokunoYumeto/erdos-problem-817-workbench/pull/1).
The reviewed contribution is commit
`155523c57cf7576ae86304af02bc073f2567b8d0`.

The declaration `ErdosProblem817.erdos_problem_817_upper_bound` states that for
each natural number `n > 0` there is a finite set `B` of integers with exactly
`n` elements, every element between `1` and
`8 * 19 ^ ((n + 2) / 3 - 1)`, and no nonconstant four-term arithmetic
progression among its subset sums. Both the cardinality and the actual
subset-sum interpretation are part of the statement and proof. Subset sums
need not be distinct: the construction deliberately retains `1 + 7 = 8`.

The extension formalizes the upper construction already proved in the paper.
It does not extend formal coverage to the signed-block lower-bound argument
or the limiting real calculation. The mathematical construction remains
attributed to the anonymous/deleted Reddit contributor; the extension's
formalization is credited separately to sneed-and-feed.

Independent elaboration passed for Core, Extended, Main, and Audit, run
serially with Lean 4.32.0 and the manifest-pinned dependency cache. All 44
extension theorem declarations use subsets of `propext`, `Classical.choice`,
and `Quot.sound`. The full output and input hashes are recorded in
`certificates/lean_extended_axioms.txt` and
`certificates/lean_extended_receipt.json`. The earlier Core receipt is
preserved unchanged; it does not itself certify the extension. Source hashes,
run order, and the complete axiom inventory pass the machine-state validator.
The largest sampled physical process-tree working set was 3,475,734,528 bytes;
the watcher used a five-billion-byte limit with early preemption. The source review is recorded in
[`reviews/pr1-integration.md`](reviews/pr1-integration.md).

## Corrections to the source rendering

- `2m` means `2^m` in the diagonal-class count.
- `19r` means `19^r` in the valuation argument.
- The magnitude-one and magnitude-two relation layers have disjoint supports;
  that fact excludes accidental coefficients `±3` when their block
  decompositions are recombined.
- The least-differing-digit proof requires the explicit observation
  `v_19(|d|) < m`.
- The final `19`-class slogan is valid for a minimal three-coordinate block in
  a four-AP-free ambient set, not for an arbitrary triple with one visible
  signed relation.

## Attribution privacy

Public artifacts identify the proof source as an anonymous/deleted Reddit
contributor. Moderators retain contemporaneous private mod-mail or notification
evidence of the original username and can use it to validate a claimant without
publishing it. The contributor is invited to request any public attribution
they prefer: the proof is theirs. No private handle, inferred identity, or
search trace belongs in this repository.
