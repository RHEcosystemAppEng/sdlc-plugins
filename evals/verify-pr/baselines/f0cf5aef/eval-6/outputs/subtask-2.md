## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility
evaluation and sub-task creation for review comment 30002. Two assertions fail:
(1) the verify-pr skill does not evaluate convention upgrade eligibility for
suggestion-classified review comments, and (2) review comment 30002 does not
result in a sub-task because the suggestion was not elevated to a code change
request via convention analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure the
  Convention Upgrade check (Check 1) properly evaluates all suggestion-classified
  comments for convention upgrade eligibility, including CONVENTIONS.md lookup
  and codebase pattern analysis
- `evals/verify-pr/evals.json` -- update eval assertions if the expected behavior
  needs to be clarified or if fixture data needs adjustment

## Implementation Notes
- The root cause is that the convention upgrade pipeline (Check 1 in
  style-conventions.md) is not being triggered or not producing sufficient
  output for suggestion-classified review comments
- The eval expects that when a review comment is classified as "suggestion",
  the style-conventions sub-agent evaluates whether the suggestion matches a
  documented or demonstrated project convention (CONVENTIONS.md lookup or
  codebase pattern analysis)
- If a convention match is found, the suggestion should be upgraded to a code
  change request, which then triggers sub-task creation
- Review the existing convention upgrade steps (1a through 1d) to verify they
  are being followed completely -- the eval evidence indicates that convention
  upgrade eligibility was not evaluated at all, not that it was evaluated and
  rejected
- The classification reasoning output (review-30002.md) should document the
  convention upgrade analysis even when no match is found

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for review comment 30002
      (index suggestion) -- the review classification output explains whether
      the suggestion matches a documented or demonstrated project convention
- [ ] Review comment 30002 results in a sub-task -- either classified directly
      as code change request based on reviewer language, or upgraded from
      suggestion via convention analysis
- [ ] The convention upgrade analysis is documented in the classification
      reasoning output

## Test Requirements
- [ ] Verify that suggestion-classified comments trigger convention upgrade
      evaluation (CONVENTIONS.md lookup and codebase pattern analysis)
- [ ] Verify that convention-matched suggestions are upgraded to code change
      requests and result in sub-task creation
- [ ] Verify eval-3 passes with the fixes applied

## Review Context
- **Source:** Eval result review from github-actions[bot] (review 40001)
- **Eval ID:** eval-3
- **Failing assertions:**
  1. "Convention upgrade eligibility is evaluated for review comment 30002
     (index suggestion) -- the review classification output (review-30002.md)
     or the report's Style/Conventions analysis explains whether the suggestion
     matches a documented or demonstrated project convention"
     Evidence: "The output file review-30002.md classifies the comment as a
     suggestion but does not evaluate convention upgrade eligibility -- no
     CONVENTIONS.md lookup or codebase pattern analysis is documented in the
     classification reasoning"
  2. "Review comment 30002 (index suggestion) results in a sub-task regardless
     of classification path -- whether classified directly as code change
     request based on reviewer language, or upgraded from suggestion via
     convention analysis"
     Evidence: "No sub-task was created for review comment 30002 -- it was
     classified as suggestion and no convention upgrade was attempted, so the
     suggestion was not elevated to a code change request"
- **Baseline classification:** regression (no prior baseline available;
  conservative default)

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
