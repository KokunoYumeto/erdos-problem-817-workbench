# PR 5: cone, lift, capacity dual, and switching audit

Reviewed head: `7641825de1bee9c57f5edef5d334abb7c21af663` (parent-provided API revision).

## Claim and verdict

For finite centrally symmetric integer sets, the seven union-cardinality observations have the nine-facet, ten-ray cone stated in Sections 2–3. The specified integer ray lift preserves the seven-coordinate action with its rank-three kernel and explicit composition defect. For integer progression length **k >= 3**, the global extremal rate has the antinorm and finite rational subcritical approximations of Sections 5–6. The two stated arithmetic blocks have exact optimal switching fifth-image rate sqrt(285) per level, and the stated linear-potential obstruction.

**Primary verdict: correct only after a stated restriction.** The standalone note must state `k >= 3` and define its inherited extremal notation. On that intended domain, I found no failed mathematical implication in the full note. The finite statements replayed successfully. Recommend merge as ordinary-proof/research work, with the small documentation repairs below. This is not a new numerical global bound, a Lean verification, or a literature-priority determination.

## Exact documentation repairs

1. `research/cone_dual/notes/cone-and-dual.md`, line 13: after the definition of k-admissibility, add:

   > Throughout, k is an integer with k>=3, and g_k(n)=min{max A: |A|=n, A is k-admissible} for n>=1.

   The omitted restriction matters: no nonempty positive generator set is 2-admissible, since its subset sums contain 0 and a positive generator. Thus the finite extremal rate used here is not defined for k=2 by the intended minimization. Powers of three give admissible sets at every rank for k>=3.

2. Before the comparison on line 719, explicitly define:

   > F_k(n)=min{2S(A)+1: |A|=n, A is k-admissible}.

3. Line 696 currently claims that the finite certificate retains both complete mass histograms. The producer's `obstructions()` computes both but serializes only the original weights, common value image, and peak multiplicities. Replace its final sentence with:

   > The producer and independent auditor recompute both complete histograms from the retained original weights; the serialized certificate records their peak multiplicities.

This last repair corrects the description of evidence, not the result: the distinct complete histograms are actually computed and compared by both implementations.

## Dependencies and proof checks

| Result | Dependency chain and check | Status |
|---|---|---|
| C1 | Literal four-bit windows; reflection-fixed circulation; integral inclusion-exclusion inverse; two balance equations; explicit positive integral flow routing; periodic endpoint error | Passed by proof reading and fresh exact replay |
| C2 | Exact residue fibres; density of actual finite-set observations; positive ray section; integral kernel coordinate extraction; associativity of lifts | Passed; the section is correctly not represented as additive |
| Lift spectral statement | Weighted column norm equals e0 P v; bounded-fibre concatenation gives rho^m <= N_m <= 4 rho^m | Correct argument; inherited bounded-fibre input restated in Section 4.2 |
| C3 | Capacity formula of Section 9 -> e0 P v >= lambda_k^reward -> retained nonnegative rows with total coefficient between 1/4 and 1 -> floor grid approximation -> strict-threshold expansion | Passed for k>=3; the all-rank arithmetic quantifier is not removed |
| Rational finite test | Active cells for each minimizing row; exact rational polyhedral duality/Farkas separation | Correct equivalence; no finite computation is promoted to the universal arithmetic inequality |
| C4 | Actual two-letter modular admissibility; aX >=17a on the cone; aY=285e0; XY=w e0; positive Farkas identity | Passed, including an independent exact arithmetic reconstruction |
| C5 | Distinct binary images for two actual sets; identical full fifth images; distinct original multiplicity histograms | Passed; observation failure is precisely scoped, not a claim of unrelatedness |

The finite rational theorem is not a numerical strengthening by itself: the coefficients are obtained from the antinorm defined using the unknown global rate. It proves the stated existence and explicit coefficient-height bound; verification over all actual arithmetic blocks remains a separate mathematical problem. The note states this correctly.

The switching result compares fifth-image growth with fifth-image growth. It retains the different largest-generator root sqrt(23) and does not claim a new global k=5 record. The factor sqrt(285) is attained along alternating blocks; every finite word has the lower bound, so the claimed infimum of lower limiting rates follows without an unstated compactness assumption.

## Predecessor and external-source boundary

The exact cited predecessor is **not inferred to be PR 4**. It is the archive `EP817_SEVEN_OBSERVABLE_20260916.zip`, SHA256 `11e2080a0135b04016723ea6929a93479d0540e519c5458d22728531d68019dd`, source `research/seven_observable/notes/seven-observable-capacity.md`, particularly Section 10. This locator comes from the actual note and source ledger. Parent should integrate or resolve that source path when publishing this continuation. Section 9 of the present note supplies the capacity proof itself; I read and checked that argument rather than accepting the archive title as evidence.

The cited Ziemian and Protasov works are explicitly contextual, not theorem inputs for the new cone or antinorm bounds. Their complete sources were not independently re-audited in this bounded review. The Korsky benchmark/priority history and the separate Zeta receiving note are likewise outside this review; no conclusion about either is added here.

## Fresh bounded computation

All four raw code files and the complete 808-line proof note were inspected. The code is standard-library-only, has no network, shell, or untrusted command execution, and uses exact integer/Fraction arithmetic.

