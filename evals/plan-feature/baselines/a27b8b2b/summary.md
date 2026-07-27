## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 13/16 | 3 | 81% |
| eval-3 | 12/15 | 3 | 80% |
| eval-4 | 9/11 | 2 | 82% |
| eval-5 | 12/15 | 3 | 80% |
| eval-6 | 11/14 | 3 | 79% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files task-1-digest.md through task-8-digest.md exist for all 8 tasks, but none contain an actual SHA-256 hash. Each digest file contains the placeholder text '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex-digest&gt;' where '&lt;64-char-hex-digest&gt;' is a literal placeholder string, not 64 lowercase hex characters. The files describe the protocol that 'would be' followed but do not include a computed hash. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md:', not a placeholder."

</details>

<details>
<summary>eval-2: 3 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 5 tasks (task-1-digest.md through task-5-digest.md), but they contain placeholder text instead of actual SHA-256 hashes. Each file shows: '[sdlc-workflow] Description digest: sha256-adf:&lt;64-char-hex-digest-computed-from-persisted-description&gt;' where '&lt;64-char-hex-digest-computed-from-persisted-description&gt;' is a placeholder string, not a valid 64-character hex hash. The files explicitly state: 'Note: The actual hex digest cannot be computed in this eval because the description is not persisted to Jira.' The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:', not a placeholder."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains any convention enrichment. The Implementation Notes sections in all 5 task files contain no 'Per CONVENTIONS.md' references, no 'Applies:' rationale lines, and no evidence of convention-applicability validation. The repo-backend.md manifest lists a CONVENTIONS.md file in the repository root, and all tasks modify .rs files, so convention-aware enrichment should have been performed. The prescribed rationale format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;') is absent from all output files."

- **Assertion:** "No testing tasks are generated because no testing readiness template is present in the eval fixture files"
  **Evidence:** "Task 5 (task-5-search-integration-tests.md) is a dedicated testing task titled 'Update search integration tests.' Its Description states: 'Add comprehensive integration tests covering the new search filtering, relevance scoring, and paginated response format.' The task's sole purpose is writing tests — its Files to Modify lists only 'tests/api/search.rs', and all Acceptance Criteria and Test Requirements are about test coverage. This is a testing task despite no testing readiness template being present in the eval fixture files."

</details>

<details>
<summary>eval-3: 3 failing assertions</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Task 5 (SbomComparePage) references Figma extensively: 'following the Figma design', 'PatternFly component mapping (from Figma design)', with specific components (Select with typeahead, ExpandableSection, Badge with colors, Table composable variant, Dropdown, EmptyState, Skeleton). However, Task 6 (comparison route and SbomListPage multi-select) is a UI-facing task that modifies SbomListPage.tsx with checkboxes and a 'Compare selected' toolbar button — it references PatternFly Table selection pattern but does not mention Figma design context at all. The word 'Figma' does not appear anywhere in task-6-comparison-route-multiselect.md."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 9 tasks (task-1-digest.md through task-9-digest.md), but all contain the placeholder '[sdlc-workflow] Description digest: sha256-md:&lt;would-be-computed-after-jira-creation&gt;' instead of an actual 64-character hex hash. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:, not a placeholder, abbreviated value, or example string.' The value '&lt;would-be-computed-after-jira-creation&gt;' is explicitly a placeholder."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention references appear in any task description. None of the 9 task files contain 'CONVENTIONS.md', 'Per CONVENTIONS.md', or 'Applies: task modifies' anywhere. Both repo manifests (repo-backend.md and repo-frontend.md) list CONVENTIONS.md as existing files in their directory trees, so convention-aware enrichment should have been performed. There is no evidence that conventions were evaluated for applicability — neither included with rationale nor documented as excluded."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Separate digest files exist for all 5 tasks (task-1-digest.md through task-5-digest.md), but all contain the placeholder 'sha256-md:&lt;would-be-computed-after-jira-creation&gt;' instead of an actual 64-character hex hash. The assertion explicitly requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:, not a placeholder, abbreviated value, or example string.' The placeholder '&lt;would-be-computed-after-jira-creation&gt;' is not a valid SHA-256 hash."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any output file. Searched all output files for 'convention', 'applicab', and 'Applies:' — the only hits are generic references to 'codebase conventions' in task-3 and task-4 implementation notes, and 'Rationale' for workflow mode selection in the impact map. No file contains the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. No conventions are listed, validated, or rationalized per the shared/convention-applicability-rules.md requirement."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks (non-documentation task files) are missing required sections. task-1-create-feature-branch.md lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. task-8-merge-feature-branch.md likewise lacks these sections. The assertion only exempts documentation tasks, not bookend tasks. Non-bookend intermediate tasks (2-6) all contain the required sections. Documentation task 7 has Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements as required by the exemption."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md), but every digest contains a placeholder value: 'sha256-md:&lt;computed-after-jira-creation&gt;' instead of an actual 64-character lowercase hex hash. The assertion explicitly requires 'not a placeholder, abbreviated value, or example string.' For example, task-1-digest.md reads: '[sdlc-workflow] Description digest: sha256-md:&lt;computed-after-jira-creation&gt;' followed by a note explaining 'In production, this digest is computed by...' None of the digest files contain a real SHA-256 hash."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains any evidence of convention-aware enrichment or applicability validation. None of the task files (task-1 through task-8), impact-map.md, or summary-comment.md contain 'Applies:', 'convention', 'applicability', or any reference to shared/convention-applicability-rules.md. No conventions are mentioned at all in any output file."

</details>

<details>
<summary>eval-6: 3 failing assertions</summary>

- **Assertion:** "Each non-documentation, non-testing task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks (tasks whose filename or description indicates doc-only scope) and testing tasks (tasks whose filename or description indicates cross-cutting testing scope) are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks 1 and 11 are not documentation or testing tasks but are missing required sections. Task 1 (task-1-create-feature-branch.md) has Repository, Target Branch, Description, Acceptance Criteria, Test Requirements but lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes'. Task 11 (task-11-merge-feature-branch.md) similarly has Repository, Target Branch, Description, Acceptance Criteria, Test Requirements but lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes'. These bookend tasks are not exempted by the documentation/testing carve-out. Non-bookend implementation tasks (2,3,4,5,6,7,8,9) all contain the full required set of sections."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 11 tasks (task-1-digest.md through task-11-digest.md), but every file contains a placeholder instead of an actual SHA-256 hash. For example, task-1-digest.md contains '[sdlc-workflow] Description digest: sha256-md:&lt;placeholder-digest-for-task-1&gt;' and explicitly notes 'Since we are writing to files instead of Jira, the actual SHA-256 digest cannot be computed.' The values '&lt;placeholder-digest-for-task-N&gt;' are not 64-character lowercase hex strings. All 11 digest files follow the same placeholder pattern."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention applicability rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). No task file references CONVENTIONS.md sections with 'Per CONVENTIONS.md' prefixes. The Implementation Notes sections in tasks 2-9 contain implementation guidance, reuse candidates, and verification commands, but no convention enrichment entries. There is no evidence in any output file that convention-aware enrichment or file-type applicability validation was performed."

</details>

**Pass rate:** 83% · **Tokens:** 77,679 · **Duration:** 354s

**Baseline** (`af479b32`): 89% · 79,139 tokens · 409s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.6*

