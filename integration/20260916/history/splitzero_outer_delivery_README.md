# SplitZero outer-parameter control

This additive contribution extends the existing `research/splitzero_transfer/` branch. It uses the Zeta workbench's support-index reconstruction and original-section metric bookkeeping, rather than assuming a Zeta arithmetic estimate transfers to this problem.

The [complete proof note](notes/outer-support-control.md) establishes support-preserving bounded realizations, the exact viable carry controller, and a finite global optimization for every fixed block size and progression length. The finite-cutoff theorem turns the complete arithmetic certificates into the following all-block/all-schedule results:

| fixed generators per level | k=5 optimal rate | k=6 optimal rate |
|---:|---:|---:|
| 1 | sqrt(8) | sqrt(8) |
| 2 | sqrt(5) | sqrt(5) |
| 3 | cube root of 13 | cube root of 13 |
| 4 | fourth root of 23 | fourth root of 23 |
| 5 | fifth root of 65 | fifth root of 47 |

Each entry allows every positive distinct block of that size and every infinite canonical mixed-radix schedule with the same block at each level. For rank five, all 41,185 candidate blocks at k=5 and all 6,074 at k=6 in the proved exhaustive domains are classified. An independent verifier checks their exact return primitives, every viable-controller transfer, every discarded support, and every positive-potential inequality.

The unrestricted rate remains the infimum over unbounded block size. This contribution does not claim that infimum has been evaluated for general k. No new Lean build was performed. The prior mathematical and formalization credits are retained in the proof note and source inventory.

## Replay

The following commands use Python's standard library only. Run them from the repository root. Output JSON paths below are newly generated records; the shipped complete records are stored losslessly as gzip files.

```sh
python research/splitzero_outer/certificates/verify_outer_control.py --output /tmp/outer_control.json
python research/splitzero_outer/certificates/verify_rank_five.py --k 5 --output /tmp/rank5_k5.json
python research/splitzero_outer/certificates/verify_rank_five.py --k 6 --output /tmp/rank5_k6.json
python research/splitzero_outer/certificates/audit_rank_five.py /tmp/rank5_k5.json /tmp/rank5_k6.json --output /tmp/rank5_audit.json
python research/splitzero_outer/certificates/verify_negative.py /tmp/rank5_k5.json --output /tmp/negative_audit.json
```

The k=5 producer also supports bounded exact shards. The executed index partition was `[0,10000)`, `[10000,20000)`, `[20000,30000)`, and `[30000,41185)`. Each shard was independently audited. The merger checks every actual generator list against the complete ordered enumeration before joining records.

```sh
python research/splitzero_outer/certificates/verify_rank_five.py --k 5 --start-index 0 --stop-index 10000 --output /tmp/k5_0.json
# Repeat for the other three stated intervals, with distinct output paths.
python research/splitzero_outer/certificates/merge_rank_shards.py /tmp/k5_0.json /tmp/k5_1.json /tmp/k5_2.json /tmp/k5_3.json --output /tmp/rank5_k5.json
```

The independent auditor accepts the shipped `.json.gz` files directly. It checks the exact covered indices and states their scope in its output. [The compact summary](certificates/verification_summary.json) records full plaintext and compressed identities. [The complete joined audit](certificates/complete_rank_five_audit.json) retains all four k=5 interval receipts and the full k=6 audit. [The negative regression receipt](certificates/negative_audit_receipt.json) records six rejected deliberate corruptions.

The outer-control replay was repeated under `python -O` with byte-identical output. All shipped checkers retain their checks under optimized Python. Finite parameter and metric regressions corroborate their accompanying general proofs; the exact capacity table instead uses a proved finite cutoff plus a complete finite proof record.

## Source state and integration

Zeta source: `KokunoYumeto/zeta-function-research-reader`, commit `42df8a2de002d5fc7090641fac46ea11be05fa71`. Existing SplitZero transfer: `KokunoYumeto/erdos-problem-817-workbench`, commit `98fd25802a387138053064e11ddd2f6d2007d55b`. Main remained at `23c0110c95b5a2036bdc04a1f352b6e5e27742c8` on the final read.

This directory is new and separate. No existing Lean file, receipt, mathematical claim catalogue, source note, or branch was changed. The current connector exposed repository reads without a write action; no remote write is claimed. The delivered patch adds only `research/splitzero_outer/` and is tested independently of the existing drafts.
