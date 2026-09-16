# EP817 delivered continuation: independent integration review

Primary verdict: **correct only after a stated restriction in the seven-observable proof**. Its reflected test-set separation must be `L>3Q`, not `L>2Q`. This changes an auxiliary witness choice, not the theorem's mathematical domain or conclusion. The latest local-flow main proof and receiving note check as written. No new Lean verification or global EP817 solution is asserted.

## Audited statement and proof dependencies

For distinct positive generators A, retain H_q(A) with coefficients 0,...,q−1 and actual numerical values counted once. Binary k-admissibility concerns H_2(A). The reviewed proof chain is:

1. The all-block note gives an explicit prime avoiding every nonzero bounded difference, keeps its logarithmic generator-height cost, and removes its per-generator exponential cost only by the displayed amplification. This establishes the global fifth-image capacity identity, without evaluating its unbounded infimum.
2. The seven-observable note constructs exact residue affine maps on translated numerical-set observations. Reflection is applied only to centrally symmetric source sets. It proves bounded pair fibres, their augmented-simplex contraction in the specified unit-face metric, the full observed matrix-radius identity, and a sharp seven-dimensional linear count model at arity five. Original word multiplicities retain their distinct quotient metric.
3. The local-flow note identifies the complete cone for all finite symmetric numerical tails, constructs the integral nine-pattern/seven-count maps, retains the zero-loop quotient, and proves its original path-level chain square and finite endpoint correction. The arbitrary-schedule optimum 893^(1/6) is for the two radix-ten blocks {1,3} and {2,4}; it is an image-rate theorem, not a new best global maximum-generator rate.
4. Saturated ternary residues give the common-ray obstruction against faithful ternary re-encoding of every mixture of the explicitly listed record blocks. This does not exclude different blocks or nonfaithful binary-safe observations.

The full main and receiving notes for local_flow and seven_observable were read; all-block-image-capacity and general-pattern-return were also read in full. Earlier additive payloads were traced for integration closure, not re-audited wholesale. Recurrence-control is reviewed separately in `recurrence_review/REVIEW.md`.

## Required publication corrections

### EP817-SO-SEPARATION-001

Both original copies of `notes/seven-observable-capacity.md`, line 215, Section 4.1:

`Y_P=P∪(L−P), L>2Q` does not guarantee that patterns of span at most Q cannot meet both components. Take Q=3, P={0,3}, L=7 and R={0,1}. Then Y_P={0,3,4,7} contains one translate of R, whereas the sum of the two single-component incidence counts is zero.

Replace the auxiliary choice by **L>3Q** and state that the inter-component gap is at least L−2Q>Q. Since P⊂[0,Q], every cross-component pair is then farther apart than the allowed pattern width. Thus every pattern lies in one component and the claimed incidence decomposition is valid. The implemented producer and independent auditor already choose L=4Q+3, so their mathematical tests and hashes need no code change. The seven-state arithmetic Hankel witness in Section 4.3 is independent of this generic separation choice and passed unchanged.

Propagate to the EP817 and Zeta-facing copies, any public mirrored proof, and current proof hash records. Preserve the original archive and its original manifests as historical identities; do not relabel them as hashes of the corrected copy.

### EP817-SO-TAG-002

Both copies, line 510, display a tab followed by `ag{7.1}`. Restore the literal LaTeX command `\tag{7.1}`. This is a rendering correction only.

## Fresh exact replays

All four default/full commands ran without a quick flag. Each script was inspected before execution; they use Python's standard library and spawn no processes. `run_bounded.py` watches the sole worker's working set every 100 ms, killing at 5,000,000,000 bytes or 180 seconds. These are sampled limits, not OS-reservation guarantees. No Git scans, Lean builds, remote writes, or source edits occurred in this review.

| Replay | Result | Seconds | Peak observed working set |
|---|---|---:|---:|
| local-flow producer | PASS | 5.24 | 527,458,304 bytes |
| local-flow independent arithmetic auditor | PASS | 1.51 | 33,742,848 bytes |
| seven-observable producer | PASS | 11.55 | 77,000,704 bytes |
| seven-observable independent arithmetic auditor | PASS | 8.34 | 36,548,608 bytes |
| supplemental separation/stability checks | PASS | 1.30 | 16,723,968 bytes |

The per-run folders contain argv, actual Python/platform versions, stdout, stderr, result, before/after source hashes and runtime in a mathbox-compatible v1 manifest. The four main manifests passed the skill validator. V1's provenance limitations remain explicit; extra input hashes and measured cap records are present. Fresh results match the original mathematical records. Byte equality does **not** hold across platforms: Windows serializes `source_sha256` path keys with backslashes and text outputs with CRLF; auditors correctly bind the resulting new producer bytes. Hash values of every original producer/helper source remain identical. Do not claim cross-platform byte-identical replay.

