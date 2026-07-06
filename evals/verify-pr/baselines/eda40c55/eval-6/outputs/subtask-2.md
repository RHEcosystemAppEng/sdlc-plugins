## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. Two assertions are failing at 85% pass rate (11/13 passed, 2 failed). The failures indicate that the verify-pr skill is not evaluating convention upgrade eligibility for review comments classified as suggestions, and is not creating sub-tasks when convention upgrade would elevate a suggestion to a code change request.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure the Convention Upgrade check (Check 1) evaluates every comment classified as suggestion for convention upgrade eligibility, including performing CONVENTIONS.md lookup and codebase pattern analysis
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b (Apply Convention Upgrades) processes upgrade-comment actions and that Step 6d creates sub-tasks for upgraded suggestions

## Implementation Notes
- The failing assertions point to a gap in the convention upgrade pipeline: comments classified as "suggestion" are not being evaluated for convention upgrade eligibility.
- The Convention Upgrade check (Check 1 in style-conventions.md) must evaluate every suggestion against CONVENTIONS.md and codebase patterns, documenting the analysis in the review classification output.
- When a suggestion matches a convention (documented in CONVENTIONS.md or demonstrated by codebase patterns), it must be upgraded to a code change request via an `upgrade-comment` action.
- The orchestrator's Step 6b must then apply the upgrade, and Step 6d must create a sub-task for the upgraded comment.
- The review classification output (review-N.md files) must include convention upgrade eligibility reasoning for suggestions -- even when no convention match is found, the output should document that a lookup was performed and no match was found.

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every review comment classified as suggestion
- [ ] The review classification output documents whether a CONVENTIONS.md lookup and/or codebase pattern analysis was performed for each suggestion
- [ ] When a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request via upgrade-comment action
- [ ] Sub-tasks are created for suggestions that are upgraded to code change requests through convention analysis
- [ ] The convention upgrade evaluation is transparent in the classification reasoning (either match found with evidence, or no match found with lookup documented)

## Test Requirements
- [ ] Verify that suggestions undergo convention upgrade eligibility evaluation
- [ ] Verify that convention-matching suggestions result in upgrade-comment actions
- [ ] Verify that upgraded suggestions result in sub-task creation
- [ ] Verify that non-matching suggestions remain as suggestions with documented lookup

## Review Context
**Eval result review (github-actions[bot], review 40001) -- eval-3 failing assertions:**

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
