## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002. Two assertions are failing at 85% pass rate: (1) the review classification output does not evaluate convention upgrade eligibility for review comment 30002 (index suggestion), and (2) no sub-task is created for review comment 30002 regardless of classification path.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade eligibility is evaluated and documented in the classification reasoning for suggestion-classified comments
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure the classification and sub-task creation pipeline handles the case where a suggestion should be elevated to a code change request via convention analysis

## Implementation Notes
- The failing assertions indicate that when a review comment (30002) is classified as a suggestion, the verify-pr skill does not attempt convention upgrade analysis (no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning)
- The convention upgrade check (Style/Conventions sub-agent Check 1) must run on all suggestion-classified comments and document its analysis in the output, even when no convention match is found
- If convention upgrade determines the suggestion matches a project convention, it should be elevated to a code change request and result in a sub-task
- Review the eval-3 test scenario to understand the expected behavior for review comment 30002 (an index suggestion) and ensure the convention upgrade pipeline processes it correctly

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for suggestion-classified review comments and the analysis is documented in the classification output
- [ ] Review comment 30002 (index suggestion) results in a sub-task when convention analysis determines it matches a project convention
- [ ] The review classification output (review-N.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify that convention upgrade eligibility is evaluated and documented for all suggestion-classified comments
- [ ] Verify that suggestions matching project conventions are elevated to code change requests and result in sub-tasks

## Review Context
Eval result review from CI (github-actions[bot], review 40001) reported 2 failing assertions in eval-3:

**Assertion 1:**
- **Assertion text:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
- **Assertion text:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
