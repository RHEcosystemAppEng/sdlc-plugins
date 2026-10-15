## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility and sub-task creation for review comments classified as suggestions. Two assertions failed in eval-3 at 85% pass rate (11/13 passed, 2 failed):

1. Convention upgrade eligibility was not evaluated for review comment 30002 (an index suggestion). The classification output did not document any CONVENTIONS.md lookup or codebase pattern analysis, meaning the convention upgrade pipeline (Check 1 in the Style/Conventions sub-agent) was not applied to the suggestion.

2. Review comment 30002 did not result in a sub-task. Because the convention upgrade was never attempted, the suggestion was not elevated to a code change request, and no sub-task was created.

The root cause is that the convention upgrade pipeline was not executed for the suggestion, preventing it from being upgraded to a code change request and subsequently generating a sub-task.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) is applied to all comments classified as suggestion, including documenting the CONVENTIONS.md lookup and codebase pattern analysis in the classification reasoning output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that Step 6b (Apply Convention Upgrades) correctly processes upgrade-comment actions and that Step 6d creates sub-tasks for upgraded suggestions

## Implementation Notes
- The convention upgrade pipeline (Check 1 in style-conventions.md) must be applied to every comment classified as **suggestion** in the Classified Review Comments
- The classification reasoning output (review-N.md files) must document whether a CONVENTIONS.md lookup was performed and what codebase pattern analysis was done, even when no convention match is found
- When a suggestion matches a documented convention (CONVENTIONS.md) or a demonstrated codebase pattern, it must be upgraded to a code change request via an `upgrade-comment` action
- After upgrade, the orchestrator's Step 6d must create a sub-task for the upgraded code change request
- Review the existing Check 1 steps (1a through 1d) to ensure they are triggered for all suggestion-classified comments, not just a subset

## Acceptance Criteria
- [ ] Convention upgrade eligibility (Check 1) is evaluated for every comment classified as suggestion
- [ ] The classification reasoning output documents the CONVENTIONS.md lookup and codebase pattern analysis for each suggestion
- [ ] Suggestions matching a documented convention or demonstrated codebase pattern are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation in Step 6d
- [ ] The eval-3 assertions pass: convention upgrade eligibility is evaluated for comment 30002, and a sub-task is created for it

## Test Requirements
- [ ] Verify that a suggestion comment triggers convention upgrade analysis (CONVENTIONS.md lookup + codebase pattern scan)
- [ ] Verify that the classification reasoning output includes convention upgrade analysis evidence
- [ ] Verify that a suggestion matching a convention is upgraded and produces a sub-task
- [ ] Verify that a suggestion not matching any convention remains a suggestion with documented reasoning

## Review Context
**Source:** Eval result review from CI (github-actions[bot], review ID 40001)
**Eval:** eval-3 (11/13 passed, 2 failed, 85% pass rate)

**Failing Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence 1:**
> "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence 2:**
> "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
