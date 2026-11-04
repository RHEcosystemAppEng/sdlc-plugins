## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 19/19 | 0 | 100% |
| eval-2 | 15/16 | 1 | 94% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 15/15 | 0 | 100% |
| eval-6 | 14/14 | 0 | 100% |
| eval-7 | 3/10 | 7 | 30% |
| eval-8 | 4/4 | 0 | 100% |
| eval-9 | 4/4 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains a 'Per CONVENTIONS.md §...' line or any 'Applies: task modifies ... matching the convention's ...' rationale. impact-map.md says CONVENTIONS.md contents are not in the fixture, so 'Task notes use the Key Conventions in repo-backend.md instead'. Those conventions appear as free-form prose with no applicability rationale. For example, task 2 says 'Caching: follow the repository convention "Uses `tower-http` caching middleware..."' and 'Error handling: return `Result&lt;T, AppError&gt;` ... as the repository conventions require.' There is no evidence of file-type applicability checks."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Tasks 5 and 6 cite the Figma design in detail ('Section order, columns and badge colors (from Figma)', 'Header toolbar (Figma)', PF5 ExpandableSection/Badge/Label/Select/EmptyState/Skeleton, green/red/blue/yellow badges). Task 8 notes 'the Figma design specifies it' and names a PF5 Dropdown. Task 7 (task-7-frontend-list-compare-selected.md) is also UI-facing because it modifies src/pages/SbomListPage/SbomListPage.tsx, but it never references Figma design context. It names PF5 Table selection and Button/Tooltip only as CONVENTIONS guidance, with no Figma visual specifications. One UI-facing task fails the requirement, so the assertion fails."

</details>

<details>
<summary>eval-7: 7 failing assertions</summary>

- **Assertion:** "Across implementation task Files to Modify or Files to Create, the plan covers all four catalog writer paths: src/workflows/registration.py, src/workflows/scheduled_sync.py, src/workflows/fallback_import.py, and src/api/on_demand_refresh.py"
  **Evidence:** "task-1 Files to Modify lists only src/catalog/store.py, src/workflows/registration.py, src/api/catalog_summary.py, src/reports/catalog_export.py and four test files. Implementation Notes say scheduled_sync.py, fallback_import.py, on_demand_refresh.py are 'Out of scope pending clarification ... Do not modify them in this task'. impact-map.md confirms they are 'deliberately left out of the Files to Modify and Test Requirements of the drafted tasks'."

- **Assertion:** "Task Test Requirements cover each writer with its corresponding test path: tests/workflows/test_registration.py, tests/workflows/test_scheduled_sync.py, tests/workflows/test_fallback_import.py, and tests/api/test_on_demand_refresh.py"
  **Evidence:** "task-1 Test Requirements include only tests/catalog/test_store.py, tests/workflows/test_registration.py, tests/api/test_catalog_summary.py, tests/reports/test_catalog_export.py. test_scheduled_sync.py, test_fallback_import.py and test_on_demand_refresh.py appear only in the impact map / summary as unresolved, not in any task's Test Requirements."

- **Assertion:** "Implementation tasks specify path-specific validation: registration persists the supplied ownerGroup, scheduled sync/fallback/on-demand updates preserve an existing value when omitted and apply a supplied replacement, and both consumers expose values from all four writers"
  **Evidence:** "Only registration validation is specified ('registration with ownerGroup persists it on the created record'). No task specifies validation for scheduled sync, fallback import, or on-demand refresh; task-1 explicitly excludes them. Consumer tests only check 'the summary response includes the record's ownerGroup', not values from all four writers."

- **Assertion:** "Generated tasks cover both catalog consumers, src/api/catalog_summary.py and src/reports/catalog_export.py, and validate that entries produced by every writer are visible to those consumers"
  **Evidence:** "task-1 covers both consumers, but its draft note states 'This task alone does not satisfy the Feature's "every record / regardless of how populated" criteria', and impact-map.md marks AC2 'Regardless of how populated is NOT covered'. No validation of entries from every writer."

- **Assertion:** "Task Test Requirements include tests/api/test_catalog_summary.py and tests/reports/test_catalog_export.py, exercising records from each writer through each consumer"
  **Evidence:** "Both test files appear in task-1 Test Requirements, but only as 'the summary response includes the record's ownerGroup' and 'the exported report includes the record's ownerGroup'. Nothing exercises records from scheduled sync, fallback import, or on-demand refresh."

- **Assertion:** "Generated tasks preserve the fixture's existing-population behavior and stable-ID compatibility acceptance criterion"
  **Evidence:** "Fixture AC3 is 'Existing catalog population behavior and stable IDs remain unchanged' (quoted in impact-map.md). task-1 narrows it to 'Stable record IDs and existing registration behavior are unchanged'; impact-map.md coverage table says AC3 is 'Covered for store and registration. The alternate paths are NOT verified. Unresolved'. Population behavior across all paths is not preserved as a criterion."

- **Assertion:** "The fallback-import and on-demand-refresh paths are explicitly planned; coverage is not limited to initial registration and scheduled sync"
  **Evidence:** "fallback_import.py and on_demand_refresh.py appear only as 'UNRESOLVED' in impact-map.md and impact-map-comment.md; task-1 says 'Do not modify them in this task'. No task plans their implementation or tests (coverage is limited to registration only)."

</details>

**Pass rate:** 91% · **Tokens:** 86,118 · **Duration:** 200s

**Baseline** (`4e3e421a`): 95% · 82,700 tokens · 190s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10*

