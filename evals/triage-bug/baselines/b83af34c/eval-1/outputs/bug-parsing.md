# Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Repository Registry**: acme-backend (Serena instance: serena_backend, Path: /home/dev/repos/acme-backend)

# Step 1 -- Fetch Bug: ACME-500

## Issue Type Validation

Issue type ID 10020 (Bug) matches Bug Configuration. Proceeding.

## Parsed Description Sections

### Required Sections

#### Issue Description

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

#### Environment / Version

**MISSING** -- This required section is not present in the Bug description. The bug description
does not include an `### **Environment / Version**` heading as required by the template at
docs/templates/bug-template.md.

However, version information is available from issue metadata: Affects Version/s = 0.9.0.

### Optional Sections

#### Root Cause

Not provided by reporter.

#### Suggested Fix

Not provided by reporter.

### Attachments

None.

## Extracted Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0 (populated in metadata)
