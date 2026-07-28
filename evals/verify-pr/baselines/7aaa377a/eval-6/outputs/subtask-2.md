## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures in the verify-pr eval suite. Two assertions are failing at 85% pass rate (11/13 passed, 2 failed). Both failures relate to the handling of review comment 30002 (an index suggestion): (1) convention upgrade eligibility is not evaluated for the comment, and (2) no sub-task is created for the comment. The implementation must ensure that suggestions classified during review feedback processing are evaluated for convention upgrade eligibility, and that comments eligible for upgrade result in sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) instructions clearly require evaluating all suggestion-classified comments for convention upgrade eligibility, including CONVENTIONS.md lookup and codebase pattern analysis
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b (Apply Convention Upgrades) and Step 6d (Create Sub-Tasks) instructions clearly require processing upgraded suggestions through the sub-task creation pipeline

## Implementation Notes
- The eval-3 failures indicate that a suggestion comment (comment 30002, an index suggestion) was not evaluated for convention upgrade eligibility -- the classification reasoning did not document any CONVENTIONS.md lookup or codebase pattern analysis
- After convention upgrade evaluation, if the suggestion matches a documented or demonstrated convention, it should be upgraded to a code change request and proceed through sub-task creation in Step 6d
- Review the Convention Upgrade check (Check 1) in style-conventions.md to ensure steps 1a-1d explicitly require processing every suggestion-classified comment
- Review Step 6b in SKILL.md to ensure upgrade-comment actions from the Style/Conventions sub-agent are applied before sub-task creation in Step 6d
- The fix should ensure convention upgrade eligibility evaluation is documented in the classification reasoning output (review-N.md files) so that eval assertions can verify it

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, with CONVENTIONS.md lookup and/or codebase pattern analysis documented in classification reasoning
- [ ] Suggestions that match documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation through the standard Step 6d pipeline
- [ ] eval-3 assertions pass: convention upgrade eligibility evaluated for comment 30002 and sub-task created for comment 30002

## Test Requirements
- [ ] Re-run eval-3 and verify both previously-failing assertions now pass
- [ ] Verify overall eval pass rate improves from 85% to 100% for eval-3
- [ ] Verify no regressions in eval-1, eval-2, eval-4, eval-5

## Review Context
**Source:** Eval result review from github-actions[bot] (review ID 40001)
**Eval ID:** eval-3
**Pass rate:** 85% (11/13 passed, 2 failed)

**Failing assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
