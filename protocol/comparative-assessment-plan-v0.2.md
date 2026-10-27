# Pilot 001 — Comparative Assessment Plan v0.2

**Status:** proposed, not registered; no assessments conducted.

## Claim under test
Does use of the Four Mirrors generate additional *validated* diagnostic value beyond ordinary data-engineering review of the identical workload, with equal evidence, tools and time?

A competent conventional engineer can discover all of the expected inefficiencies. Do not handicap Method A to manufacture Carbon Mirror differentiation.

## Reviewer plan (preferred)
Recruit **four qualified assessors** with comparable data-processing experience. Randomly assign two to Method A and two to Method B. With fewer assessors, call the exercise exploratory; with one assessor, no comparative superiority conclusion is supportable. Recruit outside the creator's immediate project where possible, disclose all conflicts, and do not permit reviewers to see the other method's worksheet or findings before submission.

Prior to assignment: record relevant experience, method familiarity and conflicts; provide equal orientation material and equal time allowances. Carbon Mirror reviewers can study the Four Mirrors before the clock starts; conventional reviewers receive their checklist and equal preparation time.

## Dataset, evidence and blinding
Give assessors a frozen commit SHA, the exact baseline code, schema, dataset sample, business requirements, summary output contract, and baseline profiling evidence produced by an impartial operator. Withhold the generator's deliberately introduced anomaly rules or answer key where possible; reviewers must not inspect `generate.py` or the sealed problem manifest during diagnostic assessment. The shared repo is public, so **true blinding cannot be guaranteed**. Note this as a material limitation, ask for signed self-report of prior exposure, and if necessary use a new independently sourced workload in a subsequent external validation.

Each reviewer must use their assigned worksheet and submit findings in a private time-stamped file before any public publication or cross-group discussion. Avoid posting unsealed observations or benchmark answers to public issues.

## Review duration
Proposal: 90 minutes of evaluation after a common 30-minute orientation. Time spent locating documentation and reproducing performance signals counts within evaluation time; pre-study/preparation budgets must be symmetric. These budgets are planning choices, not empirically validated.

## Required finding fields
`finding_id`, `reviewer`, `method`, `baseline_sha`, `evidence`, `hypothesis`, `intervention`, `predicted_metric`, `direction`, `expected_tradeoff`, `correctness_risk`, `validation_test`, `priority`, `review_minutes`, `confidence`.

## Predeclared adjudication
Before opening reviewer findings, establish an adjudicator and resolve the criteria:
- **Valid**: genuine inefficiency or meaningful operational concern supported by evidence and feasible intervention/verification; not merely generic advice.
- **Material**: plausible operational decision consequence; report expected effect and the verification outcome, without retroactively imposing thresholds.
- **Unique**: an actionable insight absent from the other method at equivalent specificity, even after combining equivalent phrasing.
- **Safety finding**: credible contract, correctness, reliability, retention or operational risk.
- **Duplicates**: equivalent root cause and action collapse into one finding regardless of language.
- Compare total validated opportunities, material unique opportunities, significant tradeoffs, assessor time, evidence completeness and false leads. Do not rely on raw finding count alone.
- Have a second independent adjudicator audit at least a sample of decisions; report disagreements and unresolved items.

## Decision rules
- Methods equivalent: both detect the same material issues with no credible difference in effort or decision quality.
- Carbon Mirror promising: at least one independently validated, materially consequential opportunity, risk or decision improvement absent under conventional review, **and** a credible explanation why the method surfaced it.
- Conventional review better: it has stronger validated findings or assessment efficiency without offsetting benefits.
- Inconclusive: insufficient reviewer independence, imbalanced exposure, low power, or adjudicator disagreement.

One small experiment does not demonstrate generalized superiority. Report individual reviewer contributions and uncertainty rather than an unsupported significance claim.

## After locked findings
Use an engineering implementation phase to test candidate improvements, retaining correct audit extract and report semantics. In future paired A/B measurement designs, compare baseline and interventions on the **same** hosted runner within one job using interleaved/randomized blocks; never compare separate CI runs as if they were identical hardware.

## Publication and ethics
Prepublish protocol, after review publish redacted findings and negative results. Do not publish private reviewer notes or personal data without consent. Report deviations and limitations. No formal Carbon Mirror score, certification or environmental claim.
