# Sub-task 2 (eval failure)

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Summary:** Fix eval-3 assertion failures: convention upgrade eligibility evaluation, sub-task creation for comment 30002
- **Labels:** `["ai-generated-jira", "eval-failure"]`
- **Link:** Blocks, sub-task (inward) to TC-9106 (outward)

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
The CI eval run on PR #747 shows 2 failing assertions in verify-pr eval-3 (11/13, 85%). Both failures are about review comment 30002 (the index suggestion). The verify-pr output classified 30002 as a suggestion, but it did not record a convention-upgrade eligibility evaluation (no CONVENTIONS.md lookup and no counted codebase pattern), so no sub-task was created. The baseline (`evals/verify-pr/baselines/latest/eval-3/grading.json`, 15/15) passes the convention-upgrade-eligibility assertion, so these failures are classified as **regressions** introduced on the PR branch. Restore the behavior: every comment classified as a suggestion must go through Style/Conventions Check 1 convention-upgrade evaluation, and the result (upgraded or not, with evidence) must appear in the classification reasoning and the report. When the evaluation finds a matching documented or demonstrated convention, the suggestion must be upgraded and a sub-task created.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — make sure Check 1 (Convention Upgrade) always records, for each suggestion, the CONVENTIONS.md lookup result and the codebase-pattern count, even when the decision is "not upgraded". Confirm the Check 6 / Output Format edits in this PR did not displace or shorten Check 1's instructions or evidence requirements
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — in Step 4c / Step 6b / Step 6e, require that classification reasoning for every suggestion includes the Check 1 convention-upgrade evaluation result, and that upgraded suggestions proceed to Step 6d sub-task creation
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new behavior

## Implementation Notes
- Check 1 sub-steps 1a–1d in `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` define the upgrade logic. Its Verdict block already requires "Evidence: list each suggestion examined, whether it was upgraded, and the evidence supporting the decision". Make the orchestrator carry that evidence into the per-comment classification output (`review-<id>.md` in evals, PR reply in production).
- Step 6b in `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` applies `upgrade-comment` actions before Steps 6c–6d. Check that the eval-3 run produced (or should have produced) an `upgrade-comment` action for 30002, given the fixture's conventions (`evals/verify-pr/files/repo-backend.md`, `evals/verify-pr/files/pr-review-comments.md`).
- The failing assertion "results in a sub-task regardless of classification path" differs from the baseline assertion for 30002 ("does NOT result in a sub-task"). Before changing skill behavior, reconcile the intended outcome for 30002 with the eval-3 fixture's conventions, so the skill and the assertions agree.
- Do not upgrade on general best practice. Evidence must cite a CONVENTIONS.md section or a counted codebase pattern (Check 1d).

## Reuse Candidates
- `evals/verify-pr/files/task-with-reviews.md` — eval-3 task fixture
- `evals/verify-pr/files/pr-review-comments.md` — eval-3 review comments, including 30002 (index suggestion)
- `evals/verify-pr/files/repo-backend.md` — repository context used to judge convention evidence for 30002
- `evals/verify-pr/baselines/latest/eval-3/grading.json` — baseline grading showing the convention-upgrade-eligibility assertion passing

## Acceptance Criteria
- [ ] For every comment classified as suggestion, the classification output documents the convention-upgrade evaluation: the CONVENTIONS.md lookup result and the codebase pattern count
- [ ] Comment 30002 in eval-3 gets a sub-task when the convention evaluation supports an upgrade (or it is classified directly as a code change request), matching the reconciled eval-3 assertion
- [ ] eval-3 passes 13/13 on the PR branch
- [ ] No regressions in eval-1, eval-2, eval-4, eval-5, eval-6

## Test Requirements
- [ ] Re-run `/sdlc-workflow:run-evals` for verify-pr and confirm eval-3 passes all assertions
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes

## Review Context
Eval result review 40001 (github-actions[bot], `## Eval Results`, footer `sdlc-workflow/run-evals` v0.9.1). Failing assertions in eval-3 (11/13), both classified **regression** against `evals/verify-pr/baselines/latest/` (baseline eval-3: 15/15):

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
   **Classification:** regression (passes at baseline)

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
   **Classification:** regression (no matching passing or failing baseline assertion; conservative default)

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
