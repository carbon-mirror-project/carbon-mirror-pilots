#!/usr/bin/env python3
"""Simple, plausible multi-stage CSV processing baseline. Do not optimize before assessment."""
import argparse,csv,json,time,resource,hashlib
from pathlib import Path
from collections import defaultdict
from datetime import date
from generate import FIELDS,CATEGORIES,checksum

def valid(r):
    try:
        if r['location_id'] not in {f'L{i:02d}' for i in range(1,11)}: return False
        date.fromisoformat(r['date'])
        if r['category'] not in CATEGORIES: return False
        if int(r['amount_cents']) <= 0 or int(r['units']) <= 0:return False
        if not r['record_id']:return False
        return True
    except (ValueError,KeyError,TypeError):return False

def process(source,out):
    out.mkdir(parents=True,exist_ok=True)
    # Two-phase ETL: standardized intermediate CSV and a separate reporting pass.
    # Common in small business reporting; these stages add I/O, but preserve an auditable extract.
    seen=set(); rejected=0; accepted=0
    with source.open(newline='',encoding='utf-8') as inf, (out/'validated.csv').open('w',newline='',encoding='utf-8') as vf:
        reader=csv.DictReader(inf);w=csv.DictWriter(vf,fieldnames=FIELDS);w.writeheader()
        for row in reader:
            if not valid(row) or row['record_id'] in seen:
                rejected+=1;continue
            seen.add(row['record_id']);w.writerow(row);accepted+=1
    aggregates=defaultdict(lambda:[0,0,0]);
    with (out/'validated.csv').open(newline='',encoding='utf-8') as vf:
        for row in csv.DictReader(vf):
            key=(row['location_id'],row['category']);a=aggregates[key]
            a[0]+=1;a[1]+=int(row['amount_cents']);a[2]+=int(row['units'])
    with (out/'summary.csv').open('w',newline='',encoding='utf-8') as sf:
        w=csv.writer(sf);w.writerow(['location_id','category','record_count','total_amount_cents','total_units'])
        for (loc,cat),values in sorted(aggregates.items()):w.writerow([loc,cat,*values])
    return {'accepted':accepted,'rejected':rejected,'groups':len(aggregates)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path('data/input.csv'));p.add_argument('--out',type=Path,default=Path('results/baseline'))
    a=p.parse_args();t=time.perf_counter();result=process(a.input,a.out);result['elapsed_sec']=round(time.perf_counter()-t,6)
    result['peak_rss_platform_units']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result['validated_sha256']=checksum(a.out/'validated.csv');result['summary_sha256']=checksum(a.out/'summary.csv')
    (a.out/'run.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
