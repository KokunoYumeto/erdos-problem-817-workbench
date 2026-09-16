# Supported resets and variable-block control

This add-only contribution contains the full proofs and exact evidence for schedules that change both generator blocks and radices. Its new general technique is a present zero-digit level with retained positive cost. The resulting bounded-block optimization is finite, and its all-rank dual uses finitely many potential coefficients in a proved compact interval.

## Read the mathematics

[Variable-block theorem and exact k=5,6 classifications](notes/variable-block-control.md) · [General translation-invariant integer-matrix theorem](notes/supported-reset-generalization.md) · [Compact all-rank dual](notes/compact-global-dual.md).

For k=5 or k=6, the exact rate is sqrt(8) with maximum block size one, sqrt(5) with maximum block size two or three, and 23^(1/4) with maximum block size four. These ranges allow every positive block of every admitted size and arbitrary infinite canonical schedules. They do not replace the separate fixed-block rank-five classifications.

The global rate is the infimum as the maximum block size grows. Equivalently, it is the largest u with a potential H in [1,2] satisfying b H(T)>=u^|A| H(R) on every actual safe AP edge. This is a proved exact dual, not an evaluation of the infinite arithmetic constraint family. The general conjecture and the matching large-k lower law remain unresolved by this contribution.

## Evidence and replay

The compressed certificates retain all literal levels, original subset masks, complete carry transition profiles, safe support graphs, rational potentials and periodic attainers. The separate auditor imports no producer code. The two rank-four records cover 41,571 literal levels each; every safe and rejected controller transfer is checked. Smaller maximum ranks are separately certified.

```sh
python certificates/verify_variable_blocks.py --k 5 --rank 4 --output certificates/variable_k5_r4.json.gz
python certificates/audit_variable_blocks.py certificates/variable_k5_r4.json.gz --producer certificates/verify_variable_blocks.py --output certificates/audit_k5_r4.json
python certificates/verify_reset_patterns.py --output certificates/reset_patterns_receipt.json
python certificates/verify_compact_dual.py --output certificates/compact_dual_receipt.json
```

The corresponding k=6 command and rank bounds one through three have also been executed. Normal and optimized rank-four producer runs were byte-identical. Eight deliberately defective records were rejected by the independent auditor. `certificates/verification_summary.json` binds the exact source and all evidence hashes; `polyclank/claims.json` separates proof scopes.

These are ordinary mathematical proofs and exact computational certificates, submitted for independent review. No new Lean elaboration, external human verification, or arithmetic zeta-weight theorem is claimed. All original support labels, quotient kernels, representation multiplicities and the tensor metric-return cost remain specified. No inherited Lean file or accepted status file is modified.

The original k=4 mathematical construction remains attributed to the anonymous/deleted Reddit contributor. The earlier finite-upper-bound Lean extension remains separately credited to sneed-and-feed.
