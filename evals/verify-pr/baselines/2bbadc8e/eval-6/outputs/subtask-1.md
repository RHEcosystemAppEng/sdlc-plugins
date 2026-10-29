# Sub-task: Add Markdown-specific documentation rule to Check 6

**Issue Type:** Sub-task
**Parent:** TC-9106
**Labels:** ai-generated-jira, review-feedback

---

## Repository
sdlc-plugins

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the Style/Conventions sub-agent. Currently Check 6 skips Markdown files entirely with "Markdown: not applicable — skip Markdown files". The reviewer identified that this is a documentation-heavy repository where skills are defined in Markdown, so the check should verify that new Markdown sections have introductory explanatory text.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — update Check 6 step 6b to replace the Markdown skip rule with a Markdown-specific documentation check

## Implementation Notes
- Replace the "Markdown: not applicable — skip Markdown files" rule with a Markdown-specific rule
- The Markdown rule should check whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the pattern of existing language-specific rules in step 6b (Rust, TypeScript/Java, Python, Go)

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] Existing language-specific rules (Rust, TypeScript/Java, Python, Go) are unchanged

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Review Context
Review comment (id: 50001) from reviewer-b on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.
