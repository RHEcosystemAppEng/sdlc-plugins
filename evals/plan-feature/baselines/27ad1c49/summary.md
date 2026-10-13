## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 15/16 | 1 | 94% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 10/11 | 1 | 91% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 14/14 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention enrichment in the prescribed format appears in any task description. The convention-applicability-rules.md requires the format 'Per CONVENTIONS.md §&lt;Section Name&gt;: &lt;action&gt;. Applies: task modifies &lt;matching file(s)&gt; matching the convention's &lt;scope signal&gt;.' None of the 4 task descriptions contain 'Per CONVENTIONS.md §' or 'Applies: task modifies' rationales. The repo-backend.md lists a CONVENTIONS.md in the directory tree and documents Key Conventions (module pattern, error handling, caching, testing), and the tasks do reference these patterns in Implementation Notes, but only as free-form prose (e.g., 'Follow the existing migration pattern in migration/src/m0001_initial/mod.rs') rather than in the prescribed convention enrichment format."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention references found in any task's Implementation Notes. None of the 9 task description files contain 'Per CONVENTIONS.md', 'Applies:', or any convention applicability rationale in the prescribed format. While the repo manifests (repo-backend.md, repo-frontend.md) both list CONVENTIONS.md files in their directory trees, no convention-aware enrichment was performed. There is no evidence that convention applicability was validated or that applicable conventions were included with the required 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention enrichment is present in any task description. None of the four task files contain 'Per CONVENTIONS.md', 'Applies:', or any convention-related rationale. The repo-backend.md fixture lists a CONVENTIONS.md file in the repository's directory tree root, indicating conventions may exist. There is no evidence that convention-aware enrichment validation was performed — no conventions section, no applicability rationale in prescribed format, and no indication that conventions were checked and found inapplicable. Burden of proof is on PASS, and no positive evidence of the convention enrichment process exists."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks are non-documentation task files but are missing required sections. task-1-create-feature-branch.md is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes'. task-6-merge-feature-branch.md is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes'. The assertion does not exempt bookend tasks — only documentation tasks are exempted. Intermediate implementation tasks (2-5) all contain the required sections: Repository, Target Branch, Description, at least one of Files to Modify/Create, Implementation Notes, Acceptance Criteria, and Test Requirements."

</details>

**Pass rate:** 95% · **Tokens:** 37,061 · **Duration:** 218s

**Baseline** (`9401c868`): 98% · 78,998 tokens · 361s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10*

