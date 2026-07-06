# Bug Parsing — ACME-500

## Step 0 — Configuration Validation

Extracted from `claude-md-bug-config.md`:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required CLAUDE.md sections are present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Issue Type Validation

- Bug issue `issuetype.id`: **10020**
- Bug Configuration `Bug issue type ID`: **10020**
- **Match confirmed** — issue type is Bug.

## Template Heading Formats

From `bug-template-mock.md`, the Required Sections table defines these heading formats:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Attachments | `### **Attachments**` |

Optional Sections:

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

## Extracted Required Sections

### 1. Description (heading: `### **Issue Description**`)

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

### 2. Steps to Reproduce (heading: `### **Steps to Reproduce**`)

> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

### 3. Expected Result (heading: `### **Expected Result**`)

> The generated task's Implementation Notes should include:
> > Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### 4. Actual Result (heading: `### **Actual Result**`)

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown — the convention is silently dropped.

## Extracted Optional Sections

- **Root Cause**: Not present in bug description.
- **Suggested Fix**: Not present in bug description.

## Extracted Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0

## Validation Result

All four required sections (Description, Steps to Reproduce, Expected Result, Actual Result) were found and successfully extracted. Bug description conforms to the template at `docs/templates/bug-template.md`.
