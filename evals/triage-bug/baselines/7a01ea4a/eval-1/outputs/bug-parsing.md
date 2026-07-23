# Bug Parsing: ACME-500

## Metadata

- **Issue Key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0 (from issue metadata field)
- **Affects Version field populated**: Yes (value: 0.9.0)

## Parsed Description Sections

### Required Sections

#### Issue Description (Present)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce (Present)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result (Present)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result (Present)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

#### Environment / Version (MISSING)

This required section is not present in the bug description. The bug description does not include
a `### **Environment / Version**` heading as required by the bug template at
`docs/templates/bug-template.md`.

Note: The issue metadata does contain `Affects Version/s: 0.9.0`, but the structured
Environment / Version section is absent from the description body.

#### Attachments (Present)

None.

### Optional Sections

#### Root Cause

Not present in bug description.

#### Suggested Fix

Not present in bug description.

## Validation Result

**Missing required section**: Environment / Version

Per the triage-bug skill Step 1, the bug description is missing the required
`### **Environment / Version**` section. The skill would normally stop execution and inform the
user. However, sufficient information exists in the issue metadata (`Affects Version/s: 0.9.0`)
and in the other sections to proceed with investigation.
