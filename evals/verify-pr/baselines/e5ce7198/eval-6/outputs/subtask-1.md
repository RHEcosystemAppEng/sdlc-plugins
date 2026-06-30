## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Fix eval-3 failing assertions in verify-pr: the review classification for comment 30002 (index suggestion) does not evaluate convention upgrade eligibility, and no sub-task is created for the comment. The convention upgrade path must be attempted for suggestions that match documented or demonstrated project conventions, and if the suggestion matches a convention, it must be elevated to a code change request with a corresponding sub-task.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context
Two failing assertions from eval-3 (85% pass rate, 2 failures out of 13 assertions):

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure the review classification logic includes convention upgrade eligibility evaluation for suggestions
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify the convention upgrade path is correctly specified in the review classification workflow

## Implementation Notes
- The verify-pr skill must evaluate convention upgrade eligibility for review comments classified as suggestions
- When a suggestion matches a documented convention (in CONVENTIONS.md) or a demonstrated codebase pattern, it should be upgraded to a code change request
- The classification reasoning output (review-N.md) must document whether convention upgrade eligibility was evaluated, including the lookup results
- If upgraded, a sub-task must be created for the resulting code change request
- Review the existing convention upgrade logic in the verify-pr skill and ensure it triggers for all suggestion-classified comments

## Acceptance Criteria
- [ ] Review comment classifications for suggestions include convention upgrade eligibility evaluation
- [ ] The classification reasoning output documents whether a CONVENTIONS.md lookup or codebase pattern analysis was performed
- [ ] Suggestions matching documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation
- [ ] eval-3 assertions pass after the fix (re-run eval to verify)

## Test Requirements
- [ ] Verify that a suggestion matching a documented convention is upgraded and produces a sub-task
- [ ] Verify that a suggestion not matching any convention remains classified as a suggestion with documented reasoning
- [ ] Verify eval-3 achieves 100% pass rate after the fix
