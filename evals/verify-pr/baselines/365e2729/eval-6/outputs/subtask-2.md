# Sub-task 2 — Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Labels:** ai-generated-jira, eval-failure
- **Link:** Blocks TC-9106

## Repository
sdlc-plugins

## Target Branch
main

## Description
The CI eval run on PR #747 (review 40001, run-evals) reports eval-3 for verify-pr at 11/13 (85%). Two assertions fail, both about review comment 30002 (the index suggestion in the eval-3 fixture). Both are classified as **regression** against `evals/verify-pr/baselines/latest/`:
- The convention-upgrade-eligibility assertion passed at baseline (`baselines/latest/eval-3/grading.json`).
- The sub-task-creation assertion has no matching baseline entry. The baseline holds the opposite assertion ("30002 does NOT result in a sub-task"), which passed. By the conservative default this counts as a regression.

Restore eval-3 so verify-pr's run on the eval-3 fixture records the Style/Conventions Check 1 convention-upgrade analysis for comment 30002 in `review-30002.md`, and so the outcome for 30002 matches the current eval-3 assertion set. Also reconcile the conflict between the PR-run assertion ("results in a sub-task regardless of classification path") and the baseline assertion ("does NOT result in a sub-task").

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — make sure Step 4c/6b/6e classification output for each suggestion carries the Style/Conventions Check 1 convention-upgrade evaluation, including when no upgrade happens
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — confirm Check 1 still emits per-suggestion evidence (CONVENTIONS.md lookup and counted codebase pattern) next to the new Check 6
- `evals/verify-pr/evals.json` — reconcile the eval-3 assertions for comment 30002 (sub-task vs. no sub-task) so the expected outcome is unambiguous and matches the eval-3 fixtures

## Implementation Notes
- Failing eval: `eval-3` in `evals/verify-pr/evals.json`. Its fixtures are under `evals/verify-pr/files/`.
- Baseline outputs to compare against: `evals/verify-pr/baselines/latest/eval-3/outputs/review-30002.md`. At baseline this file had a "Convention upgrade check (Style/Conventions Check 1)" section, which is missing in the PR run.
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` Check 1 (1a–1d) defines the evidence each suggestion must carry. SKILL.md Step 6b/6e defines how that evidence reaches replies.
- Find out whether the regression is caused by the PR's changes to `style-conventions.md`/`SKILL.md`, for example the extra check diluting the Check 1 instructions, or by the changed eval-3 assertion. Fix whichever one it is.
- Run the verify-pr evals locally (`/sdlc-workflow:run-evals`) and compare with `evals/verify-pr/baselines/latest/summary.md` before pushing.

## Reuse Candidates
- `evals/verify-pr/baselines/latest/eval-3/outputs/review-30002.md` — passing reference output that includes the convention-upgrade analysis
- `evals/verify-pr/baselines/latest/eval-3/grading.json` — baseline assertion results for eval-3 (15/15 passing)
- `evals/verify-pr/baselines/latest/summary.md` — baseline per-eval pass rates

## Acceptance Criteria
- [ ] eval-3 passes all assertions on the PR branch (no failures for comment 30002)
- [ ] `review-30002.md` produced by eval-3 documents the convention-upgrade eligibility evaluation (CONVENTIONS.md lookup and codebase pattern analysis)
- [ ] The outcome for comment 30002 (sub-task or not) matches a single, consistent eval-3 assertion in `evals/verify-pr/evals.json`
- [ ] No other verify-pr eval drops below its baseline pass rate

## Test Requirements
- [ ] Re-run the verify-pr evals and confirm eval-3 reaches 100% with no regressions in eval-1, eval-2, eval-4, eval-5 or eval-6
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes.

## Review Context
Eval result review 40001 (github-actions[bot], run-evals v0.9.1), eval-3: 2 failing assertions, both classified **regression**.

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
  **Baseline classification:** regression (passed at baseline)

- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
  **Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
  **Baseline classification:** regression (no matching baseline assertion; conservative default)

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

Add commits to the existing PR #747 head branch; do not open a new PR. The Repository Registry entry `sdlc-plugins` (path `./`) resolves to origin `RHEcosystemAppEng/sdlc-plugins`. The TC-9106 Git Pull Request field records the same PR number as `https://github.com/mrizzi/sdlc-plugins/pull/747`.

## Dependencies
- Depends on: TC-9106 — Add documentation coverage check to style-conventions sub-agent (this sub-task amends its PR)
