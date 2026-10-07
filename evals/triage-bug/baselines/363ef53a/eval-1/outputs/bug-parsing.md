# Step 1 - Bug Parsing: ACME-500

## Configuration Validation (Step 0)

Bug Configuration found in CLAUDE.md:
- Bug issue type ID: 10020
- Bug template path: docs/templates/bug-template.md
- Bug-to-Task link type: Blocks
- Project key: ACME
- Cloud ID: mock-cloud-id-for-eval

Issue type validation: Bug issue has type ID 10020, which matches Bug issue type ID 10020 from config. PASS.

## Metadata

| Field | Value |
|---|---|
| Key | ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |

## Parsed Sections

### Issue Description

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Environment / Version

Not provided in bug report.

### Attachments

None.

## Template Conformance

| Required Section | Present | Status |
|---|---|---|
| Issue Description | Yes | PASS |
| Steps to Reproduce | Yes | PASS |
| Expected Result | Yes | PASS |
| Actual Result | Yes | PASS |
| Environment / Version | No | MISSING (non-blocking) |
| Attachments | Yes (None) | PASS |

All critical required sections are present. The bug report is well-structured with clear reproduction steps.
