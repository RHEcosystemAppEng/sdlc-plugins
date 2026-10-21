# Sub-task 2: Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

**Type:** Eval failure sub-task
**Parent:** TC-9106
**Labels:** ai-generated-jira, eval-failure
**Source:** Eval result review from github-actions[bot] (review 40001), eval-3 failures

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two failing assertions in eval-3 of the verify-pr skill evaluation. The eval-3 scenario tests convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The current implementation fails to evaluate convention upgrade eligibility for suggestion-classified review comments and consequently does not create sub-tasks when convention upgrade would have elevated the suggestion to a code change request.

The two failing assertions indicate that:
1. Convention upgrade eligibility is not being evaluated for review comment 30002 (an index suggestion) -- the classification output does not show any CONVENTIONS.md lookup or codebase pattern analysis.
2. No sub-task is created for review comment 30002, which should result in a sub-task regardless of classification path (either directly as a code change request, or via convention upgrade from suggestion).

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) properly evaluates all suggestion-classified comments for convention upgrade eligibility, documenting the CONVENTIONS.md lookup and codebase pattern analysis in the classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that the orchestrator properly processes convention upgrade actions and creates sub-tasks for upgraded suggestions

## Implementation Notes
- Review the Convention Upgrade check (Check 1) in style-conventions.md to ensure it evaluates every suggestion-classified comment for convention upgrade eligibility
- The classification output (review-N.md files) must document whether a CONVENTIONS.md lookup or codebase pattern analysis was performed, even when no match is found
- When a suggestion is evaluated for convention upgrade, the reasoning must be explicit about what was checked: (1) CONVENTIONS.md sections searched, (2) codebase patterns counted, (3) why the suggestion was or was not upgraded
- Ensure the orchestrator in SKILL.md Step 6b properly processes upgrade-comment actions from the Style/Conventions sub-agent and creates sub-tasks for upgraded suggestions in Step 6d

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments
- [ ] The classification output documents the CONVENTIONS.md lookup and codebase pattern analysis for each suggestion
- [ ] When convention upgrade elevates a suggestion to a code change request, a sub-task is created
- [ ] eval-3 assertions pass on re-run

## Review Context
**Source:** Eval result review from github-actions[bot]
**Eval ID:** eval-3
**Pass rate:** 85% (11/13 assertions passed, 2 failed)

**Failing assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
