## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 12/15 | 3 | 80% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — no reviews match the eval result detection criteria, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md table does not contain an 'Eval Quality' row. The table includes: Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, and Verification Commands. There is no explicit mention of 'Eval Quality' anywhere in report.md or in any criterion file. Without an explicit Eval Quality row or section marked N/A, there is no concrete evidence that this check was evaluated and classified as N/A."

</details>

<details>
<summary>eval-3: 3 failing assertions</summary>

- **Assertion:** "Each sub-task description includes a Target PR section with the PR URL https://github.com/trustify/trustify-backend/pull/744 (constraint 1.12)"
  **Evidence:** "subtask-1.md includes '## Target PR
https://github.com/trustify/trustify-backend/pull/744' -- PASS. However, subtask-2.md (root-cause task) has no '## Target PR' section at all. The assertion requires 'Each sub-task description' to include this section, and subtask-2.md does not."

- **Assertion:** "Each sub-task description includes a Review Context section with the original review comment text (constraint 1.12)"
  **Evidence:** "subtask-1.md includes '## Review Context' with the full original comment text from reviewer-a. However, subtask-2.md has no '## Review Context' section. The assertion requires 'Each sub-task description' to include this section, and subtask-2.md does not."

- **Assertion:** "The sub-task creation for comment 30001 explicitly specifies Issue Type as Sub-task — the subtask-30001.md file, the report's sub-task section, or the review classification output (review-30001.md) indicates the Jira issue is created with issueTypeName Sub-task (not as a standalone Task) to ensure parent-child hierarchy with the parent task"
  **Evidence:** "subtask-1.md (the sub-task for comment 30001) does not contain any mention of 'Issue Type', 'issueTypeName', 'Sub-task' as a Jira issue type, or parent-child hierarchy. review-30001.md says 'Sub-task created to address this feedback' but does not specify the Jira issue type. The report says 'Sub-task created: wrap soft_delete in transaction' but does not explicitly specify that the Jira issue type is Sub-task (issueTypeName Sub-task). None of the output files explicitly indicate the Jira issue is created with issueTypeName Sub-task to ensure parent-child hierarchy."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Sub-task descriptions include a Target PR section pointing to the PR URL https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747 so that implement-task adds commits to the existing PR branch"
  **Evidence:** "Both sub-task files include a Target PR section but with a different URL. subtask-1.md line 31: 'https://github.com/mrizzi/sdlc-plugins/pull/747'. subtask-2.md line 19: 'https://github.com/mrizzi/sdlc-plugins/pull/747'. The assertion requires URL 'https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747' (owner: RHEcosystemAppEng) but the actual URL uses owner 'mrizzi'. The GitHub organization/owner does not match."

</details>

**Pass rate:** 94% · **Tokens:** 66,356 · **Duration:** 262s

**Baseline** (`3337d1fd`): 100% · 62,796 tokens · 238s

