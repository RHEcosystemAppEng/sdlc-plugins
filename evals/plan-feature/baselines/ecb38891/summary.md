## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 14/16 | 2 | 88% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 10/11 | 1 | 91% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 11/14 | 3 | 79% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:'"
  **Evidence:** "Digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md), but none contains a valid SHA-256 hash. Each digest file contains the placeholder text '[sdlc-workflow] Description digest: sha256-md:&lt;digest-would-be-computed-after-refetching-from-jira&gt;' instead of 64 lowercase hex characters. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md:' but the text after the prefix is '&lt;digest-would-be-computed-after-refetching-from-jira&gt;', not a hex hash."

</details>

<details>
<summary>eval-2: 2 failing assertions</summary>

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "Each task includes a '**Note:**' section documenting where the feature lacks specifics and what standard implementation was chosen (e.g., Task 1: 'The feature does not specify quantitative performance targets. This task implements standard PostgreSQL full-text search optimizations'). However, these are labeled as 'Note' not 'assumptions.' The word 'assumption' does not appear as a label or heading in any task description. While the notes effectively communicate assumptions pending clarification, they are not explicitly labeled as assumptions."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:'"
  **Evidence:** "Digest files exist (task-1-digest.md, task-2-digest.md, task-3-digest.md) but none contain an actual SHA-256 hash. Each file contains only a procedural description of how the digest would be computed, with the placeholder '[sdlc-workflow] Description digest: sha256-adf:&lt;64-char-hex-digest&gt;' instead of a real 64-character hex hash. The assertion requires 'exactly 64 lowercase hex characters' but the files contain the literal text '&lt;64-char-hex-digest&gt;' as a placeholder. No actual hash value appears in any output file."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No conventions from CONVENTIONS.md are referenced in any task's Implementation Notes using the prescribed format 'Per CONVENTIONS.md §...' with 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The only convention-like references are generic mentions: task-4 says 'per project conventions' and task-5 says 'per project conventions' — these are free-form prose, not the prescribed format. There is no evidence that convention-applicability-rules.md was consulted to validate and include/exclude conventions with proper rationale format."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Conventions are present with applicability rationales, and no inapplicable conventions are listed with 'Not applicable' annotations. However, several rationales deviate from the prescribed format. The prescribed format is: 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;.' Three error-handling convention rationales use free-form prose instead: Task 1 §Error handling ends with 'which loads configuration and must handle I/O errors' instead of 'matching the convention's &lt;scope&gt;'; Task 2 §Error handling ends with 'which performs database queries and policy loading'; Task 3 §Error handling ends with 'which is a handler returning Result&lt;T, AppError&gt;'. Per convention-applicability-rules.md Common Mistakes: 'Do NOT use prose-format rationales... Never use free-form prose.' The Module pattern rationales do follow the format correctly (e.g., Task 1: 'matching the convention's model directory scope'), but the error handling rationales do not."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any task file. Searching all output files for 'convention', 'CONVENTIONS', or 'Per CONVENTIONS' yielded only generic references to 'project convention' (task-4 line 33, task-6 line 15) and 'conventions' (task-2 line 28), none of which follow the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. No CONVENTIONS.md sections are referenced with the '§' format. There is no evidence of convention applicability validation."

</details>

<details>
<summary>eval-6: 3 failing assertions</summary>

- **Assertion:** "The plan documents Incorporates links from the Feature to each Epic (not from Feature to individual Tasks) — evidenced by link decisions in the impact map or task output files"
  **Evidence:** "The impact-map.md mentions Epic Grouping and Type-to-Role Mapping but does not explicitly document 'Incorporates' links from the Feature to each Epic. There is no mention of link types (Incorporates, is-parent-of, etc.) being created from Feature TC-9006 to the Epics. The plan describes Epics and their task membership but does not document the specific Jira link structure between Feature and Epics."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:'"
  **Evidence:** "All 9 digest files (task-1-digest.md through task-9-digest.md) exist but contain placeholder text: '[sdlc-workflow] Description digest: sha256-md:&lt;would-be-computed-after-jira-creation&gt;'. The placeholder '&lt;would-be-computed-after-jira-creation&gt;' is not a valid 64-character lowercase hex hash. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:', and this condition is not met."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention-related content. There are no 'Applies:' rationale statements, no convention references, and no convention-applicability validation output in any of the task description files or the impact map. Convention-aware enrichment is entirely absent from the output."

</details>

**Pass rate:** 90% · **Tokens:** 78,681 · **Duration:** 343s

**Baseline** (`e6624a8d`): 100% · 76,828 tokens · 346s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7*

