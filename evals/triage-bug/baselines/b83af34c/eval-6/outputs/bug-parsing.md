# Step 1 -- Bug Parsing: ACME-500

## Step 0 -- Configuration Validation

Extracted from CLAUDE.md (`claude-md-bug-config.md`):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Repository Registry**: acme-backend | Serena Instance: serena_backend | Path: /home/dev/repos/acme-backend

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration) are present. Validation passed.

## Issue Type Validation

Issue type ID on ACME-500: **10020** (Bug)
Bug issue type ID from Bug Configuration: **10020**
Match: **Yes** -- proceeding with triage.

## Parsed Description Sections

### Required Sections

#### Issue Description (Present)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce (Present)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result (Present)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result (Present)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

#### Environment / Version (Missing)

The bug description does not contain a `### **Environment / Version**` section.
This is a required section per the bug template at `docs/templates/bug-template.md`.

> Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md.

**Note**: In a live triage, execution would stop here pending a complete bug report. For this analysis, proceeding with available information since the Affects Version field is already set on the issue.

#### Attachments (Present)

None.

### Optional Sections

#### Root Cause

Not present in the bug description.

#### Suggested Fix

Not present in the bug description.

## Extracted Metadata

| Field | Value |
|-------|-------|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |
| Status | New |
| affectsVersions populated | **Yes** -- value "0.9.0" is already set on the issue |
