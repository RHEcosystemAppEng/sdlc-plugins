# Bug Parsing — ACME-500

## Step 0 — Validate Project Configuration

### Extracted Configuration from CLAUDE.md

| Field | Value |
|-------|-------|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

### Issue Type Validation

- Issue ACME-500 has issue type Bug with ID **10020**
- Bug Configuration specifies Bug issue type ID **10020**
- **Match confirmed.** Issue type validation passed.

## Step 1 — Fetch Bug and Parse Description

### Bug Template Heading Formats

The bug description template at `docs/templates/bug-template.md` defines the following heading formats:

**Required Sections:**

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Attachments | `### **Attachments**` |

**Optional Sections:**

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

### Parsed Required Sections

**Description** (from `### **Issue Description**`):

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

**Steps to Reproduce** (from `### **Steps to Reproduce**`):

> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

**Expected Result** (from `### **Expected Result**`):

> The generated task's Implementation Notes should include:
> > Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

**Actual Result** (from `### **Actual Result**`):

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown — the convention is silently dropped.

### Parsed Optional Sections

- **Root Cause**: not provided
- **Suggested Fix**: not provided

### Extracted Metadata

| Field | Value |
|-------|-------|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |

### Validation Result

All four required sections (Description, Steps to Reproduce, Expected Result, Actual Result) are present.
