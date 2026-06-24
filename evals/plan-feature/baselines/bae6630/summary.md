## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 6 task files contain any convention-aware enrichment. There are no 'Per CONVENTIONS.md' references, no 'Applies:' rationale lines, and no convention applicability validation in any task's Implementation Notes. The repo-backend.md structure shows a CONVENTIONS.md file exists in the repository root, but no conventions from it were applied to any task. Convention-aware enrichment with prescribed-format rationales is completely absent from all outputs."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any task file. None of the 5 task descriptions contain the prescribed 'Per CONVENTIONS.md §...' format or the required 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale. The repo-backend.md lists a CONVENTIONS.md file in the repository root, and the Key Conventions section describes conventions for framework, module pattern, error handling, endpoint registration, response types, query helpers, testing, and caching. These conventions should have been validated for applicability and included with proper rationale format where applicable. Instead, the tasks only informally reference project patterns (e.g., 'per project error handling convention', 'per project testing conventions') without the prescribed format."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the corresponding mock repository structure manifests (repo-backend.md or repo-frontend.md), not invented paths"
  **Evidence:** "Task 4 creates 'src/api/models/sbom-comparison.ts' — this introduces a 'models/' directory inside 'src/api/', but repo-frontend.md shows 'src/api/models.ts' as a file (not a directory). Creating a directory 'models/' where a file 'models.ts' already exists is inconsistent with the manifest structure and represents an invented path pattern. The task's own Implementation Notes acknowledge this deviation: 'The new file is placed in src/api/models/ to keep comparison types organized separately from the main models file.' All other Files to Modify paths correctly reference paths from the manifests."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention enrichment is present in any task output. Grep for 'CONVENTIONS', 'Per CONVENTIONS', and 'Applies:' across all task files found zero matches for prescribed convention rationale format. The only mention of 'convention' is in Task 2 line 27: 'as per the project convention in common/src/error.rs' which is an informal reference, not the prescribed format 'Per CONVENTIONS.md §&lt;Section Name&gt;: &lt;action&gt;. Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;.' Both repo manifests (repo-backend.md and repo-frontend.md) list CONVENTIONS.md files in their directory trees, indicating conventions exist that should have been evaluated for applicability and included with rationales where applicable."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains convention-aware enrichment in the prescribed format. The required format is 'Per CONVENTIONS.md §&lt;Section Name&gt;: &lt;action&gt;. Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;.' Instead, tasks 4 and 5 contain informal free-form references: task-4 says 'consistent with the caching approach noted in the repository conventions' and task-5 says 'as specified in the repository conventions'. These are free-form prose, not the prescribed applicability rationale format. No task contains a properly formatted 'Applies:' rationale line as required by convention-applicability-rules.md."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task files contain any convention applicability references, 'Per CONVENTIONS.md' citations, or 'Applies:' rationale lines in the prescribed format. A grep for 'CONVENTIONS', 'convention', 'Applies:' across all output files returned zero relevant matches. There is no evidence that convention-aware enrichment was performed with applicability validation."

</details>

**Pass rate:** 89% · **Tokens:** 38,662 · **Duration:** 178s

**Baseline** (`9aaab88`): 98% · 41,356 tokens · 180s

