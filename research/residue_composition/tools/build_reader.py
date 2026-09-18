#!/usr/bin/env python3
"""Build the single reading PDF from the included editable LaTeX.

Use --refresh-body to regenerate body.tex from the mathematical Markdown with
Pandoc. Long code paths are made breakable; no mathematical expression is edited.
Build intermediates stay in a temporary directory outside the source tree.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('continuation.pdf'))
    p.add_argument('--refresh-body',action='store_true')
    args=p.parse_args()
    tex=ROOT/'latex'
    if args.refresh_body:
        if not shutil.which('pandoc'):raise SystemExit('Pandoc is required for --refresh-body')
        body=subprocess.check_output(['pandoc','-f','markdown+tex_math_dollars','-t','latex','--wrap=none',
             str(ROOT/'notes/residue-and-composition.md')],text=True)
        def pathify(m):
            s=m.group(1)
            if len(s)>25 and ('/' in s or re.fullmatch('[0-9a-f]{40}',s)):
                return r'\path|'+s.replace(r'\_','_')+'|'
            return m.group(0)
        body=re.sub(r'\\texttt\{([^{}]*)\}',pathify,body)
        body=body.replace('https://arxiv.org/abs/1303.3539',r'\url{https://arxiv.org/abs/1303.3539}')
        (tex/'body.tex').write_text(body,encoding='utf-8')
    if not shutil.which('pdflatex'):raise SystemExit('pdflatex is required to build the reader')
    with tempfile.TemporaryDirectory(prefix='ep817-reader-') as temp:
        command=['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+temp,'main.tex']
        for _ in range(2):
            done=subprocess.run(command,cwd=tex,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            if done.returncode:
                raise SystemExit(done.stdout)
        log=(Path(temp)/'main.log').read_text(errors='replace')
        if 'Overfull \\hbox' in log:raise SystemExit('Overfull line in reader; inspect the LaTeX source')
        args.output.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(Path(temp)/'main.pdf',args.output)
    print(args.output.resolve())

if __name__=='__main__':main()
