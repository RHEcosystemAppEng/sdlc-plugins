# Bug Parsing: ACME-500

## Step 0 -- Project Configuration Validation

| Configuration Section | Present | Extracted Values |
|---|---|---|
| Repository Registry | Yes | acme-backend (Rust backend service) |
| Jira Configuration | Yes | Project key: ACME, Cloud ID: mock-cloud-id-for-eval |
| Code Intelligence | Yes | No Serena instances configured |
| Bug Configuration | Yes | Bug issue type ID: 10020, Template: docs/templates/bug-template.md, Bug-to-Task link type: Blocks |

## Issue Metadata

| Field | Value |
|---|---|
| Key | ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |

## Step 1 Validation

- Bug issue type ID from issue: **10020**
- Bug issue type ID from Bug Configuration: **10020**
- Match: **YES** -- validated

## Template Heading Formats

Headings parsed using formats from the bug template:

| Section | Heading Format | Present in Issue |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | No |
| Attachments | `### **Attachments**` | Yes (None) |

## Parsed Sections

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
> Per CONVENTIONS.md Section Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Environment / Version

Not provided in the issue. Affects Version: 0.9.0.

### Attachments

None.
