# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Extracted from project CLAUDE.md (`claude-md-bug-config.md`):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Repository Registry**: acme-backend (Serena instance: serena_backend, Path: /home/dev/repos/acme-backend)

## Issue Type Validation

Issue type ID `10020` matches Bug Configuration's Bug issue type ID `10020`. Validated as a Bug issue.

## Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0 (populated in issue metadata)
- **Status**: New

## Parsed Description Sections

### Required Sections

#### Issue Description (present)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce (present)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result (present)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result (present)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

#### Environment / Version (MISSING)

This required section is absent from the Bug description body. However, version information
is available in the issue metadata field `Affects Version/s: 0.9.0`. The description does
not include a `### **Environment / Version**` heading as required by the bug template.

#### Attachments (present)

None.

### Optional Sections

#### Root Cause

Not provided by reporter.

#### Suggested Fix

Not provided by reporter.

## Section Completeness Summary

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Environment / Version | **Missing from description** (available in metadata) |
| Attachments | Present |
| Root Cause (optional) | Not provided |
| Suggested Fix (optional) | Not provided |

**Note**: The Environment / Version section is missing from the description body per the
template at `docs/templates/bug-template.md`. The version information (0.9.0) is available
in the issue's Affects Version/s metadata field and will be used for version resolution in
Step 4.5.
