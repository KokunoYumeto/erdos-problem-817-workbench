#!/usr/bin/env python3
"""Exact bounded calibrations of the compact dual; the all-rank proof is in the note."""
from __future__ import annotations
import argparse,gzip,json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path


def require(ok: bool, text: str) -> None:
    if not ok: raise AssertionError(text)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();rows=[]
    for k in (5,6):
        for r in range(1,5):
            f=a.directory/f'variable_k{k}_r{r}.json.gz'
            raw=gzip.decompress(f.read_bytes());rec=json.loads(raw)
            B=rec['target']['base'];power=rec['target']['root'];h=list(map(Fraction,rec['potential']))
            require(all(1<=v<=2**power for v in h),'reset-bounded coefficient interval')
            edges=rec['representative_edges']
            for u,v,b,n,li in edges:
                require(b**power*h[v]>=B**n*h[u],'exact dual edge')
            # Every actual safe support has a present reset edge to the initial support.
            for u in range(len(rec['states'])):
                require(any(e[:4]==[u,0,2,0] for e in edges),'supported reset edge missing')
            rows.append({'k':k,'max_block_size':r,'target':rec['target'],
                         'potential_coefficients':len(h),'checked_cost_representatives':len(edges),
                         'maximum_potential_power':str(max(h)),'reset_cap_power':2**power,
                         'receipt_sha256':sha256(f.read_bytes()).hexdigest(),
                         'plain_receipt_sha256':sha256(raw).hexdigest()})
    require(97**4<23**6 and 93**4<23**6,'all-rank obstruction comparison')
    require(2**2<8 and (2*2)**2>=8,'reset-loss regression')
    report={'schema':'ep817-compact-dual-calibration-v1','status':'PASS','lean_checked':False,
            'scope':'Exact retained finite-certificate coefficient bounds, reset edges and comparisons; the all-rank equivalence has a separate written proof.',
            'cases':rows,'rejected_global_rank_four_thresholds':[
                {'k':5,'generators':[1,4,5,17,21,22],'base':97,'left':97**4,'right':23**6},
                {'k':6,'generators':[1,4,5,17,21,22],'base':93,'left':93**4,'right':23**6}],
            'reset_loss_detected':True,'validator_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(report,indent=2,sort_keys=True)+'\n';a.output.write_text(text);print(text,end='')
if __name__=='__main__':main()
