## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 14/16 | 2 | 88% |
| eval-3 | 12/15 | 3 | 80% |
| eval-4 | 10/11 | 1 | 91% |
| eval-5 | 13/15 | 2 | 87% |
| eval-6 | 13/14 | 1 | 93% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "All 8 digest files (task-1-digest.md through task-8-digest.md) contain '[sdlc-workflow] Description digest: sha256-md:&lt;computed-from-jira-persisted-description&gt;' — the value '&lt;computed-from-jira-persisted-description&gt;' is a placeholder, not a 64-character lowercase hex string. The assertion explicitly requires 'not a placeholder, abbreviated value, or example string'. No actual SHA-256 hash is present in any digest file or elsewhere in the outputs."

</details>

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "No output file contains the word 'assumption' or 'pending clarification'. While task descriptions use conditional language (Task 1: 'If the SearchService uses PostgreSQL full-text search (tsvector), add GIN indexes'; Task 2: 'If the search uses tsvector/tsquery... If the search uses LIKE/ILIKE patterns') and the impact map identifies ambiguities, none of these are explicitly labeled as 'assumptions pending clarification'. The impact map's Excluded Requirements column uses 'Yes (partial)' labels with suggestions for the team but does not use the word 'assumption' or 'pending clarification'."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist (task-1-digest.md, task-2-digest.md, task-3-digest.md) but they describe the digest protocol procedurally rather than containing actual SHA-256 hashes. All three digest files contain the placeholder '&lt;tagged-digest&gt;' instead of an actual 64-character hex hash. For example, task-1-digest.md line 14: '"text": "[sdlc-workflow] Description digest: &lt;tagged-digest&gt;"' -- this is a placeholder template, not a computed hash value. No 'sha256-md:' or 'sha256-adf:' prefixed 64-char hex string appears in any output file."

</details>

<details>
<summary>eval-3: 3 failing assertions</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Task 5 (Build SBOM comparison page) correctly references Figma: 'Build the SBOM comparison page UI based on the Figma design' and lists specific PatternFly components (Select, ExpandableSection, Badge, Table, EmptyState, Dropdown, Skeleton) with visual specifications (badge colors: green/red/blue/yellow, Critical severity highlighting, CodeBranchIcon empty state). However, Task 6 (Add comparison route and SBOM list page selection) modifies SbomListPage.tsx with visible UI changes (checkbox selection column, 'Compare selected' button) but contains no Figma design context reference -- it only mentions 'PatternFly Table's built-in row selection support' without Figma context. Task 4 (API types, client, hook) is correctly exempt as API-layer."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 9 tasks (task-1-digest.md through task-9-digest.md), but they all contain a placeholder instead of an actual SHA-256 hash. Every digest file contains: '[sdlc-workflow] Description digest: sha256-md:&lt;computed-after-jira-creation&gt;' followed by a note explaining 'In a real execution, this digest would be computed by...' The value '&lt;computed-after-jira-creation&gt;' is not a 64-character hex string -- it is an explicit placeholder. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md:', not a placeholder."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention’s &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains convention-applicability rationales in the prescribed format. Searched all task files for 'Per CONVENTIONS.md' and 'Applies: task modifies' -- neither phrase appears in any output file. The convention-applicability-rules.md requires rationales like 'Per CONVENTIONS.md §&lt;Section Name&gt;: &lt;action&gt;. Applies: task modifies &lt;matching file(s)&gt; matching the convention’s &lt;scope signal&gt;.' None of the Implementation Notes in tasks 2-7 include this format. Convention-aware enrichment was not performed."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Separate digest files exist for all 5 tasks (task-1-digest.md through task-5-digest.md). However, none contain an actual SHA-256 hash. Each file shows the text '[sdlc-workflow] Description digest: sha256-adf:&lt;64-char-hex-digest&gt;' where '&lt;64-char-hex-digest&gt;' is a literal placeholder string, not an actual 64-character lowercase hex value. The assertion requires 'not a placeholder, abbreviated value, or example string'. A grep for the pattern 'sha256-(md|adf):[a-f0-9]+' returned no matches, confirming no actual hex digest is present."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks (non-documentation) are missing required sections. task-1-create-feature-branch.md lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections -- it only has Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, Dependencies. task-10-merge-feature-branch.md similarly lacks 'Files to Modify', 'Files to Create', and 'Implementation Notes'. Implementation tasks 2-8 all pass with all required sections present. Documentation task 9 passes its exempted requirements (has Repository, Target Branch, Description, Acceptance Criteria, Test Requirements)."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No evidence of convention-aware enrichment exists in any output file. Grep for 'CONVENTIONS', 'Applies:' across all output files returned no matches related to convention applicability. The only 'Convention' references are 'Conventional Commits format' in docs/constraints.md citations (tasks 2-8 Implementation Notes), which are project constraints, not CONVENTIONS.md conventions. No task file contains an 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale. There is no evidence that convention-applicability validation was performed."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 7 tasks (task-1-digest.md through task-7-digest.md), but each contains the placeholder 'sha256-adf:&lt;computed-after-jira-creation&gt;' instead of an actual 64-character hex string. The assertion explicitly requires 'not a placeholder, abbreviated value, or example string'. The note in each digest file confirms: 'The actual hex digest cannot be computed in this eval since no Jira API interaction occurs.'"

</details>

**Pass rate:** 89% · **Tokens:** 77,107 · **Duration:** 378s

**Baseline** (`3337d1fd`): 96% · 44,994 tokens · 214s

