## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 failures in the verify-pr skill related to convention upgrade eligibility evaluation. Two assertions fail: (1) convention upgrade eligibility is not evaluated for suggestion-classified review comments, and (2) review comments that should result in sub-tasks (either directly as code change requests or via convention upgrade) do not produce sub-tasks when convention upgrade is not attempted.

The verify-pr skill should evaluate whether a suggestion-classified review comment matches a documented or demonstrated project convention (via CONVENTIONS.md lookup or codebase pattern analysis), and if so, upgrade the classification to a code change request that produces a sub-task.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- add or update the review comment classification logic to include convention upgrade eligibility evaluation for suggestions
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- if convention upgrade logic interacts with style/conventions analysis, update accordingly

## Implementation Notes
- The convention upgrade eligibility check should apply when a review comment is classified as a "suggestion"
- The check should look up CONVENTIONS.md (or equivalent) and analyze codebase patterns to determine if the suggestion aligns with a documented or demonstrated project convention
- If the suggestion matches a convention, upgrade the classification to "code change request" and create a sub-task
- Ensure the classification reasoning output (review-N.md) documents the convention upgrade evaluation

## Review Context
**Failing Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

**Source:** eval-3 (verify-pr eval suite), 2 of 13 assertions failing (~85% pass rate)

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for review comments classified as suggestions
- [ ] The classification reasoning output documents the convention upgrade evaluation (CONVENTIONS.md lookup or codebase pattern analysis)
- [ ] Suggestions matching a documented or demonstrated project convention are upgraded to code change requests
- [ ] Upgraded code change requests result in sub-task creation
- [ ] eval-3 assertions pass after the fix