Latest finite scope: 722 symmetric digit sources; 3,610 actual joins; 11,352 full paths; 1,089 balanced flows; 2,187 dual rows, of which 990 have positive decompositions and 1,197 have actual finite counterexamples; 2,046 switching words; 62 direct switched images; 16 saturated macro images; eight corrupted records rejected.

Seven-observable finite scope: 5,050 complete raw alphabets, 15,150 joins, 45,450 producer raw-moment vectors, 1,375 original generator comparisons, 140 schedules, 49 actual admissible Hankel entries, 2,828 cut fibres, 126 simplex identities, 18 selected matrices, 36 selected original counts and 108 independent selected moments; eight corruptions rejected. The separate auditor reconstructs raw matrices from literal joins rather than importing the producer's carrier.

The local-flow package reports a separate 2,046-word stability replay, but its reproducible main producer/auditor do not compute the crossed-run bad-length statistic. This is not a failure of the written inequality. `supplemental/certificates/check_separation_stability.py` now supplies that exact replay with integer-power inequalities, independently computes the crossed-run lengths, checks every binary word of lengths 1–10, and also checks the corrected separated-reflection identity for every nonempty P⊂[0,Q], 0≤Q≤6. Its result is in `supplemental_checks/receipt.json`.

## Full browsable integration closure

The latest ZIP is a nested cumulative delivery, not only its top-level eight EP817 files. Publish the unpacked additive research payloads, with navigation and honest per-layer verification status:

- `research/local_flow/` from `intake/ep817/EP817_LOCAL_FLOW_20260916/payloads/ep817/`.
- `research/seven_observable/` from `intake/ep817_previous/EP817_SEVEN_OBSERVABLE_20260916/payloads/ep817/`.
- `research/all_block_image/`, `research/arity_boundary/`, `research/canonical_isolation/`, `research/defect_closure/`, `research/supported_defects/`, `research/graphical_obstructions/`, `research/variable_blocks/`, and `research/splitzero_outer/` from their corresponding package directories under `intake/ep817_ancestors/*/payloads/ep817/`.
- `research/recurrence_control/` from `intake/ep817_recurrence/EP817_RECURRENCE_CONTROL_20260915/payloads/ep817/`.
- Preserve and integrate the separately reviewed live PR2/PR3 work rather than overwrite it with the oldest nested copies. The package's flat PR2 archive was extracted separately to `intake/ep817_ancestors/pr2_original_isolated/` after a safe conflict refusal.
- Preserve every corresponding Zeta receiving note in a browsable interface area with its actual dependencies. Their original package path is `payloads/zeta/workbenches/ep817-.../`; no mutation of the separate Zeta repository was performed.

The recurrence package was concretely missing from the latest nested chain despite the transcript's source links at lines 3813–4442. A bounded exact Downloads check found `EP817_RECURRENCE_CONTROL_20260915.zip`; it was safely extracted and independently reviewed. This resolves that delivery gap without fabricating absent files or copying private transcript bulk.

## PR overlap and remote state

The live main tree was read via GitHub API; at review time it contained the original k=4/Lean publication and no research directory. Open owner-authored drafts were #2, #3, #4, and #5, with heads 612020848e4bbec5f5a723a64c5fdc85636b5e83, a4ac40a60a91a45ab364f882904e07039b7ede27, 74ba7dcc4bd623b3555046feb6d45ccac38417a3, and 7641825de1bee9c57f5edef5d334abb7c21af663. A separate parent-directed audit handles their merge readiness.

Archive `splitzero_outer` has 23 files; PR4 has 14 files in that directory. Twelve paths overlap: eleven mathematical/code/data files are byte-identical as Git blobs, while the README is newer publication-oriented prose on PR4. PR4 additionally has `publication_replay.py` and `publication_replay_receipt.json`, absent from the old archive. Preserve the newer README and these two files; retain the eleven archive-only files. No mathematical conflict was found in the overlap.

## Zeta handoff scope

The actual source was fetched read-only at revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`, `workbenches/splitzero-tandem/tex/support_diagrams.tex`, blob `d3493f891291ee6e94dbf2c77649f7d85d240df2`; D1–D8 were read. The delivered interfaces use its support-labelled quotient and additional receiving-kernel distinction correctly. The useful transfer is an explicit finite observation cone, original path chain maps, a retained zero-loop kernel, section and metric defects, and the rank-independent bounded-fibre contraction at its specified metric. They do not identify a theta complex with seven coordinates or imply RH/analytic arithmetic estimates. Send source links plus the separation correction to the authorized Zeta task after publication; no direct Zeta mutation is needed.

Canonical corpus routing and exact source roles are recorded in `topic_route.json`. The pinned Korsky arXiv v1 introduction and benchmarks were checked as historical context; no new priority or September-status claim follows. These source-independent carrier/prime proofs do not import an unread analytic result.
