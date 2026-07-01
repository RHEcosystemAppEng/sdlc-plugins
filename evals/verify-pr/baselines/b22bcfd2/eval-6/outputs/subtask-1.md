## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository defines skills primarily in Markdown. The check should verify that new Markdown sections (introduced by `###` headings) have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to add a Markdown-specific rule that replaces the blanket "skip Markdown files" with a check for introductory text under new `###` headings

## Implementation Notes
- In step 6b of Check 6, replace the Markdown entry ("Markdown: not applicable -- skip Markdown files") with a Markdown-specific rule
- The rule should check whether new `###` headings (identified in the PR diff with `+` prefix) have at least one paragraph of explanatory text before any sub-sections (`####` or deeper) or code blocks (triple backticks)
- A "new heading" is a `###` line appearing in the diff with a `+` prefix
- The documentation check for Markdown is structural (presence of explanatory text) rather than comment-based (no doc comments in Markdown)
- Follow the structure of the other language entries in step 6b for consistency

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule instead of skipping Markdown files
- [ ] The Markdown rule checks whether new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The rule applies only to new headings introduced in the PR diff (not pre-existing headings)
- [ ] The verdict logic in step 6c correctly accounts for Markdown documentation gaps (WARN when heading lacks explanatory text)

## Review Context
**PR Comment ID:** 50001
**Reviewer:** reviewer-b
**File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310
**Comment:** "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
