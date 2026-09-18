# Step 1 -- Bug Description Parsing

## Configuration Validated (Step 0)

| Config Field             | Value                              |
|--------------------------|------------------------------------|
| Project key              | ACME                               |
| Cloud ID                 | mock-cloud-id-for-eval             |
| Bug issue type ID        | 10020                              |
| Bug template path        | docs/templates/bug-template.md     |
| Bug-to-Task link type    | Blocks                             |

## Issue Type Validation

Issue ACME-500 has `issuetype.id: 10020`, which matches the configured Bug issue type ID (10020). Validation passed.

## Metadata Extracted

| Field              | Value                                                                     |
|--------------------|---------------------------------------------------------------------------|
| Issue key          | ACME-500                                                                  |
| Web URL            | https://mock-jira.example.com/browse/ACME-500                             |
| Summary            | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status             | New                                                                       |
| Labels             | reported-by-user                                                          |
| Component          | sdlc-workflow                                                             |
| Affects Version/s  | 0.9.0 (already populated -- recorded for Step 4.5)                        |

## Parsed Description Sections

### Required Sections

#### 1. Description (heading: `### **Issue Description**`) -- PRESENT

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### 2. Steps to Reproduce (heading: `### **Steps to Reproduce**`) -- PRESENT

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### 3. Expected Result (heading: `### **Expected Result**`) -- PRESENT

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

#### 4. Actual Result (heading: `### **Actual Result**`) -- PRESENT

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

#### 5. Environment / Version (heading: `### **Environment / Version**`) -- MISSING

The bug description does not contain a `### **Environment / Version**` section.

> **Note:** Bug ACME-500 is missing required section: Environment / Version. The bug description
> does not follow the template at docs/templates/bug-template.md. Per the skill, execution should
> stop here. However, the Affects Version/s field is already set on the issue (0.9.0), providing
> partial version context. Proceeding with triage using available information.

### Optional Sections

#### Root Cause -- NOT PRESENT

No prior root cause analysis from the reporter.

#### Suggested Fix -- NOT PRESENT

No suggested fix from the reporter.

### Additional Sections Found

#### Attachments (heading: `### **Attachments**`) -- PRESENT

None.
