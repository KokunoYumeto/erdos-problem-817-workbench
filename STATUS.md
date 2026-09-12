# Verification status

Last updated: 2026-09-12 (Europe/Berlin)

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
| Lean | passing | Bounded mod-19 kernel, digit rigidity, recursive all-length base-19 lifting, binary-block digit image, relation-splitting algebra |
| Lean not yet covered | open formalization work | Minimal signed-block decomposition, exact ternary quotient product, real asymptotic squeeze |
| Python certificate | passing | Exhaustive finite kernel, digit/AP, lifting, deletion, and bounded stress tests |
| Literature crosswalk | bounded, primary-source based | Erdős-Sárközy 1992, Erdős Problems #817, Korsky 2026, Costa 2026 |
| Novelty/priority | not claimed | Absence from checked sources does not prove novelty |

The theorem resolves the exponential-rate question for the `k = 4` subcase of
Problem 817. It does not address all of Problem 817 or determine every finite
value. Costa's arXiv:2609.06303v1 separately answers the historical `k = 3`
lower-bound question negatively.

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
