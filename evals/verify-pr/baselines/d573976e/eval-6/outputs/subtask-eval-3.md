## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Fix eval-3 assertion failures in the verify-pr eval suite. Two assertions are failing at 85% pass rate (11/13 passed, 2 failed). Both failures relate to convention upgrade eligibility evaluation for review comment 30002 (an index suggestion). The implementation must ensure that convention upgrade eligibility is evaluated for suggestions and that sub-tasks are created when the convention upgrade path applies.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) logic is correctly applied to all suggestion-classified comments, including documentation of the evaluation in output files
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 6b (Apply Convention Upgrades) correctly processes upgrade-comment actions and creates sub-tasks for upgraded suggestions

## Implementation Notes
- The eval-3 scenario includes a review comment (id 30002) classified as a suggestion about adding an index
- The eval expects that convention upgrade eligibility is explicitly evaluated and documented in the classification output (review-30002.md), showing whether the suggestion matches a documented CONVENTIONS.md convention or demonstrated codebase pattern
- The eval also expects that the suggestion results in a sub-task, either through direct classification as a code change request or through convention upgrade
- Review the eval-3 fixture data and assertions to understand the exact expected behavior
- The baseline (latest) shows these assertions passing at 100%, so this is a regression introduced by the current PR's changes

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) and the evaluation is documented in the classification output
- [ ] Review comment 30002 results in a sub-task regardless of classification path -- whether classified directly as code change request or upgraded from suggestion via convention analysis
- [ ] eval-3 pass rate returns to 100% (13/13 assertions passing)

## Review Context

The following eval assertions are failing (from the CI eval result review on PR #747):

> **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
> **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

> **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
> **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

These assertions pass on the baseline branch (14/14 at 100%) but fail on this PR branch, indicating a regression.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
