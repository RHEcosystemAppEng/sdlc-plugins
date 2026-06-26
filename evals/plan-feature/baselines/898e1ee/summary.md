## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 11/12 | 1 | 92% |
| eval-4 | 8/8 | 0 | 100% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention-applicability enrichment. grep for 'CONVENTIONS', 'Per CONVENTIONS', and 'Applies:' across all task files found zero matches for convention-applicability rationale lines. The word 'conventions' appears only in generic references to coding patterns (e.g., 'serialization and documentation conventions' in task-2, 'test conventions' in task-5), not in the prescribed 'Per CONVENTIONS.md §...' format with 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale. Convention-aware enrichment was not performed at all."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Bookend tasks (task-1-create-feature-branch.md and task-7-merge-feature-branch.md) lack 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Task 1 has only: Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, Dependencies. Task 7 has the same structure. The assertion requires 'each task file' to have these sections with no exemption for bookend tasks."

</details>

**Pass rate:** 97% · **Tokens:** 37,392 · **Duration:** 166s

**Baseline** (`0adea80`): 75% · 47,086 tokens · 187s

