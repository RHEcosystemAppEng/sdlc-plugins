# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

| Config Item | Value | Source |
|---|---|---|
| Project key | ACME | Jira Configuration |
| Cloud ID | mock-cloud-id-for-eval | Jira Configuration |
| Bug issue type ID | 10020 | Bug Configuration |
| Bug template path | docs/templates/bug-template.md | Bug Configuration |
| Bug-to-Task link type | Blocks | Bug Configuration |

## Issue Type Validation

- Issue type from ACME-500: Bug (ID: 10020)
- Bug issue type ID from Bug Configuration: 10020
- **Result: MATCH** -- issue type is confirmed as Bug.

## Metadata

| Field | Value |
|---|---|
| Issue Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |
| Status | New |

## Bug Template Sections

### Required Sections (from template)

| Section | Heading Format | Present in ACME-500 |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Attachments | `### **Attachments**` | Yes |

### Optional Sections (from template)

| Section | Heading Format | Present in ACME-500 |
|---|---|---|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

**Result: All required sections are present.** No missing sections.

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

### Attachments

None.

### Root Cause (Optional)

Not provided by reporter.

### Suggested Fix (Optional)

Not provided by reporter.
