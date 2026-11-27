## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 15/15 | 0 | 100% |
| eval-6 | 14/14 | 0 | 100% |
| eval-7 | 3/10 | 7 | 30% |
| eval-8 | 4/4 | 0 | 100% |
| eval-9 | 4/4 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Tasks 4, 5, 7 do reference Figma (Task 4 '**Figma header toolbar:**' PF Select/Button/EmptyState/CodeBranchIcon; Task 5 'Sections, columns and badge colors (Figma, in this order)' with PF tokens like --pf-v5-global--success-color--100; Task 7 'Figma: "Export" is a secondary Dropdown'). However, the UI-facing Task 6 (task-6-frontend-sbom-list-compare-selected.md, which modifies src/pages/SbomListPage/SbomListPage.tsx to add selection checkboxes and a 'Compare selected' button) contains no reference to Figma design context at all. It names PF components ('composable Table row selection', 'Button (variant secondary)'), but these aren't tied to any Figma design. Because one UI-facing task doesn't meet the requirement, this fails."

</details>

<details>
<summary>eval-7: 7 failing assertions</summary>

- **Assertion:** "Across implementation task Files to Modify or Files to Create, the plan covers all four catalog writer paths: src/workflows/registration.py, src/workflows/scheduled_sync.py, src/workflows/fallback_import.py, and src/api/on_demand_refresh.py"
  **Evidence:** "task-1 Files to Modify lists only src/catalog/store.py, src/workflows/registration.py, src/api/catalog_summary.py, src/reports/catalog_export.py and four tests. Implementation Notes say: "**Do not modify** `scheduled_sync.py`, `fallback_import.py` or `on_demand_refresh.py` in this task." impact-map.md line 61: "The non-onboarding writers do not appear in any task's Files to Modify or Test Requirements.""

- **Assertion:** "Task Test Requirements cover each writer with its corresponding test path: tests/workflows/test_registration.py, tests/workflows/test_scheduled_sync.py, tests/workflows/test_fallback_import.py, and tests/api/test_on_demand_refresh.py"
  **Evidence:** "task-1 Test Requirements cover only test_store.py, test_registration.py, test_catalog_summary.py and test_catalog_export.py. No task lists test_scheduled_sync.py, test_fallback_import.py or test_on_demand_refresh.py, and impact-map.md line 61 confirms they are excluded."

- **Assertion:** "Implementation tasks specify path-specific validation: registration persists the supplied ownerGroup, scheduled sync/fallback/on-demand updates preserve an existing value when omitted and apply a supplied replacement, and both consumers expose values from all four writers"
  **Evidence:** "Only registration has path-specific validation (task-1 AC: "A service registered through `src/workflows/registration.py` is persisted with the supplied `ownerGroup`"). No validation for scheduled sync, fallback import or on-demand refresh. Consumer tests use only "a registered record"."

- **Assertion:** "Generated tasks cover both catalog consumers, src/api/catalog_summary.py and src/reports/catalog_export.py, and validate that entries produced by every writer are visible to those consumers"
  **Evidence:** "Both consumers are in task-1 Files to Modify, but the tests validate only registration-produced records ("the summary response includes `ownerGroup` for a registered record"). impact-map.md line 49 marks the 'regardless of how populated' criterion "PARTIALLY COVERED ... Records from sync, fallback import or on-demand refresh are not covered.""

- **Assertion:** "Task Test Requirements include tests/api/test_catalog_summary.py and tests/reports/test_catalog_export.py, exercising records from each writer through each consumer"
  **Evidence:** "Both test files are present in task-1 Test Requirements, but they exercise only "a registered record" and "a record with no `ownerGroup`". They do not exercise records from scheduled sync, fallback import or on-demand refresh."

- **Assertion:** "Generated tasks preserve the fixture's existing-population behavior and stable-ID compatibility acceptance criterion"
  **Evidence:** "task-1 AC narrows the criterion to "Record IDs and existing registration, summary and export behavior are unchanged". impact-map.md line 50 marks "Existing catalog population behavior and stable IDs remain unchanged" as "PARTIALLY COVERED ... Regression tests for the three other writers are out of scope." The outputs contradict each other on coverage, so this fails."

- **Assertion:** "The fallback-import and on-demand-refresh paths are explicitly planned; coverage is not limited to initial registration and scheduled sync"
  **Evidence:** "fallback_import.py and on_demand_refresh.py are marked "UNRESOLVED: outside stakeholder scope" (impact-map.md lines 22-23) and are explicitly excluded from tasks. Task 1 says "Do not modify ... fallback_import.py or on_demand_refresh.py". Implementation coverage is limited to registration only."

</details>

**Pass rate:** 91% · **Tokens:** 88,595 · **Duration:** 210s

**Baseline** (`365e2729`): 97% · 87,667 tokens · 196s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0*

