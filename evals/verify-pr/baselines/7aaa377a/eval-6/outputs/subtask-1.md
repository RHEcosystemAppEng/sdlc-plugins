## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository defines skills and documentation in Markdown, so new Markdown sections should be checked for introductory explanatory text. The rule should verify that new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 section 6b to add a Markdown-specific rule replacing the blanket "not applicable" exclusion with a rule that checks for introductory paragraphs under new headings

## Implementation Notes
- In section "6b -- Check Documentation Comments", replace the Markdown bullet ("Markdown: not applicable -- skip Markdown files") with a Markdown-specific rule
- The new rule should check whether new `###` (or deeper) headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- Keep the rule scoped to structural Markdown files (skill definitions, documentation) -- do not apply to changelog entries, templates, or generated Markdown
- Follow the pattern of existing language-specific rules in section 6b (each defines what constitutes documentation for that language)

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific documentation rule
- [ ] The rule checks that new `###` headings have at least one explanatory paragraph before sub-sections or code blocks
- [ ] The blanket "Markdown: not applicable -- skip Markdown files" exclusion is removed or replaced
- [ ] The rule does not flag Markdown files where documentation rules are not applicable (e.g., changelogs, templates)

## Test Requirements
- [ ] Verify the Markdown rule correctly flags new headings without explanatory text
- [ ] Verify the Markdown rule does not flag headings that already have explanatory text
- [ ] Verify excluded Markdown file types (changelogs, templates) are not flagged

## Review Context
**Comment ID:** 50001
**Reviewer:** reviewer-b
**File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310
**Comment text:**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
