## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 14/16 | 2 | 88% |
| eval-3 | 13/15 | 2 | 87% |
| eval-4 | 10/11 | 1 | 91% |
| eval-5 | 13/15 | 2 | 87% |
| eval-6 | 13/14 | 1 | 93% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "All 7 digest files (task-1-digest.md through task-7-digest.md) exist but contain placeholder text instead of actual SHA-256 hashes. Each digest file contains: '[sdlc-workflow] Description digest: sha256-md:&lt;digest-of-task-N-description-as-persisted-by-jira&gt;' followed by a note explaining 'This is a placeholder for the eval'. The value '&lt;digest-of-task-N-description-as-persisted-by-jira&gt;' is not a 64-character lowercase hex string — it is literal placeholder text. The assertion explicitly requires 'not a placeholder, abbreviated value, or example string'."

</details>

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "None of the 4 task description files contain the word 'assumption' or the phrase 'pending clarification.' Task 3's description notes 'The feature requirement (TC-9002) calls for "some kind of filtering capability" -- this task implements filtering by the most commonly useful dimensions based on the existing data model' but does not label this as an assumption pending clarification. The impact map mentions 'The planning assumes entity-type, severity, and date-range filters' (line 22) but this is in the impact map, not in the task descriptions, and lacks a 'pending clarification' label. Task 1's description provides rationale for column choices but doesn't mark them as assumptions."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "All four digest files (task-1-digest.md through task-4-digest.md) contain the marker '[sdlc-workflow] Description digest: sha256-adf:&lt;computed-after-refetch&gt;' where '&lt;computed-after-refetch&gt;' is a placeholder string, not a 64-character lowercase hex hash. The files explicitly state 'The digest cannot be pre-computed because Jira normalizes content during storage. The actual digest value depends on the ADF representation returned by the Jira API after creation.' The assertion requires exactly 64 lowercase hex characters after the prefix, not a placeholder."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "All 6 digest files (task-1-digest.md through task-6-digest.md) exist but contain placeholder text: 'sha256-md:&lt;computed-after-jira-creation&gt;' instead of an actual 64-character hex hash. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:', not a placeholder. The digest files explicitly state 'In production, this digest is computed by...' confirming the hash was never actually computed."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention references (CONVENTIONS.md, 'Per CONVENTIONS.md', 'Applies: task modifies') were found in any output file. grep -ni 'convention\|CONVENTIONS\|Per CONVENTIONS' returned 'No convention references found'. The convention-applicability-rules.md requires that applicable conventions include rationales in the prescribed format in Implementation Notes, but no conventions are referenced at all in any task's Implementation Notes. Without any evidence of convention applicability validation, this assertion fails."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Separate digest files exist for all 5 tasks (task-1-digest.md through task-5-digest.md). However, all contain the placeholder text 'sha256-adf:&lt;computed-after-jira-creation&gt;' instead of an actual 64-character lowercase hex hash. For example, task-1-digest.md line 16: '[sdlc-workflow] Description digest: sha256-adf:&lt;computed-after-jira-creation&gt;'. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:, not a placeholder, abbreviated value, or example string.' The value '&lt;computed-after-jira-creation&gt;' is explicitly a placeholder."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Intermediate non-documentation tasks 2-6 all contain the required sections (Repository, Target Branch, Description, Files to Modify/Create, Implementation Notes, Acceptance Criteria, Test Requirements). Documentation task 7 contains its required subset (Repository, Target Branch, Description, Acceptance Criteria, Test Requirements). However, bookend tasks 1 and 8 are non-documentation task files that lack 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Task 1 (create-branch) has only Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, Dependencies. Task 8 (merge-branch) has only Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, Dependencies. The assertion makes no exception for bookend tasks."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md). However, every digest file contains a placeholder instead of an actual SHA-256 hash. The marker reads: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex-digest-computed-from-persisted-description&gt;' — the string '&lt;64-char-hex-digest-computed-from-persisted-description&gt;' is a template placeholder, not 64 lowercase hex characters. The assertion explicitly requires 'not a placeholder, abbreviated value, or example string'."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md). However, every digest file contains the placeholder 'sha256-adf:&lt;64-char-hex-digest&gt;' instead of an actual 64-character hex hash. The note in each file states 'The actual hex digest would be computed from the Jira-persisted description content.' The assertion requires 'exactly 64 lowercase hex characters', 'not a placeholder, abbreviated value, or example string'. The placeholder '&lt;64-char-hex-digest&gt;' fails this requirement."

</details>

**Pass rate:** 90% · **Tokens:** 78,589 · **Duration:** 382s

**Baseline** (`d8904c3e`): 98% · 82,054 tokens · 381s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7*

