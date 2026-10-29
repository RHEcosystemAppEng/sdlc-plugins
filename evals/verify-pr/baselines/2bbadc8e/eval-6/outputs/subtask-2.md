# Sub-task: Fix eval-3 assertion failures — convention upgrade eligibility and sub-task creation

**Issue Type:** Sub-task
**Parent:** TC-9106
**Labels:** ai-generated-jira, eval-failure

---

## Repository
sdlc-plugins

## Description
Fix eval-3 assertion failures from the verify-pr eval suite. Two assertions are failing at 85% pass rate: (1) convention upgrade eligibility is not evaluated for review comment 30002, and (2) review comment 30002 does not result in a sub-task. The verify-pr skill must evaluate convention upgrade eligibility for suggestions and, when a convention match is found, upgrade the suggestion to a code change request and create a sub-task.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — ensure convention upgrade analysis in Check 1 is triggered for all suggestions, including documenting the eligibility evaluation reasoning in the review classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — verify that upgraded suggestions flow through the sub-task creation pipeline in Step 6d

## Implementation Notes
- The failing assertions indicate that when review comment 30002 (an index suggestion) is classified as "suggestion", no convention upgrade eligibility is evaluated — no CONVENTIONS.md lookup or codebase pattern analysis is documented
- The fix should ensure that every comment classified as "suggestion" goes through the convention upgrade pipeline (Check 1 in style-conventions.md) and that the eligibility evaluation is documented in the classification output
- If a convention match is found, the suggestion must be upgraded to "code change request" and a sub-task must be created
- Review the convention upgrade pipeline flow: Step 4c classification → Style/Conventions sub-agent Check 1 upgrade evaluation → Step 6b apply upgrades → Step 6d create sub-tasks

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for every suggestion-classified comment
- [ ] The review classification output explains whether the suggestion matches a documented or demonstrated project convention
- [ ] When a convention match is found, the suggestion is upgraded to code change request and a sub-task is created
- [ ] Eval-3 assertions pass after the fix

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Review Context
Failing assertions from eval-3 (from github-actions[bot] eval result review):

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
