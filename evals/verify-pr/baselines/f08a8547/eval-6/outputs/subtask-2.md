## Repository
sdlc-plugins

## Target Branch
main

## Description
Add Markdown-specific documentation verification to Check 6 (Documentation Coverage) in the style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown sections (identified by `###` or lower-level headings) have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to add a Markdown-specific rule instead of skipping Markdown files entirely

## Implementation Notes
- Replace the Markdown exclusion (`Markdown: not applicable -- skip Markdown files`) with a Markdown-specific documentation rule
- The Markdown rule should check whether new `###` headings (or lower-level headings) introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- A "paragraph of explanatory text" means at least one non-empty, non-heading, non-code-fence line between the heading and the next heading or code block
- This aligns with the repository's documentation-centric nature where skills are defined in Markdown files

## Review Context
Reviewer feedback from reviewer-b on PR #747, comment 50001 at plugins/sdlc-workflow/skills/verify-pr/style-conventions.md line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new headings (### or lower) have explanatory text before sub-sections or code blocks
- [ ] The rule does not flag headings that already have introductory text
- [ ] Check 6 produces WARN when a new Markdown heading lacks explanatory text

## Test Requirements
- [ ] Verify that new Markdown headings with explanatory text produce PASS
- [ ] Verify that new Markdown headings without explanatory text produce WARN
- [ ] Verify that modified (non-new) Markdown headings are not flagged
