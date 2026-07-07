# Sub-Task: Add Markdown-specific documentation coverage rule to Check 6

**Summary:** Add Markdown-specific documentation coverage rule to Check 6
**Labels:** ai-generated-jira, review-feedback
**Parent:** TC-9106

## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. The current implementation explicitly skips Markdown files ("Markdown: not applicable -- skip Markdown files"), but this is a documentation-heavy repository where skills are defined in Markdown. The check should verify that new Markdown sections have introductory text explaining their purpose, even though traditional doc comments do not apply to Markdown.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the "Markdown: not applicable" exclusion in Check 6 section 6b with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- The current Check 6 section 6b lists language-specific doc comment conventions and explicitly excludes Markdown
- Replace the exclusion with a Markdown-specific rule: for new `###` (or deeper) headings in Markdown files, check whether at least one paragraph of explanatory text follows the heading before any sub-headings or code blocks
- This applies to skill definition files (`.md` files under `plugins/`) which define behavior through prose -- undocumented headings make the skill harder to understand
- Follow the pattern of existing language-specific rules: define what constitutes a "documented" heading in Markdown context

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific rule instead of the "not applicable" exclusion
- [ ] The Markdown rule verifies that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] Markdown files in the PR diff are processed by Check 6 (not skipped)
- [ ] The Markdown rule does not produce false positives for headings that already have explanatory text

## Test Requirements
- [ ] Verify the Markdown-specific rule flags headings without explanatory text
- [ ] Verify the Markdown-specific rule passes headings with explanatory text
- [ ] Verify the rule applies to skill definition files (.md) in the repository

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context

**Original review comment (id: 50001, reviewer-b):**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310
