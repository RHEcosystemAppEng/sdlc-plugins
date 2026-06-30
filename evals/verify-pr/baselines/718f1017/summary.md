## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 9/10 | 1 | 90% |
| eval-6 | 10/10 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — no reviews match the eval result detection criteria, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md does not contain an 'Eval Quality' row in the check table. The table includes: Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, and Verification Commands. There is no explicit 'Eval Quality' check with N/A verdict. While Test Quality is N/A, the specific assertion about Eval Quality being N/A is not satisfied because Eval Quality is not mentioned at all in the report."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "The test change classification verdict appears in the verification report summary table and is accompanied by a detailed analysis section explaining the structural and semantic assessment"
  **Evidence:** "The verification report summary table (lines 12-18) only contains Acceptance Criteria rows (criteria 1-5). The Test Change Classification does NOT appear as a row in that table. It appears as a standalone section header at line 29 ('## Test Change Classification: MIXED') and is mentioned in the Overall Verdict text at line 83, but is absent from the actual summary table. The detailed analysis section IS present (lines 33-70 covering Methodology, Structural Assessment, Semantic Assessment, and Classification), but the verdict is not in the summary table as required by the assertion."

</details>

**Pass rate:** 97% · **Tokens:** 29,905 · **Duration:** 144s

**Baseline** (`7142c02`): 100% · 34,764 tokens · 171s

