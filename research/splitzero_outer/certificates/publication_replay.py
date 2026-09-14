#!/usr/bin/env python3
"""Regenerate and independently audit the delivered outer-control proof records.

Original sources and decoded certificate bytes are hash-pinned. Work happens in
a separate directory. Only successful, completely checked outputs are installed.
No token, network access, or Git operation occurs in this program.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / 'certificates'
SOURCES = {
    'notes/outer-support-control.md': 'cf87ac7e695ad4b64b80e2e0049f8b2088539973426b49bc046e500fa7a1a543',
    'certificates/verify_outer_control.py': '7069fd11355c02f05371489ffb4dc62a6e0247d5b05a553c7bbcd334104d02d0',
    'certificates/verify_rank_five.py': 'f38dd2921f5f9e92a984d0796df9b353d603e23459cf34b58ae8f248c1fcc7f5',
    'certificates/audit_rank_five.py': '2535c7548c524645edeafa4eac7a7d8917c13ac0b3a8855d6d105b00f375825c',
    'certificates/merge_rank_shards.py': '8b24f2939a4c4c024eceed6d4876ff67bf8712b06ff49e527280617313c3b0c4',
    'certificates/verify_negative.py': '96a732e5706ad62bda1001a2a3739b3ecb295a6400657924a5e721050010c854',
}
RECORDS = {
    'outer_control_receipt.json': '3478663013d47efb313de4b63dff68250a1b9d80f31f085ff886b10026cc969f',
    'rank_five_k5_receipt.json': '5bd67da0abbc63cad5a226d5ade39ed2f95ece357ed3b121ff2ce40c7e99c240',
    'rank_five_k6_receipt.json': '708502d4bfa7e696e8f5435baeac775df8eda521974ca26b022df2941a4f5445',
}
INTERVALS = ((0,10000),(10000,20000),(20000,30000),(30000,41185))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def check_sources() -> None:
    for name, expected in SOURCES.items():
        require(digest(ROOT/name) == expected, 'source identity changed: '+name)


def command(work: Path, label: str, script: str, *args: object, optimized: bool = False) -> None:
    argv = [sys.executable] + (['-O'] if optimized else []) + [str(CERT/script)] + list(map(str,args))
    log = work/(label+'.log')
    with log.open('wb') as out:
        result = subprocess.run(argv, stdout=out, stderr=subprocess.STDOUT, timeout=7200, check=False)
    if result.returncode:
        tail = log.read_text(errors='replace')[-6000:]
        raise RuntimeError(f'{label} exited {result.returncode}:\n{tail}')
    print('PASS',label,flush=True)


def parallel(tasks, workers: int) -> None:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(fn,*args,**kwargs) for fn,args,kwargs in tasks]
        for done in as_completed(futures):
            done.result()


def install(work: Path) -> dict:
    encoded = {}
    # Check every original full plaintext before installing even one record.
    for name, expected in RECORDS.items():
        source = work/name
        require(digest(source) == expected, 'full decoded record differs: '+name)
        raw = source.read_bytes()
        compressed = gzip.compress(raw, compresslevel=9, mtime=0)
        require(gzip.decompress(compressed) == raw, 'lossless compression failed')
        encoded[name] = compressed
    records = {}
    for name, data in encoded.items():
        target = CERT/(name+'.gz')
        temporary = target.with_suffix('.gz.new')
        temporary.write_bytes(data)
        temporary.replace(target)
        records[name] = {'plain_sha256':RECORDS[name], 'gzip_sha256':sha256(data).hexdigest(),
                         'gzip_bytes':len(data), 'path':target.name}
    return records


def replay(work: Path, workers: int) -> dict:
    check_sources()
    tasks = [
        (command,(work,'outer','verify_outer_control.py','--output',work/'outer_control_receipt.json'),{}),
        (command,(work,'rank6','verify_rank_five.py','--k',6,'--output',work/'rank_five_k6_receipt.json'),{}),
    ]
    for i,(lo,hi) in enumerate(INTERVALS):
        tasks.append((command,(work,f'k5_{i}','verify_rank_five.py','--k',5,
            '--start-index',lo,'--stop-index',hi,'--output',work/f'k5_{i}.json'),{}))
    parallel(tasks,workers)
    shards = [work/f'k5_{i}.json' for i in range(len(INTERVALS))]
    command(work,'merge','merge_rank_shards.py',*shards,'--output',work/'rank_five_k5_receipt.json')
    for name,expected in RECORDS.items():
        require(digest(work/name)==expected,'producer result differs from delivered proof: '+name)
    audit_tasks = [(command,(work,f'audit5_{i}','audit_rank_five.py',p,'--output',work/f'audit5_{i}.json'),{})
                   for i,p in enumerate(shards)]
    audit_tasks += [
        (command,(work,'audit6','audit_rank_five.py',work/'rank_five_k6_receipt.json','--output',work/'audit6.json'),{}),
        (command,(work,'negative','verify_negative.py',work/'rank_five_k5_receipt.json','--output',work/'negative.json'),{}),
        (command,(work,'negative_optimized','verify_negative.py',work/'rank_five_k5_receipt.json','--output',work/'negative_optimized.json'),{'optimized':True}),
        (command,(work,'outer_optimized','verify_outer_control.py','--output',work/'outer_optimized.json'),{'optimized':True}),
    ]
    parallel(audit_tasks,workers)
    require((work/'outer_optimized.json').read_bytes()==(work/'outer_control_receipt.json').read_bytes(),
            'normal/optimized outer replay differs')
    require((work/'negative_optimized.json').read_bytes()==(work/'negative.json').read_bytes(),
            'normal/optimized negative replay differs')
    parts = [json.loads((work/f'audit5_{i}.json').read_text())['results'][0] for i in range(4)]
    for (lo,hi),part in zip(INTERVALS,parts):
        require(part['status']=='PASS' and part['audited_indices']==[lo,hi], 'audit interval differs')
    sixth = json.loads((work/'audit6.json').read_text())['results'][0]
    require(sixth['status']=='PASS' and sixth['audited_indices']==[0,6074], 'k6 audit incomplete')
    negative = json.loads((work/'negative.json').read_text())
    require(len(negative['rejected_mutations'])==6 and all(x['rejected'] for x in negative['rejected_mutations']),
            'negative tests incomplete')
    check_sources()
    records = install(work)
    return {'schema':'ep817-outer-publication-replay-v1','status':'PASS','lean_checked':False,
        'scope':'Fresh complete producers, independent arithmetic audits, source and decoded-record identity checks.',
        'source_sha256':SOURCES,'records':records,'k5_audit_parts':parts,'k6_audit':sixth,
        'independently_audited_generator_sets':47259,'negative_audit':negative,
        'normal_optimized_outer_identical':True,'normal_optimized_negative_identical':True,
        'python':platform.python_version(),'zlib':zlib.ZLIB_VERSION,
        'github_run_id':os.environ.get('GITHUB_RUN_ID'),
        'github_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
        'checked_commit':os.environ.get('CHECKED_COMMIT'),
        'driver_sha256':digest(Path(__file__))}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=2)
    parser.add_argument('--work-dir',type=Path)
    args=parser.parse_args()
    require(1<=args.jobs<=8,'jobs must be in [1,8]')
    with tempfile.TemporaryDirectory(prefix='ep817-publication-') as temporary:
        work=args.work_dir or Path(temporary)
        work.mkdir(parents=True,exist_ok=True)
        result=replay(work,args.jobs)
        text=json.dumps(result,indent=2,sort_keys=True)+'\n'
        (CERT/'publication_replay_receipt.json').write_text(text,encoding='utf-8')
        print(text,end='')


if __name__=='__main__':
    main()
