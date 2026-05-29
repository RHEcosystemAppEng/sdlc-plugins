## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/13 | 2 | 85% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 6/8 | 2 | 75% |
| eval-5 | 9/12 | 3 | 75% |

### Failed Assertions

<details>
<summary>eval-1: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash -- exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "No output file contains a description digest comment. Searched all 7 output files (impact-map.md and task-1 through task-6) for 'digest', 'sha256', 'sha-256', or '[sdlc-workflow]' -- none found. No digest comments were posted for any task."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention -- inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any reference to CONVENTIONS.md, convention applicability rationales, or the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' format. The repo-backend.md structure includes a CONVENTIONS.md file with documented conventions (Migration Patterns, Axum/SeaORM patterns, error handling, endpoint registration, response types, query helpers, testing, caching), yet no task's Implementation Notes include any 'Per CONVENTIONS.md' references or applicability rationales. There is no evidence that convention-aware enrichment was performed."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains CONVENTIONS.md convention references with the prescribed applicability rationale format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). The tasks reference docs/constraints.md sections (§2.1, §2.2, §2.3, §5.1, §5.4, §5.9-§5.12) but these are constraint references, not CONVENTIONS.md convention enrichment. The repo-backend.md manifest shows a CONVENTIONS.md file exists in the repository. There is no evidence that convention-applicability-rules.md was followed — no 'Applies:' rationale lines appear in any task's Implementation Notes."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "No output file contains any '[sdlc-workflow] Description digest: sha256:' marker or any SHA-256 hash. The outputs consist only of task description markdown files (task-1 through task-6) and an impact-map.md. No digest comments are present anywhere in the output files."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains any reference to CONVENTIONS.md, any 'Per CONVENTIONS.md' lines, any 'Applies:' rationale lines, or any convention enrichment whatsoever. Convention-aware enrichment was not performed in any of the 6 task descriptions. The convention-applicability-rules.md requires applicable conventions to include rationale in prescribed format, but no conventions appear in any Implementation Notes section."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "Searched all files in /tmp/plan-feature-eval-baseline/eval-4/ for 'sha256', 'digest', and 'hex'. No matches found anywhere. No description digest comments were posted for any of the 5 tasks. The description-digest-protocol.md requires producers to post a digest comment immediately after creating each task."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Searched all output files for 'CONVENTIONS', 'Applies:', and 'applicab'. No convention-applicability rationales in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;') were found in any task description. The CONVENTIONS.md for this project exists and contains conventions (e.g., Commit Messages, Naming Conventions, File Organization) — some of these are broadly applicable and should have been included with the prescribed rationale format. Tasks 1 and 5 reference 'Per docs/constraints.md' but not 'Per CONVENTIONS.md'. No evidence of convention-applicability validation per the shared/convention-applicability-rules.md protocol."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "The plan includes a workflow:feature-branch label decision to be applied to the feature issue"
  **Evidence:** "No output file contains any reference to a 'workflow:feature-branch' label or any label decision. The impact-map.md mentions 'Mode: feature-branch' as a workflow mode but does not include a label decision directive to apply 'workflow:feature-branch' to the Jira feature issue TC-9005."

- **Assertion:** "After each task is created, a description digest comment is posted with a real computed SHA-256 hash — exactly 64 lowercase hex characters, not a placeholder (&lt;hex-digest&gt;, &lt;hex&gt;), abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256:&lt;64-char-hex&gt;'"
  **Evidence:** "No output files contain any reference to 'digest', 'sha256', or any SHA-256 hash values. There are no transcript or log files showing Jira comments being posted with description digests. The outputs directory contains only the impact-map.md and 7 task files with no digest-related content."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output files contain any references to 'CONVENTIONS.md', 'Per CONVENTIONS', convention applicability, or any applicability rationale in the prescribed format. The Implementation Notes sections in intermediate task files reference existing code patterns and conventions informally but do not include any structured convention applicability validation or rationales."

</details>

**Pass rate:** 82% · **Tokens:** 48,824 · **Duration:** 213s

**Baseline** (`d3d6601`): 84% · 52,160 tokens · 186s

