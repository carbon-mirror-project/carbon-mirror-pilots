# Method A — Conventional data-engineering review (draft)

Reviewer: __________  Date: __________  Baseline revision: __________  Time budget: __________

Evaluate each area, recording **evidence, impact, recommendation, correctness risks, measurement proposal and reviewer confidence**:

1. Input/output contract and auditability
2. Algorithmic complexity and duplicate detection
3. CPU profiling and redundant transformations
4. Disk I/O passes, intermediary materialization and serialization
5. File formats and compression, including decompression overhead
6. Memory allocation and streaming behaviour
7. Caching, repeated work and incremental processing
8. Scheduling constraints and concurrency
9. Reliability, error handling, reproducibility and recoverability
10. Deployment cost, implementation effort and operational burden

For each observation: **ID | evidence | hypothesis | expected gain | possible loss | validation test | priority**.

Lock this checklist *before* seeing or scoring assessor findings. The checklist deliberately includes techniques that overlap with the Four Mirrors; omitting conventional knowledge would rig the comparison.
