## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 15/15 | 0 | 100% |
| eval-6 | 13/14 | 1 | 93% |
| eval-7 | 4/10 | 6 | 40% |
| eval-8 | 4/4 | 0 | 100% |
| eval-9 | 4/4 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Tasks 5, 6 and 8 reference Figma (for example task-5 '**Figma UI structure (header toolbar):**' with PF Select/Button/EmptyState/Skeleton; task-6 has a 'Section specifications (from Figma...)' table with badge colors; task-8 'Figma: Export is a PatternFly `Dropdown`'). But UI-facing Task 7 (task-7-frontend-sbom-list-compare-selected.md, which modifies SbomListPage.tsx) has 0 mentions of 'Figma'. It names PF Table selection, Button and Tooltip without any Figma design context or visual specifications. Since not every UI-facing task meets the requirement, this fails."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation, non-testing task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks (tasks whose filename or description indicates doc-only scope) and testing tasks (tasks whose filename or description indicates cross-cutting testing scope) are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "The bookend tasks task-1-create-feature-branch.md and task-9-merge-feature-branch.md are neither documentation nor testing tasks. Their only sections are Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, and Dependencies (7 '##' headings). Both lack Files to Modify/Files to Create and Implementation Notes. Tasks 2–7 do include all required sections."

</details>

<details>
<summary>eval-7: 6 failing assertions</summary>

- **Assertion:** "Across implementation task Files to Modify or Files to Create, the plan covers all four catalog writer paths: src/workflows/registration.py, src/workflows/scheduled_sync.py, src/workflows/fallback_import.py, and src/api/on_demand_refresh.py"
  **Evidence:** "Task 1 Files to Modify lists only src/workflows/registration.py among the writers (plus store.py, catalog_summary.py, catalog_export.py and tests). Task 1 says 'Do not modify those writers in this task', and impact-map.md says 'the excluded paths are intentionally not listed in any task's Files to Modify or Test Requirements.'"

- **Assertion:** "Task Test Requirements cover each writer with its corresponding test path: tests/workflows/test_registration.py, tests/workflows/test_scheduled_sync.py, tests/workflows/test_fallback_import.py, and tests/api/test_on_demand_refresh.py"
  **Evidence:** "Task 1 Test Requirements include only tests/catalog/test_store.py, tests/workflows/test_registration.py, tests/api/test_catalog_summary.py and tests/reports/test_catalog_export.py. The scheduled_sync, fallback_import and on_demand_refresh tests appear only in the impact map's 'Excluded paths' list."

- **Assertion:** "Implementation tasks specify path-specific validation: registration persists the supplied ownerGroup, scheduled sync/fallback/on-demand updates preserve an existing value when omitted and apply a supplied replacement, and both consumers expose values from all four writers"
  **Evidence:** "Only registration has path-specific validation ('registering a service stores the provided ownerGroup'). Task 1 Acceptance Criteria mark the other writers as '(Not covered by this task — pending scope decision)', and the consumer tests use only 'a registered record'."

- **Assertion:** "Generated tasks cover both catalog consumers, src/api/catalog_summary.py and src/reports/catalog_export.py, and validate that entries produced by every writer are visible to those consumers"
  **Evidence:** "Both consumers are in Task 1 Files to Modify, but the validation covers only 'a registered record' and 'legacy record without ownerGroup'. Records from scheduled sync, fallback import and on-demand refresh are never checked through the consumers. Task 1 states it 'does not satisfy ... displayed regardless of how the record was populated'."

- **Assertion:** "Task Test Requirements include tests/api/test_catalog_summary.py and tests/reports/test_catalog_export.py, exercising records from each writer through each consumer"
  **Evidence:** "Both test files are in Task 1 Test Requirements, but they only cover 'ownerGroup for a registered record' and a legacy record. They do not exercise records from each writer."

- **Assertion:** "The fallback-import and on-demand-refresh paths are explicitly planned; coverage is not limited to initial registration and scheduled sync"
  **Evidence:** "Fallback import and on-demand refresh are left as an 'Unresolved scope conflict' pending a user decision in impact-map.md. No implementation task covers them, and Task 1 says 'Do not modify those writers in this task.'"

</details>

**Pass rate:** 92% · **Tokens:** 86,127 · **Duration:** 201s

**Baseline** (`c608077a`): 99% · 88,416 tokens · 208s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0*

