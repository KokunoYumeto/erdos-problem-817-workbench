#!/usr/bin/env python3
"""Verify exported identities and exact audit-to-full-record bindings.

This verifies artifact identity and scope; it does not rerun the arithmetic
proofs. The separate producer and independent auditor provide those checks.
"""
from __future__ import annotations
import gzip,json
from hashlib import sha256
from pathlib import Path


def require(ok,text):
    if not ok:raise AssertionError(text)


def digest(p):return sha256(p.read_bytes()).hexdigest()


def main():
    root=Path(__file__).resolve().parents[1];cert=root/'certificates'
    manifest=json.loads((root/'polyclank/artifacts.json').read_text())
    for row in manifest['files']:
        p=root/row['path'];require(p.is_file() and digest(p)==row['sha256'],'artifact mismatch: '+row['path'])
    summary=json.loads((cert/'verification_summary.json').read_text());records={}
    for name,row in summary['records'].items():
        p=root/row['path'];require(digest(p)==row['gzip_sha256'],'gzip identity: '+name)
        raw=gzip.decompress(p.read_bytes());require(sha256(raw).hexdigest()==row['sha256'],'plaintext identity: '+name)
        records[name]=json.loads(raw)
    outer=records['outer_control_receipt.json'];helper=digest(cert/'verify_outer_control.py')
    require(outer['validator_sha256']==helper,'outer producer identity')
    for k in (5,6):
        rr=records[f'rank_five_k{k}_receipt.json']
        require(rr['validator_sha256']==digest(cert/'verify_rank_five.py') and rr['helper_sha256']==helper,'rank producer identity')
    audit=json.loads((cert/'complete_rank_five_audit.json').read_text());auditor=digest(cert/'audit_rank_five.py')
    require(audit['auditor_sha256']==auditor,'independent auditor identity')
    k5=records['rank_five_k5_receipt.json'];cursor=0
    for part in audit['k5']['parts']:
        lo,hi=part['audited_indices'];require(lo==cursor and hi>lo,'audit coverage gap');cursor=hi
        reconstructed=dict(k5);r=dict(k5['result']);reconstructed['result']=r
        r['domain']=r['domain'][lo:hi];r['evaluated_indices']=[lo,hi];r['exhaustive_generator_sets']=hi-lo
        r['complete_return']=sum(e.get('method')=='complete_return' for e in r['domain'])
        r['full_controllers']=sum(e.get('method')=='full_controller' for e in r['domain'])
        r['integer_admissible']=r['complete_return']+r['full_controllers']
        payload=(json.dumps(reconstructed,indent=2,sort_keys=True)+'\n').encode()
        require(sha256(payload).hexdigest()==part['plain_receipt_sha256'],'audited shard differs from full record')
    require(cursor==k5['result']['complete_domain_size']==41185,'rank-five k5 coverage incomplete')
    require(audit['k5']['full_plain_receipt_sha256']==summary['records']['rank_five_k5_receipt.json']['sha256'],'combined audit binding')
    require(audit['k6']['audited_indices']==[0,6074] and
            audit['k6']['plain_receipt_sha256']==summary['records']['rank_five_k6_receipt.json']['sha256'],'rank-five k6 coverage incomplete')
    negative=json.loads((cert/'negative_audit_receipt.json').read_text())
    require(negative['auditor_sha256']==auditor and negative['validator_sha256']==digest(cert/'verify_negative.py'),'negative checker identity')
    require(len(negative['rejected_mutations'])==6 and all(x['rejected'] for x in negative['rejected_mutations']),'negative regressions incomplete')
    print(json.dumps({'status':'PASS','artifact_files':len(manifest['files']),'complete_receipts':3,
                      'independently_audited_rank_five_cases':41185+6074,
                      'scope':'Exact file, producer, auditor, and complete audit-coverage bindings; no arithmetic replay claimed.'},indent=2))

if __name__=='__main__':main()
