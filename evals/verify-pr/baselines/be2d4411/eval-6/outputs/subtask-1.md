## Repository
sdlc-plugins

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. Two assertions fail in eval-3 at 85% pass rate (11/13 passed, 2 failed):

1. Convention upgrade eligibility is not being evaluated for suggestion-classified review comments -- the classification reasoning does not document any CONVENTIONS.md lookup or codebase pattern analysis.
2. Review comments that should result in sub-tasks (whether through direct code change request classification or through convention upgrade from suggestion) are not producing sub-tasks when the convention upgrade path is the expected route.

The root cause is that the verify-pr skill's classification pipeline does not consistently evaluate convention upgrade eligibility for suggestions, and when convention upgrade is skipped, no sub-task is created for comments that should be elevated.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) evaluation is consistently applied and documented in classification reasoning for all suggestion-classified comments
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 4c classification and Step 6b convention upgrade flow ensure sub-task creation for upgraded suggestions

## Implementation Notes
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must evaluate every suggestion-classified comment for convention upgrade eligibility, documenting the CONVENTIONS.md lookup and/or codebase pattern analysis in the classification reasoning output
- When a suggestion is upgraded to a code change request via convention analysis, the orchestrator's Step 6d must create a sub-task for it
- The classification output file (review-N.md) must explicitly state whether convention upgrade eligibility was evaluated and what evidence was found (or not found)
- Review the existing Check 1a (Check CONVENTIONS.md), 1b (Check Codebase Patterns), and 1d (Upgrade Decision) steps to ensure they run for every suggestion, not just those with obvious convention matches

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every review comment classified as suggestion, with documented reasoning in the classification output
- [ ] When convention upgrade analysis finds a matching convention, the suggestion is upgraded to code change request and a sub-task is created
- [ ] The classification reasoning output explicitly documents whether CONVENTIONS.md was checked and whether codebase pattern analysis was performed
- [ ] eval-3 assertions about convention upgrade eligibility and sub-task creation pass

## Review Context

The following assertions from the eval-3 eval run (posted by CI via sdlc-workflow/run-evals) failed:

**Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence 1:**
> "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence 2:**
> "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

These failures indicate that the convention upgrade pipeline (Style/Conventions Check 1) is not being invoked or documented for suggestion-classified comments, and the resulting lack of upgrade prevents sub-task creation for comments that match project conventions.
