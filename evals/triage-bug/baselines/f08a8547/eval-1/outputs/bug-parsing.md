# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Extracted from project CLAUDE.md:

| Parameter | Value |
|-----------|-------|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

## Issue Type Validation

Issue ACME-500 has issue type Bug (ID: 10020), which matches the configured Bug issue type ID (10020). Validation passed.

## Metadata

| Field | Value |
|-------|-------|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 (field is populated) |
| Status | New |

## Parsed Required Sections

### Issue Description

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

### Steps to Reproduce

> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

### Expected Result

> The generated task's Implementation Notes should include:
> > Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown -- the convention is silently dropped.

### Environment / Version

**MISSING** -- This required section is not present in the bug description.

Note: Version information is available from issue metadata (Affects Version/s: 0.9.0) but the structured description section is absent. Per the skill protocol, missing required sections should cause execution to halt with a notification to the user. However, proceeding with analysis since version context is available from metadata.

### Attachments

> None.

## Parsed Optional Sections

### Root Cause

Not present in the bug description.

### Suggested Fix

Not present in the bug description.

## Missing Sections Summary

- **Environment / Version** -- required section missing from the description body. The bug does not follow the template at `docs/templates/bug-template.md`. Normally this would trigger a stop: "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."
