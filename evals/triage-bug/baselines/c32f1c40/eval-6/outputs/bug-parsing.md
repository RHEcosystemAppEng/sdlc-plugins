# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Extracted from CLAUDE.md (`claude-md-bug-config.md`):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Issue Type Validation

- Issue type from ACME-500: Bug (ID: 10020)
- Bug issue type ID from config: 10020
- **Match**: Yes -- issue is a valid Bug.

## Parsed Description Sections

### Required Sections

**1. Issue Description** (`### **Issue Description**`)

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

**2. Steps to Reproduce** (`### **Steps to Reproduce**`)

> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

**3. Expected Result** (`### **Expected Result**`)

> The generated task's Implementation Notes should include:
> > Per CONVENTIONS.md "Migration Patterns: add `Index::create()` for all FK columns.

**4. Actual Result** (`### **Actual Result**`)

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown -- the convention is silently dropped.

**5. Environment / Version** (`### **Environment / Version**`)

**MISSING** -- The bug description does not contain an `### **Environment / Version**` section.

> **Note**: Per the triage-bug skill, missing required sections should trigger a stop.
> However, the `Affects Version/s` metadata field is already populated on the issue (see below),
> providing version context through issue metadata rather than the description body.

**6. Attachments** (`### **Attachments**`)

> None.

### Optional Sections

- **Root Cause**: Not present in the bug description.
- **Suggested Fix**: Not present in the bug description.

### Missing Required Sections

The following required section (per the bug template) is absent from the description:

- **Environment / Version** (`### **Environment / Version**`)

## Extracted Metadata

| Field | Value |
|-------|-------|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | **0.9.0** (already populated) |
| Status | New |

### affectsVersions Field Status

The `affectsVersions` (Jira `versions` field) is **already populated** with value: **0.9.0**.
This will be evaluated in Step 4.5 to determine whether to keep, replace, or augment.
