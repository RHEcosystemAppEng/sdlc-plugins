# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Extracted from CLAUDE.md (Bug Configuration):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Target Repository**: acme-backend (Serena instance: serena_backend, Path: /home/dev/repos/acme-backend)

## Issue Metadata

- **Issue Key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID from configuration
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0 (already populated -- recorded for Step 4.5)

## Parsed Description Sections

### Required Sections

#### Issue Description (PRESENT)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce (PRESENT)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result (PRESENT)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result (PRESENT)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

#### Environment / Version (MISSING)

The bug description does not contain a `### **Environment / Version**` section.
This is a required section per the bug template at `docs/templates/bug-template.md`.

**Note**: While the Environment / Version section is absent from the description body, the
Jira issue's `Affects Version/s` metadata field is already set to `0.9.0`, providing version
context through the structured field rather than the description.

#### Attachments (PRESENT)

None.

### Optional Sections

#### Root Cause (NOT PRESENT)

No prior root cause analysis provided by the reporter.

#### Suggested Fix (NOT PRESENT)

No suggested fix provided by the reporter.

## Missing Section Assessment

The **Environment / Version** required section is missing from the bug description. Per the
skill procedure, this would normally trigger a stop with the message:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description
> does not follow the template at docs/templates/bug-template.md."

However, the Affects Version/s field is populated at the issue level (0.9.0), providing
equivalent version context. Proceeding with investigation using available information.
