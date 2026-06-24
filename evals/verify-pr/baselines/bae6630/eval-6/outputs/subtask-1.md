## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but since this is a documentation-heavy repository where skills are defined in Markdown, the check should verify that new Markdown sections have introductory explanatory text. Specifically, add a rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6, section 6b (Check Documentation Comments) to replace the Markdown skip rule with a Markdown-specific rule that verifies new `###` headings have introductory text

## Implementation Notes
- In section 6b of Check 6, replace the current Markdown bullet ("Markdown: not applicable -- skip Markdown files") with a Markdown-specific rule
- The new rule should check that each new `###` heading introduced in the PR diff has at least one paragraph of explanatory text before any sub-headings (`####`) or code blocks appear
- Follow the structure of the existing language-specific rules in section 6b
- The rule applies only to new headings (lines with `+` prefix in the diff), consistent with Check 6's focus on new symbols

## Review Context
**Reviewer:** reviewer-b
**Comment:** "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific documentation rule
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The previous "skip Markdown files" directive is replaced with the new rule
