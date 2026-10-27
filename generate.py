#!/usr/bin/env python3
"""Deterministic fictional transaction dataset for Carbon Mirror Pilot 001."""
import argparse, csv, hashlib, json, random
from pathlib import Path
from datetime import date, timedelta

FIELDS=['record_id','location_id','date','category','amount_cents','units','note']
CATEGORIES=('materials','services','shipping','maintenance','supplies')

def checksum(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def generate(count,seed,out):
    rng=random.Random(seed); out.mkdir(parents=True,exist_ok=True)
    path=out/'input.csv'; invalid=0; dup=0
    # Preserve first occurrence: duplicates repeat an earlier complete business record.
    originals=[]
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader()
        for i in range(count):
            if i%23==0 and originals:
                row=dict(originals[rng.randrange(len(originals))]); dup+=1
            else:
                row={'record_id':f'R{i:09d}', 'location_id':f'L{rng.randint(1,10):02d}',
                     'date':(date(2026,1,1)+timedelta(days=rng.randint(0,89))).isoformat(),
                     'category':rng.choice(CATEGORIES),'amount_cents':str(rng.randint(100,200000)),
                     'units':str(rng.randint(1,20)),
                     'note':rng.choice(('routine monthly run','scheduled processing','regional operation','audit candidate'))}
                # Controlled malformed rows; expected to be rejected.
                if i%97==0: row['amount_cents']='invalid';invalid+=1
                elif i%131==0: row['location_id']='UNKNOWN';invalid+=1
                originals.append(row)
            w.writerow(row)
    manifest={'generator':'generate.py','schema_version':'1.0','seed':seed,'rows':count,
              'input_sha256':checksum(path),'intentional_duplicate_rows':dup,
              'intentional_invalid_original_rows':invalid,
              'data_policy':'fictional/synthetic; no personal data',
              'duplicate_policy':'first valid occurrence of a record_id wins; subsequent occurrences rejected',
              'validity_policy':'valid location L01-L10, ISO date, category allowlist, positive integer amount_cents and units'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rows',type=int,default=1000000);p.add_argument('--seed',type=int,default=1847);p.add_argument('--out',type=Path,default=Path('data'))
    a=p.parse_args();assert a.rows>0;generate(a.rows,a.seed,a.out)
