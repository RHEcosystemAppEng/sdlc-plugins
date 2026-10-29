# Step 1 -- Bug Parsing: ACME-500

## Step 0 -- Configuration Validation

Extracted from project CLAUDE.md (`claude-md-bug-config.md`):

| Config Field            | Value                                    |
|-------------------------|------------------------------------------|
| Project key             | ACME                                     |
| Cloud ID                | mock-cloud-id-for-eval                   |
| Bug issue type ID       | 10020                                    |
| Bug template path       | docs/templates/bug-template.md           |
| Bug-to-Task link type   | Blocks                                   |

Repository Registry:

| Repository   | Role                 | Serena Instance  | Path                             |
|--------------|----------------------|------------------|----------------------------------|
| acme-backend | Rust backend service | serena_backend   | /home/dev/repos/acme-backend     |

## Issue Type Validation

- Issue type on ACME-500: Bug (ID: 10020)
- Bug issue type ID from config: 10020
- **Match confirmed** -- issue is a valid Bug.

## Bug Metadata

| Field              | Value                                                              |
|--------------------|--------------------------------------------------------------------|
| Issue key          | ACME-500                                                           |
| Web URL            | https://mock-jira.example.com/browse/ACME-500                      |
| Summary            | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status             | New                                                                |
| Labels             | reported-by-user                                                   |
| Component          | sdlc-workflow                                                      |
| Affects Version/s  | **0.9.0** (already populated)                                      |

**Note:** The `affectsVersions` field is already populated with value `0.9.0`. This is recorded for Step 4.5 to decide whether to keep, replace, or augment.

## Bug Template Sections (from `bug-template-mock.md`)

### Required Sections

| Section              | Heading Format                    |
|----------------------|-----------------------------------|
| Description          | `### **Issue Description**`       |
| Steps to reproduce   | `### **Steps to Reproduce**`      |
| Expected Result      | `### **Expected Result**`         |
| Actual Result        | `### **Actual Result**`           |
| Environment / Version| `### **Environment / Version**`   |
| Attachments          | `### **Attachments**`             |

### Optional Sections

| Section        | Heading Format              |
|----------------|-----------------------------|
| Root Cause     | `### **Root Cause**`        |
| Suggested Fix  | `### **Suggested Fix**`     |

## Parsed Description Sections

### Required Sections

#### Issue Description (FOUND)

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

#### Steps to Reproduce (FOUND)

> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

#### Expected Result (FOUND)

> The generated task's Implementation Notes should include:
> > Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result (FOUND)

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown -- the convention is silently dropped.

#### Environment / Version (MISSING)

The bug description does not contain a `### **Environment / Version**` section.

**Note:** Per SKILL.md, a missing required section would normally halt execution with the message:
> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

However, the Affects Version/s field on the issue metadata is already set to `0.9.0`, providing version context through the Jira field rather than the description body.

#### Attachments (FOUND)

> None.

### Optional Sections

#### Root Cause (NOT PRESENT)

No prior root cause analysis from the reporter.

#### Suggested Fix (NOT PRESENT)

No proposed solution from the reporter.
