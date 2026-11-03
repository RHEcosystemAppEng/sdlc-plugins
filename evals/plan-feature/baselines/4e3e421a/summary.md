## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 15/16 | 1 | 94% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 14/15 | 1 | 93% |
| eval-6 | 14/14 | 0 | 100% |
| eval-7 | 8/10 | 2 | 80% |
| eval-8 | 4/4 | 0 | 100% |
| eval-9 | 4/4 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains any 'Per CONVENTIONS.md' line or any 'Applies:' rationale (grep for 'CONVENTIONS', 'Applies:' returned nothing), even though repo-backend.md lists CONVENTIONS.md and Key Conventions. Conventions are instead applied as free-form prose, e.g. Task 1: 'Follow the module pattern `model/ + service/ + endpoints/` used throughout modules/fundamental/src/' with no applicability rationale in the prescribed format. There is no evidence that file-type applicability validation was performed."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "The 'Per CONVENTIONS.md §...' entries use the prescribed format, e.g. task-1: 'Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint handler scope.' No 'Not applicable' annotations exist. However, task-1's Implementation Notes also apply two repo conventions as free-form prose with no 'Applies:' rationale: the Caching convention ('Caching: the repository configures `tower-http` caching middleware in endpoint route builders. Apply the same configuration...') and the Error handling convention ('Error handling: handlers return `Result&lt;T, AppError&gt;` (`common/src/error.rs`) with `.context()` wrapping'). Tasks 2 and 3 give Error handling a formal rationale, so the treatment is inconsistent. Under the default-to-FAIL rule, this fails."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Tasks 5, 6 and 8 cite Figma with PF components and visual specs (Task 5: 'Section order, titles and badge colors (from Figma)', ExpandableSection/Label/Table/Skeleton; Task 6: 'Header toolbar (Figma)', PF5 Select typeahead, EmptyState with CodeBranchIcon; Task 8: 'Figma: the Export button is a secondary PF5 Dropdown'). But task-7-frontend-list-compare-selected.md is UI-facing (it modifies src/pages/SbomListPage/SbomListPage.tsx) and has 0 mentions of Figma (grep count 0). It names PF components (Td select, Button, Tooltip) but cites no Figma design context. Note that figma-context.md does not cover the list page. Under the strict rule, one UI task without Figma context means FAIL."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Tasks 2, 3, and 4 have all required sections (task 2 has Files to Modify and Files to Create, tasks 3 and 4 have Files to Modify, and all three have Implementation Notes, Acceptance Criteria, and Test Requirements). Doc Task 5 has Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements. But the bookend tasks are non-documentation tasks and are missing sections. task-1-create-feature-branch.md and task-6-merge-feature-branch.md contain only Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, and Dependencies. Neither has Files to Modify/Create or Implementation Notes. Under the literal assertion ('Each non-documentation task file'), these two files fail."

</details>

<details>
<summary>eval-7: 2 failing assertions</summary>

- **Assertion:** "Implementation tasks cover src/catalog/store.py and tests/catalog/test_store.py, verifying ownerGroup persistence, omitted-update preservation, explicit replacement, and unchanged stable IDs"
  **Evidence:** "task-1 covers `src/catalog/store.py` (line 31) and `tests/catalog/test_store.py` with tests for round-trip persistence (line 94), fail-closed validation (line 95), and 'an update without `ownerGroup` keeps the stored value, and an update with a new value replaces it' (line 96). None of the test_store.py items, and none of the store.py descriptions, check that stable IDs stay unchanged. Stable-ID checks appear only in the writer tests (lines 97-100) and the general AC on line 91. Because the store-level verification of stable IDs is missing, this assertion fails under the strict, no-partial-credit rule."

- **Assertion:** "Implementation tasks specify path-specific validation: registration persists the supplied ownerGroup, scheduled sync/fallback/on-demand updates preserve an existing value when omitted and apply a supplied replacement, and both consumers expose values from all four writers"
  **Evidence:** "The following parts are present. Registration: 'registering a service stores the supplied `ownerGroup`' (line 97). Fallback: 'importing exported data with `ownerGroup` stores it. Importing data without `ownerGroup` keeps the existing value' (line 99). On-demand: 'without `ownerGroup` keeps the stored value. With `ownerGroup`, it updates the value' (line 100). Consumers: lines 101-102. Scheduled sync, however, only preserves the value: 'syncing an existing record keeps its `ownerGroup`' (line 98) and 'keep the existing `ownerGroup` when synchronizing provider metadata' (line 33). Sync has no item that applies a supplied replacement value, so the requirement is not met for scheduled sync."

</details>

**Pass rate:** 95% · **Tokens:** 82,700 · **Duration:** 190s

**Baseline** (`7c25e5c0`): 99% · 96,891 tokens · 195s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10*

