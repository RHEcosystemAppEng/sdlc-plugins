## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002. Two assertions fail because the verify-pr skill does not evaluate convention upgrade eligibility for suggestion-classified comments and does not create sub-tasks when convention upgrade would apply. The implementation must ensure that review comments classified as suggestions are evaluated for convention upgrade eligibility (checking CONVENTIONS.md and codebase patterns), and that suggestions matching a documented or demonstrated convention are upgraded to code change requests with corresponding sub-tasks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade logic is applied to all suggestion-classified comments, including those where the reviewer language is suggestive but the pattern matches a project convention
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- verify the Convention Upgrade check (Check 1) correctly identifies convention-backed suggestions and produces upgrade-comment actions for the orchestrator

## Implementation Notes
- The root cause is that review comment 30002 (an index suggestion) was classified as a suggestion and no convention upgrade was attempted. The Style/Conventions sub-agent's Convention Upgrade check should analyze whether the suggestion matches a pattern in CONVENTIONS.md or a demonstrated codebase convention.
- Follow the existing convention upgrade flow: Style/Conventions sub-agent produces `upgrade-comment` actions (Check 1), orchestrator applies them in Step 6b before sub-task creation in Step 6d.
- Ensure the classification reasoning output (review-30002.md) documents whether convention upgrade eligibility was evaluated, including CONVENTIONS.md lookup and codebase pattern analysis.

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for suggestion-classified review comments, with CONVENTIONS.md lookup and codebase pattern analysis documented in the classification reasoning
- [ ] Review comments matching a documented or demonstrated project convention are upgraded from suggestion to code change request
- [ ] Upgraded suggestions result in sub-task creation with convention evidence in the PR reply
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify eval-3 passes with all assertions succeeding
- [ ] Verify convention upgrade eligibility evaluation appears in classification output for suggestion comments

## Review Context

This sub-task addresses 2 failing assertions from eval-3 (85% pass rate, 11/13 passed) detected in the CI eval result review:

**Failing Assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
