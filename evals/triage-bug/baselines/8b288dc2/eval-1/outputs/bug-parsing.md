# Step 1: Bug Description Parsing

## Bug Template Validation

### Required Heading Formats (from bug template)

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Attachments | `### **Attachments**` |

### Issue Type Validation

- Bug Configuration defines Bug issue type ID: **10020**
- Issue ACME-500 reports Issue Type: **Bug (ID: 10020)**
- Result: **MATCH** -- issue type ID is valid per project Bug Configuration

## Parsed Required Sections

### 1. Issue Description (PRESENT)

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

### 2. Steps to Reproduce (PRESENT)

> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

### 3. Expected Result (PRESENT)

> The generated task's Implementation Notes should include:
> > Per CONVENTIONS.md "Migration Patterns: add `Index::create()` for all FK columns.

### 4. Actual Result (PRESENT)

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown -- the convention is silently dropped.

### 5. Attachments (PRESENT)

> None.

## Section Completeness

All 4 required sections are present and contain substantive content. The bug description conforms to the bug template.

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Attachments | Present (None) |
