# Proposed title

research: general-k rate existence, exact carry capacity, and improved k=5,6 constructions

# Proposed description

This contribution extends the workbench to every k>=3 without changing its
existing Lean sources or verification receipts.

## Results

An exact composition A star B = A union (2 sum(A)+1)B preserves actual subset
representations, their multiplicities, and the complete arithmetic-progression
tuple sets. The observable R(A)=2 sum(A)+1 is multiplicative. This proves that
lambda_k = lim_n g_k(n)^(1/n) exists for every k, and gives an exact infimum
over finite modular certificates, canonical carry certificates, or full
above-base carry certificates with the generator distinctness condition kept.

The canonical carry graph proves all-word-length safety and produces a
counterexample of at most 3^(k-2) columns whenever one exists. The full graph
retains above-base digits and tracks the actual common difference with a
separate quotient/remainder carry. It supplies an explicit finite state bound
without assuming unique word representations.

The verified block A={1,4,5,17,21,22} gives, for every n>0:

- g_5(n) <= 22 * 97^(ceil(n/6)-1);
- g_6(n) <= 22 * 93^(ceil(n/6)-1).

Modulus 93 is tested at every nonzero step, including small-order residues.
Both statements improve the corresponding retrieved general graph upper
rates. No exact-value or literature-priority claim is made.

An explicit path family proves that minimal signed relations can overlap in
arbitrarily large connected patterns already for k=5. A separate counting
argument identifies the entire positive interval-digit column-model budget,
with a relation-preserving obstruction showing why correlated digit sets
extend that model. Every result has a full proof or a finite arithmetic
certificate with an all-length lifting proof.

## Checks

Run the verifier in the contribution directory:

    python certificates/verify_general_k.py --output certificates/general_k_receipt.json

PASS: 1,016 canonical and 384 full carry-graph instances, independently
checked safe closures, explicit negative witnesses, and 4,200 direct finite
languages. Exact composition was checked on 256 input pairs, 1,024 AP tuple
comparisons, and 4,096 associativity triples. The retained search comprises
784 parameter records; all witness blocks are replayed. Ninety-six additional
above-base probes produce explicit two-level progressions. Binary representation
multiplicities, generator distinctness, the correlated cube fibers, and
invalid-input/mutation regressions are also checked. A replay with Python -O
produces the same receipt bytes.

## Proof and provenance boundary

These are ordinary mathematical proofs plus exact finite checks. This
contribution supplies no new Lean elaboration. The original k=4 mathematics
remains credited to the anonymous/deleted contributor; sneed-and-feed retains
separate credit for PR #1's Lean formalization. Draft PR #2 remains separate.

The exact general lambda_k values and the matching large-k lower estimate
remain to be evaluated. Review should focus on the composition AP bijection,
full-carry slope identity, generator power-alias condition, and finite modular
checks before promotion into an accepted main manuscript.

Base revision: 23c0110c95b5a2036bdc04a1f352b6e5e27742c8.
Intended branch: research/general-k-carry-capacity-20260914.

Publication status: this file is a prepared pull-request description. It does
not assert that a new pull request has been created.
