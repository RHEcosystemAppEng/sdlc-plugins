# Step 1 -- Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Extracted from CLAUDE.md (`claude-md-bug-config.md`):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

## Issue Type Validation

Issue type on ACME-500: Bug (ID: 10020)
Bug Configuration Bug issue type ID: 10020
**Result**: Match confirmed -- issue is a Bug.

## Metadata

| Field | Value |
|-------|-------|
| Issue Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 (field is populated) |
| Status | New |

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
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result (PRESENT)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

#### Environment / Version (MISSING)

The bug description does not contain a `### **Environment / Version**` section.
However, the Affects Version/s metadata field is populated with `0.9.0`.

Note: Per SKILL.md Step 1, missing required sections should halt execution. For
this eval, the missing section is recorded but triage proceeds since version
information is available in the issue metadata (Affects Version/s: 0.9.0).

#### Attachments (PRESENT)

None.

### Optional Sections

#### Root Cause (NOT PRESENT)

No prior root cause analysis provided by the reporter.

#### Suggested Fix (NOT PRESENT)

No suggested fix provided by the reporter.
