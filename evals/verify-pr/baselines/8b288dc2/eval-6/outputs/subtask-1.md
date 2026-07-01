## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two failing eval assertions in eval-3 for the verify-pr skill. The eval results from PR #747 show that eval-3 has an 85% pass rate (11/13) with 2 failing assertions related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The verify-pr skill must evaluate convention upgrade eligibility for suggestion-type review comments and create sub-tasks when appropriate.

## Review Context

This sub-task originates from eval failures detected in the CI eval run on PR #747.

**Failing Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

Evidence: "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

Evidence: "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- update review comment classification logic to include convention upgrade eligibility evaluation for suggestion-type comments
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Style/Conventions analysis documents convention upgrade evaluation when applicable

## Implementation Notes
- When a review comment is classified as a "suggestion," the verify-pr skill must additionally evaluate whether the suggestion aligns with a documented project convention (e.g., in CONVENTIONS.md) or a demonstrated codebase pattern
- If convention upgrade eligibility is confirmed, the suggestion should be elevated to a code change request, and a sub-task must be created
- The classification reasoning output (review-N.md) must document the convention upgrade evaluation, including what conventions or patterns were checked
- Reference the existing review comment classification flow in SKILL.md to understand where convention upgrade evaluation should be inserted

## Acceptance Criteria
- [ ] When a review comment is classified as a suggestion, the classification reasoning documents whether convention upgrade eligibility was evaluated
- [ ] Convention upgrade evaluation checks for matching patterns in CONVENTIONS.md or demonstrated codebase conventions
- [ ] If a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request and a sub-task is created
- [ ] eval-3 passes with 13/13 assertions (100% pass rate) after the fix
