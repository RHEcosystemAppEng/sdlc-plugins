## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 14/14 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the corresponding mock repository structure manifests (repo-backend.md or repo-frontend.md), not invented paths"
  **Evidence:** "Task 4 lists 'tests/api/mod.rs' under Files to Modify, but the backend manifest (repo-backend.md lines 109-114) shows tests/api/ containing only sbom.rs, advisory.rs, and search.rs -- no mod.rs file is listed. This is an invented path not present in the manifest. All other Files to Modify paths across all tasks correctly reference manifest paths (e.g., modules/fundamental/src/sbom/model/mod.rs, src/api/models.ts, tests/mocks/handlers.ts)."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks 1 and 8 are non-documentation tasks but lack required sections. Task 1 (task-1-create-feature-branch.md) is missing: Files to Modify, Files to Create, and Implementation Notes sections. Task 8 (task-8-merge-feature-branch.md) is missing: Files to Modify, Files to Create, and Implementation Notes sections. Implementation tasks 2-6 all have the required sections. Documentation task 7 has all required sections (Repository, Target Branch, Description, Acceptance Criteria, Test Requirements) and is correctly exempt from Files and Implementation Notes."

</details>

**Pass rate:** 98% · **Tokens:** 90,951 · **Duration:** 502s

**Baseline** (`eda40c55`): 100% · 77,643 tokens · 338s

