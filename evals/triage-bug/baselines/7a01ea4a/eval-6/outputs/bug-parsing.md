# Step 1 -- Bug Parsing: ACME-500

## Configuration Validated (Step 0)

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Issue Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Issue Type**: Bug (ID: 10020) -- matches Bug Configuration issue type ID
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0 (ALREADY POPULATED -- `affectsVersions` field has existing value; Step 4.5 must handle this)

## Template Sections Parsed

Bug template at `docs/templates/bug-template.md` defines the following required and optional headings.

### Required Sections

| Section | Heading Format | Present | Content |
|---------|----------------|---------|---------|
| Description | `### **Issue Description**` | Yes | When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `), the plan-feature skill's convention conformance analysis fails to match the heading and silently skips the convention. No warning is logged. The generated task description omits the convention that should have been included. |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes | 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading: `## Migration Patterns  ` / `Add Index::create() for all FK columns.` 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys. 3. Inspect the generated task's Implementation Notes. |
| Expected Result | `### **Expected Result**` | Yes | The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns." |
| Actual Result | `### **Actual Result**` | Yes | The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped. |
| Environment / Version | `### **Environment / Version**` | **MISSING** | Not present in the bug description. |
| Attachments | `### **Attachments**` | Yes | None. |

### Optional Sections

| Section | Heading Format | Present | Content |
|---------|----------------|---------|---------|
| Root Cause | `### **Root Cause**` | No | Not provided by reporter. |
| Suggested Fix | `### **Suggested Fix**` | No | Not provided by reporter. |

### Missing Required Section

The **Environment / Version** section is missing from the bug description. Per the skill protocol, this would normally trigger a stop with:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

For this triage analysis, the missing section is recorded. The absence of version information in the description body is relevant to Step 4.5 (Affects Version Resolution), but the `affectsVersions` Jira field is already populated with `0.9.0`.
