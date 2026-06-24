## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002. Two assertions fail because the verify-pr skill does not evaluate convention upgrade eligibility for suggestion-classified comments and does not create sub-tasks when convention upgrade would be warranted.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure the Convention Upgrade check (Check 1) evaluates all suggestion-classified comments for convention upgrade eligibility, including performing CONVENTIONS.md lookup and codebase pattern analysis
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade processing and Step 6d sub-task creation handle upgraded suggestions correctly so that convention-backed suggestions result in sub-tasks

## Implementation Notes
- The failing assertions indicate that review comment 30002 (an index suggestion) was classified as a suggestion but no convention upgrade eligibility was evaluated -- no CONVENTIONS.md lookup or codebase pattern analysis was documented in the classification reasoning
- The Convention Upgrade check (Check 1 in style-conventions.md) must evaluate every suggestion-classified comment, documenting the CONVENTIONS.md lookup and codebase pattern analysis in the output even when no match is found
- When a suggestion is upgraded to a code change request via convention match, the orchestrator's Step 6d must create a sub-task for it
- Review the existing Check 1 steps (1a through 1d) to ensure the evaluation pipeline runs completely for all suggestions and produces transparent evidence in the output

## Review Context
The following eval-3 assertions failed:

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, with documented reasoning (CONVENTIONS.md lookup and/or codebase pattern analysis)
- [ ] When a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request and a sub-task is created
- [ ] The classification output for suggestion comments includes explicit evidence of convention upgrade evaluation
