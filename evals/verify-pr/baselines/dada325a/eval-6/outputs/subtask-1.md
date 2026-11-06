# Sub-task 1: Replace Markdown exclusion in Check 6 with a Markdown section-introduction rule

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Summary:** Replace Markdown exclusion in Documentation Coverage check with a rule requiring introductory text for new `###` headings
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Link:** this sub-task **Blocks** TC-9106

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
The Documentation Coverage check (Check 6) added to the Style/Conventions sub-agent in PR #747 skips Markdown files completely ("**Markdown:** not applicable — skip Markdown files"). sdlc-plugins is a documentation-first repository: skills are defined in Markdown (`SKILL.md` and sibling sub-agent files). With this exclusion, Check 6 returns N/A on nearly every PR in the repository. Replace the exclusion with a Markdown-specific rule: every new `###` heading must have at least one paragraph of explanatory text before any sub-section heading or code block. This brings documentation coverage to the repository's main format.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — in Check 6: extend 6a so new `###` headings in Markdown files count as new documentable items; replace the "Markdown: not applicable" bullet in 6b with the introductory-paragraph rule; make sure the 6c verdict/evidence wording covers Markdown headings (file path + line of the heading)
- `evals/verify-pr/evals.json` — add or update eval assertions to cover the new Markdown rule

## Implementation Notes
- The rule to change is the bullet `- **Markdown:** not applicable — skip Markdown files` in `#### 6b — Check Documentation Comments` of Check 6 in `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`.
- Proposed rule: a new `###` heading (an added `+` line starting with `### ` and no matching `-` line, using the same "new" definition as 6a) is **documented** when at least one non-empty paragraph line comes after it, before the next heading (`#`–`######`) or the opening of a fenced code block (```` ``` ````). Otherwise it is **undocumented**.
- Follow the pattern in `style-conventions.md`: each `### Check N — <name>` section opens with an explanatory paragraph before its `#### Na` sub-steps. Check 1 ("Before finalizing any comment classified as **suggestion**..."), Check 2 ("Scan test files in the PR for repetitive test functions...") and the new Check 6 ("Verify that new public symbols introduced in the PR...") all show it. The new rule should formalize this existing pattern.
- Keep the PASS/WARN/N/A semantics from 6c. Undocumented Markdown headings count toward WARN just like undocumented code symbols. N/A applies only when there are no new code symbols **and** no new `###` headings.
- Keep the Check 6 structure consistent with Checks 1–5 (`#### 6a`/`6b`/`6c` sub-steps, then a Verdict list and an Evidence line).
- CONVENTIONS.md lists "Primary format: Markdown documentation". Mention this when explaining why Markdown is in scope.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 3 — Test Documentation` — existing per-language doc-comment list that Check 6b mirrors
- `evals/verify-pr/files/pr-diff-with-eval-results.md` — PR diff fixture that contains Check 6 and the Markdown exclusion line
- `evals/verify-pr/files/pr-reviews-with-evals.md` — review fixture with reviewer-b's comment 50001 asking for this change
- `evals/verify-pr/files/task-with-eval-results.md` — task fixture for TC-9106 (Documentation Coverage check)

## Acceptance Criteria
- [ ] Check 6b no longer says Markdown files are "not applicable" or skipped
- [ ] Check 6a/6b treat new `###` headings in Markdown files as items needing documentation
- [ ] A new `###` heading with at least one paragraph of explanatory text before any sub-section or code block is classified as documented
- [ ] A new `###` heading followed directly by a sub-heading or code block is classified as undocumented and causes WARN
- [ ] Check 6 returns N/A only when the PR adds no new code symbols and no new `###` headings
- [ ] WARN evidence lists undocumented Markdown headings with file path and line number

## Test Requirements
- [ ] Verify that a diff adding a `###` heading followed directly by a `####` heading or code block is flagged as undocumented
- [ ] Verify that a diff adding a `###` heading followed by an explanatory paragraph is not flagged
- [ ] Verify that a Markdown-only diff with no new `###` headings gives N/A
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the behavior changes introduced by this task. Add new eval cases if existing cases do not exercise the modified behavior, or update assertions on existing cases if their expected output changes.

## Review Context
- **Reviewer:** reviewer-b (review 40002, state `CHANGES_REQUESTED`)
- **Comment ID:** 50001
- **File/line:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT)
- **Original comment:**
  > The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
