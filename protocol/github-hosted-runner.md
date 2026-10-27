# Hosted-runner research environment

**Status: exploratory; baseline not frozen.**

Pilot 001 uses GitHub-hosted `ubuntu-24.04`, Python 3.11, 100,000 synthetic records (seed 1847), 2 warmup runs and 5 measured repetitions. The benchmark is triggered by the workflow or source changes on the pilot branch; manual dispatch may require the workflow on the default branch and is not relied upon.

Runner CPU specifications, image versions and background load can change. These runs check execution feasibility and output correctness **only**, not comparable cross-runner performance or environmental savings. The artifact contains host metadata, SHA-256 input manifest and run-by-run measurements, retained for 30 days. Archive relevant evidence before expiration.

**Before scientific freeze:** choose full data size (proposed 1,000,000 records); address memory use of SQLite verifier; create within-job interleaved/randomized control vs intervention measurements; establish fair independent method reviewers and pre-registered success thresholds; document runner limitations and complete protocol registration. The original pipeline is unchanged, and this workflow makes no claims for Carbon Mirror scoring or certification.
