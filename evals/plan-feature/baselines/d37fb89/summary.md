## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 7/8 | 1 | 88% |
| eval-5 | 12/12 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "Every generated task description contains Target Branch, Description, Acceptance Criteria, and Test Requirements sections as required by the handoff contract in task-description-template.md"
  **Evidence:** "Task 1 (create-branch bookend) has Target Branch, Description, and Acceptance Criteria but lacks a Test Requirements section. Task 8 (merge-branch bookend) has Target Branch, Description, Acceptance Criteria and Dependencies but lacks a Test Requirements section. While the template says 'Omit sections that don't apply', the assertion explicitly states 'every generated task description' must contain these four sections. Tasks 2-7 all contain Target Branch, Description, Acceptance Criteria, and Test Requirements."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the task descriptions contain any convention-aware enrichment. There are no references to CONVENTIONS.md sections with the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format in any of the 8 tasks' Implementation Notes. The repo-backend.md mentions a CONVENTIONS.md file exists, and repo-frontend.md mentions a CONVENTIONS.md file exists, but no convention references appear in any task description. Convention enrichment appears to have been entirely omitted."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any of the 5 task files. None of the task descriptions contain any 'Per CONVENTIONS.md', 'Applies:', or convention rationale references. The only CONVENTIONS.md available is for the sdlc-plugins repo itself, not for the target trustify-backend repository. There is no evidence that the convention-applicability validation process was executed at all — no conventions were included (with or without rationale), so there is no evidence the prescribed format was followed. Cannot confirm the enrichment step ran and validated applicability."

</details>

**Pass rate:** 94% · **Tokens:** 39,822 · **Duration:** 174s

**Baseline** (`41f6a7e`): 70% · 54,459 tokens · 212s

