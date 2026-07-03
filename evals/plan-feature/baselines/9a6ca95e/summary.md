## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 15/15 | 0 | 100% |
| eval-4 | 10/11 | 1 | 91% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 13/14 | 1 | 93% |

### Failed Assertions

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** No 'Applies:' rationale format found in any task description output file. Convention-aware enrichment was not performed with the prescribed format.

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** No convention-aware enrichment with prescribed 'Applies:' rationale format found in any output file.

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** No convention enrichment sections with prescribed 'Applies:' rationale format found in any task description file.

</details>

**Pass rate:** 96% · **Tokens:** 51,739 · **Duration:** 250s

**Baseline** (`fcbfa091`): 93% · 44,337 tokens · 250s

