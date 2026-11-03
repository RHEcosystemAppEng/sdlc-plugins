# Sub-task: Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation for comment 30002

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Summary:** Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation for comment 30002
- **Labels:** `["ai-generated-jira", "eval-failure"]`
- **Link:** Blocks (inward: this sub-task, outward: TC-9106)

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
The CI eval run on PR #747 (`github-actions[bot]` review 40001) shows verify-pr eval-3 at 11/13 (85%), down from 15/15 (100%) at the base-branch baseline (`evals/verify-pr/baselines/latest/summary.md`). Both failures concern review comment 30002 (the index suggestion in the eval-3 fixture). The verify-pr run no longer evaluates whether that suggestion qualifies for a convention upgrade (Style/Conventions Check 1), and no sub-task outcome follows from that evaluation. Both failures are classified as **regressions**. Restore the Convention Upgrade evaluation so that every comment classified as a suggestion gets a documented convention lookup, and so the eval-3 assertions pass again.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — make sure the new Check 6 does not crowd out or replace Check 1 (Convention Upgrade). Bring the check counts in line: the Verdicts table/Output Format row count and the `## Constraints` bullet "**MUST** process all four checks" should both match the real number of checks, and Convention Upgrade must stay a required verdict row.
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — check that the Step 6a verdict mapping changes from PR #747 still route the Convention Upgrade verdict to Step 6b. Make Step 4c/6e require the per-comment classification output to record the convention-upgrade evaluation (CONVENTIONS.md lookup, codebase pattern count, performance scrutiny) for every suggestion.
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new behavior

## Implementation Notes
- Check 1 in `style-conventions.md` (sub-steps 1a–1d) is the logic that went missing in the eval-3 output: `review-30002.md` classified the comment as a suggestion but recorded no CONVENTIONS.md lookup or codebase pattern analysis.
- PR #747 changed the Output Format from "exactly five rows" to "exactly six rows" but left the Constraints section saying "all four checks". Fix these mismatched counts first, since they make it easier for the sub-agent to skip a check.
- Compare with the baseline output `evals/verify-pr/baselines/latest/eval-3/outputs/review-30002.md`, which has a `### Convention Upgrade Eligibility` section with the three Check 1 sub-checks and an explicit upgrade decision. That is the expected behavior.
- **Conflicting assertion.** The failing assertion "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path" contradicts the baseline assertion "Review comment 30002 (index suggestion) does NOT result in a sub-task … no project convention in the fixture data backs an upgrade" (`evals/verify-pr/baselines/latest/eval-3/grading.json`). Before changing skill behavior, decide which expectation is correct for the eval-3 fixture data (`evals/verify-pr/files/pr-review-comments.md`, `evals/verify-pr/files/repo-backend.md`), then align `evals/verify-pr/evals.json` and the skill. Do not make the skill create sub-tasks for unsupported suggestions just to satisfy a contradictory assertion.
- Run the verify-pr evals and compare against `evals/verify-pr/baselines/latest/` before pushing.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 1 — Convention Upgrade` — existing upgrade logic (1a–1d) that must keep running
- `evals/verify-pr/baselines/latest/eval-3/outputs/review-30002.md` — reference classification output with a complete Convention Upgrade Eligibility section
- `evals/verify-pr/files/task-with-reviews.md` — eval-3 task fixture
- `evals/verify-pr/files/pr-review-comments.md` — eval-3 review comments fixture containing comment 30002
- `evals/verify-pr/files/pr-diff-with-reviews.md` — eval-3 PR diff fixture

## Acceptance Criteria
- [ ] For every review comment classified as a suggestion, verify-pr records a convention-upgrade evaluation (CONVENTIONS.md lookup, codebase pattern analysis, performance scrutiny) in the classification output or the Style/Conventions findings
- [ ] For comment 30002 in eval-3, the sub-task outcome matches the convention-upgrade decision and the reconciled eval assertion
- [ ] The check counts in `style-conventions.md` (Output Format row count, Constraints "process all N checks") match the real number of checks
- [ ] The conflict between the PR-run eval-3 assertion and the baseline assertion about a sub-task for comment 30002 is resolved in `evals/verify-pr/evals.json`
- [ ] verify-pr eval-3 passes all assertions (no regressions against `evals/verify-pr/baselines/latest/`)

## Test Requirements
- [ ] Re-run verify-pr eval-3 and confirm all assertions pass
- [ ] Re-run the full verify-pr eval suite (eval-1 to eval-6) and confirm there are no new regressions against the baseline
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context
Source: eval result review 40001 by `github-actions[bot]` (run-evals v0.9.1), eval-3: 11/13 passed (85%).

Failing assertions (both classified **regression**: baseline `evals/verify-pr/baselines/latest/` has eval-3 at 15/15):

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
   **Classification:** regression (the identical assertion passed at baseline)

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
   **Classification:** regression (this assertion text has no baseline counterpart, so it is treated as new by the conservative default; the related baseline assertion about sub-task creation for 30002 passed)
