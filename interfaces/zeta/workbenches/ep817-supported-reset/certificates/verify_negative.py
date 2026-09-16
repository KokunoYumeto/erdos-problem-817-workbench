#!/usr/bin/env python3
"""Reject deliberately corrupted complete variable-block certificates."""
from __future__ import annotations
import argparse,copy,gzip,importlib.util,json
from hashlib import sha256
from pathlib import Path


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--receipt',type=Path,required=True);ap.add_argument('--auditor',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    spec=importlib.util.spec_from_file_location('independent_variable_auditor',a.auditor);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    raw=gzip.decompress(a.receipt.read_bytes()) if a.receipt.suffix=='.gz' else a.receipt.read_bytes();original=json.loads(raw)
    mod.audit(original)
    mutations=[]
    def run(name,change):
        rec=copy.deepcopy(original);change(rec)
        try:mod.audit(rec)
        except AssertionError as e:mutations.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise AssertionError('mutation was accepted: '+name)
    run('omit_literal_level',lambda r:r['profiles'].pop())
    run('erase_present_zero_word',lambda r:r['profiles'][0]['fibres'].clear())
    run('reset_as_identity',lambda r:r['profiles'][0].update(transfers=[1<<i for i in range(len(r['orbits']))]))
    run('false_initial_carry',lambda r:r['profiles'][0].update(initial=1))
    run('nonpositive_potential',lambda r:r['potential'].__setitem__(0,'0'))
    run('wrong_target_rate',lambda r:r['target'].update(base=r['target']['base']+1))
    run('omit_cost_representative',lambda r:r['representative_edges'].pop())
    run('erase_accepting_bit',lambda r:r.update(reject_bit=0))
    report={'schema':'variable-block-negative-audit-v1','status':'PASS','base_receipt_sha256':sha256(raw).hexdigest(),
            'auditor_sha256':sha256(a.auditor.read_bytes()).hexdigest(),'validator_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'rejected_mutations':mutations}
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
