## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the verify-pr style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but since sdlc-plugins is a documentation-heavy repository where skills are defined in Markdown, the check should verify that new Markdown sections have introductory explanatory text.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the "Markdown: not applicable" line in Check 6b with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- In step 6b of Check 6, the current Markdown rule is: "Markdown: not applicable -- skip Markdown files"
- Replace this with a rule that checks new `###` (or lower) headings for at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the existing pattern of the other language-specific rules in 6b
- This does not change the PASS/WARN/N/A verdict logic in 6c -- the same rules apply, just with Markdown sections now counted as documentable symbols

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] Existing language-specific rules (Rust, TypeScript/Java, Python, Go) remain unchanged

## Review Context
Reviewer reviewer-b requested this change (review state: CHANGES_REQUESTED):

> "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
