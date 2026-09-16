#!/usr/bin/env python3
"""Rebuild all arithmetic records without changing stored evidence."""
from __future__ import annotations
import argparse
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import tempfile

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--optimized',action='store_true')
    a=p.parse_args();root=Path(__file__).resolve().parent;c=root/'certificates'
    executable=[sys.executable]+(['-O'] if a.optimized else [])
    with tempfile.TemporaryDirectory(prefix='ep817-supported-check-') as d:
        t=Path(d)
        jobs=[('verify_supported_defects.py',['--output',str(t/'supported_defect_receipt.json'),'--proof-data',str(t/'supported_defect_proof.json.gz')]),
              ('audit_supported_defects.py',['--proof-data',str(t/'supported_defect_proof.json.gz'),'--output',str(t/'independent_audit.json')]),
              ('verify_observation_quotient.py',['--output',str(t/'observation_quotient_receipt.json')]),
              ('audit_observation_quotient.py',['--receipt',str(t/'observation_quotient_receipt.json'),'--output',str(t/'observation_quotient_audit.json')])]
        for name,args in jobs:
            result=subprocess.run(executable+[str(c/name)]+args,capture_output=True,text=True)
            if result.returncode:
                print(result.stdout,end='');print(result.stderr,end='',file=sys.stderr)
                raise SystemExit(f'FAIL: {name}, exit {result.returncode}')
            print(f'PASS: {name}')
        files=['supported_defect_receipt.json','supported_defect_proof.json.gz','independent_audit.json','observation_quotient_receipt.json','observation_quotient_audit.json']
        for name in files:
            got=(t/name).read_bytes();expected=(c/name).read_bytes()
            if got!=expected:
                raise SystemExit(f'FAIL: {name}: new {sha256(got).hexdigest()}, stored {sha256(expected).hexdigest()}')
        print('PASS: all five generated evidence files are byte-identical to the stored records.')

if __name__=='__main__':main()
