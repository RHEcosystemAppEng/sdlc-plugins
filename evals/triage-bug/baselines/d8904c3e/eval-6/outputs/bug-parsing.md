# Step 1 -- Bug Description Parsing

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |

### Issue Type Validation

Bug issue type ID from Bug Configuration: **10020**
Issue's issuetype.id: **10020**
Result: **Match** -- issue is confirmed as a Bug.

### Affects Version/s Pre-existing Value

The `affectsVersions` field is already populated with one value: **0.9.0**. This is recorded for Step 4.5 to decide whether to skip or augment.

## Bug Template Validation

Template path: `docs/templates/bug-template.md`

### Required Sections

| Section | Heading Format | Present |
|---------|----------------|---------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | No |

Note: The **Environment / Version** section is listed as a required section in the bug template but is absent from the bug description. However, since the `Affects Version/s` field is already populated on the issue itself (0.9.0), version information is available through issue metadata.

### Optional Sections

| Section | Heading Format | Present |
|---------|----------------|---------|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

### Attachments

Section present with value: None.

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
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.
