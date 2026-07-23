# Step 1 -- Bug Parsing: ACME-500

## Configuration Validated (Step 0)

| Parameter | Value |
|-----------|-------|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

## Issue Type Validation

Issue type ID `10020` matches Bug Configuration's Bug issue type ID `10020`. Validated as Bug.

## Metadata

| Field | Value |
|-------|-------|
| Issue Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 (already populated) |

## Parsed Required Sections

### Issue Description

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md "Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Environment / Version

**MISSING from description body.** The bug description does not contain a `### **Environment / Version**` section as required by the template at `docs/templates/bug-template.md`.

However, the issue metadata field Affects Version/s is populated with `0.9.0`, providing version context via metadata.

### Attachments

None.

## Parsed Optional Sections

### Root Cause

Not present in description.

### Suggested Fix

Not present in description.

## Missing Sections Note

The required section **Environment / Version** (`### **Environment / Version**`) is missing from the Bug description body. Per the skill protocol, this would normally halt execution. Version information is available from the issue metadata (Affects Version/s: 0.9.0), so investigation proceeds with that context.
