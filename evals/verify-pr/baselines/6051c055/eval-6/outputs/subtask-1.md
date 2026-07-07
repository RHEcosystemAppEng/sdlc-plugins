# Sub-Task: Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

**Summary:** Fix eval-3 assertion failures: convention upgrade eligibility evaluation and sub-task creation for suggestions
**Labels:** ai-generated-jira, eval-failure
**Parent:** TC-9106

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two failing eval-3 assertions in the verify-pr eval suite. The eval results show that the verify-pr skill does not evaluate convention upgrade eligibility for suggestion-classified review comments and does not create sub-tasks when convention upgrade analysis would elevate a suggestion to a code change request. The style-conventions sub-agent's Check 1 (Convention Upgrade) must be invoked for all suggestion-classified comments, and its findings must flow through the upgrade pipeline to sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) processes all suggestion-classified comments and documents the convention lookup and codebase pattern analysis in its findings
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 6b (Apply Convention Upgrades) correctly processes upgrade-comment actions from the Style/Conventions sub-agent and feeds upgraded suggestions into the sub-task creation pipeline (Step 6d)
- `evals/verify-pr/evals.json` -- update eval-3 assertions if behavior expectations need adjustment after the fix

## Implementation Notes
- The convention upgrade pipeline has two stages: (1) the Style/Conventions sub-agent evaluates whether a suggestion matches a documented or demonstrated convention (Check 1), and (2) the orchestrator applies the upgrade (Step 6b) before sub-task creation (Step 6d)
- The failing assertions indicate that stage 1 is not running for suggestion-classified comments -- the sub-agent must check CONVENTIONS.md and codebase patterns for every suggestion, even if no convention match is found
- The classification output (review-N.md) must document the convention lookup reasoning so it is auditable
- Follow existing Check 1 structure in style-conventions.md: 1a (Check CONVENTIONS.md), 1b (Check Codebase Patterns), 1c (Performance-Related Scrutiny), 1d (Upgrade Decision)

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every suggestion-classified review comment, with the evaluation reasoning documented in the classification output
- [ ] When convention upgrade analysis elevates a suggestion to code change request, a sub-task is created through the standard pipeline (Step 6b -> Step 6d)
- [ ] The Style/Conventions sub-agent's Check 1 findings include CONVENTIONS.md lookup results and codebase pattern analysis for each evaluated suggestion
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the convention upgrade evaluation behavior
- [ ] Verify that suggestion-classified comments receive convention upgrade analysis in the Style/Conventions sub-agent output
- [ ] Verify that upgraded suggestions flow through to sub-task creation

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context

The following eval assertion failures from the CI eval run triggered this sub-task:

**Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Baseline classification:** regression (no baseline exists for verify-pr evals)

**Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

**Baseline classification:** regression (no baseline exists for verify-pr evals)

**Source:** eval-3 from verify-pr eval suite (pass rate: 85%, 11/13 assertions passed, 2 failed)
