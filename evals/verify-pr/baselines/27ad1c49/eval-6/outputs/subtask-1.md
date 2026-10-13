## Repository
sdlc-plugins

## Target Branch
main

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the Style/Conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but sdlc-plugins is a documentation-heavy repository where skills are defined in Markdown. The check should verify that new Markdown sections (identified by `###` headings) have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to replace the Markdown exclusion with a Markdown-specific documentation rule

## Implementation Notes
- In step 6b of Check 6 ("Check Documentation Comments"), replace the current Markdown entry (`- **Markdown:** not applicable -- skip Markdown files`) with a Markdown-specific rule
- The Markdown rule should check whether new `###` headings (identified by `+` prefix lines in the diff starting with `### `) have at least one paragraph of explanatory text before any sub-section (`####` or deeper) or fenced code block
- Follow the structure of the existing language-specific entries in step 6b (Rust, TypeScript/Java, Python, Go) -- each has a brief description of what constitutes a documentation comment
- A "documented" Markdown section means: at least one non-empty paragraph line exists between the `###` heading and the first sub-heading or code fence
- An "undocumented" Markdown section means: the `###` heading is immediately followed by a sub-heading, code block, or another `###` heading with no explanatory text

## Review Context
Reviewer **reviewer-b** commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The Markdown rule follows the same format as the existing language-specific entries (Rust, TypeScript/Java, Python, Go)
- [ ] Check 6 produces WARN when a new Markdown section lacks introductory text
- [ ] Check 6 produces PASS when all new Markdown sections have introductory text

## Test Requirements
- [ ] Verify the Markdown rule correctly identifies undocumented new `###` sections in a diff
- [ ] Verify the Markdown rule does not flag `###` sections that have explanatory text
- [ ] Verify backward compatibility with non-Markdown language checks (Rust, TypeScript/Java, Python, Go remain unchanged)
