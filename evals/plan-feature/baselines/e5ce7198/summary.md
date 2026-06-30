## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 16/16 | 0 | 100% |
| eval-2 | 14/14 | 0 | 100% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 15/16 | 1 | 94% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Every generated task description contains a Repository section with a single repository name (not multiple repos per task)"
  **Evidence:** "Task 1 (create-branch) has 'Repository: trustify-backend, trustify-ui' — two repos in one task. Task 9 (merge-branch) also has 'Repository: trustify-backend, trustify-ui' — two repos in one task. The assertion requires a SINGLE repository name per task, not multiple."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Bookend tasks (task-1 and task-7) intentionally omit Files to Modify/Files to Create and Implementation Notes sections. task-1-create-feature-branch.md has Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements but lacks Files to Modify/Create and Implementation Notes. task-7-merge-feature-branch.md similarly lacks these sections. However, this assertion does not exempt bookend tasks -- it says 'Each task file contains all required template sections' without exception. While the eval instructions note that bookend tasks intentionally omit Implementation Notes, the assertion text itself requires 'at least one of Files to Modify or Files to Create' from every task, and bookend tasks have neither. Intermediate tasks 2-6 all contain all required sections. FAIL because bookend tasks lack Files to Modify/Create sections."

</details>

**Pass rate:** 97% · **Tokens:** 44,968 · **Duration:** 199s

**Baseline** (`7142c02`): 100% · 0 tokens · 0s

