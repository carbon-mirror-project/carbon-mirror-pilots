"""Functional smoke tests; no performance conclusions."""
import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class PilotTests(unittest.TestCase):
    def run_script(self,*args):
        return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,check=True,capture_output=True,text=True)
    def test_baseline_oracle_determinism(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);data=p/'data'
            self.run_script(ROOT/'generate.py','--rows','10000','--seed','1847','--out',data)
            results=[]
            for out in (p/'one',p/'two'):
                self.run_script(ROOT/'baseline.py','--input',data/'input.csv','--out',out)
                self.run_script(ROOT/'verify.py','--input',data/'input.csv','--out',out)
                results.append(json.loads((out/'run.json').read_text()))
            self.assertEqual((results[0]['accepted'],results[0]['rejected'],results[0]['groups']),(9393,607,50))
            for field in ('validated_sha256','summary_sha256'):
                self.assertEqual(results[0][field],results[1][field])
    def test_harness_outputs(self):
        from measure import bench
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);data=p/'data';out=p/'runs'
            self.run_script(ROOT/'generate.py','--rows','300','--seed','1847','--out',data)
            bench(data/'input.csv',out,1,2,True)
            self.assertEqual(len((out/'measurements.csv').read_text().splitlines()),3)
            m=json.loads((out/'measurement-manifest.json').read_text())
            self.assertTrue(m['independent_verification'])
            self.assertEqual(m['repetitions'],2)
if __name__=='__main__':unittest.main()
