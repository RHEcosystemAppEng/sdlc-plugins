## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments. Two assertions are failing in eval-3 (85% pass rate, 2 failures out of 13 assertions): the verify-pr skill is not evaluating convention upgrade eligibility for suggestion-classified review comments, and is not creating sub-tasks when comments should be elevated to code change requests through convention analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 1 (Convention Upgrade) to ensure convention upgrade eligibility is explicitly evaluated and documented for all suggestion-classified comments, including those where no convention match is found
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade processing and Step 6d sub-task creation correctly handle the case where a suggestion should be upgraded based on convention analysis

## Implementation Notes
- The eval-3 failures indicate that when a review comment is classified as a suggestion (e.g., an index suggestion for comment 30002), the convention upgrade eligibility check is either not running or not producing output that documents the analysis
- The review classification output (review-30002.md) must document the convention upgrade eligibility assessment -- whether a CONVENTIONS.md lookup or codebase pattern analysis was performed
- The sub-task creation path must account for both direct code change request classification and suggestion-to-code-change-request upgrades via convention analysis
- Follow the existing Check 1 structure in style-conventions.md (steps 1a through 1d) to ensure the upgrade decision is always recorded with evidence

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments
- [ ] The review classification output documents whether CONVENTIONS.md lookup or codebase pattern analysis was performed for each suggestion
- [ ] When a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request and a sub-task is created
- [ ] eval-3 assertions pass at 100% (all 13 assertions)

## Test Requirements
- [ ] Verify eval-3 passes with all 13 assertions after the fix
- [ ] Verify that suggestion-classified comments have convention upgrade eligibility documented in their review output files

## Review Context
Two failing assertions from eval-3 in the CI eval results:

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
