# Bug Parsing — ACME-500

## Step 0 — Configuration Validation

Extracted from CLAUDE.md (`claude-md-bug-config.md`):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Repository Registry**: acme-backend (Path: /home/dev/repos/acme-backend)

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration. Validation passed.

## Issue Type Validation

Issue type ID from Bug issue: **10020**
Bug issue type ID from Bug Configuration: **10020**
Match: **Yes** — proceeding with triage.

## Metadata

- **Issue Key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0

## Bug Template Sections

Template at `docs/templates/bug-template.md` defines:

**Required Sections:**

| Section | Heading Format | Present in Bug? |
|---------|----------------|-----------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |

**Optional Sections:**

| Section | Heading Format | Present in Bug? |
|---------|----------------|-----------------|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

All required sections are present. Validation passed.

## Parsed Description Sections

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
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

### Attachments

None.

### Root Cause (Optional)

Not provided by reporter.

### Suggested Fix (Optional)

Not provided by reporter.
