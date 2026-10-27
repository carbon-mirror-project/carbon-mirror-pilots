#!/usr/bin/env python3
"""Independent SQLite-based oracle: verifies baseline results against the raw input."""
import argparse,csv,sqlite3
from pathlib import Path
from datetime import date
from generate import CATEGORIES,checksum

def valid(r):
    try:
        return (r['location_id'] in tuple(f'L{i:02d}' for i in range(1,11)) and
                bool(date.fromisoformat(r['date'])) and r['category'] in CATEGORIES and
                int(r['amount_cents'])>0 and int(r['units'])>0 and bool(r['record_id']))
    except (ValueError,TypeError,KeyError):return False

def check(source,out):
    db=sqlite3.connect(':memory:');db.execute('CREATE TABLE t (record_id TEXT PRIMARY KEY, location_id TEXT, category TEXT, amount INT, units INT)')
    rejects=0;count=0
    with source.open(newline='',encoding='utf-8') as inf:
        for r in csv.DictReader(inf):
            if not valid(r):rejects+=1;continue
            try:
                db.execute('INSERT INTO t VALUES (?,?,?,?,?)',(r['record_id'],r['location_id'],r['category'],int(r['amount_cents']),int(r['units'])));count+=1
            except sqlite3.IntegrityError:rejects+=1
    expected={(loc,cat):(n,total,units) for loc,cat,n,total,units in db.execute('SELECT location_id,category,count(*),sum(amount),sum(units) FROM t GROUP BY location_id, category')}
    actual={}
    with (out/'summary.csv').open(newline='',encoding='utf-8') as sf:
        for r in csv.DictReader(sf):
            key=(r['location_id'],r['category'])
            if key in actual:raise AssertionError('Duplicate summary group')
            actual[key]=(int(r['record_count']),int(r['total_amount_cents']),int(r['total_units']))
    assert actual==expected,'Summary mismatch'
    with (out/'validated.csv').open(newline='',encoding='utf-8') as vf:
        rows=list(csv.DictReader(vf))
    assert len(rows)==count,'Validated record count mismatch'
    for r in rows:
        result=db.execute('SELECT location_id,category,amount,units FROM t WHERE record_id=?',(r['record_id'],)).fetchone()
        assert result==(r['location_id'],r['category'],int(r['amount_cents']),int(r['units'])),'Incorrect validated row'
    print(f'PASS: {count} validated; {rejects} rejected; {len(expected)} summary groups')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path('data/input.csv'));p.add_argument('--out',type=Path,default=Path('results/baseline'))
    a=p.parse_args();check(a.input,a.out)
