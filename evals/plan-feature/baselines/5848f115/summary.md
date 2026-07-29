## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 13/16 | 3 | 81% |
| eval-3 | 13/15 | 2 | 87% |
| eval-4 | 9/11 | 2 | 82% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 13/14 | 1 | 93% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md), but every digest contains a placeholder instead of an actual hash. All digest files contain '[sdlc-workflow] Description digest: sha256-adf:&lt;digest-computed-after-refetch&gt;' with a note saying 'The actual digest value would be computed by re-fetching the created issue'. The string '&lt;digest-computed-after-refetch&gt;' is not a 64-character lowercase hex string — it is a placeholder. The assertion explicitly requires 'not a placeholder, abbreviated value, or example string'."

</details>

<details>
<summary>eval-2: 3 failing assertions</summary>

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the repo-backend.md mock repository structure manifest, not invented paths"
  **Evidence:** "The repo-backend.md structure shows search module paths under 'modules/search/src/' (e.g., 'modules/search/src/service/mod.rs', 'modules/search/src/endpoints/mod.rs'). However, all three tasks reference these paths without the 'src/' directory segment: task-1 lists 'modules/search/endpoints/mod.rs' and 'modules/search/service/mod.rs'; task-2 lists the same; task-3 lists the same plus 'common/src/db/limiter.rs' (correct). The search module paths are consistently wrong — they should be 'modules/search/src/endpoints/mod.rs' and 'modules/search/src/service/mod.rs' per the repo-backend.md directory tree. Other paths like 'common/src/db/query.rs', 'tests/api/search.rs', and 'migration/src/...' are correct, but the primary Files to Modify entries for the search module are invented paths that don't match the manifest."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all three tasks (task-1-digest.md, task-2-digest.md, task-3-digest.md), but all contain the placeholder '[sdlc-workflow] Description digest: sha256-md:&lt;computed-after-refetch&gt;' instead of an actual 64-character hex SHA-256 hash. The files explicitly state: 'Note: The actual hex digest cannot be computed in eval mode because the description is not persisted to Jira.' The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:, not a placeholder' — '&lt;computed-after-refetch&gt;' is a placeholder, not a valid hash."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention applicability rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;') appears in any of the three task description files or the impact map. The Implementation Notes sections reference code patterns and file paths but do not contain any 'Per CONVENTIONS.md' references or 'Applies:' rationale lines as required by convention-applicability-rules.md. Convention-aware enrichment was not performed."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "All 8 digest files (task-1-digest.md through task-8-digest.md) exist, but they all contain placeholder values instead of actual SHA-256 hashes. For example, task-1-digest.md contains: '[sdlc-workflow] Description digest: sha256-md:placeholder-digest-for-task-1-created-from-tc-9003'. The assertion requires exactly 64 lowercase hex characters after 'sha256-md:', but 'placeholder-digest-for-task-1-created-from-tc-9003' is not a 64-character hex string. All 8 digests fail this requirement."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains any convention-aware enrichment section with 'Applies:' rationale in the prescribed format. Searching for 'Applies:' across all output files returned no results. There is no evidence of convention applicability validation having been performed per the shared/convention-applicability-rules.md specification."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Six digest files exist (task-1-digest.md through task-6-digest.md), but all contain the placeholder '[sdlc-workflow] Description digest: sha256-md:&lt;hash-computed-after-jira-roundtrip&gt;' instead of an actual 64-character lowercase hex hash. grep for 'sha256-(md|adf):[0-9a-f]{64}' across all output files returned no matches (exit code 1). The assertion explicitly requires 'not a placeholder, abbreviated value, or example string', and '&lt;hash-computed-after-jira-roundtrip&gt;' is clearly a placeholder."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention applicability analysis found in any output file. grep for 'convention', 'applicab', and 'Applies:' returned only generic mentions of 'per project conventions' in task-2 and task-3 (about serde derive macros and error handling). No task description contains convention sections with 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format. No reference to shared/convention-applicability-rules.md validation."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced -- evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash -- exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md), but every digest file contains a placeholder: '[sdlc-workflow] Description digest: sha256-md:&lt;computed-after-jira-persistence&gt;' instead of an actual 64-character hex hash. The assertion explicitly requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:, not a placeholder, abbreviated value, or example string.' The placeholder '&lt;computed-after-jira-persistence&gt;' is not a valid SHA-256 hash."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation, non-testing task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks (tasks whose filename or description indicates doc-only scope) and testing tasks (tasks whose filename or description indicates cross-cutting testing scope) are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Task 1 (task-1-create-feature-branch.md) and Task 10 (task-10-merge-feature-branch.md) are bookend tasks — not documentation or testing tasks — yet both are missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. These tasks only have Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements. Since they are neither documentation nor testing tasks per the exemption criteria, they fail the requirement for 'at least one of Files to Modify or Files to Create' and 'Implementation Notes'. Non-bookend tasks (2,3,4,6,7,8) all contain the full set of required sections. Documentation task 9 and testing task 5 meet their respective exempted requirements."

</details>

**Pass rate:** 88% · **Tokens:** 79,234 · **Duration:** 350s

**Baseline** (`7aaa377a`): 90% · 78,589 tokens · 382s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7*

