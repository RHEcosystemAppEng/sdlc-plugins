# Sub-Task: Fix eval-3 assertion failures — convention upgrade eligibility and sub-task creation

**Type:** Eval failure sub-task
**Parent:** TC-9106
**Labels:** `["ai-generated-jira", "eval-failure"]`
**Summary:** Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two failing eval assertions in eval-3 for the verify-pr skill. The failures indicate that review comment 30002 (an index suggestion) is not being evaluated for convention upgrade eligibility and is not resulting in a sub-task. The verify-pr skill should either: (a) evaluate convention upgrade eligibility for the suggestion and document the analysis in review-30002.md, or (b) classify the comment directly as a code change request based on the reviewer's language, ensuring a sub-task is created in either path.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — ensure convention upgrade logic (Check 1) evaluates all suggestions for convention eligibility, including documenting the CONVENTIONS.md lookup and codebase pattern analysis in the classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — ensure the orchestrator's Step 4c classification and Step 6b convention upgrade pipeline processes all suggestions through upgrade eligibility, and that upgraded suggestions result in sub-task creation in Step 6d

## Implementation Notes
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must evaluate every comment classified as "suggestion" for convention upgrade eligibility
- The classification output file (review-N.md) must document whether a CONVENTIONS.md lookup or codebase pattern analysis was performed, even when no match is found
- If a suggestion is upgraded to a code change request via convention analysis, a sub-task must be created in Step 6d
- If the reviewer's language is sufficiently directive (e.g., "this should..."), consider whether Step 4c should classify it directly as a code change request rather than a suggestion
- Review the eval-3 test case to understand the expected behavior for comment 30002

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention
- [ ] Review comment 30002 results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis

## Test Requirements
- [ ] Verify that the convention upgrade check (Check 1) processes all suggestions and documents the analysis
- [ ] Verify that upgraded suggestions result in sub-task creation
- [ ] Verify that the classification output includes convention eligibility reasoning

## Review Context
The following eval assertions failed in eval-3 (2 failures at 85% pass rate):

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
