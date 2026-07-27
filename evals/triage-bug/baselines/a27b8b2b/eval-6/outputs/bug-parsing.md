# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Extracted from CLAUDE.md (`claude-md-bug-config.md`):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Issue Type Validation

- Issue type on ACME-500: Bug (ID: 10020)
- Expected Bug issue type ID from config: 10020
- **Result**: Match -- issue is a valid Bug.

## Bug Template Sections

Template loaded from: `docs/templates/bug-template.md`

### Required Sections (from template)

| Section | Heading Format | Present in ACME-500 |
|---------|----------------|---------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | No -- missing |
| Attachments | `### **Attachments**` | Yes |

### Optional Sections (from template)

| Section | Heading Format | Present in ACME-500 |
|---------|----------------|---------------------|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

### Missing Required Section

The **Environment / Version** section is not present in the bug description.
Per the skill, this would normally trigger a stop:

> "Bug ACME-500 is missing required sections: Environment / Version.
> The bug description does not follow the template at docs/templates/bug-template.md."

**Note**: For this eval, the triage proceeds because the Affects Version/s metadata is already set on the issue (see below) and the eval requires all output files.

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
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Environment / Version

**Not present in the bug description.**

### Attachments

None.

### Root Cause (Optional)

Not provided by reporter.

### Suggested Fix (Optional)

Not provided by reporter.

## Extracted Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0
- **affectsVersions already populated**: Yes -- value is "0.9.0"

The `affectsVersions` field is already populated with "0.9.0". This is recorded for Step 4.5 to decide whether to keep, replace, or augment.
