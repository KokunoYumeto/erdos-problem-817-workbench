# PR #4 audit — SplitZero outer-control contribution

Reviewed head: `74ba7dcc4bd623b3555046feb6d45ccac38417a3`.
Repository: `KokunoYumeto/erdos-problem-817-workbench`.
Audit date: 2026-09-16. This audit made no remote changes and ran no Lean build.

## Primary claim and verdict

For fixed integers k >= 3 and n >= 1, minimize the limiting inferior radix-product rate over every n-element positive generator block A and every infinite canonical schedule b_j > sum(A) that has k-AP-free subset sums at every finite prefix. The optimum is attained, algebraic, and exactly computable by a finite search.

**Primary verdict: proved as written.** The proof is specific to the same block A at each level and canonical radices. It does not evaluate the infimum over all n and does not permit the block itself to vary between levels under this fixed-rank theorem. No claim of originality was audited.

## Proof audit

Source locators below refer to `research/splitzero_outer/notes/outer-support-control.md` at the reviewed head.

- Definitions and quantified scope: lines 7–46 and 59–88. Distinct positive generators, actual empty subset, canonical schedule, and limiting inferior are explicit.
- The signature transport (lines 207–250) correctly derives integral carries in {-1,0,1} from the strict canonical digit bound. Complete affine signs preserve every carry equation, binary representation fibre, order, and pair-sum equality in both directions. This supplies the Freiman-2 correspondence; it does not claim preservation of arbitrary unbounded integer relations (lines 254–276 explicitly retain the difference).
- The bounded-realization lemma (lines 280–320) uses a pointed nonnegative polyhedron, bounded Cramer/cofactor vectors, at most d nonnegative recession directions, and integer-part subtraction. The bound V_d + d R_d = 3*2^(d-1)*d! and coordinatewise decrease follow. This is separate from, and is not needed to substitute for, the sharper optimization cutoff.
- Return primitives (lines 339–385) supply actual next-column witnesses. A previously nonzero first difference cannot vanish after adding a multiple of the current place value because its magnitude is strictly smaller. Conversely b=2S+2 kills every nonreturning true carry and retains only constant false branches. Thus the viable support criterion is exact.
- Finite optimization (lines 387–406): all radices >=2S+2 have the same transition table; the finite graph minimum cycle mean gives the minimum liminf cost. Monotonicity proves that the minimizing period is safe even from the initial empty support. The benchmark Q excludes every S(A)>=Q strictly, and the base-three binary construction supplies the universal benchmark Q=3^n. Cycles are bounded by the number of safe states, and comparing integer powers computes their algebraic rates exactly.
- Global-rate passage (lines 471–501) retains the actual generator set and proves submultiplicativity for 2S+1. The polynomial factor between this minimum and g_k(n) disappears under nth roots. No unrestricted-rank optimum is asserted.
- Finite quotient/section/tensor formulas (lines 92–205) and exact chain-defect recurrence (lines 507–550) follow directly from their displayed maps and fibre counts. No Zeta arithmetic endpoint or determinant estimate is imported as a hypothesis.

No blocking mathematical defect was found in the inspected arguments. External priority and cited-source attribution are not authenticated by this review; the principal arguments above are given internally rather than depending on an unchecked external theorem.

## Computation evidence

All five original producer/auditor sources plus the publication driver and workflow were read. Producer and independent auditor use different transfer-enumeration paths; exact integer and rational arithmetic is retained. Runtime checks survive Python optimization.

Fresh bounded checks performed here:

1. Every original source hash and the publication driver hash match the execution receipt.
2. All three compressed record hashes and all three decompressed hashes match that receipt.
3. Reconstructed the full fixed-rank block domain independently from the auditor's increasing-tuple generator and checked exact record coverage: 41,185 blocks for k=5, Q=65; 6,074 for k=6, Q=47. The partitions are 38,782 / 2,172 / 231 and 5,906 / 150 / 18 for integer obstruction / complete return / controller.
4. Reran the six-mutation negative suite. Both baseline fragments passed; all six deliberately corrupted fragments were rejected.
5. Queried GitHub directly: Actions run `34891977899` is completed with conclusion `success`, on publication input commit `68d64ed4fe050d51e4247cecae79e419a48bad63`. URL: https://github.com/KokunoYumeto/erdos-problem-817-workbench/actions/runs/34891977899 . Its output receipt is now in the reviewed head and names all complete audit intervals.

Local records: `bounded_evidence_check.json`, `negative_recheck.json`, `source_manifest.json`. Exact received sources are under `source/`.

**Limit:** this review did not rerun the complete rank-five arithmetic auditor. The complete execution is evidenced by the live successful workflow and byte-matching supplied records; the fresh checks here independently cover identities, complete input coverage, code inspection, and representative mutation rejection. No new Lean verification is claimed.

## Workflow/data safety

Workflow is `pull_request`, not `pull_request_target`; it excludes forks and accepts only the literal same-repository research branch. Actions are commit-pinned. The branch SHA is checked before publication, the push is non-forcing to that exact research branch, and only three named compressed records plus the receipt are staged. No private paths, token reads, network requests, shell execution from record fields, or dependency installation appear in the Python programs. No main-branch write or merge occurs in this workflow.

Nonblocking hardening caveat: the computation job itself has `contents: write`, and checkout credentials persist while branch Python runs. The reviewed exact code has no misuse, but future edits on that authorized branch would execute with write access. Separating a read-only calculation job from a narrowly scoped publication job (or retiring this one-off publication workflow after integration) would reduce that future trust surface. This does not prevent merging the reviewed exact head as a research contribution.

## Recommendation

Merge PR #4 at the audited head, preserving its research-note status, finite certificate provenance, predecessor attribution, and explicit fixed-block/canonical scope. Do not silently promote it to a new Lean-verified theorem, a full solution of Problem 817, or a verified priority claim.

The Zeta-relevant connection to relay is the finite support quotient, original-metric section correction, tensor return cost, and exact return-primitive/viability construction. Those are concrete maps and formulas in Sections 2–3 and 6, not a claim about RH or an imported Zeta endpoint estimate.
