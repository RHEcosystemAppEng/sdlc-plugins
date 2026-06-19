## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 8/8 | 0 | 100% |
| eval-5 | 11/12 | 1 | 92% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Task 1 (task-1-search-indexes.md) line 28 contains a convention rationale that deviates from the prescribed format: 'Applies: task creates migration/src/m0002_search_indexes/mod.rs matching the convention's .rs scope.' The prescribed format uses 'task modifies' but this rationale uses 'task creates' instead. The convention-applicability-rules.md specifies the exact template as 'Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;.' While the file is in Files to Create rather than Files to Modify, the prescribed format explicitly uses 'modifies' and does not provide an alternative wording for created files. All other convention rationales across Tasks 2-5 correctly use 'Applies: task modifies &lt;file&gt; matching the convention's .rs scope.' No inapplicable conventions are listed with 'Not applicable' annotations. No free-form prose rationales found."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "Every generated task description contains Target Branch, Description, Acceptance Criteria, and Test Requirements sections as required by the handoff contract in task-description-template.md"
  **Evidence:** "Bookend tasks (task-1, task-6, task-12, task-13) do not contain Test Requirements sections. Task-1 (create-backend-feature-branch) has: Repository, Target Branch, Description, Bookend Type, Acceptance Criteria — no Test Requirements. Task-6 (create-frontend-feature-branch) has: Repository, Target Branch, Description, Bookend Type, Acceptance Criteria — no Test Requirements. Task-12 (merge-backend) has: Repository, Target Branch, Description, Bookend Type, Dependencies, Acceptance Criteria — no Test Requirements. Task-13 (merge-frontend) has: Repository, Target Branch, Description, Bookend Type, Dependencies, Acceptance Criteria — no Test Requirements. Non-bookend tasks 2-5 and 7-11 all contain Target Branch, Description, Acceptance Criteria, and Test Requirements."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "The digests.md file contains 13 entries, one per task, but the format does not match the required marker format. The entries use the format '[sdlc-workflow] task-N-slug.md digest: sha256-md:&lt;64-hex&gt;' (e.g., '[sdlc-workflow] task-1-create-backend-feature-branch.md digest: sha256-md:2587a9f064625281e31efc2be444aab8902de9e240139f9ab8c13ff3ebac71be'). The required format is '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;'. The word 'Description' is replaced by the task filename, which does not match the exact marker format specified in the assertion. Each hash is 64 lowercase hex characters and properly prefixed with 'sha256-md:', but the marker text includes the task filename instead of 'Description'."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Task 1 (task-1-create-feature-branch.md) is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Task 7 (task-7-merge-feature-branch.md) is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. These bookend tasks contain only Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, and Dependencies."

</details>

**Pass rate:** 93% · **Tokens:** 0 · **Duration:** 0s

**Baseline** (`91c3899`): 90% · 0 tokens · 0s

