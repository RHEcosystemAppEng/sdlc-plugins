# Bug Parsing -- ACME-500

## Issue Metadata

- **Key**: ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0
- **Web URL**: https://mock-jira.example.com/browse/ACME-500

## Parsed Description Sections

### Issue Description (PRESENT)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce (PRESENT)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result (PRESENT)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result (PRESENT)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Environment / Version (MISSING)

This required section is not present in the bug description. The Affects Version/s field on the issue is set to 0.9.0, which partially covers this gap.

### Attachments (PRESENT)

None.

## Template Conformance

| Section | Required | Present |
|---------|----------|---------|
| Issue Description | Yes | Yes |
| Steps to Reproduce | Yes | Yes |
| Expected Result | Yes | Yes |
| Actual Result | Yes | Yes |
| Environment / Version | Yes | **No** |
| Attachments | Yes | Yes (None) |

**Note**: The "Environment / Version" required section is missing from the bug description. However, the bug is still triageable since the Affects Version/s field (0.9.0) is set on the issue itself, and the Steps to Reproduce are sufficiently detailed.
