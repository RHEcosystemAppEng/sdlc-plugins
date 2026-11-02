# Step 1 -- Parse Bug Description

## Issue Metadata

| Field | Value |
|---|---|
| Key | ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | **0.9.0** (ALREADY SET on the issue) |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |

## Parsed Sections

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

Not provided in the bug description. Note that the issue-level metadata has Affects Version/s: 0.9.0 already set.

### Attachments (PRESENT)

None.

### Root Cause (OPTIONAL -- NOT PROVIDED)

Not provided.

### Suggested Fix (OPTIONAL -- NOT PROVIDED)

Not provided.

## Template Conformance

| Required Section | Present? |
|---|---|
| Issue Description | Yes |
| Steps to Reproduce | Yes |
| Expected Result | Yes |
| Actual Result | Yes |
| Environment / Version | No (missing from description body, but Affects Version/s is set at issue level) |
| Attachments | Yes (stated "None") |

The bug description is largely conformant with the template. The Environment / Version section is missing from the description body, though the Affects Version/s field is already populated at the issue metadata level with value 0.9.0.