Ran Python 3.13.9 with `-B`, importing the reviewed producer and auditor. No source files or committed receipts were overwritten. In memory:

1. `prove_cone`, `obstructions`, `matrices`, `switching`, `finite_sources`;
2. JSON packing as the producer uses;
3. independent `reconstruct_cone`, `audit_matrices`, `check_switching`, `final_obstructions`;
4. SHA256 of the exact regenerated proof JSON bytes.

Exact execution command (PowerShell):

```powershell
python -B -c "import sys,time,json,hashlib; from pathlib import Path; p=Path(r'C:/Users/LOCAL_USER/Documents/Erdos Strauss and related/private_review/program_updates_20260916/reviews/ep817_prs/pr5/research/cone_dual'); sys.path.insert(0,str(p/'certificates')); import verify_cone_dual as v; import audit_cone_dual as a; t=time.time(); d=v.prove_cone(); d['obstructions']=v.obstructions(); selected,mat=v.matrices(); d['selected_matrices']=selected; d['switching']=v.switching(); finite=v.finite_sources(); packed=v.pack(d); sets,F,N,J,facets=a.reconstruct_cone(packed); ac=a.audit_matrices(packed,sets,F,facets); sc=a.check_switching(packed,facets); a.final_obstructions(packed); raw=(json.dumps(packed,indent=2,sort_keys=True)+'\n').encode(); expected=json.loads((p/'certificates/cone_receipt.json').read_text()); print(json.dumps({'status':'PASS','seconds':time.time()-t,'finite':finite,'matrix':mat,'independent_matrices':ac,'independent_switching':sc,'proof_sha256':hashlib.sha256(raw).hexdigest(),'matches_stored_proof_hash':hashlib.sha256(raw).hexdigest()==expected['proof_sha256'],'version':sys.version},indent=2))"
```

Elapsed time: 7.30984 seconds. These were finite exact domains and no Lean process was launched. Applicable non-critical resource ceiling was 5,000,000,000 bytes; no OS-enforced RSS cap or watcher was attached to this small, fully inspected bounded computation. RSS was not instrumented. The stated finite input bounds, not a claimed measured memory bound, describe the actual run.

Results:

- 2,044 finite symmetric source cases, widths 1–18.
- 1,089 balanced flows with orbit coordinates in 0–2.
- 1,191 original block/radix cases and 3,573 literal transfer comparisons.
- 1,012 symmetric digit sets.
- 11 positive lifts, 36 composition pairs (2 nonzero defects), and 64 cocycle triples.
- Independent reconstruction: 11 matrices from 77 literal set images.
- 16,383 switching words through depth 13, 624 independent cone inequalities, and 14 direct generator-set checks.
- All six producer negative controls rejected their false formulas.
- Reconstructed proof hash exactly matches the committed receipt: `751f89b55161ef32b19c148628e46e100255c2a58ffebaf71cb5e11e905aa1c8`.

The auditor's additional 1,020-case loop and its eight mutation tests are in `main()` and were **not rerun** by this in-memory invocation. The producer covers a larger literal-source range, but that does not stand in for a claim to have rerun those eight separate mutations.

### Raw source hashes

- Note: `5f8b16549ee13041749707c1421c94f860b39d79f0db8055d0d2a013aa4ca9fb`.
- `tools/exact_cone.py`: `90da7fddd14a8035b9ad1b572fe787b3aa1cb0ac9d6d76ea169de2cbaa2ad24f`.
- `certificates/verify_cone_dual.py`: `d1b712f9e9a7f29f2d0416f1b841707f3c2e7812160eb498538f2e51dc27b8f7`.
- `certificates/audit_cone_dual.py`: `544daea31165078b37ee7f8a90742af88766c912766cf2bd7a828fd73d052d38`.

## Bounded corpus routing record

```json
{
  "topic": "EP817 exact feasible observation cone, arithmetic antinorm and finite rational certificates",
  "index_contract": "C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/Zeta-Function-Foundation/config/literature_index_entrypoint.json",
  "queries": [
    {"query":"antinorm","layer":"all","index_level":"canonical","limit_per_layer":3},
    {"query":"arithmetic progression subset sum","layer":"all","index_level":"canonical","limit_per_layer":3}
  ],
  "relevant_publication_units": [
    {"id":"PUBUNIT-BFE4AE843A54AE6279E176C6","title":"Convexity from the Geometric Point of View","reading_status":"routing only; no source-dependent implication imported"},
    {"id":"PUBUNIT-A4894D5AC1047F2167AE1B6F","title":"Additive Combinatorics","reading_status":"routing only; no source-dependent implication imported"}
  ],
  "audited_primary_source": "research/cone_dual/notes/cone-and-dual.md",
  "section_check": "complete Sections 1-10 and references read",
  "predecessor_source": "EP817_SEVEN_OBSERVABLE_20260916.zip:research/seven_observable/notes/seven-observable-capacity.md#Section10",
  "missing_dependency": "parent must resolve/publish actual predecessor path; it was not available at the guessed PR4 path and no PR4 identity is asserted",
  "unresolved_literature_questions": ["No priority determination or complete external literature review performed in this PR audit"],
  "refresh_reason": "new submitted PR head 7641825de1bee9c57f5edef5d334abb7c21af663"
}
```

No remote writes, no claim/status edits, and no changes to the submitted source were performed by this auditor.
