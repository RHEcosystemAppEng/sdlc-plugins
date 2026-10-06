## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 17/19 | 2 | 89% |
| eval-2 | 14/16 | 2 | 88% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 9/11 | 2 | 82% |
| eval-5 | 13/15 | 2 | 87% |
| eval-6 | 12/14 | 2 | 86% |

### Failed Assertions

<details>
<summary>eval-1: 2 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:'"
  **Evidence:** "All 8 digest files (task-1-digest.md through task-8-digest.md) exist but contain placeholder text: '[sdlc-workflow] Description digest: sha256-md:&lt;computed-after-jira-persistence&gt;'. The value '&lt;computed-after-jira-persistence&gt;' is not 64 lowercase hex characters — it is a placeholder explanation. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:', which is not satisfied by any digest file."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Tasks 1-5 include convention references in free-form prose format ('Per repo conventions: all handlers return Result&lt;T, AppError&gt; with .context() wrapping', 'Per repo conventions: integration tests in tests/api/ use the assert_eq! pattern'). None of these follow the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. No instance of the string 'Applies:' or the prescribed format appears anywhere in the output files. The convention-applicability-rules.md requires this exact format and prohibits free-form prose rationales."

</details>

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "Tasks document where they fill in missing details using 'Note:' prefixed statements (e.g., Task 3: 'Note: the feature does not specify which fields should be filterable. This task implements a reasonable set...'; Task 4: 'Note: the feature does not define what relevant means... This task implements PostgreSQL full-text search ranking (ts_rank) as a reasonable default'). The impact map uses 'Tasks assume...' phrasing. However, none of these are explicitly 'labeled as assumptions pending clarification' — the word 'assumption' does not appear in any task description, and 'pending clarification' is not used anywhere in the outputs. The assumptions are documented implicitly through 'Note:' sections rather than being explicitly labeled as required by the assertion."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:'"
  **Evidence:** "Separate digest files exist for all 5 tasks (task-1-digest.md through task-5-digest.md). However, none contain an actual format-tagged SHA-256 hash. Each digest file contains the placeholder '&lt;tagged-digest-from-script&gt;' instead of a real 64-char hex hash. For example, task-1-digest.md line 28 shows '[sdlc-workflow] Description digest: &lt;tagged-digest-from-script&gt;' with a note: 'The actual digest value is computed from the Jira-normalized description (not the submitted markdown), so it cannot be pre-computed here.' No output file contains a 'sha256-md:' or 'sha256-adf:' prefixed hash with 64 hex characters."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:'"
  **Evidence:** "Digest files exist for all 9 tasks (task-1-digest.md through task-9-digest.md). However, none contain an actual 64-character hex hash. All digest files contain the placeholder: '[sdlc-workflow] Description digest: sha256-md:&lt;hash-computed-from-jira-persisted-description&gt;' where '&lt;hash-computed-from-jira-persisted-description&gt;' is a descriptive placeholder, not a 64-character lowercase hex string. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md:' — the placeholder text does not satisfy this requirement."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:'"
  **Evidence:** "Five digest files exist (task-1-digest.md through task-5-digest.md), each containing '[sdlc-workflow] Description digest: sha256-md:&lt;computed-after-jira-creation&gt;'. However, none contain a valid 64-character lowercase hex hash. The placeholder '&lt;computed-after-jira-creation&gt;' is not a SHA-256 hash — grep for the pattern 'sha256-(md|adf):[0-9a-f]{64}' returned zero matches across all output files. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:', which is not satisfied."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Conventions are filtered for applicability and no 'Not applicable' annotations exist. However, one rationale violates the prescribed format. In task-2-license-compliance-service.md, the second convention rationale reads: 'Applies: task modifies service code that queries the database matching the convention's query helper scope.' Per convention-applicability-rules.md line 135-136: 'Every applicability rationale must name at least one specific file from the task's Files to Modify or Files to Create that matches the convention's scope.' This rationale uses the generic phrase 'service code that queries the database' instead of naming a specific file path (e.g., modules/fundamental/src/sbom/service/license_report.rs). The other 5 rationales across tasks 1-4 correctly name specific file paths."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Non-documentation intermediate implementation tasks (2-6) all contain the required sections: Repository, Target Branch, Description, Files to Modify/Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation task 7 contains its required sections (Repository, Target Branch, Description, Acceptance Criteria, Test Requirements). However, the bookend task files (task-1-create-feature-branch.md and task-8-merge-feature-branch.md) are non-documentation tasks that lack 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. The assertion requires these for all non-documentation task files without exempting bookend tasks."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:'"
  **Evidence:** "Separate digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md). However, none contains an actual SHA-256 hash. All digest files use the placeholder text 'sha256-md:&lt;64-char-hex-digest&gt;' instead of a real 64-character lowercase hex hash. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:' — the placeholder '&lt;64-char-hex-digest&gt;' is not 64 hex characters."

</details>

<details>
<summary>eval-6: 2 failing assertions</summary>

- **Assertion:** "Each non-documentation, non-testing task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks (tasks whose filename or description indicates doc-only scope) and testing tasks (tasks whose filename or description indicates cross-cutting testing scope) are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Task 1 (task-1-create-feature-branch.md) is a bookend task, not a documentation or testing task. It is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Task 10 (task-10-merge-feature-branch.md) is also a bookend task missing 'Files to Modify', 'Files to Create', and 'Implementation Notes'. Neither is exempted by the documentation/testing carve-out. Tasks 2-8 all have the required sections. Task 9 (documentation) is exempt and correctly includes Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Task files include convention references but use free-form prose instead of the prescribed format. Task 2: 'Per repo conventions: use tower-http caching middleware for the summary endpoint route builder to enable response caching.' Task 3: 'Per repo conventions: return Result&lt;Json&lt;PaginatedResults&lt;ProductRemediation&gt;&gt;, AppError&gt; with .context() error wrapping.' Task 6: 'Per frontend conventions: PascalCase for component names, use PatternFly 5 components exclusively.' None of these include the required 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format prescribed by convention-applicability-rules.md."

</details>

**Pass rate:** 87% · **Tokens:** 78,099 · **Duration:** 385s

**Baseline** (`f08a8547`): 98% · 79,397 tokens · 405s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9*

