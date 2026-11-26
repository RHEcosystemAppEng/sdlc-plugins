# Sub-task 1 — Add Markdown section-introduction rule to Check 6 (Documentation Coverage)

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Labels:** ai-generated-jira, review-feedback
- **Link:** Blocks TC-9106

## Repository
sdlc-plugins

## Target Branch
main

## Description
Check 6 (Documentation Coverage) in the verify-pr Style/Conventions sub-agent skips Markdown files ("Markdown: not applicable — skip Markdown files"). sdlc-plugins is a Markdown-first repository where skills are defined in Markdown, so the check returns N/A for almost every PR here. Replace the Markdown exclusion with a Markdown-specific rule: every new `###` heading added in the PR must have at least one paragraph of explanatory text before any sub-section (`####`) or code block. A new `###` heading with no introductory paragraph counts as an undocumented symbol for the verdict.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — in Check 6: replace the "Markdown: not applicable" bullet in 6b with a Markdown section-introduction rule, extend 6a so new `###` headings in `.md` files count as new symbols, and make the 6c verdict/evidence cover undocumented headings
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new behavior

## Implementation Notes
- Follow the structure of Checks 1–5 in `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. Each `### Check N` heading there opens with an introductory paragraph before its `####` sub-sections (12/12 `### Check N` headings across `style-conventions.md`, `correctness.md`, `intent-alignment.md` and `security.md`). That is the pattern the new rule enforces.
- A new heading is a `+### ` line in a `.md` file with no matching `-` line, using the same "new" definition as 6a.
- "Has introductory text" means: the first non-blank line after the heading is prose. It is not another heading (`#`), a code fence (a line starting with three backticks), a table row (`|`) or a list item.
- Evidence format matches 6c: file path, line number and heading text for each heading without an introductory paragraph.
- Keep the existing language rules (Rust, TS/Java, Python, Go) unchanged.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 3 — Test Documentation` — the existing per-language doc-comment rule list and flag-missing pattern
- `evals/verify-pr/files/pr-diff-with-eval-results.md` — example fixture of a Markdown-only PR diff that adds a `###` section
- `evals/verify-pr/files/pr-reviews-with-evals.md` — example review fixture with an inline review comment

## Acceptance Criteria
- [ ] Check 6b no longer skips Markdown files; it defines a Markdown rule for new `###` headings
- [ ] A new `###` heading followed directly by a sub-section, code block, table or list (no prose paragraph) is recorded as undocumented and contributes to WARN
- [ ] A new `###` heading followed by at least one paragraph of explanatory text is recorded as documented
- [ ] Check 6a counts new `###` headings in `.md` files as new symbols, so a Markdown-only PR that adds sections no longer yields N/A

## Test Requirements
- [ ] Verify a diff adding a `###` heading with no introductory paragraph yields a WARN that cites the heading's file and line
- [ ] Verify a diff adding a `###` heading with an introductory paragraph is not flagged
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes.

## Review Context
- **Reviewer:** reviewer-b, comment 50001 (review 40002, CHANGES_REQUESTED)
- **Location:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310
- **Comment:** "The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

Add commits to the existing PR #747 head branch; do not open a new PR. The Repository Registry entry `sdlc-plugins` (path `./`) resolves to origin `RHEcosystemAppEng/sdlc-plugins`. The TC-9106 Git Pull Request field records the same PR number as `https://github.com/mrizzi/sdlc-plugins/pull/747`.

## Dependencies
- Depends on: TC-9106 — Add documentation coverage check to style-conventions sub-agent (this sub-task amends its PR)
