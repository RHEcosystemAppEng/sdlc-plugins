# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Issue type validation: Bug (ID: 10020) matches Bug issue type ID (10020) -- confirmed.

## Extracted Metadata

| Field | Value |
|-------|-------|
| Issue Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 (field populated -- one value present) |

## Parsed Description Sections

### Required Sections

**1. Description (heading: `### **Issue Description**`)** -- PRESENT

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

**2. Steps to Reproduce (heading: `### **Steps to Reproduce**`)** -- PRESENT

> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

**3. Expected Result (heading: `### **Expected Result**`)** -- PRESENT

> The generated task's Implementation Notes should include:
> > Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

**4. Actual Result (heading: `### **Actual Result**`)** -- PRESENT

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown -- the convention is silently dropped.

**5. Environment / Version (heading: `### **Environment / Version**`)** -- MISSING

The bug description does not contain a `### **Environment / Version**` section. However, the
Affects Version/s metadata field is populated with `0.9.0`.

**6. Attachments (heading: `### **Attachments**`)** -- PRESENT

> None.

### Optional Sections

**Root Cause (heading: `### **Root Cause**`)** -- NOT PRESENT

**Suggested Fix (heading: `### **Suggested Fix**`)** -- NOT PRESENT

## Missing Section Assessment

The `### **Environment / Version**` required section is missing from the bug description.

Per the skill protocol, this would normally trigger a stop:
> "Bug ACME-500 is missing required sections: Environment / Version. The bug description
> does not follow the template at docs/templates/bug-template.md."

However, version information is available from the Affects Version/s metadata field (0.9.0),
and the component (sdlc-workflow) is specified. The bug is sufficiently described to proceed
with investigation.
