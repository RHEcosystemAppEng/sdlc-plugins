## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 16/16 | 0 | 100% |
| eval-2 | 12/14 | 2 | 86% |
| eval-3 | 15/15 | 0 | 100% |
| eval-4 | 7/11 | 4 | 64% |
| eval-5 | 11/15 | 4 | 73% |
| eval-6 | 14/14 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the three task files contain convention applicability rationale in the prescribed format. No 'Per CONVENTIONS.md §...' lines appear in any Implementation Notes section. No 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale appears anywhere. The repo-backend.md lists Key Conventions (Framework, Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching) which should have been validated and included with proper rationale. grep for 'Per CONVENTIONS' and 'Applies:' across all task files returned no matches. The only mention of 'convention' is a casual reference in Task 3: 'follows the model/ convention established in' — free-form prose, not the prescribed format."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment output file exists. The outputs directory contains only: impact-map.md, task-1-add-search-performance-indexes.md, task-2-implement-search-relevance-scoring.md, task-3-add-search-filter-parameters.md. The impact-map.md does not mention priority or fixVersion propagation. grep for 'propagat', 'inherit.*priority', 'inherit.*fixVers' across all output files returned no matches related to a summary comment. No file documents the priority and fixVersion values that were propagated to tasks."

</details>

<details>
<summary>eval-4: 4 failing assertions</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the four task descriptions contain the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Grep for 'Applies:' and 'CONVENTIONS' across all output files returned zero matches in the prescribed format. The repo has a CONVENTIONS.md file (per repo-backend.md) but no convention references with applicability rationales appear in any task's Implementation Notes. The tasks reference 'docs/constraints.md section 5' and use informal phrases like 'Follow the existing module pattern' and 'conventional approach', but these are not convention-aware enrichment per the rules."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature TC-9004 has Priority: Major. Grep for 'priority', 'additional_fields', and 'Major' across all output files returned zero matches. None of the four task descriptions mention priority inheritance or additional_fields containing priority. There is no evidence that the Major priority was propagated to created tasks."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature TC-9004 has Fix Versions: RHTPA 1.5.0. CLAUDE.md has no '### Jira Field Defaults' section, so fixVersion scope defaults to 'both'. Grep for 'fixVersion', 'RHTPA', and 'additional_fields' across all output files returned zero matches. None of the four task descriptions mention fixVersions inheritance. There is no evidence that RHTPA 1.5.0 was propagated to created tasks."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment file exists in the outputs directory. The only files present are impact-map.md, task-1-license-report-model.md, task-2-license-report-service.md, task-3-license-report-endpoint.md, and task-4-license-report-integration-tests.md. There is no file containing a summary comment for the feature issue (Step 6c). No mention of priority or fixVersion propagation appears anywhere in the outputs."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Bookend task files are missing required sections. task-1-create-feature-branch.md lacks 'Files to Modify' / 'Files to Create' and 'Implementation Notes' sections. task-8-merge-feature-branch.md similarly lacks 'Files to Modify' / 'Files to Create' and 'Implementation Notes' sections. Intermediate tasks 2-7 all contain every required section (Repository, Target Branch, Description, Files to Modify/Create, Implementation Notes, Acceptance Criteria, Test Requirements)."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains convention-aware enrichment with the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The tasks reference 'Key Conventions' from the repo description in Implementation Notes sections (e.g., task-2 line 22: 'Per repo Key Conventions: framework is SeaORM for database operations'), but these are informal prose references to the repository's coding patterns, not the formal convention applicability validation with structured rationale required by the assertion. No 'Applies:' rationale lines exist in any output file."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment file exists in the outputs directory. The outputs contain only impact-map.md and task-1 through task-8. The impact-map.md discusses workflow mode selection and the change impact but contains no mention of priority ('High') or fixVersion ('RHTPA 2.0.0') propagation. No output file contains a summary comment describing which field values were inherited by tasks or why they were omitted."

</details>

**Pass rate:** 87% · **Tokens:** 82,759 · **Duration:** 389s

**Baseline** (`40c31ac8`): 100% · 40,782 tokens · 233s

