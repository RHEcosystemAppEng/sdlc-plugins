## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/12 | 1 | 92% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 11/15 | 4 | 73% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "The report includes detailed findings with specific evidence for each domain — file-by-file scope comparison (Intent Alignment), line-level pattern scanning results (Security), per-criterion code-level verification (Correctness), and test quality assessment (Style/Conventions) — not just pass/fail verdicts in the summary table"
  **Evidence:** "Correctness has detailed findings via criterion-1.md through criterion-5.md with code snippets, analysis sections, and evidence for each acceptance criterion. However, Intent Alignment has only the summary table entry 'PR files match task specification exactly (3 files expected, 3 files changed)' with no file-by-file scope comparison listing individual files against the task specification. Security has only 'No secrets, credentials, or sensitive patterns detected in any added lines' with no line-level pattern scanning results. Style/Conventions has 'Repetitive Test Detection: WARN (2 tests could be parameterized); Test Documentation: PASS (all 4 tests documented)' in the table and one sentence in the summary paragraph, but no dedicated detailed findings section. Three of four domains lack detailed findings beyond the summary table."

</details>

<details>
<summary>eval-3: 4 failing assertions</summary>

- **Assertion:** "The review comment about adding an index (id 30002) is classified as suggestion — the reviewer uses suggestive language ('should also', 'would help') and the classification output (review-30002.md) explains this reasoning"
  **Evidence:** "review-30002.md classifies 30002 as 'code change request', not 'suggestion'. The reasoning states: 'The language "The migration should also add an index" is directive, not optional.' The file does not acknowledge the suggestive language ('should also', 'would help') as indicators of a suggestion. The assertion requires classification as 'suggestion' with reasoning about suggestive language, but the output classifies it as a code change request and treats the language as directive."

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "review-30002.md classifies comment 30002 as 'code change request' rather than 'suggestion', so no convention upgrade eligibility evaluation is performed. The file does not contain any analysis of whether the index suggestion matches a documented or demonstrated project convention. The report.md does not contain a Style/Conventions analysis section. No output file evaluates convention upgrade eligibility for this comment."

- **Assertion:** "Review comment 30002 (index suggestion) does NOT result in a sub-task — the suggestion classification is correct (suggestive language, no directive) and no project convention in the fixture data backs an upgrade from suggestion to code change request"
  **Evidence:** "review-30002.md classifies comment 30002 as 'code change request' (not 'suggestion') and states 'Action: Sub-task created to address this feedback.' subtask-2.md exists with a sub-task titled 'Add partial index on sbom.deleted_at in migration' for comment 30002. Report.md shows '30002 | ... | Code change request | Sub-task created'. The assertion requires no sub-task to be created, but a sub-task was created."

- **Assertion:** "The sub-task creation for comment 30001 explicitly specifies Issue Type as Sub-task — the subtask-30001.md file, the report's sub-task section, or the review classification output (review-30001.md) indicates the Jira issue is created with issueTypeName Sub-task (not as a standalone Task) to ensure parent-child hierarchy with the parent task"
  **Evidence:** "subtask-1.md (corresponding to comment 30001) does not contain any mention of 'Issue Type', 'Sub-task' as a Jira issue type, 'issueTypeName', or parent-child hierarchy. review-30001.md states 'Sub-task created' but does not specify the Jira issue type. Report.md sub-task table shows '| Wrap soft_delete cascade operations in a database transaction | Review feedback | Comment 30001 |' with a 'Type' column value of 'Review feedback', not the Jira issue type. No output file explicitly specifies that the Jira issue should be created with issueTypeName 'Sub-task'."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Sub-task descriptions include a Target PR section pointing to the PR URL https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747 so that implement-task adds commits to the existing PR branch"
  **Evidence:** "Both sub-task descriptions include a '## Target PR' section but with the wrong URL. subtask-1.md line 59: 'https://github.com/mrizzi/sdlc-plugins/pull/747'. subtask-2.md line 80: 'https://github.com/mrizzi/sdlc-plugins/pull/747'. The assertion requires 'https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747' (org: RHEcosystemAppEng) but the outputs use 'https://github.com/mrizzi/sdlc-plugins/pull/747' (org: mrizzi)."

</details>

**Pass rate:** 92% · **Tokens:** 73,744 · **Duration:** 347s

**Baseline** (`f08a8547`): 100% · 64,613 tokens · 249s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9*

