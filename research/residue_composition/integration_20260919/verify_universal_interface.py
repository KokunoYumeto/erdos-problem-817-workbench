"""Exact verification of residue-fibre matrices and original weighted quotients.

This verifier does not import either supplied certificate program.  It retains
the actual digits, residue shifts, word multiplicities, and quotient maps.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
STATES = [(0,), (0,1), (0,2), (0,1,2), (0,3), (0,1,3), (0,1,2,3)]
EXPECTED = {
 "A": [[3,7,0,0,0,0,0],[2,8,0,0,0,0,0],[1,9,0,0,0,0,0],
       [1,9,0,0,0,0,0],[0,10,0,0,0,0,0],[0,10,0,0,0,0,0],
       [0,10,0,0,0,0,0]],
 "B": [[0,2,0,3,0,0,0],[0,4,0,6,0,0,0],[0,1,0,4,0,0,0],
       [0,3,0,7,0,0,0],[0,4,0,6,0,0,0],[0,3,0,7,0,0,0],
       [0,2,0,8,0,0,0]],
}

def check(value, message):
    if not value:
        raise RuntimeError(message)

rows = []
for name, digits in (("A", list(range(17))), ("B", list(range(0,25,2)))):
    for i, state in enumerate(STATES):
        coefficients = [0]*7
        fibres = []
        for residue in range(10):
            original = sorted({(d+r-residue)//10 for d in digits for r in state
                               if (d+r)%10 == residue})
            if not original:
                fibres.append({"residue":residue,"original":[], "shift":None,
                               "state_index":None})
                continue
            shift = min(original)
            target = tuple(x-shift for x in original)
            check(target in STATES, "Fibre is outside the original seven states.")
            j = STATES.index(target)
            coefficients[j] += 1
            check([shift+x for x in target] == original, "Shift inverse failed.")
            fibres.append({"residue":residue,"original":original,"shift":shift,
                           "state_index":j})
        check(coefficients == EXPECTED[name][i], "Arithmetic matrix differs.")
        rows.append({"letter":name,"state_index":i,"fibres":fibres,
                     "coefficients":coefficients})

metrics = []
for radix, weights in ((3,(1,)),(5,(1,2)),(13,(1,3,4)),(23,(1,3,4,7)),
                       (10,(1,3)),(10,(2,4))):
    masses = Counter(sum(c*a for c,a in zip(word,weights))
                     for word in product(range(3), repeat=len(weights)))
    fibres = {}
    for value,mass in masses.items():
        fibres.setdefault(value%radix, {})[value] = mass
    for residue, fm in sorted(fibres.items()):
        mass_total = sum(fm.values())
        selected = min(fm)
        section = {x: Fraction(mu,mass_total) for x,mu in fm.items()}
        check(sum(section.values()) == 1, "Section is not a right inverse.")
        attained_norm = sum(c*c/fm[x] for x,c in section.items())
        check(attained_norm == Fraction(1,mass_total), "Wrong quotient metric.")
        defect_norm = sum((int(x==selected)-c)**2/fm[x] for x,c in section.items())
        check(Fraction(1,fm[selected]) == attained_norm+defect_norm,
              "Pythagoras failed in the original quotient metric.")
        metrics.append({"radix":radix,"weights":list(weights),"residue":residue,
                        "masses":fm,"selected":selected,"total_mass":mass_total,
                        "quotient_norm":str(attained_norm),
                        "boundary_norm":str(defect_norm),
                        "relative_integral_loss":str(Fraction(mass_total,fm[selected]))})

# Both evaluations retain every local-value pair before quotient.
pairs = list(product(range(17), repeat=2))
expanded = {x+100*y for x,y in pairs}
contracted = {x+10*y for x,y in pairs}
check(len(expanded)==289 and len(contracted)==177,"Active-position values differ.")
check(contracted==set(range(177)),"Contracted image is not the stated interval.")
receipt={"status":"passed","matrix_rows":len(rows),"original_residue_fibres":rows,
         "weighted_residue_fibres":metrics,"weighted_fibre_count":len(metrics),
         "active_position":{"original_pair_count":289,
                            "retained_image_count":289,"erased_image_count":177,
                            "extra_receiving_kernel_rank":112},
         "domains":"All 14 original matrix rows, their 140 literal residue fibres; "
                   "six displayed ternary blocks; both original active-position maps."}
(OUT/"UNIVERSAL_INTERFACE_CHECKS.json").write_text(
    json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps({k:receipt[k] for k in
                  ("status","matrix_rows","weighted_fibre_count","active_position")}))
