## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable — skip Markdown files"). Since this repository defines skills and specifications primarily in Markdown, the check should verify that new Markdown sections have introductory text explaining their purpose. Specifically, new `###` headings should have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — update Check 6 step 6b to replace the Markdown exclusion with a Markdown-specific documentation rule

## Implementation Notes
- In step 6b "Check Documentation Comments," replace the current Markdown rule ("Markdown: not applicable — skip Markdown files") with a Markdown-specific rule
- The Markdown rule should check that new `###` (or lower-level) headings in Markdown files have at least one paragraph of explanatory text before the next sub-section heading or code block
- A "paragraph of explanatory text" is one or more non-empty lines of prose (not a heading, not a code fence, not a table row, not a bare list that is itself structural)
- Follow the existing pattern in step 6b for language-specific rules: each language entry has a bold label, doc comment convention, and brief description

## Acceptance Criteria
- [ ] Check 6 no longer unconditionally skips Markdown files
- [ ] Check 6 includes a Markdown-specific rule that checks new headings for introductory explanatory text
- [ ] New `###` headings without explanatory text before sub-sections or code blocks produce WARN
- [ ] New `###` headings with at least one paragraph of explanatory text produce PASS
- [ ] The rule does not flag headings that are followed by explanatory prose before sub-structure

## Test Requirements
- [ ] Verify Markdown headings with explanatory text are not flagged
- [ ] Verify Markdown headings without explanatory text (immediately followed by sub-headings or code blocks) are flagged as undocumented
- [ ] Verify existing non-Markdown language rules in step 6b are unaffected by the change

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Review Context
**Source**: reviewer-b inline comment (id 50001) on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310
**Review State**: CHANGES_REQUESTED

**Comment**: "The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."
