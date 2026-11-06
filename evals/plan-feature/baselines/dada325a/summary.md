## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 13/15 | 2 | 87% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 13/15 | 2 | 87% |
| eval-6 | 14/14 | 0 | 100% |
| eval-7 | 8/10 | 2 | 80% |
| eval-8 | 4/4 | 0 | 100% |
| eval-9 | 4/4 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "A summary of inherited field propagation is produced — evidenced by a summary-comment.md file in the outputs directory, or a summary section in the impact map that includes the inherited priority and fixVersion values propagated to tasks, or states they were omitted and why"
  **Evidence:** "impact-map.md 'Jira comments written as files' claims 'summary-comment.md: plan summary, posted on TC-9001 (Step 6c)', but no summary-comment.md exists in the outputs directory (only impact-map.md, impact-map-comment.md, task files and digest files). The impact map has no summary section (Step 6c); propagated values appear only in the Step 6a creation log's additional_fields block, not in a produced plan summary. The claimed artifact is missing, so this fails."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Tasks 5, 6, and 8 cite Figma. Task 5 has 'Figma layout (SBOMCompare / Comparison View)' with PF Select typeahead, primary Button, EmptyState with CodeBranchIcon, and Skeleton. Task 6 has a 'Section specification (from Figma)' table with badge colors and PF tokens. Task 8 refers to 'the Export dropdown from the Figma header toolbar'. Task 7 (task-7-sbom-list-compare-selection.md) is UI-facing: it modifies the SbomListPage.tsx page and adds a 'Compare selected' Button and checkboxes. It never references Figma design context; it lists only PF5 Table row selection and a secondary Button with no Figma attribution. Not every UI-facing task meets the requirement, so this fails."

- **Assertion:** "A summary of inherited field propagation is produced — evidenced by a summary-comment.md file in the outputs directory, or a summary section in the impact map that includes the inherited priority and fixVersion values propagated to tasks, or states they were omitted and why"
  **Evidence:** "There is no summary-comment.md in the outputs directory, although impact-map.md '### 6c — Summary comment' says 'See summary-comment.md'. The summary comment is referenced but was never produced. The impact map has no dedicated summary section; the priority and fixVersion values appear only in the Step 6a task creation log, which the separate fixVersion/priority assertions already cover. The output points to a summary artifact that does not exist, so this fails."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Tasks 2–5 contain all required sections, and documentation task 6 has its required ones. But the non-documentation bookend task files task-1-create-feature-branch.md and task-7-merge-feature-branch.md have no '## Files to Modify', '## Files to Create' or '## Implementation Notes' section. They contain only Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements and Dependencies. The assertion exempts only documentation tasks, not bookends."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains an 'Applies: task modifies ...' rationale. impact-map.md says CONVENTIONS.md 'contents were not available in this eval' and that tasks cite Key Conventions instead. The task files mention conventions only in free-form prose, e.g. task-5: 'Follow the error-handling convention: return `Result&lt;T, AppError&gt;`...'. There is no evidence of applicability validation against convention-applicability-rules.md."

</details>

<details>
<summary>eval-7: 2 failing assertions</summary>

- **Assertion:** "Implementation tasks cover src/catalog/store.py and tests/catalog/test_store.py, verifying ownerGroup persistence, omitted-update preservation, explicit replacement, and unchanged stable IDs"
  **Evidence:** "Task 1 covers both files. The store test requirements check that the merge helper 'keeps the existing value when incoming is missing or empty, and overrides when incoming is non-empty', and that writes without ownerGroup fail closed. No store-level test checks that stable IDs are unchanged. 'IDs unchanged' appears only in the writer test requirements (sync, import, refresh). No store test explicitly checks the persistence round trip either; the Files to Modify entry just says 'schema, merge and validation tests'."

- **Assertion:** "Implementation tasks specify path-specific validation: registration persists the supplied ownerGroup, scheduled sync/fallback/on-demand updates preserve an existing value when omitted and apply a supplied replacement, and both consumers expose values from all four writers"
  **Evidence:** "Registration ('persists the supplied ownerGroup'), fallback import ('uses ownerGroup from exported data when present, and otherwise keeps the existing value'), on-demand refresh ('refresh without ownerGroup keeps it; refresh with a new ownerGroup updates it'), and both consumers ('for records populated through each of the four writers') are all specified. Scheduled sync is the gap. Its acceptance criterion says only that it 'keeps the existing ownerGroup when refreshing a record that has one', and its test says only that sync 'leaves it unchanged'. No path-specific check covers sync applying a supplied replacement. That behavior is implied only through the shared merge helper."

</details>

**Pass rate:** 94% · **Tokens:** 83,807 · **Duration:** 214s

**Baseline** (`47e860e6`): 91% · 86,118 tokens · 200s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10*

