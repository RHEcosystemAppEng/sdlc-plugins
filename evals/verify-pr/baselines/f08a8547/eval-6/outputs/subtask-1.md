## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The eval-3 results show two failing assertions: (1) convention upgrade eligibility is not evaluated for suggestion-classified review comments, and (2) sub-tasks are not created for suggestions that should be elevated to code change requests via convention analysis. The implementation must ensure that the verify-pr skill evaluates convention upgrade eligibility for all suggestion-classified comments and creates sub-tasks when convention analysis upgrades a suggestion to a code change request.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) logic covers all suggestion-classified comments and produces upgrade-comment actions when conventions match
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 6b (Apply Convention Upgrades) correctly processes upgrade-comment actions and feeds upgraded suggestions into the sub-task creation pipeline (Step 6d)

## Implementation Notes
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must evaluate every comment classified as **suggestion** for convention upgrade eligibility -- currently review comment 30002 (index suggestion) was not evaluated
- Convention upgrade eligibility requires either a CONVENTIONS.md match or a demonstrated codebase pattern (counted occurrences in similar files)
- When a suggestion is upgraded to code change request, it must flow through Step 6b into Step 6d for sub-task creation
- Review the existing Convention Upgrade check (steps 1a-1d) in style-conventions.md for completeness of the evaluation pipeline
- Ensure the upgrade-comment action format in the Output Format section matches what the orchestrator expects in Step 6b

## Review Context
Eval-3 produced 2 failing assertions (85% pass rate, 11/13 passed):

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all review comments classified as suggestion, with documented reasoning (CONVENTIONS.md lookup result or codebase pattern count)
- [ ] When convention analysis matches a documented or demonstrated pattern, the suggestion is upgraded to code change request and an upgrade-comment action is produced
- [ ] Upgraded suggestions flow through Step 6b into Step 6d, resulting in sub-task creation
- [ ] Eval-3 assertions pass after the fix (convention upgrade eligibility is evaluated and sub-task is created for review comment 30002)

## Test Requirements
- [ ] Verify eval-3 passes with all assertions after the fix
- [ ] Verify that suggestions without convention backing remain classified as suggestions (no false upgrades)
- [ ] Verify that upgraded suggestions produce both an upgrade-comment action and a downstream sub-task
