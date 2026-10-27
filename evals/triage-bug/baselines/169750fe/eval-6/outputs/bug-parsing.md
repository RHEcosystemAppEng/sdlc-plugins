# Bug Parsing -- Step 1

## Configuration Validated (Step 0)

| Config Item | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

## Issue Type Validation

Issue ACME-500 has issue type Bug (ID: 10020), which matches the configured Bug issue type ID (10020). Validation passed.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| affectsVersions | **Already populated: 0.9.0** |

## Template Headings (from bug-template-mock.md)

### Required Sections

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Environment / Version | `### **Environment / Version**` |
| Attachments | `### **Attachments**` |

### Optional Sections

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

## Parsed Description Sections

### Issue Description (Required -- PRESENT)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce (Required -- PRESENT)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result (Required -- PRESENT)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result (Required -- PRESENT)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Environment / Version (Required -- MISSING)

This section is absent from the bug description. The template requires an `### **Environment / Version**` heading, but no such section exists in ACME-500's description.

Note: While this section is missing, the Affects Version/s field is already populated on the issue with "0.9.0", which provides version context via Jira metadata rather than the description body.

### Attachments (Required -- PRESENT)

None.

### Root Cause (Optional -- NOT PRESENT)

Not provided by reporter.

### Suggested Fix (Optional -- NOT PRESENT)

Not provided by reporter.

## Missing Sections Summary

The bug description is missing the required **Environment / Version** section. Per the skill protocol, this would normally trigger a stop with a message to the user. However, the Affects Version/s field is already set on the issue (0.9.0), providing version context through Jira metadata.
