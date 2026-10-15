# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Issue type validation: Bug (ID: 10020) matches Bug issue type ID in configuration. Passed.

## Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0 (populated in Jira field)

## Template Heading Formats

Parsed from bug template at `docs/templates/bug-template.md`:

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
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result (from `### **Actual Result**`)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Environment / Version (from `### **Environment / Version**`)

**MISSING** -- This required section is not present in the bug description body. However, the Jira metadata field `Affects Version/s` is populated with `0.9.0`.

### Attachments (from `### **Attachments**`)

None.

## Optional Sections

- **Root Cause**: Not present
- **Suggested Fix**: Not present

## Missing Sections Note

The `### **Environment / Version**` section is missing from the bug description body. Per the triage-bug procedure, this would normally halt processing. However, version information is available from the Jira `Affects Version/s` metadata field (0.9.0), providing sufficient context to proceed with investigation.
