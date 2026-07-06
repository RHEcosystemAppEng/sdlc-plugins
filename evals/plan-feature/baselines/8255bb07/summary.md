## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 15/15 | 0 | 100% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 14/14 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks (non-documentation) lack required sections. task-1-create-feature-branch.md is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. task-8-merge-feature-branch.md is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Implementation tasks 2-6 all contain the required sections (Repository, Target Branch, Description, Files to Modify/Create, Implementation Notes, Acceptance Criteria, Test Requirements). Documentation task 7 correctly includes Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements."

</details>

**Pass rate:** 99% · **Tokens:** 393,887 · **Duration:** 940s

**Baseline** (`7b46435b`): 98% · 81,180 tokens · 334s

