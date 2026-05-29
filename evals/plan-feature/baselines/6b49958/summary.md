## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The repo-backend.md manifest lists a CONVENTIONS.md file in the repository root, indicating conventions exist that should have been evaluated for applicability. The Implementation Notes in all 5 tasks reference 'docs/constraints.md' sections (e.g., '§4.7', '§5.4', '§3.1', '§5.2', '§5.1', '§5.9-5.10', '§5.11-5.13') but never reference CONVENTIONS.md with the prescribed applicability rationale format. No task contains the string 'Applies:' in any context. Convention-aware enrichment per convention-applicability-rules.md was not performed."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No references to CONVENTIONS.md, convention applicability, or the prescribed 'Applies:' rationale format appear anywhere in the output files. Searched all output files for 'CONVENTIONS', 'convention', 'Per CONVENTIONS', and 'Applies:' — zero matches found. The repo-backend.md manifest lists a CONVENTIONS.md file in the repository root, so convention-aware enrichment should have been performed. The feature description references a repository (trustify-backend) that contains a CONVENTIONS.md file, but no convention analysis was performed or documented."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task in the output contains any reference to CONVENTIONS.md or convention applicability rationales. The prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' does not appear in any task's Implementation Notes. The repo-backend.md mentions a CONVENTIONS.md file exists, and repo-frontend.md mentions a CONVENTIONS.md file exists, but no task includes convention enrichment. Since the convention-applicability-rules.md requires that applicable conventions be included with rationale in the prescribed format, and no conventions are referenced at all, this assertion fails — there is no evidence that convention-aware enrichment was performed."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains any CONVENTIONS.md references, 'Applies:' rationale lines, or convention applicability analysis. The task Implementation Notes reference 'Per constraints doc section 2 (Commit Rules)' and 'Per constraints doc section 3 (PR Rules)' but these are constraints doc references, not CONVENTIONS.md convention enrichment with the prescribed rationale format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). There is no evidence that convention-aware enrichment was performed — no conventions are included with applicability rationales in the prescribed format. Without any convention enrichment present, the assertion cannot be confirmed as PASS."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No intermediate task files (tasks 2-7) contain any convention references, 'Per CONVENTIONS.md' citations, or 'Applies:' rationale lines. The Implementation Notes sections in all intermediate tasks contain only free-form implementation guidance without any convention enrichment. The CONVENTIONS.md for sdlc-plugins contains broadly applicable conventions (e.g., §Commit Messages — 'Use Conventional Commits format') that have no file-type restriction and should have been included with the rationale 'Applies: convention has no file-type restriction (broadly applicable).' per the convention-applicability-rules.md. There is no evidence that convention-aware enrichment was performed at all."

</details>

**Pass rate:** 91% · **Tokens:** 57,513 · **Duration:** 184s

**Baseline** (`b89536d`): 73% · 45,989 tokens · 178s

