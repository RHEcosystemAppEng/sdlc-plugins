## Repository
sdlc-plugins

## Target Branch
main

## Description
Root-cause: Improve plan-feature task generation to include repository-specific documentation format considerations when planning documentation coverage checks. The TC-9106 task description specified adding a Documentation Coverage check but did not account for the fact that this repository's primary format is Markdown documentation, not traditional source code. This led to the implementation blanket-excluding Markdown files from documentation coverage, which a reviewer correctly identified as a gap.

The plan-feature skill should analyze the target repository's primary language and documentation format (available in CONVENTIONS.md under "Language and Framework") when generating tasks related to documentation checks, and include guidance about format-specific handling in the Implementation Notes section.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add guidance in the task generation steps to cross-reference the target repository's primary format (from CONVENTIONS.md "Language and Framework" section) when planning documentation-related checks, and include format-specific considerations in Implementation Notes

## Implementation Notes
- The plan-feature skill already reads CONVENTIONS.md during task generation; the improvement is to explicitly check the "Language and Framework" section when the task involves documentation coverage or documentation quality checks
- When the repository's primary format is non-traditional (e.g., Markdown documentation rather than source code), the Implementation Notes should include guidance about adapting standard code-focused checks to the repository's actual format
- This is a method-based improvement: "When planning documentation-related tasks, verify the target repository's primary content format and include format-specific adaptation guidance" -- this applies universally to any repository

## Acceptance Criteria
- [ ] plan-feature checks the target repository's primary format when generating documentation-related tasks
- [ ] Implementation Notes include format-specific considerations when the repository uses non-traditional formats
- [ ] The guidance is general enough to apply to any repository format, not just Markdown

## Test Requirements
- [ ] Verify that a documentation coverage task for a Markdown-heavy repository includes Markdown-specific guidance
- [ ] Verify that a documentation coverage task for a traditional source code repository is unaffected
