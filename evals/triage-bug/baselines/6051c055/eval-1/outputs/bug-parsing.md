# Bug Parsing — ACME-500

## Step 0 — Validate Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 — Issue Type Validation

The issue's `issuetype.id` is **10020**, which matches the **Bug issue type ID** (10020) from Bug Configuration. Validation passed.

## Step 1 — Parsed Description Sections

The bug template defines the following heading formats for Required Sections:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |

All four required sections were found and parsed from the bug description:

### Description (from `### **Issue Description**`)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce (from `### **Steps to Reproduce**`)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result (from `### **Expected Result**`)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md "Migration Patterns": add `Index::create()` for all FK columns.

### Actual Result (from `### **Actual Result**`)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

## Optional Sections

- **Root Cause**: Not present in the bug description.
- **Suggested Fix**: Not present in the bug description.

## Extracted Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0
