## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. Currently Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository defines skills primarily in Markdown. The check should verify that new Markdown sections (new `###` headings) have at least one paragraph of introductory/explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to add a Markdown-specific rule replacing the "not applicable" skip with a heading-level documentation check

## Implementation Notes
- In Check 6 step 6b, replace the Markdown entry ("Markdown: not applicable -- skip Markdown files") with a rule that checks whether new `###` headings (identified by `+` prefix lines starting with `###` in the diff) have at least one paragraph of explanatory text before any sub-sections or code blocks
- A "paragraph of explanatory text" means at least one non-empty, non-heading, non-code-fence line following the heading before the next heading or code block
- This rule applies specifically to Markdown files (`.md` extension) in the PR diff
- Follow the same structure as the other language-specific rules in step 6b

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule that checks new `###` headings for introductory text
- [ ] The Markdown rule replaces the previous "not applicable -- skip Markdown files" entry
- [ ] The rule checks that at least one paragraph of explanatory text exists before any sub-sections or code blocks following a new heading
- [ ] The PASS/WARN/N/A verdict logic in step 6c accounts for Markdown headings lacking explanatory text as undocumented symbols

## Test Requirements
- [ ] Verify Check 6 flags new Markdown `###` headings that lack explanatory text
- [ ] Verify Check 6 does not flag new Markdown `###` headings that have explanatory text
- [ ] Verify the overall verdict correctly reflects Markdown documentation gaps

## Review Context
Reviewer reviewer-b (comment 50001, line 310 of plugins/sdlc-workflow/skills/verify-pr/style-conventions.md) requested:
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
