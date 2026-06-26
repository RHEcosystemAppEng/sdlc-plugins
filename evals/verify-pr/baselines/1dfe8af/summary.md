## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 10/10 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — no reviews match the eval result detection criteria, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md verification table does not contain an 'Eval Quality' row at all. The table includes: Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, Verification Commands. There is no Eval Quality check present, so the assertion that it is marked N/A with the specified reasoning cannot be confirmed."

</details>

**Pass rate:** 98% · **Tokens:** 34,895 · **Duration:** 140s

**Baseline** (`14692f2`): 100% · 64,828 tokens · 205s

