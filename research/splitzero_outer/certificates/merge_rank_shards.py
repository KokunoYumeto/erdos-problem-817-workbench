#!/usr/bin/env python3
"""Merge exact rank-five shards after checking complete ordered coverage."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from hashlib import sha256
import verify_rank_five as producer


def require(ok,text):
    if not ok:raise AssertionError(text)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('shards',nargs='+',type=Path)
    p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    data=[json.loads(x.read_text()) for x in args.shards]
    data.sort(key=lambda x:x['result']['evaluated_indices'][0]);r0=data[0]['result']
    k=r0['k'];Q=r0['benchmark_base'];domain=list(producer.blocks(5,Q-1));cursor=0
    require(len({x['validator_sha256'] for x in data})==1,'producer identities differ')
    require(len({x['helper_sha256'] for x in data})==1,'helper identities differ')
    for d in data:
        r=d['result'];lo,hi=r['evaluated_indices']
        require(r['k']==k and r['benchmark_base']==Q and lo==cursor and hi>lo,'gap or mismatched shard')
        require([tuple(a['generators']) for a in r['domain']]==domain[lo:hi],'literal shard coverage')
        cursor=hi
    require(cursor==len(domain),'incomplete final coverage')
    r=dict(r0);r['evaluated_indices']=[0,len(domain)]
    r['domain']=[a for d in data for a in d['result']['domain']]
    for key in ['exhaustive_generator_sets','integer_admissible','complete_return','full_controllers']:
        r[key]=sum(d['result'][key] for d in data)
    out=dict(data[0]);out['result']=r
    text=json.dumps(out,indent=2,sort_keys=True)+'\n';args.output.write_text(text,encoding='utf-8')
    print(json.dumps({'status':'PASS','k':k,'covered_generator_sets':cursor,
                      'output_sha256':sha256(text.encode()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
