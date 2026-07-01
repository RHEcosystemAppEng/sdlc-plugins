# Bug Parsing — Step 1

## Issue Metadata

- **Issue Key**: ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0
- **Web URL**: https://mock-jira.example.com/browse/ACME-500

## Issue Type Validation

The issue's `issuetype.id` is **10020**. The Bug Configuration in CLAUDE.md specifies `Bug issue type ID: 10020`. These match — the issue is confirmed as a Bug.

## Bug Template Heading Formats

From `bug-template-mock.md`, the required heading formats are:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to Reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Attachments | `### **Attachments**` |

## Parsed Required Sections

### Description (heading: `### **Issue Description**`)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce (heading: `### **Steps to Reproduce**`)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result (heading: `### **Expected Result**`)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md "Migration Patterns": add `Index::create()` for all FK columns.

### Actual Result (heading: `### **Actual Result**`)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

## Parsed Optional Sections

### Attachments (heading: `### **Attachments**`)

None.

### Root Cause

Not provided by reporter.

### Suggested Fix

Not provided by reporter.

## Validation Result

All four required sections (Description, Steps to Reproduce, Expected Result, Actual Result) are present in the bug description. Parsing is complete — proceeding to investigation.
