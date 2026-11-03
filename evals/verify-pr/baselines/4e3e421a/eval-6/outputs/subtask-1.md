# Sub-task: Add Markdown section-introduction rule to Check 6 Documentation Coverage

- **Issue Type:** Sub-task
- **Parent:** TC-9106
- **Summary:** Add Markdown section-introduction rule to Check 6 Documentation Coverage
- **Labels:** `["ai-generated-jira", "review-feedback"]`
- **Link:** Blocks (inward: this sub-task, outward: TC-9106)

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Check 6 (Documentation Coverage) in the verify-pr Style/Conventions sub-agent skips Markdown files entirely ("Markdown: not applicable — skip Markdown files"). In sdlc-plugins, skills, sub-agent instructions and docs are all Markdown, so the check returns N/A on almost every PR to this repository. Replace the blanket exclusion with a Markdown rule: every newly added `###` heading must have at least one paragraph of explanatory text before any sub-heading or fenced code block. A new heading without that paragraph counts as an undocumented symbol and feeds the existing PASS/WARN/N/A verdict.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — in Check 6: add new Markdown `###` headings to the symbols 6a looks for, replace the "Markdown: not applicable" bullet in 6b with the introductory-paragraph rule, and update the N/A wording in 6a/6c so it covers "no new symbols or Markdown sections"

## Implementation Notes
- Edit only the Check 6 block added by PR #747 (`### Check 6 — Documentation Coverage`, sub-steps `6a — Identify New Symbols`, `6b — Check Documentation Comments`, `6c — Produce Verdict`). Keep the sub-step structure used by Checks 1–5 in the same file.
- In 6a, treat a `+`-prefixed line starting with `### ` (with no matching `-` line) in a `*.md` file as a new Markdown section, alongside the code symbols already listed.
- In 6b, replace `- **Markdown:** not applicable — skip Markdown files` with a rule like: "**Markdown:** each new `###` heading must be followed by at least one non-empty paragraph line before the next heading (`#`–`######`) or fenced code block (```)". Lists and tables directly under the heading do not count as an introductory paragraph.
- Exempt eval/test fixture files under `evals/*/files/`. They are deliberate test material (see CONVENTIONS.md "Fixture documentation") and must not trigger WARNs.
- Keep the evidence format in 6c, a list of undocumented items with file path and line number, and use the heading line number for Markdown sections.
- Follow the existing doc-comment list style in Check 3a (`style-conventions.md`, "Doc comment conventions vary by language") for consistent wording.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 3 — Test Documentation` — existing per-language doc-comment list to keep consistent with
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md::Check 2 — Repetitive Test Detection` (2a) — existing early-exit "skip to the Verdict and record N/A" pattern
- `evals/verify-pr/files/pr-diff-with-eval-results.md` — fixture with Markdown-only diff introducing new `###` headings (useful for checking the new rule)

## Acceptance Criteria
- [ ] Check 6b no longer excludes Markdown files outright
- [ ] Check 6 treats each newly added `###` heading in a Markdown file as an item to check
- [ ] A new `###` heading followed by at least one explanatory paragraph before any sub-heading or code block counts as documented
- [ ] A new `###` heading followed directly by a sub-heading, code block, list or table, with no paragraph, counts as undocumented and produces WARN with file path and line number
- [ ] Eval/test fixture files under `evals/*/files/` are excluded from the Markdown rule
- [ ] The N/A verdict wording covers PRs with no new code symbols and no new Markdown sections

## Test Requirements
- [ ] Verify Check 6 flags a new `###` heading immediately followed by a code block or sub-heading as undocumented
- [ ] Verify Check 6 does not flag a new `###` heading that has an introductory paragraph
- [ ] Verify Check 6 still returns N/A for a PR with no new symbols and no new Markdown headings

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context
- **Comment ID:** 50001 (review 40002, state CHANGES_REQUESTED)
- **Author:** reviewer-b
- **Location:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310 (RIGHT)
- **Original comment:**
  > The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.
