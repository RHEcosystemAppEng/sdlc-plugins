# Bug Parsing — ACME-500

## Step 0 — Configuration Validation

| Config Item | Value | Source |
|---|---|---|
| Project key | ACME | Jira Configuration |
| Cloud ID | mock-cloud-id-for-eval | Jira Configuration |
| Bug issue type ID | 10020 | Bug Configuration |
| Bug template path | docs/templates/bug-template.md | Bug Configuration |
| Bug-to-Task link type | Blocks | Bug Configuration |

**Issue type validation**: Issue type ID 10020 matches Bug Configuration Bug issue type ID 10020. Confirmed Bug.

## Metadata

| Field | Value |
|---|---|
| Issue Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |
| Status | New |

## Template Heading Formats

From `docs/templates/bug-template.md`:

**Required Sections:**

| Section | Heading Format |
|---|---|
| Description | `### **Issue Description**` |
| Steps to Reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Attachments | `### **Attachments**` |

**Optional Sections:**

| Section | Heading Format |
|---|---|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

## Parsed Required Sections

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
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

### Attachments

None.

## Parsed Optional Sections

- **Root Cause**: Not provided by reporter.
- **Suggested Fix**: Not provided by reporter.

## Validation Result

All required sections present. Bug description conforms to the template.
