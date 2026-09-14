#!/usr/bin/env python3
"""Exact finite checks accompanying the general-k capacity/carry proof.

Run from the repository root. Uses Python's standard library only. The finite
checks corroborate the general proof; no output is a Lean verification receipt.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
import json
from math import factorial, prod
from pathlib import Path
from typing import Iterator

BASE_COMMIT = "23c0110c95b5a2036bdc04a1f352b6e5e27742c8"


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def subset_sums(weights: tuple[int, ...]) -> tuple[int, ...]:
    values = {0}
    for weight in weights:
        values |= {x + weight for x in tuple(values)}
    return tuple(sorted(values))


def integer_ap(values: tuple[int, ...], k: int) -> tuple[int, ...] | None:
    require(k >= 3, "k must be at least 3")
    if not values:
        return None
    present = set(values)
    for i, start in enumerate(values):
        for second in values[i + 1:]:
            step = second - start
            if start + (k - 1) * step > values[-1]:
                break
            points = tuple(start + j * step for j in range(k))
            if all(x in present for x in points):
                return points
    return None


def modular_witnesses(digits: tuple[int, ...], q: int, k: int) -> list[dict]:
    present = {x % q for x in digits}
    return [{"start": a, "step": d,
             "residues": [(a + i * d) % q for i in range(k)]}
            for a in range(q) for d in range(1, q)
            if all((a + i * d) % q in present for i in range(k))]


def modular_ap_bits(bits: int, q: int, k: int) -> bool:
    mask = (1 << q) - 1
    for step in range(1, q):
        starts = bits
        for i in range(1, k):
            shift = (i * step) % q
            rotated = bits if not shift else ((bits >> shift) | (bits << (q - shift))) & mask
            starts &= rotated
            if not starts:
                break
        if starts:
            return True
    return False


def modular_chain_profile(digits: tuple[int,...], q: int) -> dict:
    D = {x % q for x in digits}
    maxima = []
    for step in range(1,q):
        starts = [x for x in sorted(D) if (x-step) % q not in D]
        covered, longest = set(), 0
        for start in starts:
            length = 0
            while (start+length*step) % q in D:
                covered.add((start+length*step) % q)
                length += 1
                require(length <= q,"complete modular orbit encountered")
            longest = max(longest,length)
        require(covered == D,"a complete nonzero-step coset was missed")
        maxima.append(longest)
    return {"maximal_chain_lengths_by_step":maxima,
            "histogram":{str(a):b for a,b in sorted(Counter(maxima).items())}}


def q_coordinates(value: int, q: int) -> tuple[int, int]:
    """Return the pair (valuation, residual) with exact inverse q**v * residual."""
    require(value > 0 and q >= 2, "invalid q-coordinate input")
    original, valuation = value, 0
    while value % q == 0:
        value //= q
        valuation += 1
    require(q**valuation * value == original, "q-coordinate inverse failed")
    return valuation, value


def separated(weights: tuple[int, ...], q: int) -> bool:
    residuals = [q_coordinates(w, q)[1] for w in weights]
    return len(set(residuals)) == len(residuals)


def carry_edges(digits: tuple[int, ...], q: int, k: int,
                state: tuple[tuple[int, ...], bool]) -> Iterator[tuple]:
    """All labeled edges; allows actual block sums >= q and signed carries."""
    carries, seen_nonzero = state
    residues: dict[int, list[int]] = {}
    for b in digits:
        residues.setdefault(b % q, []).append(b)
    for a in digits:
        for e in range(q):
            totals = tuple(a + i * e + carries[i - 1] for i in range(1, k))
            choices = [residues.get(total % q, []) for total in totals]
            for tail in product(*choices):
                next_c = tuple((total - b) // q for total, b in zip(totals, tail))
                nxt = (next_c, seen_nonzero or e != 0)
                yield nxt, a, e, tuple(tail)


def carry_audit(digits: tuple[int, ...], q: int, k: int) -> dict:
    require(q >= 2 and k >= 3, "invalid base or progression length")
    require(bool(digits) and tuple(sorted(set(digits))) == digits and digits[0] == 0,
            "digits must be distinct nonnegative integers containing zero")
    canonical = digits[-1] < q
    L = (digits[-1] + q - 2) // (q - 1)
    bound = 2 * factorial(k) if canonical else 2 * prod(2 * L + i + 1 for i in range(1, k))
    zero = (0,) * (k - 1)
    initial = (zero, False)
    target = (zero, True)
    parent: dict[tuple, tuple | None] = {initial: None}
    queue = deque([initial])
    digest, edge_count = sha256(), 0
    terminal = None
    while queue and terminal is None:
        state = queue.popleft()
        for nxt, a, e, tail in carry_edges(digits, q, k, state):
            require(all((0 <= c <= i) if canonical else (-L <= c <= L + i)
                        for i, c in enumerate(nxt[0], 1)), "carry box is not invariant")
            edge_count += 1
            digest.update((repr((state, nxt, a, e, tail)) + "\n").encode())
            if nxt in parent:
                continue
            parent[nxt] = (state, a, e, tail)
            if nxt == target:
                terminal = nxt
                break
            queue.append(nxt)
    require(len(parent) <= bound, "state count bound exceeded")
    report = {"base": q, "k": k, "digits": list(digits),
              "canonical_digits": canonical, "theoretical_state_bound": bound,
              "reachable_states": len(parent), "examined_valid_edges": edge_count,
              "edge_transcript_sha256": digest.hexdigest(), "all_lengths_safe": terminal is None}
    if terminal is None:
        # Independent closure verification checks every actual label once more.
        for state in parent:
            for nxt, a, e, tail in carry_edges(digits, q, k, state):
                require(nxt in parent and nxt != target, "reachable closure is defective")
                require(all(a + i * e + state[0][i-1] == tail[i-1] + q * nxt[0][i-1]
                            for i in range(1, k)), "edge arithmetic failed")
        report["closed_reachable_states"] = [[list(c), b] for c, b in sorted(parent)]
    else:
        labels = []
        cur = terminal
        while parent[cur] is not None:
            previous, a, e, tail = parent[cur]
            labels.append((a, e, tail))
            cur = previous
        labels.reverse()
        points = [sum(([a] + list(tail))[i] * q**j
                      for j, (a, e, tail) in enumerate(labels)) for i in range(k)]
        difference = sum(e * q**j for j, (a, e, tail) in enumerate(labels))
        require(difference > 0 and all(points[i] == points[0] + i * difference for i in range(k)),
                "accepted path does not reconstruct a nonconstant AP")
        require(len(labels) <= bound - 1, "short-witness bound failed")
        report["witness"] = {"word_length": len(labels), "start": points[0],
                             "step": difference, "points": points,
                             "labels": [[a, e, list(tail)] for a, e, tail in labels]}
    return report


def digit_language(digits: tuple[int, ...], q: int, length: int) -> tuple[int, ...]:
    values = {0}
    for j in range(length):
        values = {x + q**j * d for x in values for d in digits}
    return tuple(sorted(values))


def block_case(weights: tuple[int, ...], q: int, k: int) -> dict:
    require(bool(weights) and weights[0] > 0 and tuple(sorted(set(weights))) == weights,
            "weights must be sorted, distinct and positive")
    require(separated(weights, q), "geometric generator families would repeat")
    digits = subset_sums(weights)
    audit = carry_audit(digits, q, k)
    require(audit["all_lengths_safe"], f"unsafe claimed block: {weights}, {q}, {k}")
    require(not modular_witnesses(digits, q, k), "claimed modular certificate failed")
    replays = []
    # Direct generator subsets, independent of the automaton, for two full blocks.
    for length in (1, 2):
        generators = tuple(sorted(q**j * b for j in range(length) for b in weights))
        actual = subset_sums(generators)
        require(actual == digit_language(digits, q, length), "generator/digit bridge failed")
        require(len(set(generators)) == length * len(weights), "generator injection failed")
        require(integer_ap(actual, k) is None, "direct lifted AP found")
        replays.append({"blocks": length, "generators": len(generators), "subset_sums": len(actual)})
    return {"weights": list(weights), "sum": sum(weights), "max": max(weights),
            "modular_parameter_pairs": q*(q-1), "modular_ap_count": 0,
            "carry": audit, "modular_chain_profile":modular_chain_profile(digits,q), "direct_lifts": replays}


def exhaustive_small_alphabets(max_q: int = 6) -> dict:
    tested, safe, unsafe, comparisons = 0, 0, 0, 0
    digest = sha256()
    for k in range(3, 7):
        for q in range(2, max_q + 1):
            for bits in range(1 << (q - 1)):
                digits = (0,) + tuple(i for i in range(1, q) if bits & (1 << (i - 1)))
                exact_mod = bool(modular_witnesses(digits, q, k))
                require(exact_mod == modular_ap_bits(sum(1 << d for d in digits), q, k),
                        "independent modular checkers disagree")
                audit = carry_audit(digits, q, k)
                tested += 1
                safe += audit["all_lengths_safe"]
                unsafe += not audit["all_lengths_safe"]
                if not exact_mod:
                    require(audit["all_lengths_safe"], "modular-to-carry implication failed")
                for length in (1, 2, 3):
                    actual = digit_language(digits, q, length)
                    witness = integer_ap(actual, k)
                    if audit["all_lengths_safe"]:
                        require(witness is None, "safe automaton/direct enumeration disagreement")
                    else:
                        m = audit["witness"]["word_length"]
                        if m <= length:
                            require(witness is not None, "automaton witness absent from padded language")
                    comparisons += 1
                digest.update((json.dumps([k,q,digits,audit["all_lengths_safe"],audit.get("witness")],
                                          sort_keys=True) + "\n").encode())
    return {"k_range": [3,6], "base_range": [2,max_q], "alphabets_tested": tested,
            "safe": safe, "unsafe": unsafe, "direct_length_comparisons": comparisons,
            "transcript_sha256": digest.hexdigest()}


def exhaustive_noncanonical() -> dict:
    tested, safe, comparisons = 0, 0, 0
    digest = sha256()
    for k in range(3, 6):
        for q in range(2, 5):
            for bits in range(1 << (2*q)):
                digits = (0,) + tuple(i for i in range(1, 2*q+1) if bits & (1 << (i-1)))
                if digits[-1] < q:
                    continue
                a = carry_audit(digits, q, k)
                tested += 1
                safe += a["all_lengths_safe"]
                for length in (1,2):
                    witness = integer_ap(digit_language(digits,q,length),k)
                    if a["all_lengths_safe"]:
                        require(witness is None,"noncanonical safe/direct disagreement")
                    elif a["witness"]["word_length"] <= length:
                        require(witness is not None,"noncanonical failure/direct disagreement")
                    comparisons += 1
                digest.update((json.dumps([k,q,digits,a["all_lengths_safe"],a.get("witness")],
                                          sort_keys=True)+"\n").encode())
    return {"k_range":[3,5],"base_range":[2,4],"digit_domain":"all D subset [0,2q] containing 0 with max(D)>=q",
            "alphabets_tested":tested,"safe":safe,"unsafe":tested-safe,
            "direct_length_comparisons":comparisons,"transcript_sha256":digest.hexdigest()}


def composition_checks() -> dict:
    pairs, admissible = 0, 0
    digest = sha256()
    for k in range(3, 7):
        examples = [b for size in range(1,4) for b in combinations(range(1,9),size)
                    if integer_ap(subset_sums(b), k) is None]
        admissible += len(examples)
        # Each left block paired with three distinct right-block choices.
        for a in examples:
            for b in ((1,), (1,3), examples[-1]):
                require(integer_ap(subset_sums(b), k) is None, "invalid right block")
                R = 2 * sum(a) + 1
                c = tuple(sorted(a + tuple(R*x for x in b)))
                da, db, dc = subset_sums(a), subset_sums(b), subset_sums(c)
                images = tuple(sorted(x + R*y for x in da for y in db))
                require(images == dc and len(dc) == len(da)*len(db), "composition bijection failed")
                require(2*sum(c)+1 == (2*sum(a)+1)*(2*sum(b)+1), "cost product failed")
                require(len(c) == len(a)+len(b) and len(set(c)) == len(c), "distinctness failed")
                require(integer_ap(dc,k) is None, "composition created a progression")
                require(not modular_witnesses(da, R, k), "universal modular embedding failed")
                pairs += 1
                digest.update((repr((k,a,b,R,len(dc)))+"\n").encode())
    return {"left_domain": "nonempty subsets of [1,8] of size at most 3", "k_range": [3,6],
            "admissible_left_instances": admissible, "composition_pairs": pairs,
            "transcript_sha256": digest.hexdigest()}


def modular_search(q: int, k: int) -> tuple[tuple[int,...], int]:
    """Exhaustive branch-and-bound over literal distinct weights; no rescaling."""
    best: tuple[int,...] = ()
    visited = 0
    def visit(weights: tuple[int,...], total: int, bits: int) -> None:
        nonlocal best, visited
        visited += 1
        if len(weights) > len(best):
            best = weights
        first = weights[-1] + 1 if weights else 1
        need = len(best)+1-len(weights)
        for w in range(first, q-total):
            if need*w + need*(need-1)//2 + total >= q:
                break
            new_bits = bits | (bits << w)
            if not modular_ap_bits(new_bits, q, k):
                visit(weights+(w,),total+w,new_bits)
    visit((),0,1)
    return best, visited


def search_receipt(max_q: int) -> dict:
    entries=[];digest=sha256()
    for k in (5,6):
        best_q,best_m=3,1
        for q in range(3,max_q+1):
            weights,nodes=modular_search(q,k)
            require(bool(weights), "unexpected absence of a singleton certificate")
            require(not modular_witnesses(subset_sums(weights),q,k), "search output invalid")
            if q**best_m < best_q**len(weights):
                best_q,best_m=q,len(weights)
            row={"k":k,"base":q,"maximum_generators":len(weights),
                 "first_witness":list(weights),"visited_prefixes":nodes}
            entries.append(row)
            digest.update((json.dumps(row,sort_keys=True)+"\n").encode())
    return {"base_range":[3,max_q],"progression_lengths":[5,6],
            "scope":"all distinct positive B with sum(B)<base; modular criterion",
            "entries":entries,"transcript_sha256":digest.hexdigest()}


def regressions() -> dict:
    # Exact obstruction to the k=4 layer splitting outside k=4.
    A=(1,2)
    require(integer_ap(subset_sums(A),5) is None, "five-term example failed")
    require(2*A[0]-A[1] == 0 and A[0] != 0 and -A[1] != 0,
            "relation-splitting obstruction failed")
    # Modular failure with prime base, but safe all-length carry graph.
    carry_only=carry_audit(subset_sums((2,7)),11,3)
    modular=modular_witnesses(subset_sums((2,7)),11,3)
    require(modular and carry_only["all_lengths_safe"], "strict carry advantage failed")
    # Actual digits outside [0,q-1]; the full signed-carry graph retains them.
    noncanonical=carry_audit((0,4),3,3)
    require(noncanonical["all_lengths_safe"] and not noncanonical["canonical_digits"],
            "noncanonical digit regression failed")
    negative = carry_audit((0,2),2,3)
    require(not negative["all_lengths_safe"],"signed carry failure was missed")
    # Search-domain failures are returned as actual integer witnesses.
    near=[]
    for k,B,first,last in [(4,(1,7,8),17,18),(5,(1,3,4,7),16,22),
                           (5,(1,4,5,17,21,22),71,96),(6,(1,4,5,17,21,22),71,92)]:
        for q in range(first,last+1):
            a=carry_audit(subset_sums(B),q,k)
            require(not a["all_lengths_safe"], "purported lower-base obstruction failed")
            w=a["witness"]
            actual=digit_language(subset_sums(B),q,w["word_length"])
            require(all(x in actual for x in w["points"]), "reconstructed witness is outside image")
            near.append({"k":k,"base":q,"weights":list(B),"witness":w})
    require(not separated((1,3),3) and separated((2,7),11), "generator separation regression failed")
    require(97 < 5**3 and 97**2 < 23**3 and 93**5 < 7**12,
            "exact upper-rate comparisons failed")
    return {"layer_obstruction":{"weights":[1,2],"relation":[2,-1],"four_ap":[0,1,2,3]},
            "carry_strictness":{"weights":[2,7],"modular_witnesses":modular,"carry":carry_only},
            "noncanonical_safe_example":noncanonical,"signed_carry_failure":negative,
            "nearby_base_obstructions":near,
            "exact_rate_comparisons":{"97_lt_5_cubed":97<5**3,
              "97_squared_lt_23_cubed":97**2<23**3,"93_fifth_lt_7_twelfth":93**5<7**12}}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--search-max-base",type=int,default=48)
    args=parser.parse_args()
    require(3 <= args.search_max_base <= 127,"search bound must be in [3,127]")
    blocks=[(4,19,(1,7,8)),(5,23,(1,3,4,7)),(6,47,(1,2,6,7,14)),
            (5,97,(1,4,5,17,21,22)),(6,93,(1,4,5,17,21,22))]
    report={"schema":"ep817-general-k-capacity-v1","status":"PASS","lean_checked":False,
            "base_commit":BASE_COMMIT,
            "scope":"Exact finite certificates plus bounded independent replays; general proofs in notes/general-k-capacity.md",
            "certified_blocks":[block_case(B,q,k) for k,q,B in blocks],
            "small_alphabet_replay":exhaustive_small_alphabets(),
            "composition_replay":composition_checks(),"noncanonical_replay":exhaustive_noncanonical(),
            "regressions":regressions(),
            "modular_search":search_receipt(args.search_max_base),
            "validator_sha256":sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text,encoding="utf-8")
    print(text,end="")

if __name__=="__main__":
    main()
