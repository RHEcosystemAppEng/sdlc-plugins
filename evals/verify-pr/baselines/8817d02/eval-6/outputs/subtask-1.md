## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. Two assertions fail because the verify-pr skill does not evaluate convention upgrade eligibility for suggestion-classified comments and does not create sub-tasks when convention analysis would elevate a suggestion to a code change request.

The first failing assertion requires that convention upgrade eligibility is evaluated for review comments classified as suggestions — the classification output or report must document whether the suggestion matches a documented or demonstrated project convention (CONVENTIONS.md lookup or codebase pattern analysis).

The second failing assertion requires that review comments eligible for convention upgrade result in a sub-task — either classified directly as a code change request or upgraded from suggestion via convention analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — ensure Check 1 (Convention Upgrade) evaluates all suggestion-classified comments for convention upgrade eligibility and documents the analysis in classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — ensure Step 6b (Apply Convention Upgrades) processes upgrade-comment actions and creates sub-tasks for upgraded suggestions

## Implementation Notes
- The convention upgrade pipeline (Check 1 in style-conventions.md) must evaluate every suggestion-classified comment against CONVENTIONS.md and codebase patterns
- The classification output for each suggestion must document whether convention upgrade eligibility was evaluated, including the evidence (convention section match or codebase pattern count)
- When a suggestion matches a convention, the upgrade-comment action must be produced so the orchestrator's Step 6b can upgrade the classification and Step 6d can create a sub-task
- Review the existing Check 1 steps (1a through 1d) in style-conventions.md to ensure the upgrade decision pipeline covers all suggestion-classified comments without skipping any

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every review comment classified as a suggestion
- [ ] The classification reasoning output documents the CONVENTIONS.md lookup or codebase pattern analysis for each suggestion
- [ ] Suggestions that match a documented or demonstrated convention are upgraded to code change requests via upgrade-comment actions
- [ ] Upgraded suggestions result in sub-task creation through the standard Step 6d pipeline

## Test Requirements
- [ ] Verify that a suggestion matching a CONVENTIONS.md pattern is upgraded and results in a sub-task
- [ ] Verify that a suggestion not matching any convention remains classified as a suggestion with documented reasoning
- [ ] Verify that the classification output includes convention upgrade eligibility analysis

## Review Context

The following eval assertions failed in the CI eval run, indicating regressions in convention upgrade handling:

**Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence 1:**
> "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence 2:**
> "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

Source: eval-3 (2 of 13 assertions failing, 85% pass rate)

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
