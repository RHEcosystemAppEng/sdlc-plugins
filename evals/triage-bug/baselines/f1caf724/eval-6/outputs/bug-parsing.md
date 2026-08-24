# Step 1 -- Bug Parsing: ACME-500

## Metadata

- **Issue Key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Issue Type**: Bug (ID: 10020) -- matches Bug Configuration (Bug issue type ID: 10020) -- VALID
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0 (ALREADY SET -- recorded for Step 4.5)
- **affectsVersions field populated**: Yes (1 value: "0.9.0")

## Bug Template Validation

Template path: `docs/templates/bug-template.md`

### Required Sections (per template)

| Section | Heading Format | Present in Bug? | Content |
|---------|----------------|-----------------|---------|
| Description | `### **Issue Description**` | YES | Present with content |
| Steps to Reproduce | `### **Steps to Reproduce**` | YES | Present with 3 steps |
| Expected Result | `### **Expected Result**` | YES | Present with content |
| Actual Result | `### **Actual Result**` | YES | Present with content |
| Environment / Version | `### **Environment / Version**` | NO -- MISSING | Not present in description |
| Attachments | `### **Attachments**` | YES | "None." |

### Optional Sections (per template)

| Section | Heading Format | Present in Bug? |
|---------|----------------|-----------------|
| Root Cause | `### **Root Cause**` | NO |
| Suggested Fix | `### **Suggested Fix**` | NO |

### Missing Required Section Note

The bug description is missing the required **Environment / Version** section. Per the skill's Step 1 rules, this would normally halt execution:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

However, the Affects Version/s field is already set on the issue to "0.9.0", providing version context through metadata rather than the description body. Proceeding with analysis for eval purposes.

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
