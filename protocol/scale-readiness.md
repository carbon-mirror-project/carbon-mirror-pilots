# Pilot 001 — Scale readiness checkpoint

**Exploratory readiness only. No baseline freeze or optimization.**

One GitHub Actions job generates one million synthetic records at seed 1847, runs the unchanged ETL baseline once, then checks every accepted row and summary group using a disk-backed SQLite oracle with streamed validated rows.

The dataset/output are ephemeral; only the checksum manifest, run metadata and host metadata are uploaded (30-day artifact retention). This demonstrates functional capacity but cannot justify optimization effects, carbon/energy reductions or a validated Carbon Mirror score.

The verifier is intentionally outside `baseline.py`; it does not change the workload whose resource use will later be measured.

**Unresolved preregistration items:** independent assessors and blinding; objective review scoring; performance acceptance criteria and uncertainty approach; within-runner randomized/blocked A/B tests; retention of durable evidence beyond Actions artifact expiry; hardware variability and environment details. Do not create the permanent baseline tag until resolved.
