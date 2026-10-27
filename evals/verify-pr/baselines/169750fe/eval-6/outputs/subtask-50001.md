## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the Style/Conventions sub-agent. The current implementation excludes Markdown files entirely ("Markdown: not applicable — skip Markdown files"), but since this repository defines skills in Markdown, the check should verify that new Markdown sections have introductory explanatory text.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — update Check 6 step 6b to add a Markdown-specific rule instead of blanket exclusion; add logic to check that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks

## Implementation Notes
- Replace the current Markdown exclusion in step 6b ("Markdown: not applicable — skip Markdown files") with a Markdown-specific rule
- The rule should check whether new `###` headings (identified as new in step 6a by `+` prefix) have at least one paragraph of explanatory text before any sub-sections or code blocks
- This recognizes that Markdown files in this repository serve as skill definitions and benefit from section-level documentation

## Acceptance Criteria
- [ ] Check 6 no longer blanket-excludes Markdown files
- [ ] New `###` headings in Markdown files are checked for introductory text
- [ ] A heading followed immediately by a sub-section or code block without explanatory text triggers WARN
- [ ] Existing Markdown headings with proper introductory text produce PASS

## Test Requirements
- [ ] Verify Markdown-specific rule detects headings without introductory text
- [ ] Verify headings with proper explanatory text pass the check

## Review Context
Reviewer reviewer-b (comment 50001 on style-conventions.md line 310):

> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
