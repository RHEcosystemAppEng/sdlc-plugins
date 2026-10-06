## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage)
in the verify-pr style-conventions sub-agent. The current implementation blanket-
excludes Markdown files ("Markdown: not applicable -- skip Markdown files"), but
this repository is documentation-heavy with skills defined in Markdown. Check 6
should verify that new Markdown sections have introductory text explaining their
purpose.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- add a
  Markdown-specific rule to Check 6 step 6b that verifies new `###` headings
  have at least one paragraph of explanatory text before any sub-sections or
  code blocks; replace the "Markdown: not applicable" exclusion with the new rule

## Implementation Notes
- In step 6b (Check Documentation Comments), replace the Markdown exclusion line
  with a Markdown-specific rule: "**Markdown:** new `###` (or deeper) headings
  must have at least one paragraph of explanatory text before any sub-sections
  or code blocks"
- Follow the pattern of the existing language-specific rules in step 6b (Rust,
  TypeScript/Java, Python, Go) -- each specifies the convention and what to look for
- The check should verify that new headings added in the diff have descriptive text,
  not just empty headings followed immediately by sub-headings or fenced code blocks
- The CONVENTIONS.md for this repository documents: "No source code: This is a
  documentation-heavy repository -- skills are defined in Markdown (SKILL.md files)"
  which confirms the need for Markdown documentation coverage

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph
      of explanatory text before sub-sections or code blocks
- [ ] The "Markdown: not applicable -- skip Markdown files" exclusion is replaced
      with the new rule
- [ ] The rule does not flag headings that already have explanatory text

## Test Requirements
- [ ] Verify the Markdown rule flags headings without explanatory text
- [ ] Verify the Markdown rule does not flag headings with explanatory text
- [ ] Verify the check handles mixed-language PRs (Markdown + code files) correctly

## Review Context
- **Original comment:** reviewer-b (comment 50001) on
  `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:
  "The Check 6 description says 'Markdown: not applicable -- skip Markdown files'
  but this is a documentation-heavy repository where skills are defined in Markdown.
  The check should still verify that new Markdown sections have introductory text
  explaining their purpose, even if traditional doc comments don't apply. Consider
  adding a Markdown-specific rule that checks whether new `###` headings have at
  least one paragraph of explanatory text before any sub-sections or code blocks."
- **Classification:** code change request

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
