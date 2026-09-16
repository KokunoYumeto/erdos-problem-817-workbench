from certificates.carry_tools import *
import json
from pathlib import Path
from time import monotonic
A=(1,4,5,17,21,22);D=subset_sums(A);out=[];t=monotonic()
for k in (5,6):
 for b in range(23,71):
  cert=full_carry_certificate(D,b,k)
  out.append({'k':k,'base':b,'safe':cert['safe'],'states_seen':cert['states_seen'],
              'length':cert.get('length'),'witness':cert.get('witness')})
  if cert['safe']: print('SAFE',k,b,cert['states_seen'],flush=True)
 print('DONE',k,monotonic()-t,flush=True)
directory=Path(__file__).resolve().parent/'logs';directory.mkdir(exist_ok=True)
(directory/'noncanonical_fixed_block.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
