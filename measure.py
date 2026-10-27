#!/usr/bin/env python3
"""Pilot 001 baseline measurements, not a methodology validation."""
import argparse,csv,hashlib,json,os,platform,subprocess,sys,tempfile,time,shutil
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def bench(source,out,warmups=3,runs=20,verify=False):
    source=Path(source).resolve();out=Path(out)
    if runs<1 or warmups<0:raise ValueError('Invalid repetition counts')
    if not source.is_file():raise FileNotFoundError(source)
    out.mkdir(parents=True,exist_ok=True)
    baseline=ROOT/'baseline.py';oracle=ROOT/'verify.py'
    meta={'status':'exploratory: not preregistered or frozen','timestamp_utc':datetime.now(timezone.utc).isoformat(),
          'input_sha256':digest(source),'baseline_sha256':digest(baseline),
          'oracle_sha256':digest(oracle),'harness_sha256':digest(__file__),
          'python':sys.version,'platform':platform.platform(),'cpu':platform.processor(),
          'logical_cpus':os.cpu_count(),'warmups':warmups,'repetitions':runs,
          'independent_verification':bool(verify),
          'limitations':'No energy, emissions, cost, or portable CPU/disk/memory metrics. Peak RSS is in platform units.'}
    expected=None; observations=[]
    with tempfile.TemporaryDirectory(prefix='cm-pilot001-') as tmp:
        for index in range(warmups+runs):
            target=Path(tmp)/('run-'+str(index));target.mkdir()
            start=time.perf_counter_ns()
            process=subprocess.run([sys.executable,str(baseline),'--input',str(source),'--out',str(target)],
                                   cwd=ROOT,check=True,capture_output=True,text=True)
            wall=(time.perf_counter_ns()-start)/1e9
            payload=json.loads(process.stdout)
            row={'run':index,'wall_seconds':round(wall,9),'internal_seconds':payload['elapsed_sec'],
                 'accepted':payload['accepted'],'rejected':payload['rejected'],'groups':payload['groups'],
                 'validated_bytes':(target/'validated.csv').stat().st_size,
                 'summary_bytes':(target/'summary.csv').stat().st_size,
                 'validated_sha256':digest(target/'validated.csv'),
                 'summary_sha256':digest(target/'summary.csv'),
                 'peak_rss_platform_units':payload.get('peak_rss_platform_units')}
            signature=tuple(row[k] for k in ('accepted','rejected','groups','validated_sha256','summary_sha256'))
            if expected is None:
                expected=signature
                if verify:
                    subprocess.run([sys.executable,str(oracle),'--input',str(source),'--out',str(target)],
                                   cwd=ROOT,check=True,capture_output=True,text=True)
            elif signature!=expected:raise AssertionError('Nondeterministic output at run '+str(index))
            if index>=warmups:observations.append(row)
            shutil.rmtree(target)
    (out/'measurement-manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    with (out/'measurements.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(observations[0]));writer.writeheader();writer.writerows(observations)
    print(json.dumps({'runs':runs,'verified':verify,'output':str(out)},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,default=Path('data/input.csv'))
    p.add_argument('--out',type=Path,default=Path('results/measurements'))
    p.add_argument('--warmups',type=int,default=3)
    p.add_argument('--runs',type=int,default=20)
    p.add_argument('--verify',action='store_true')
    a=p.parse_args();bench(a.input,a.out,a.warmups,a.runs,a.verify)
