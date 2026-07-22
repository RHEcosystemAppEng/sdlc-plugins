## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. Two regression assertions failed in eval-3:

1. Convention upgrade eligibility is not being evaluated for suggestion-classified review comments -- the classification output does not document any CONVENTIONS.md lookup or codebase pattern analysis.
2. Review comments that should result in sub-tasks (whether classified directly as code change requests or upgraded from suggestions via convention analysis) are not producing sub-tasks when the convention upgrade path is the expected route.

The root cause is that the verify-pr skill's convention upgrade pipeline (Style/Conventions sub-agent Check 1) is not being triggered or is not producing the expected upgrade-comment actions for comments that match documented or demonstrated project conventions. This results in suggestion-classified comments remaining as suggestions without convention analysis, and consequently no sub-tasks being created for them.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- review and strengthen the convention upgrade logic in Check 1 (steps 1a-1d) to ensure convention eligibility is evaluated and documented for every suggestion-classified comment
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- review Step 6b (Apply Convention Upgrades) to ensure upgrade-comment actions from the Style/Conventions sub-agent are correctly processed and result in sub-task creation

## Review Context
The following eval assertions failed in eval-3 with evidence from the CI eval run:

**Assertion 1:**
- **Text:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
- **Text:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Implementation Notes
- The convention upgrade pipeline in the Style/Conventions sub-agent (Check 1, steps 1a-1d) must evaluate every suggestion-classified comment for convention eligibility
- The classification output (review-N.md files) must document the convention analysis reasoning, including whether CONVENTIONS.md was consulted and whether codebase patterns were searched
- When a suggestion matches a convention (documented in CONVENTIONS.md or demonstrated by codebase patterns), the upgrade-comment action must be emitted so the orchestrator (Step 6b) can reclassify and create sub-tasks
- Follow the existing convention upgrade evidence format: cite the CONVENTIONS.md section or counted codebase pattern

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every suggestion-classified review comment
- [ ] Classification output documents the convention analysis (CONVENTIONS.md lookup and/or codebase pattern search)
- [ ] Suggestions matching documented or demonstrated conventions are upgraded to code change requests via upgrade-comment actions
- [ ] Upgraded suggestions result in sub-task creation through the orchestrator's Step 6b pipeline
- [ ] eval-3 assertions pass on re-run

## Test Requirements
- [ ] Verify convention upgrade evaluation is documented in review classification output for suggestion-classified comments
- [ ] Verify sub-task creation occurs for convention-upgraded suggestions
- [ ] Verify eval-3 passes with 13/13 assertions after the fix
