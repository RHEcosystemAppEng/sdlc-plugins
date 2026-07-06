## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility
evaluation and sub-task creation for review comments classified as suggestions.
Two assertions in eval-3 fail because the verify-pr implementation does not
evaluate convention upgrade eligibility for suggestions (review comment 30002)
and consequently does not create a sub-task when the suggestion should have been
elevated to a code change request via convention analysis.

The root cause is that the classification pipeline stops at the initial
classification ("suggestion") without proceeding to Check 1 of the
Style/Conventions sub-agent to evaluate whether the suggestion matches a
documented or demonstrated project convention. When convention upgrade
eligibility is not evaluated, suggestions that should be elevated to code
change requests remain as suggestions, and no sub-task is created.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) evaluation is triggered for all comments classified as suggestion, and that the classification reasoning documents the CONVENTIONS.md lookup and codebase pattern analysis
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that the orchestrator's Step 6b applies convention upgrades before sub-task creation in Step 6d, and that the pipeline does not skip upgrade evaluation for any suggestion

## Implementation Notes
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must process
  every comment classified as "suggestion" in the Classified Review Comments
  input. The current implementation appears to skip convention upgrade
  evaluation for some suggestions.
- The convention upgrade check has two paths: CONVENTIONS.md lookup (step 1a)
  and codebase pattern search (step 1b). Both paths must be attempted and
  documented in the classification reasoning output (review-N.md files).
- When a suggestion is not upgraded, the classification reasoning must still
  document that convention upgrade eligibility was evaluated and explain why
  no upgrade was warranted (e.g., "no matching convention in CONVENTIONS.md,
  no established codebase pattern found").
- When a suggestion IS upgraded via convention match, the upgraded
  classification must flow through to Step 6d sub-task creation so that a
  sub-task is created for the code change request.

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all review comments classified as suggestion
- [ ] The classification reasoning output (review-N.md) documents whether convention upgrade was attempted, including CONVENTIONS.md lookup and codebase pattern analysis results
- [ ] Suggestions that match a documented or demonstrated project convention are upgraded to code change request classification
- [ ] Upgraded suggestions result in sub-task creation in Step 6d
- [ ] eval-3 assertions pass: convention upgrade eligibility is evaluated for review comment 30002 and a sub-task is created when appropriate

## Test Requirements
- [ ] Verify that a suggestion matching a CONVENTIONS.md convention is upgraded and produces a sub-task
- [ ] Verify that a suggestion with no convention match remains a suggestion with documented upgrade evaluation reasoning
- [ ] Verify that the convention upgrade evaluation is recorded in the review classification output files

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context
This sub-task addresses eval-3 assertion failures from the CI eval results
review (github-actions[bot], review ID 40001). Two assertions failed:

**Failing Assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
- **Classification:** regression (no baseline exists for verify-pr evals)

**Failing Assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
- **Classification:** regression (no baseline exists for verify-pr evals)

**Eval metrics context:**
- eval-3 pass rate: 11/13 (85%)
- Overall eval pass rate: 91%
- Both failures relate to the same root cause: convention upgrade eligibility
  is not being evaluated for suggestions, preventing elevation to code change
  requests and subsequent sub-task creation.
