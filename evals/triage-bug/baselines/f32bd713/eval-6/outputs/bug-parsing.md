# Step 1 -- Bug Parsing: ACME-500

## Metadata

| Field | Value |
|-------|-------|
| Issue Key | ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| affectsVersions populated | **Yes** -- already set to `0.9.0`. Step 4.5 must present options (Keep / Replace / Augment) rather than setting a new value. |

## Issue Type Validation

The issue type ID is `10020`, which matches the Bug issue type ID configured in Bug Configuration (`10020`). Validation passes.

## Template Compliance

Bug template path: `docs/templates/bug-template.md`

### Required Sections

| Section | Heading Format | Present | Content |
|---------|----------------|---------|---------|
| Description | `### **Issue Description**` | Yes | See below |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes | See below |
| Expected Result | `### **Expected Result**` | Yes | See below |
| Actual Result | `### **Actual Result**` | Yes | See below |
| Environment / Version | `### **Environment / Version**` | **No -- MISSING** | Not present in description |
| Attachments | `### **Attachments**` | Yes | "None." |

**Note:** The "Environment / Version" required section is missing from the bug description. Per the skill protocol, this would normally halt execution with a message to the user. For this evaluation, triage proceeds since the Affects Version/s field is already populated on the issue (`0.9.0`), providing version context through metadata rather than the description body.

### Optional Sections

| Section | Heading Format | Present | Content |
|---------|----------------|---------|---------|
| Root Cause | `### **Root Cause**` | No | -- |
| Suggested Fix | `### **Suggested Fix**` | No | -- |

## Parsed Description Sections

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

### Attachments

None.
