## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 9/11 | 2 | 82% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "The report includes detailed findings for each failing check with specific evidence from the diff — Scope Containment identifies the missing test file by comparing PR files against the task specification, Acceptance Criteria provides per-criterion analysis explaining each gap"
  **Evidence:** "The Acceptance Criteria section does provide detailed per-criterion analysis with code-level evidence for each gap. However, Scope Containment is marked as PASS ('Changes are scoped to the two files specified in the task') and does NOT identify the missing test file. The missing test file is instead flagged under 'Test Quality'. The assertion requires Scope Containment to identify the missing test file by comparing PR files against the task specification, but it does not — it only checks that the files present in the diff are within scope, not that required files are missing."

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — no reviews match the eval result detection criteria, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md verification table does not contain an 'Eval Quality' row at all. The table includes: Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, and Verification Commands. There is no Eval Quality row marked N/A or otherwise."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "report.md line 6: '| Root-Cause Investigation | N/A | Defect is a feature scope gap, not a systemic workflow issue |' — the Root-Cause Investigation verdict is N/A, contradicting the assertion that it should not be N/A. The investigation pipeline did not process the eval failure sub-tasks through root-cause investigation."

</details>

**Pass rate:** 95% · **Tokens:** 65,724 · **Duration:** 275s

**Baseline** (`cc2dc3d`): 100% · 35,450 tokens · 180s

