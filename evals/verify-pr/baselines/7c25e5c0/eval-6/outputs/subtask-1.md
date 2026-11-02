## Repository
sdlc-plugins

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the Style/Conventions sub-agent. The current implementation excludes Markdown files entirely ("Markdown: not applicable — skip Markdown files"), but this repository's skills are defined in Markdown, so new sections should be verified for introductory documentation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — replace the Markdown exclusion in Check 6 section 6b with a Markdown-specific rule

## Implementation Notes
- Replace the "Markdown: not applicable — skip Markdown files" line in section 6b with a Markdown-specific rule
- The rule should check whether new `###` headings (identified by `+` prefix in the diff) have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the same pattern as the existing language-specific rules in 6b (Rust, TypeScript/Java, Python, Go)
- Consider that not all Markdown files are documentation — the rule should focus on skill files and structured documentation where section introductions are expected

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific documentation rule instead of excluding Markdown files
- [ ] The Markdown rule verifies that new headings have introductory explanatory text
- [ ] The rule checks for at least one paragraph before sub-sections or code blocks
- [ ] Existing language-specific rules remain unchanged

## Review Context
**Comment ID:** 50001
**Author:** reviewer-b
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310

**Original comment:**
> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.
