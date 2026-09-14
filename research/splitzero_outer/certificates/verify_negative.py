#!/usr/bin/env python3
"""Check six deliberately corrupted rank-five certificate fragments fail."""
from __future__ import annotations
import argparse,copy,gzip,json,tempfile
from hashlib import sha256
from pathlib import Path
import audit_rank_five as auditor


def fragment(full,index):
    x=dict(full);r=dict(full['result']);x['result']=r;e=copy.deepcopy(r['domain'][index])
    r['domain']=[e];r['evaluated_indices']=[index,index+1];r['exhaustive_generator_sets']=1;r['integer_admissible']=1
    r['complete_return']=int(e['method']=='complete_return');r['full_controllers']=1-r['complete_return']
    return x


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args();raw=gzip.decompress(args.record.read_bytes()) if args.record.suffix=='.gz' else args.record.read_bytes()
    full=json.loads(raw);D=full['result']['domain']
    i=next(i for i,e in enumerate(D) if e.get('method')=='complete_return' and e['best']['product']==65)
    j=next(i for i,e in enumerate(D) if e.get('method')=='full_controller')
    samples={'full':fragment(full,i),'ctrl':fragment(full,j)};mutations=[]
    with tempfile.TemporaryDirectory() as work:
        target=Path(work)/'probe.json'
        for x in samples.values():target.write_text(json.dumps(x));auditor.audit(target)
        def reject(name,kind,change):
            x=copy.deepcopy(samples[kind]);change(x['result']);target.write_text(json.dumps(x))
            try:auditor.audit(target)
            except (AssertionError,KeyError,IndexError,ValueError) as error:
                mutations.append({'mutation':name,'rejected':True,'diagnostic':str(error)})
            else:raise AssertionError('mutation accepted: '+name)
        reject('alter actual return primitive','full',lambda r:r['domain'][0]['section'][0][1].__setitem__(0,1000000))
        reject('remove earlier-base witness','full',lambda r:r['domain'][0]['smaller_base_obstructions'].pop())
        reject('claim smaller unproved base','full',lambda r:r['domain'][0]['best'].__setitem__('product',64))
        reject('remove a viable transfer','ctrl',lambda r:r['domain'][0]['edges'].pop())
        reject('erase positive potential','ctrl',lambda r:r['domain'][0]['potential'].__setitem__(0,'0'))
        reject('omit original generator support','full',lambda r:r.__setitem__('domain',[]))
    result={'status':'PASS','baseline_fragments':2,'rejected_mutations':mutations,
            'auditor_sha256':sha256(Path(auditor.__file__).read_bytes()).hexdigest(),
            'validator_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':main()
