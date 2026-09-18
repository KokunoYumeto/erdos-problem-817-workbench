"""Check complete advertised EP817 finite domains, including missing records.

This complements the original arithmetic auditor and keeps its source intact.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent
def need(ok, message):
    if not ok:
        raise ValueError(message)

def guard(report):
    rows=report['composition_spectrum']['all_compositions_through_length18']
    need([r['length'] for r in rows]==list(range(1,19)), 'Expected every length 1 through 18 exactly once in order')
    for r in rows:
        m=r['length']
        need(r['literal_words']==2**m,'Incorrect full word domain size')
        need([(c['A_count'],c['B_count']) for c in r['compositions']]==[(s,m-s) for s in range(m+1)],'Missing, duplicate, or reordered composition')
    ab=((10,(1,3)),(10,(2,4)))
    abc=((3,(1,)),(5,(1,2)),(10,(2,4)))
    profiles=(Fraction(1,4),Fraction(1,3),Fraction(2,5),Fraction(1,2),Fraction(2,3),Fraction(3,4))
    expected={(ab,5,m,(1-p,p)) for m in range(1,9) for p in profiles}
    expected|={(abc,q,m,p) for q in (2,3,5) for m in range(1,5) for p in ((Fraction(1,2),Fraction(1,3),Fraction(1,6)),(Fraction(1,3),)*3,(Fraction(1,2),Fraction(1,2),Fraction(0)))}
    actual=[]
    for c in report['finite_composition_LPs']:
        actual.append((tuple((d['radix'],tuple(d['weights'])) for d in c['dictionary']),c['q'],c['horizon'],tuple(map(Fraction,c['profile']))))
    need(len(actual)==len(set(actual))==84 and set(actual)==expected,'Wrong LP certificate domain')
    return {'lengths':list(range(1,19)),'composition_classes':sum(m+1 for m in range(1,19)), 'literal_words':sum(2**m for m in range(1,19)),'LP_certificates':len(actual)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proof",type=Path,
                        default=HERE.parent/"certificates"/"proof_data.json")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    original=json.loads(args.proof.read_text(encoding="utf-8"))
    result=guard(original)
    corrupt=deepcopy(original)
    corrupt["composition_spectrum"]["all_compositions_through_length18"].pop()
    try:
        guard(corrupt)
    except ValueError as exc:
        rejection=str(exc)
    else:
        raise ValueError("The guard accepted a truncated through-18 domain.")
    report={"status":"PASS","domain":result,"truncation_rejected":rejection,
            "original_sources_modified":False}
    encoded=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_bytes(encoded.encode("utf-8"))
    print(encoded,end="")

if __name__=="__main__":
    main()
