# Sub-Task: Add Markdown-specific documentation rule to Check 6

**Type:** Review feedback sub-task
**Parent:** TC-9106
**Labels:** `["ai-generated-jira", "review-feedback"]`
**Summary:** Add Markdown-specific documentation coverage rule for new section headings

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific rule to Check 6 (Documentation Coverage) in the Style/Conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable — skip Markdown files"), but since this is a documentation-heavy repository where skills are defined in Markdown, the check should verify that new Markdown sections have introductory text explaining their purpose.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — update Check 6 step 6b to replace the blanket Markdown exclusion with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- The current Markdown exclusion in step 6b says "Markdown: not applicable — skip Markdown files"
- Replace this with a Markdown-specific rule: for new `###` (or deeper) headings introduced in the PR diff, verify that at least one paragraph of explanatory text follows the heading before any sub-sections or code blocks
- This is relevant because the sdlc-plugins repository defines skills primarily in Markdown, so documentation coverage for Markdown sections is meaningful
- The PASS/WARN/N/A verdict logic in step 6c should treat missing introductory text the same as missing doc comments (contributes to WARN)

## Acceptance Criteria
- [ ] Check 6 includes a Markdown-specific rule for new section headings
- [ ] New `###` headings in Markdown files are checked for introductory explanatory text
- [ ] Markdown files are no longer blanket-excluded from documentation coverage checking
- [ ] The verdict logic correctly accounts for Markdown section documentation status

## Test Requirements
- [ ] Verify that new Markdown headings without introductory text produce WARN
- [ ] Verify that new Markdown headings with introductory text produce PASS
- [ ] Verify that Markdown files with no new headings produce N/A for the Markdown rule

## Review Context
Reviewer reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` at line 310:

> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
