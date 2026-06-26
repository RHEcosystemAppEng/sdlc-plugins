## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the Style/Conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but since sdlc-plugins is a documentation-heavy repository where skills are defined in Markdown, the check should verify that new Markdown sections have introductory explanatory text.

The new rule should check whether new `###` headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks. This ensures that new documentation sections are self-documenting.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6's section 6b to replace the Markdown "not applicable" exclusion with a Markdown-specific rule that checks for introductory text after new `###` headings

## Implementation Notes
- In section "6b -- Check Documentation Comments", replace the current Markdown bullet:
  ```
  - **Markdown:** not applicable -- skip Markdown files
  ```
  with a rule such as:
  ```
  - **Markdown:** check that new `###` (or deeper) headings have at least one paragraph of explanatory text before any sub-sections or code blocks
  ```
- Follow the existing structure of the other language-specific rules in section 6b
- The rule should only apply to newly added headings (lines with `+` prefix in the diff), not existing headings
- Consider whether the verdict logic in 6c needs adjustment -- a missing introductory paragraph in Markdown should produce the same WARN verdict as a missing doc comment in code

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific rule for verifying introductory text on new headings
- [ ] The Markdown rule checks that new `###` (or deeper) headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The previous "Markdown: not applicable" exclusion is removed or replaced
- [ ] The verdict logic in 6c applies consistently to Markdown documentation gaps (WARN when introductory text is missing)

## Review Context
**Original review comment (PR comment 50001):**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
