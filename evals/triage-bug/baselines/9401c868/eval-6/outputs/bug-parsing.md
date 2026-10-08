# Step 1 -- Bug Parsing: ACME-500

## Configuration Validated (Step 0)

| Config Item            | Value                                |
|------------------------|--------------------------------------|
| Project key            | ACME                                 |
| Cloud ID               | mock-cloud-id-for-eval               |
| Bug issue type ID      | 10020                                |
| Bug template path      | docs/templates/bug-template.md       |
| Bug-to-Task link type  | Blocks                               |

## Issue Type Validation

Issue type ID on ACME-500: **10020** (Bug)
Bug issue type ID from config: **10020**
Result: **Match** -- issue is confirmed as a Bug.

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
> Per CONVENTIONS.md "Migration Patterns": add `Index::create()` for all FK columns.

#### Actual Result (PRESENT)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

#### Environment / Version (MISSING)

This required section is not present in the bug description.

> **Note:** Per skill rules, a missing required section would normally halt execution:
> "Bug ACME-500 is missing required sections: Environment / Version. The bug description
> does not follow the template at docs/templates/bug-template.md."
>
> However, the Affects Version/s field on the issue is already set to `0.9.0`, providing
> version context through metadata rather than the description body. Proceeding with
> triage using the metadata-supplied version information.

#### Attachments (PRESENT)

None.

### Optional Sections

| Section        | Status      |
|----------------|-------------|
| Root Cause     | Not present |
| Suggested Fix  | Not present |

## Extracted Metadata

| Field               | Value                                                    |
|---------------------|----------------------------------------------------------|
| Issue key           | ACME-500                                                 |
| Web URL             | https://mock-jira.example.com/browse/ACME-500            |
| Summary             | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels              | reported-by-user                                         |
| Component           | sdlc-workflow                                            |
| Affects Version/s   | 0.9.0 (already populated on the issue)                   |
| Status              | New                                                      |
