## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 15/16 | 1 | 94% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 10/11 | 1 | 91% |
| eval-5 | 12/15 | 3 | 80% |
| eval-6 | 13/14 | 1 | 93% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md), but they contain placeholder strings, not valid SHA-256 hashes. For example, task-1-digest.md contains: '[sdlc-workflow] Description digest: sha256-md:task-1-advisory-summary-model-service-placeholder'. The value after 'sha256-md:' is 'task-1-advisory-summary-model-service-placeholder' — not 64 lowercase hex characters. The files explicitly state 'Note: In a live run, this digest would be computed by...' confirming these are placeholders, not actual digests."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "Tasks document ambiguity via 'Note:' paragraphs (e.g., task-1: 'Implementers should measure current p95 latency before optimization', task-2: 'Implementers should define the scoring factors', task-3: 'Implementers should start with entity type filtering'). However, these are labeled as 'Note:' recommendations, not explicitly labeled as 'assumptions pending clarification' or similar assumption-flagging language. The assertion requires assumptions to be 'labeled as assumptions pending clarification' which is not the labeling used."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "All 11 digest files exist (task-1-digest.md through task-11-digest.md), but the hash values are invalid. Issues: (1) All hashes have a non-hex suffix appended (e.g., '-task1', '-task2'), making the value after 'sha256-md:' not exactly 64 hex characters. Example from task-1-digest.md: 'sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855-task1'. (2) Task 1's hash (e3b0c44298fc1c...) is the well-known SHA-256 of an empty string. (3) Hashes from task-2 through task-11 are clearly fabricated sequential hex patterns, not real SHA-256 hashes: task-2 uses 'a1b2c3d4e5f6a7b8c9d0e1f2...', task-3 uses 'b2c3d4e5f6a7b8c9d0e1f2a3...', each shifting by one hex byte. These are placeholder values, not actual content hashes."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Separate digest files exist for all 5 tasks (task-1-digest.md through task-5-digest.md), but each contains only a placeholder: 'sha256-md:&lt;64-char-hex-digest&gt;'. Each file explicitly states: 'The &lt;64-char-hex-digest&gt; is a placeholder. The actual digest would be computed from the Jira-stored description content using scripts/sha256-digest.py.' The assertion requires exactly 64 lowercase hex characters, not a placeholder string. No actual SHA-256 hash was computed."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks 1 and 10 are non-documentation tasks but lack required sections. task-1-create-feature-branch.md has Repository, Target Branch, Description, Acceptance Criteria, Test Requirements but is missing 'Files to Modify' or 'Files to Create' and 'Implementation Notes'. task-10-merge-feature-branch.md has the same missing sections. Implementation tasks 2-8 all have the full set of required sections. Documentation task 9 has Repository, Target Branch, Description, Acceptance Criteria, Test Requirements (exempt from Files/Implementation Notes)."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 10 tasks (task-1-digest.md through task-10-digest.md), but every digest file contains the placeholder value 'sha256-adf:&lt;computed-after-refetch&gt;' instead of an actual 64-character lowercase hex hash. For example, task-1-digest.md line 17: '[sdlc-workflow] Description digest: sha256-adf:&lt;computed-after-refetch&gt;'. The assertion explicitly requires 'not a placeholder, abbreviated value, or example string'. No actual SHA-256 hashes appear anywhere in the outputs."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any output file. grep for 'Applies:' returns zero matches. The only 'convention' mentions are informal references in Implementation Notes sections (e.g., task-2-database-migration.md line 34: 'use .context() wrapping per the project's error handling convention'), which are free-form prose, not the prescribed format. No task file contains a conventions section, applicability validation, or rationale in the format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 7 tasks (task-1-digest.md through task-7-digest.md), but none contains an actual SHA-256 hash. All use placeholders: 'sha256-md:&lt;64-char-hex-digest&gt;' and '&lt;tagged-digest-from-step-3&gt;' instead of a real 64-character hex string. The assertion explicitly requires 'not a placeholder, abbreviated value, or example string'. No actual computed digest appears in any output file."

</details>

**Pass rate:** 91% · **Tokens:** 128,604 · **Duration:** 1340s

**Baseline** (`9a6ca95e`): 96% · 51,739 tokens · 250s

