## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two eval-3 assertion regressions introduced by the Documentation Coverage changes. The eval-3 assertions fail because convention upgrade eligibility is not evaluated for review comment 30002 (index suggestion), and no sub-task is created for that comment regardless of classification path.

The baseline shows eval-3 passing 14/14 (100%), but the PR branch shows 11/13 (85%), confirming these are regressions.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- investigate whether the addition of Check 6 or the Output Format changes affected convention upgrade processing or sub-task creation logic
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- check if the new Step 6a verdict mapping for Documentation Coverage introduced a conflict with existing convention upgrade processing

## Implementation Notes
- The two failing assertions are:
  1. "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention" -- Evidence: "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
  2. "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis" -- Evidence: "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
- These failures suggest the convention upgrade check (Check 1 in style-conventions.md) may not be executing properly after the addition of Check 6
- Review the Check 1 convention upgrade logic to ensure it still processes all suggestion-classified comments correctly
- Check whether the Output Format change from five rows to six rows affected how the Style/Conventions sub-agent processes its checks

## Acceptance Criteria
- [ ] eval-3 passes all assertions (14/14 or higher) with the fix applied
- [ ] Convention upgrade eligibility is properly evaluated for suggestion-classified review comments
- [ ] Sub-tasks are created for review comments that match project conventions, whether classified directly as code change requests or upgraded from suggestions

## Review Context
**Eval result review excerpt (from CI eval run):**

eval-3: 2 failing assertions:

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

**Baseline comparison:** eval-3 passes 14/14 at baseline (commit bae6630), confirming these are regressions.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
