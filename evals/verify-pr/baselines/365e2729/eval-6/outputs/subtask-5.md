# Sub-task 5 — Add verify-pr eval coverage for Check 6 (Documentation Coverage)

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Labels:** ai-generated-jira, review-feedback
- **Link:** Blocks TC-9106

## Repository
sdlc-plugins

## Target Branch
main

## Description
TC-9106's Test Requirements ask to verify that Check 6 flags undocumented new symbols, does not flag documented ones, and returns N/A when no new symbols are present. PR #747 contains no eval fixtures or `evals/verify-pr/evals.json` changes, so none of these is verified. Add eval cases covering the three scenarios.

## Files to Modify
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new behavior (Documentation Coverage PASS, WARN and N/A)

## Files to Create
- `evals/verify-pr/files/pr-diff-doc-coverage.md` — PR diff fixture adding public symbols, some with doc comments and some without, across at least two languages
- `evals/verify-pr/files/task-doc-coverage.md` — matching task fixture

## Implementation Notes
- Start each fixture with the canonical header `<!-- SYNTHETIC TEST DATA — <purpose> -->`, per CONVENTIONS.md §Testing Conventions (Fixture documentation).
- Follow the existing case structure in `evals/verify-pr/evals.json`: prompt, input files, and assertions on `outputs/report.md`.
- The N/A scenario can reuse an existing Markdown-only diff fixture. Note that once sub-task 1 lands, Markdown `###` headings count as symbols.

## Reuse Candidates
- `evals/verify-pr/files/task-with-eval-results.md` — task fixture pattern
- `evals/verify-pr/files/pr-diff-with-eval-results.md` — Markdown-only PR diff fixture (current N/A scenario for language symbols)
- `evals/verify-pr/files/pr-reviews-with-evals.md` — review fixture pattern

## Acceptance Criteria
- [ ] An eval case asserts Documentation Coverage WARN and lists the undocumented symbols with file and line
- [ ] An eval case (or assertion) confirms documented symbols are not flagged
- [ ] An eval case asserts Documentation Coverage N/A when no new symbols are introduced
- [ ] New fixtures carry the `SYNTHETIC TEST DATA —` header

## Test Requirements
- [ ] Run the verify-pr evals and confirm the new cases pass with no regressions against `evals/verify-pr/baselines/latest/summary.md`
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes.

## Review Context
Source: verify-pr Correctness sub-agent. None of TC-9106's three Test Requirements ("Verify Check 6 correctly identifies undocumented new symbols in a diff", "Verify Check 6 does not flag symbols that already have doc comments", "Verify N/A verdict when no new symbols are present") is backed by fixtures or `evals/verify-pr/evals.json` changes in PR #747. The PR diff touches only `style-conventions.md` and `SKILL.md`.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

Add commits to the existing PR #747 head branch; do not open a new PR. The Repository Registry entry `sdlc-plugins` (path `./`) resolves to origin `RHEcosystemAppEng/sdlc-plugins`. The TC-9106 Git Pull Request field records the same PR number as `https://github.com/mrizzi/sdlc-plugins/pull/747`.

## Dependencies
- Depends on: Sub-task 4 — Wire Documentation Coverage into the live Step 6a mapping and the Step 8 report (so the verdict appears in the report the evals assert on)
