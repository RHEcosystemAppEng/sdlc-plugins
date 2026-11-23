# Sub-task 1 (eval failure)

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Summary:** Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation
- **Labels:** `ai-generated-jira`, `eval-failure`
- **Link:** Blocks → TC-9106 (inward: this sub-task, outward: TC-9106)

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
The CI eval run on PR #747 (review 40001, github-actions[bot]) reports verify-pr **eval-3 at 11/13 (85%)**, with 2 failing assertions. Both concern review comment 30002 (the index suggestion) in the eval-3 fixture. The baseline comparison (`evals/verify-pr/baselines/latest/`, where eval-3 is 15/15) classifies both failures as **regressions**.

The main regression: when verify-pr classifies a review comment as a suggestion, it no longer evaluates or records whether the suggestion qualifies for a convention upgrade (Style/Conventions Check 1 / SKILL.md Step 6b). The classification output therefore has no CONVENTIONS.md lookup and no codebase pattern analysis.

This task restores that behaviour on the PR branch. Every suggestion must get an explicit convention-upgrade evaluation, with evidence recorded in its classification reasoning. The task also reconciles the second assertion's expected outcome with the eval definition.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — make sure Check 1 (Convention Upgrade) still runs for every suggestion and reports per-comment evidence (CONVENTIONS.md sections checked, codebase pattern counts), whether or not it upgrades. The PR added Check 6, so also update stale counts: the Constraints line "MUST process all four checks" must cover all checks now defined.
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — in Step 4c / Step 6b / Step 6e, require the suggestion classification reasoning (and the reply text) to state the outcome and evidence of the convention-upgrade evaluation, so it appears in the per-comment classification output.
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new behavior, and reconcile the eval-3 assertion on 30002's sub-task outcome (see Implementation Notes).

## Implementation Notes
- Restore the behaviour that baseline `evals/verify-pr/baselines/latest/eval-3/grading.json` shows passing for the assertion "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention". Compare `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` Check 1 (sub-steps 1a CONVENTIONS.md lookup, 1b codebase pattern, 1d no-inference rule) on the PR branch against `main`. Find any instruction the PR changed or diluted.
- The PR changed the Style/Conventions Output Format ("exactly six rows") and added Check 6 after Check 5. Check that the Output Format still includes the **Convention Upgrade** row, and that the Constraints section's check count matches the checks actually defined. A stale or missing row can make the sub-agent skip Check 1.
- The second failing assertion ("Review comment 30002 (index suggestion) results in a sub-task regardless of classification path …") is **not** in the baseline. Baseline and current `evals/verify-pr/evals.json` (eval-3 `assertions` and `expected_output`) say the opposite: 30002 does NOT result in a sub-task, because no project convention in the fixture backs an upgrade. Decide which expectation is correct and make `evals.json` and the skill behaviour agree. If the current definition stands, the fix is to evaluate the upgrade explicitly and record it (assertion 1) while keeping 30002 without a sub-task.
- Follow the existing per-comment reply pattern in SKILL.md Step 6e ("For suggestions upgraded to code change requests via convention check" and "For all other classifications") so non-upgraded suggestions also explain why no convention backs an upgrade.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 1 — Convention Upgrade` — existing upgrade logic (1a–1d) to restore and reuse, not rewrite
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md::Step 6b – Apply Convention Upgrades` — orchestrator handling of `upgrade-comment` actions
- `evals/verify-pr/files/task-with-reviews.md` — eval-3 task fixture (review-feedback scenario)
- `evals/verify-pr/files/pr-review-comments.md` — eval-3 review comments fixture containing comment 30002
- `evals/verify-pr/files/pr-diff-with-reviews.md` — eval-3 PR diff fixture
- `evals/verify-pr/baselines/latest/eval-3/grading.json` — baseline grading showing the expected passing evidence

## Acceptance Criteria
- [ ] For every review comment classified as a suggestion, verify-pr's classification output records an explicit convention-upgrade evaluation (CONVENTIONS.md sections checked and codebase pattern evidence) and its outcome
- [ ] eval-3 assertion "Convention upgrade eligibility is evaluated for review comment 30002 …" passes again
- [ ] The eval-3 assertion on whether 30002 results in a sub-task is consistent between the CI eval definition, `evals/verify-pr/evals.json`, and skill behaviour, and passes
- [ ] The style-conventions Output Format and Constraints reference every defined check (no stale "four checks" count), including Convention Upgrade and Documentation Coverage
- [ ] No regression in the other verify-pr evals (eval-1, eval-2, eval-4, eval-5 stay at 100%)

## Test Requirements
- [ ] Re-run the verify-pr evals and confirm eval-3 reaches 13/13 (or the reconciled assertion count) with no new failures in other evals
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes.

## Review Context
Source: CI eval result review **40001** by `github-actions[bot]` on PR #747 (`## Eval Results`, generated by sdlc-workflow/run-evals v0.9.1).

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-3 | 11/13 | 2 | 85% |

Failing assertions (from the eval review body):

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility — no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
   **Baseline classification:** regression (passes at baseline `evals/verify-pr/baselines/latest/eval-3/grading.json`)

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path — whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 — it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
   **Baseline classification:** regression (conservative default, since the exact assertion text is absent from the baseline; the baseline has the opposite assertion, "30002 does NOT result in a sub-task", which passed)

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
