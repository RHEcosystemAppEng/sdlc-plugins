## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix the convention upgrade eligibility evaluation in the verify-pr skill's review comment classification pipeline. Currently, when a review comment is classified as a "suggestion," the pipeline does not evaluate whether the suggestion aligns with a documented project convention (from CONVENTIONS.md or demonstrated codebase patterns). If a match is found, the suggestion should be upgraded to a code change request, triggering sub-task creation. This gap caused two eval-3 assertion failures where review comment 30002 (an index suggestion) was classified as a suggestion without convention upgrade evaluation, and no sub-task was created.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — add convention upgrade eligibility step to the review comment classification pipeline, after initial classification and before sub-task creation decision
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — document the convention upgrade evaluation in the Style/Conventions analysis output format

## Implementation Notes
- After a review comment is classified as a "suggestion," add a convention upgrade step that:
  1. Looks up the project's CONVENTIONS.md (if it exists) for matching convention rules
  2. Searches the codebase for demonstrated patterns that align with the suggestion
  3. If a match is found, upgrades the classification from "suggestion" to "code change request"
  4. Documents the convention lookup result in the review classification output (review-N.md)
- The convention upgrade evaluation must be recorded in the classification reasoning regardless of outcome (match found or no match) so that eval assertions can verify it was attempted
- If upgraded to code change request, a sub-task must be created following the standard sub-task creation path
- Follow existing review comment classification patterns in SKILL.md Step 4

## Acceptance Criteria
- [ ] When a review comment is classified as a suggestion, convention upgrade eligibility is evaluated
- [ ] The review classification output (review-N.md) documents the convention upgrade evaluation, including CONVENTIONS.md lookup or codebase pattern analysis
- [ ] If the suggestion matches a documented or demonstrated convention, it is upgraded to a code change request
- [ ] Upgraded suggestions result in sub-task creation
- [ ] The convention upgrade evaluation is documented regardless of whether a match is found (both positive and negative results are recorded)

## Test Requirements
- [ ] Eval-3 assertion "Convention upgrade eligibility is evaluated for review comment 30002" passes
- [ ] Eval-3 assertion "Review comment 30002 results in a sub-task regardless of classification path" passes
- [ ] Verify convention upgrade does not affect comments already classified as code change requests
- [ ] Verify convention upgrade does not affect comments classified as praise or questions

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Review Context
**Source**: eval-3 failing assertions (2 of 13 assertions failed, 85% pass rate)

**Failing Assertion 1**: "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence**: "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2**: "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence**: "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
