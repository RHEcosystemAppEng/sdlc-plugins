## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 10/11 | 1 | 91% |
| eval-5 | 15/15 | 0 | 100% |
| eval-6 | 14/14 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention applicability rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). None of the Implementation Notes sections in tasks 1-5 contain 'Per CONVENTIONS.md §' references or 'Applies:' rationale lines. The repo-backend.md directory tree includes a CONVENTIONS.md file at the repo root, and the tasks modify .rs files, so convention-aware enrichment should have produced rationales for applicable conventions. There is no evidence that convention-applicability-rules.md was followed."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No evidence of convention-aware enrichment in any output file. Searched all task descriptions for 'Per CONVENTIONS.md', 'Applies:', or convention applicability rationale — none found. The only references to 'convention' are generic (task-1: 'Reference for struct conventions and serde derivations', task-2: 'per the error handling convention'). These are informal prose references, not the prescribed format from convention-applicability-rules.md ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). No convention applicability validation is evidenced."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No evidence of convention-aware enrichment in any output file. Searched all output files for 'convention', 'Per §', 'Applies:', and 'CONVENTIONS.md'. The only match was a generic use of the word 'convention' in task-3-license-report-service.md ('per the project's error handling convention') which is not a CONVENTIONS.md reference. No task contains the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format. No convention applicability validation is documented anywhere in the outputs. Burden of proof is on PASS and no evidence exists."

</details>

**Pass rate:** 96% · **Tokens:** 44,994 · **Duration:** 214s

**Baseline** (`1dab64e0`): 98% · 79,848 tokens · 368s

