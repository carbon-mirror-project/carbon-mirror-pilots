# Pilot branch policy

`main` is intentionally a README-only landing branch. `pilot-001/research-foundation` is a standalone research branch with its own data, scripts, tests, and Actions workflows.

**Do not merge the pilot branch into `main`.** Both branches descended from a commit containing the pilot files, but `main` deliberately removed them. A pull-request synthetic merge checks out a tree that may not contain the test scripts and fails even when the source branch works.

To validate the pilot, use **push-triggered GitHub Actions on `pilot-001/research-foundation`**, not a PR merge build. Future PR-based review should use a dedicated pilot base branch or a restructured repository where the pilot lives under a directory in main; neither change has been approved.

The experimental baseline is not frozen; no optimized implementation or certification claim has been made.
