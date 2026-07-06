## Repository
sdlc-plugins

## Target Branch
main

## Description
Document a Markdown documentation convention in CONVENTIONS.md: in this repository, skills and sub-agent specifications are defined as Markdown files, making Markdown the primary "source code" format. New Markdown section headings (especially `###` and below) should include at least one paragraph of explanatory text describing the section's purpose before any sub-sections or code blocks.

This convention gap was identified during verification of TC-9106, where a reviewer flagged that Check 6 (Documentation Coverage) skips Markdown files entirely despite Markdown being the dominant file type in this repository. The root cause is the undocumented convention that Markdown sections in this repo serve as functional specifications and require the same documentation discipline as code symbols in traditional programming languages.

## Files to Modify
- `CONVENTIONS.md` -- add a section documenting the Markdown documentation convention (create the file if it does not exist)

## Implementation Notes
- Document the convention under a clear section heading (e.g., "Markdown Section Documentation").
- State the rule: new Markdown section headings (`###` and below) in skill/sub-agent specification files must include at least one paragraph of explanatory text before sub-sections or code blocks.
- Explain the rationale: Markdown files serve as executable specifications in this repository; section headings without explanatory text are analogous to undocumented public functions.
- Include examples of well-documented vs. poorly-documented sections for clarity.
- This convention applies specifically to files under `plugins/sdlc-workflow/skills/` and related specification directories.

## Acceptance Criteria
- [ ] CONVENTIONS.md contains a section documenting the Markdown section documentation convention
- [ ] The convention specifies that new `###` headings should have explanatory text before sub-sections or code blocks
- [ ] The scope of the convention is specified (skill/sub-agent specification files)
- [ ] The rationale for the convention is documented

## Test Requirements
- [ ] Verify CONVENTIONS.md is parseable and follows existing project documentation patterns
- [ ] Verify the convention section is discoverable by grep/search for downstream tooling
