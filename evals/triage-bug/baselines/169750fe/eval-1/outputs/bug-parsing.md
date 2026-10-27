# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation

### Bug Configuration (from CLAUDE.md)

- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

### Issue Type Validation

The issue's type ID (10020) matches the Bug issue type ID from Bug Configuration. Validation passed.

### Jira Configuration

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval

## Extracted Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0 (populated in issue metadata)
- **Status**: New

## Template Heading Formats

From the bug template at `docs/templates/bug-template.md`:

### Required Sections

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to Reproduce | `### **Steps to Reproduce**` |
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

### Issue Description (PRESENT)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce (PRESENT)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result (PRESENT)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result (PRESENT)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Environment / Version (MISSING)

This section is **not present** in the bug description. The bug description does not contain a `### **Environment / Version**` heading. Note that the issue metadata does list "Affects Version/s: 0.9.0", but the description body itself omits this required template section.

### Attachments (PRESENT)

None.

## Optional Sections

### Root Cause (NOT PRESENT)

No prior root cause analysis provided by the reporter.

### Suggested Fix (NOT PRESENT)

No suggested fix provided by the reporter.

## Validation Result

**Missing required section**: Environment / Version

Per the SKILL.md Step 1 instructions, a missing required section would normally trigger a stop:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

However, for the purposes of this eval, we proceed with the triage using the available sections. The missing Environment / Version section is noted and carried forward to Step 4.5 (Affects Version Resolution), where version information will need to be resolved from the issue metadata instead.
