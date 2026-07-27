## Repository
sdlc-plugins

## Target Branch
main

## Description
Add Markdown-specific documentation checking to Check 6 (Documentation Coverage) in the style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown sections (identified by `###` or lower-level headings) have at least one paragraph of introductory text explaining their purpose before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to replace the Markdown "not applicable" exclusion with a Markdown-specific rule, and adjust step 6a if needed to identify new Markdown headings as "symbols"

## Implementation Notes
- In step 6b, replace the Markdown entry `- **Markdown:** not applicable -- skip Markdown files` with a Markdown-specific rule
- The Markdown rule should check that new `###` (or lower-level) headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- A "paragraph of explanatory text" means at least one non-empty line of prose (not a heading, code fence, or list) between the heading and the next structural element
- In step 6a, consider whether Markdown headings should be treated as "symbols" for identification purposes, or whether a separate Markdown-specific scan path is more appropriate
- Follow the existing structure of Check 6 steps 6a-6c for consistency

## Review Context
**Original review comment (comment 50001) by reviewer-b on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:**

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule instead of "not applicable"
- [ ] The Markdown rule verifies that new headings have introductory text before sub-sections or code blocks
- [ ] Existing language-specific rules (Rust, TypeScript/Java, Python, Go) are preserved unchanged
- [ ] The N/A verdict logic in step 6a/6c still applies when no new symbols or headings are introduced
