# Bug Parsing Results: ACME-500

## Step 0 -- Configuration Validation

The project CLAUDE.md was validated. All required configuration is present:

- **Repository Registry**: 1 entry found (`acme-backend` -- Rust backend service)
- **Jira Configuration**: Project key `ACME`, Cloud ID `mock-cloud-id-for-eval`
- **Code Intelligence**: Section present (no Serena instances configured)
- **Bug Configuration**: All required fields present
  - Bug issue type ID: `10020`
  - Bug template path: `docs/templates/bug-template.md`
  - Bug-to-Task link type: `Blocks`

## Step 1 -- Issue Type Validation

- Issue type ID from bug issue: **10020** (Bug)
- Bug issue type ID from Bug Configuration: **10020**
- Match: **YES** -- confirmed this is a valid Bug issue

## Bug Template Heading Formats

The bug template defines the following required sections and their heading formats:

| Section | Heading Format | Found in Bug? |
|---------|----------------|---------------|
| Description | `### **Issue Description**` | YES |
| Steps to Reproduce | `### **Steps to Reproduce**` | YES |
| Expected Result | `### **Expected Result**` | YES |
| Actual Result | `### **Actual Result**` | YES |
| Attachments | `### **Attachments**` | YES (optional content: "None.") |

All required sections are present.

## Parsed Sections

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
