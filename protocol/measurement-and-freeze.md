# Pilot 001 — Measurement and freeze gate

**Status: NOT FROZEN / NOT PREREGISTERED.** The committed 10,000-record dataset and outputs are smoke-test fixtures, not formal benchmark findings.

## Before formal experiment

1. Review and checksum `baseline.py`, `generate.py`, `verify.py`, `measure.py`, conventional checklist and Four Mirrors worksheet.
2. Specify machine CPU, physical RAM, disk type, OS, Python version, governor/power settings and competing-workload controls.
3. Select dataset size and seed **before trials** (1,000,000 records proposed). Confirm the independent SQLite oracle has sufficient memory; otherwise implement and test a disk-backed oracle before freeze.
4. Define output contract: `validated.csv` is an audit artifact and cannot be silently deleted to inflate results; both report and extract must remain correct.
5. Lock reviewer identities and comparability, assessment order, equal assessment-time budget, and blinding. The planted inefficiency manifest must be withheld before locked findings. Single-assessor reviews are exploratory only.
6. Define primary metrics, unacceptable regressions, practical significance thresholds and variance treatment. The proposed 10% improvement is not yet an approved statistical pass gate.
7. Complete `registration-template.md`, commit the registration and tag exact baseline SHA before optimization or official measurements.

## Tooling

From repository root:

```bash
python -m unittest -v test_pilot.py
python measure.py --input data/input.csv --out results/measurements --warmups 3 --runs 20 --verify
```

Runs launch a fresh baseline subprocess in a clean temporary directory. Manifest logs code/input SHA-256, environment and repeated raw wall times, file sizes, counters and output checksums. The first run may be checked against SQLite with `--verify`; later output must match exactly. This is **not** formal benchmark randomization and is affected by caching, thermal behaviour and host load.

**Instrument limitations:** `baseline.py` requires Unix `resource`, and its peak RSS has platform-specific units. The harness does not measure portable CPU time, true disk-I/O bytes, energy use, emissions, or cloud bills. No environmental claims should be based on runtime or output-size changes alone.

A conventional optimization result is not a Carbon Mirror methodology win unless a fair, independently reviewed methods comparison supports a distinct contribution. Do not tag or freeze the baseline until all seven conditions above are fulfilled.
