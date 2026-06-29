## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 9/10 | 1 | 90% |
| eval-6 | 7/10 | 3 | 70% |

### Failed Assertions

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "The structural summary or reductive findings note the assertion change in test_recommend_purls_basic — the PURL assertion changed from checking a fully qualified PURL with qualifiers to checking a versioned PURL without qualifiers, which the semantic assessment may identify as a relaxation contributing to the MIXED classification"
  **Evidence:** "report.md line 19 mentions 'test_recommend_purls_basic updated' but does not describe the specific assertion change (from fully qualified PURL with qualifiers to versioned PURL without qualifiers). The report does not characterize this assertion change as a relaxation or reductive signal. criterion-1.md references the new assertion value ('pkg:maven/org.apache/commons-lang3@3.12') but does not compare it to the previous assertion or note the change as a relaxation contributing to the MIXED classification."

</details>

<details>
<summary>eval-6: 3 failing assertions</summary>

- **Assertion:** "An eval failure sub-task is created for failing eval-3 — a sub-task description file targets eval-3 assertion failures and includes the failing assertion text and evidence"
  **Evidence:** "The only sub-task file is subtask-1.md, which addresses the Documentation Coverage verdict mapping defect in SKILL.md Step 6a (a mapping to a non-existent 'Style Quality' report row). This sub-task was created from the acceptance criteria failure (AC7), not from eval-3's failing assertions. No sub-task description file targets eval-3 assertion failures about convention upgrade eligibility or sub-task creation for review comment 30002. The report.md confirms 'Root-Cause Investigation | N/A | No sub-tasks created from review feedback' and the Eval Results Summary states the failures are 'unrelated to the Documentation Coverage changes in this PR' but no eval-specific sub-task was created."

- **Assertion:** "Sub-task descriptions include Review Context with the failing assertion text and evidence from the eval review — the Review Context section quotes the two failing assertions about convention upgrade eligibility and sub-task creation, including the evidence text explaining what was missing"
  **Evidence:** "subtask-1.md has a 'Review Context' section (lines 22-27) but it discusses the AC7 mapping defect, not eval-3's failing assertions. The Review Context states: 'The original review comment (reviewer-b, comment 50001) flagged the Markdown exclusion rule in Check 6 but did not identify this mapping defect.' It does not quote any eval-3 assertions about convention upgrade eligibility or sub-task creation, nor does it include evidence text about what was missing from the eval review."

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "In report.md line 6, the Root-Cause Investigation row reads: '| Root-Cause Investigation | N/A | No sub-tasks created from review feedback |'. The verdict is N/A, not a non-N/A value. No eval failure sub-tasks were created, so no root-cause investigation was run on them."

</details>

**Pass rate:** 93% · **Tokens:** 71,166 · **Duration:** 291s

**Baseline** (`1dfe8af`): 98% · 34,895 tokens · 140s

