# General-k Erdős Problem 817 contribution

The investigation extends the workbench from the four-term case to every
progression length k>=3. Its central result is an exact finite-certificate
capacity for the exponential rate, with a proof that the rate exists. The
certificate includes an explicit all-word-length carry argument; above-base
digits and subset-representation collisions are retained by an additional
carry for the actual progression difference.

The full mathematical argument is in
[`notes/general-k-carry-capacity.md`](notes/general-k-carry-capacity.md).
The universal statements are ordinary proofs, submitted for independent
review. Existing Lean Core/Extended coverage is unchanged.

The explicit six-generator block {1,4,5,17,21,22} gives

    g_5(n) <= 22 * 97^(ceil(n/6)-1)
    g_6(n) <= 22 * 93^(ceil(n/6)-1)

for every positive integer n. The proof retains all 38 distinct subset sums
and their binary representation multiplicities. These upper bounds improve
the graph-construction rates in the inspected Korsky preprint. The exact
values of the general rates and a matching large-k estimate remain to be
evaluated. No claim of literature priority is made.

## Reproduce

From this directory, run:

```sh
python certificates/verify_general_k.py --output certificates/general_k_receipt.json
```

The checker uses only the Python standard library, integer arithmetic, and
explicit exception-raising checks. It works with or without `python -O`.
Its output includes exact source hashes, positive closed-state certificates,
negative progression witnesses, and the exhaustive-domain descriptions.

The default replay checks 1,400 graph instances, 4,200 finite digit languages,
784 retained search witnesses, and the exact product/fiber maps. It also
rechecks the 96 failed noncanonical-base probes for the six-generator block.
The mathematical note explains why graph closure proves all word lengths.
Finite language tests by themselves carry only their stated finite scope.

The larger bounded searches can be rerun separately:

```sh
python search_carry.py --mode carry --min-base 3 --max-base 80 --k 5 6
python search_carry.py --mode carry --min-base 81 --max-base 160 --k 5 6
python search_carry.py --mode modular --min-base 3 --max-base 80 --k 7 8 9 10 11 12
python search_noncanonical.py
```

The maximum-base flags specify the completed search ranges, not a proposed
universal cutoff. Search maximality concerns positive generator sets whose
sum is below the base; the full-carry theorem also covers larger digit sums.

## Files and lineage

`certificates/carry_tools.py` implements the canonical and full graphs, with
independent direct-column closure validators. `verify_general_k.py` combines
the checks. `logs/` retains exact bounded-search results and failed-base
witnesses. `polyclank/claims.json` gives claim-local proof locations and
verification status; `polyclank/research_state.json` records the mathematical
objective, present conclusions, and outstanding extremal questions.

The base repository revision is
`23c0110c95b5a2036bdc04a1f352b6e5e27742c8`.
The anonymous/deleted Reddit contributor retains credit for the original
k=4 construction and signed-block proof. The contributor sneed-and-feed
retains separate credit for the Lean upper-bound formalization in PR #1.
Draft PR #2, at `612020848e4bbec5f5a723a64c5fdc85636b5e83`, is the preceding
ternary-variance contribution. The all-k composition and carry proofs here
have no dependency on that draft's new variance lemma.
