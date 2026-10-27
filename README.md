# Carbon Mirror Pilot 001 — Baseline Design Package

**Status:** baseline design + smoke test only. No optimization, independent methods comparison, or environmental claim has been made.

## Purpose

A reproducible fictional transaction-processing system for the approved Data Weight Challenge. It gives both assessment methods the same raw workload and correctness oracle. No production data or APIs are used.

## Requirements

Python 3.10+; standard library only. The scripts have been tested in a Linux environment. `baseline.py` uses `resource` (Unix-only); on Windows run under WSL or adjust measurement instrumentation before starting the formal experiment.

## Quick start

```bash
python generate.py --rows 10000 --seed 1847 --out data
python baseline.py --input data/input.csv --out results/baseline
python verify.py --input data/input.csv --out results/baseline
```

**Before a formal baseline**, establish machine specification, freeze scripts and dependencies, choose a scale (proposed 1,000,000 rows, subject to hardware), and produce a signed or hashed pre-registration record. The 10,000-row example is a smoke test, not experimental evidence.

## Data schema

`record_id`, `location_id`, `date`, `category`, `amount_cents`, `units`, `note`. Locations L01–L10; five categories; synthetic dates in January–March 2026. Money uses integer cents to avoid rounding discrepancies. Source duplicates reuse an earlier entire row. Invalid original rows have deliberately malformed amount or location; they are rejected. A row is accepted only if it is valid and its `record_id` has not already been accepted. Summary is grouped by location and category.

## Baseline architecture

1. Stream input CSV and validate each row.
2. Deduplicate by record ID, preserving the first valid occurrence.
3. Write a complete standardized intermediate `validated.csv`, as is common in file-oriented back-office ETL.
4. Re-read that intermediate file for aggregation.
5. Write an auditable `summary.csv` and per-run metadata.

This is functional and plausible, not artificial delay code. A second-stage re-read and an intermediate extract may have real business justifications, which are to be weighed against their costs. They are **not pre-labelled as waste**.

## Test integrity

- `verify.py` uses an independent SQLite grouping implementation rather than reusing baseline aggregation code.
- The generator's record volume and seed plus SHA-256 manifest ensure input reproducibility.
- The `run.json` metadata offers a convenience timer but is **not** a formally adequate benchmark. CPU time, I/O bytes, energy (if available), variance and confidence intervals require a separate frozen measurement harness.
- A single-method assessment by the founder and assistant is exploratory, not an independent comparative validation.
- No composite efficiency score or Bronze/Silver/Obsidian claim is authorized by this package.

## Known risks and decisions before formal execution

- Independent assessment needs reviewers of comparable experience and a conventional checklist frozen beforehand.
- A deliberately synthetic workload can make certain optimizations easier to discover than in actual operations.
- SQLite oracle for one million rows uses memory; confirm capacity or change oracle to an on-disk database before registration.
- `ru_maxrss` units vary by platform, so do not use it as a cross-platform metric without normalization.
- Choose an experimental measurement method and decide how intermediate audit files factor into the output contract **before** optimization.
- No methods should be declared superior based only on technical speedup.
