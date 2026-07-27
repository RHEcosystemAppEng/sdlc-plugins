## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The eval results show two failing assertions in eval-3 (11/13 passed, 85% pass rate), both concerning review comment 30002 (an index suggestion): (1) convention upgrade eligibility is not being evaluated for the comment, and (2) no sub-task is created for the comment regardless of classification path. These failures indicate that the verify-pr skill is not correctly processing suggestion-classified comments through the convention upgrade pipeline, resulting in missed sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) correctly processes all suggestion-classified comments, including those like comment 30002 where the suggestion aligns with a documented or demonstrated convention
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that Step 6b (Apply Convention Upgrades) and Step 6d (Create Sub-Tasks) correctly handle upgraded suggestions in the sub-task creation pipeline

## Implementation Notes
- The convention upgrade pipeline (Style/Conventions Check 1) must evaluate every comment classified as "suggestion" for convention upgrade eligibility -- no suggestions should bypass this evaluation
- The evaluation must include both CONVENTIONS.md lookup (Check 1a) and codebase pattern search (Check 1b) for each suggestion
- When a suggestion is upgraded to a code change request via convention match, it must flow through Step 6d sub-task creation the same way as directly-classified code change requests
- The classification reasoning output (review-N.md files) must document the convention upgrade eligibility evaluation, including whether CONVENTIONS.md was consulted and whether codebase patterns were analyzed
- Review the eval-3 test scenario to understand the specific context of comment 30002 (index suggestion) and ensure the convention upgrade pipeline handles that pattern

## Review Context
**Eval-3 failing assertions from CI eval results (review 40001 by github-actions[bot]):**

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

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, including comment 30002
- [ ] The classification reasoning output documents CONVENTIONS.md lookup and/or codebase pattern analysis for each suggestion
- [ ] Suggestions that match documented or demonstrated conventions are upgraded to code change requests
- [ ] Upgraded suggestions flow through the sub-task creation pipeline and result in Jira sub-tasks
- [ ] eval-3 assertions pass after the fix (convention upgrade evaluated, sub-task created for comment 30002)
