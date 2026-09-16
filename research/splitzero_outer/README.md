# SplitZero outer-parameter control for Erdős Problem 817

This is the repository publication of the owner-delivered `EP817_SPLITZERO_OUTER_20260914.zip` (SHA-256 `95d5612ed25c8fbe1ae875e523c91b96e5352a3ef2425fd6d13d0090f816203b`). The complete mathematical note and all five production/audit programs below preserve their original bytes. The small archive verification records are retained as historical records; their original `remote_write_performed: false` describes the delivery before this publication.

[Full theorem–proof note](notes/outer-support-control.md) · [Prior complete rank-five audit](certificates/complete_rank_five_audit.json) · [Prior verification summary](certificates/verification_summary.json).

## Results and precise domain

For every fixed progression length k>=3 and number n of distinct positive generators per level, the optimum over all such blocks and all canonical mixed-radix schedules is attained and exactly computable. A benchmark radix Q restricts the complete block domain to sum(A)<Q; every block needs only radices sum(A)+1 through 2*sum(A)+2. Exact returning carry primitives determine the viable controller.

| n | k=5 fixed-block optimum | k=6 fixed-block optimum |
|---:|---:|---:|
| 1 | 8^(1/2) | 8^(1/2) |
| 2 | 5^(1/2) | 5^(1/2) |
| 3 | 13^(1/3) | 13^(1/3) |
| 4 | 23^(1/4) | 23^(1/4) |
| 5 | 65^(1/5) | 47^(1/5) |

Each entry allows the same block at every level, with every infinite canonical radix schedule. Changing the block at successive levels is a separately defined optimization. The unrestricted exponential rate is the infimum over all block sizes. That infimum has not been evaluated for general k.

The support-index quotient, original representation multiplicities, affine-signature transport, reversible integer realization, and full tensor metric-return cost are retained in the note. The source reconstruction is from Zeta commit `42df8a2de002d5fc7090641fac46ea11be05fa71`; the predecessor is Erdős 817 commit `98fd25802a387138053064e11ddd2f6d2007d55b`.

## Full reproducible proof records

The three full plaintext proof records are approximately 64 MB. Their lossless compressed copies occupy approximately 2.2 MB. The publication workflow regenerates them from the unchanged producers, checks the exact original plaintext SHA-256 values, independently audits every one of the 47,259 rank-five blocks, repeats the outer and negative suites under Python -O, and only then installs the compressed records and a fresh replay receipt.

Run from the repository root:

```sh
python research/splitzero_outer/certificates/publication_replay.py --jobs 2
```

The same program can run locally without GitHub access. Its expected source and full-record hashes are literal constants. Every producer/auditor is dependency-free Python; no assertions are disabled by optimized Python. The compressed representation may vary with the zlib version, but the complete decompressed bytes must match the original delivered records exactly.

Generated files are `certificates/outer_control_receipt.json.gz`, `certificates/rank_five_k5_receipt.json.gz`, `certificates/rank_five_k6_receipt.json.gz`, and `certificates/publication_replay_receipt.json`. A workflow definition alone is not evidence that a run succeeded: observed job conclusions and the resulting receipt identify the actual replay. The workflow never merges this branch or updates main.

The individual producer and independent-auditor entry points are also available:

```sh
python research/splitzero_outer/certificates/verify_outer_control.py --output /tmp/outer.json
python research/splitzero_outer/certificates/verify_rank_five.py --k 5 --output /tmp/k5.json
python research/splitzero_outer/certificates/verify_rank_five.py --k 6 --output /tmp/k6.json
python research/splitzero_outer/certificates/audit_rank_five.py /tmp/k5.json /tmp/k6.json
python research/splitzero_outer/certificates/verify_negative.py /tmp/k5.json
```

## Formalization and attribution

These are ordinary mathematical proofs and exact finite certificates submitted for independent review. No new Lean elaboration is claimed. Existing Core/Extended sources, their receipt hashes, the accepted claim catalogue, and the other research branches are unchanged.

The anonymous/deleted Reddit contributor retains credit for the original k=4 construction and signed-block proof. `sneed-and-feed` retains separate credit for PR #1's checked Lean upper-bound extension. No private attribution material is included. This continuation does not depend on the unformalized variance argument in PR #2.
