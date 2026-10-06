## Repository
sdlc-plugins

## Target Branch
main

## Description
Investigate and fix eval-3 failures in verify-pr evals. Two assertions are failing at 85% pass rate (11/13 passed, 2 failed). Both failures relate to convention upgrade eligibility not being evaluated for review comment 30002 (an index suggestion). The verify-pr skill should evaluate whether a suggestion matches a documented or demonstrated project convention, and if so, upgrade it to a code change request that produces a sub-task.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update review classification logic to include convention upgrade eligibility evaluation for suggestions
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure the review processing pipeline documents convention upgrade path from suggestion to code change request

## Implementation Notes
- The two failing assertions both concern review comment 30002, which is an "index suggestion"
- The first failure indicates that when classifying a suggestion, the skill must evaluate convention upgrade eligibility by checking CONVENTIONS.md or analyzing codebase patterns
- The second failure indicates that comment 30002 should result in a sub-task regardless of classification path -- either classified directly as a code change request, or upgraded from suggestion via convention analysis
- The fix likely involves adding a convention upgrade step in the review classification pipeline: after a comment is classified as "suggestion," check whether the suggestion aligns with a documented convention or demonstrated codebase pattern, and if so, upgrade it to a code change request

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for suggestions during review classification
- [ ] The review classification output documents whether CONVENTIONS.md lookup or codebase pattern analysis was performed
- [ ] Suggestions that match documented or demonstrated conventions are upgraded to code change requests and produce sub-tasks
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify that a suggestion matching a documented convention is upgraded to a code change request
- [ ] Verify that the classification reasoning includes convention upgrade eligibility analysis
- [ ] Verify that upgraded suggestions produce sub-tasks

## Review Context
The following eval assertions failed for eval-3:

**Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence:**
> "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence:**
> "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
