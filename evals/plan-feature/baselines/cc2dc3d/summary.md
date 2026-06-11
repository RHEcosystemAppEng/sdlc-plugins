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
  **Evidence:** "None of the 4 task Implementation Notes contain any convention applicability rationales in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). The repo-backend.md directory tree includes a CONVENTIONS.md file, and the convention-applicability-rules.md requires that applicable conventions include the rationale 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;.' No task contains 'Per CONVENTIONS.md' references or the prescribed 'Applies:' rationale format. Tasks reference docs/constraints.md sections but not CONVENTIONS.md sections with proper applicability validation."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "The tasks reference conventions in free-form prose rather than the prescribed format. Task 1 line 27: 'Per the repository's error handling convention: all fallible operations should return Result&lt;T, AppError&gt; with .context() wrapping.' Task 2 line 25: 'per the repository's error handling convention.' Task 3 line 31: 'per the error handling convention.' None of these follow the required format 'Per CONVENTIONS.md §&lt;Section Name&gt;: &lt;action&gt;. Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;.' The prescribed applicability rationale format ('Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;.') is absent from all three tasks."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any task description. Searched all 6 task files for 'CONVENTIONS', 'convention', 'Per CONVENTIONS', and 'Applies:' — zero matches found. Both repo-backend.md and repo-frontend.md list a CONVENTIONS.md file in their directory trees, indicating conventions should have been evaluated and applicable ones included with proper applicability rationales. The complete absence of any convention references means the enrichment feature was not performed."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Searched all 5 task files for 'CONVENTIONS', 'convention', 'Per CONVENTIONS', and 'Applies:' — zero matches found in any task file. The repo-backend.md fixture lists a CONVENTIONS.md file at the repository root (line 15), indicating conventions exist that should have been evaluated. The convention-applicability-rules.md requires that applicable conventions include a rationale in the format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. No task contains any 'Per CONVENTIONS.md' references or applicability rationales. There is no evidence that convention-aware enrichment was performed."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the intermediate task files (tasks 2-5) contain any 'Per CONVENTIONS.md' references or 'Applies:' rationale lines in their Implementation Notes sections. The repo structure (repo-backend.md) shows a CONVENTIONS.md file exists in the repository, so convention-aware enrichment should have been performed. Task Implementation Notes reference patterns and conventions informally (e.g., 'Follow the existing migration pattern', 'Follow the existing error handling pattern') but do not use the prescribed format for convention applicability rationales. No evidence of systematic convention applicability validation was found."

</details>

**Pass rate:** 91% · **Tokens:** 54,028 · **Duration:** 163s

**Baseline** (`750b4ac`): 95% · 62,477 tokens · 210s

