# Sub-task 4 — Wire Documentation Coverage into the live Step 6a mapping and the Step 8 report

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Labels:** ai-generated-jira, review-feedback
- **Link:** Blocks TC-9106

## Repository
sdlc-plugins

## Target Branch
main

## Description
TC-9106 Acceptance Criterion 7 requires the Step 6a verdict mapping to include Documentation Coverage. The PR adds the row inside a fenced block under "Add a new mapping row:" instead of the live Step 6a table. The row also maps to a "Style Quality *(new)*" report row that exists in neither the Step 8 report table nor the verdict source mapping, so the verdict never reaches the report. Wire Documentation Coverage end to end.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — add the Documentation Coverage row to the live Step 6a mapping table and remove the stray fenced row. Then either fold Documentation Coverage into an existing combined row and update its combination rule (per the task's "combined Style/Conventions verdict"), or add the new report row to the Step 8 table and the Verdict source mapping. State whether the row is informational for the Overall result.
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — make the Output Format table and "exactly N rows" text agree with the actual rows (including Test Change Classification), and update the Constraints line "MUST process all four checks" to the real count
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new behavior

## Implementation Notes
- Live mapping table: SKILL.md Step 6a, item 1 (rows `| Style/Conventions | ... |`). The new row goes after `Eval Quality`, next to `Test Change Classification`.
- If Documentation Coverage joins Test Quality, extend the combination bullets in Step 6a ("If any of the three is WARN…") to cover four checks. Otherwise add a row to the Step 8 report template and the "Verdict source mapping" table, and add it to the informational-rows note if appropriate.
- Follow how Eval Quality was added: mapping row, combination rule, report Details text and source mapping all updated together.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md::Step 6a` — Test Quality combination rule (pattern for combined verdicts)
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md::Step 8` — report table and Verdict source mapping

## Acceptance Criteria
- [ ] The live Step 6a mapping table contains a Documentation Coverage row; no stray fenced mapping block remains
- [ ] The report row it maps to exists in the Step 8 report table and the Verdict source mapping (or it is folded into an existing combined row with an updated rule)
- [ ] The style-conventions.md Output Format row count, the table and the Constraints check count agree with each other

## Test Requirements
- [ ] Verify a verify-pr run produces a report that shows the Documentation Coverage verdict, either in its own row or in the combined row's details
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes.

## Review Context
Source: verify-pr Correctness sub-agent, Acceptance Criteria check. AC7 "Step 6a verdict mapping includes Documentation Coverage" was judged FAIL. The PR diff for `SKILL.md` hunk `@@ -354,6 +354,7 @@ Add a new mapping row:` adds `| Style/Conventions | Documentation Coverage | Style Quality *(new)* |` right before a closing code fence. Base SKILL.md has no "Style Quality" row in Step 8 or the Verdict source mapping.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

Add commits to the existing PR #747 head branch; do not open a new PR. The Repository Registry entry `sdlc-plugins` (path `./`) resolves to origin `RHEcosystemAppEng/sdlc-plugins`. The TC-9106 Git Pull Request field records the same PR number as `https://github.com/mrizzi/sdlc-plugins/pull/747`.

## Dependencies
- Depends on: TC-9106 — Add documentation coverage check to style-conventions sub-agent (this sub-task amends its PR)
