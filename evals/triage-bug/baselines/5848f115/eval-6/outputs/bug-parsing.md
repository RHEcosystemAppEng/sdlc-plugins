# Step 1 -- Bug Parsing: ACME-500

## Configuration Validated (Step 0)

| Config Item | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

## Issue Metadata

| Field | Value |
|---|---|
| Issue Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type | Bug (ID: 10020) -- matches Bug Configuration |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 (already populated) |

## Template Section Matching

Bug template at `docs/templates/bug-template.md` defines the following required and optional sections.

### Required Sections

| Template Section | Heading Format | Present in ACME-500 | Content |
|---|---|---|---|
| Description | `### **Issue Description**` | Yes | When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `), the plan-feature skill's convention conformance analysis fails to match the heading and silently skips the convention. No warning is logged. The generated task description omits the convention that should have been included. |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes | 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading: `## Migration Patterns  ` / `Add Index::create() for all FK columns.` 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys. 3. Inspect the generated task's Implementation Notes. |
| Expected Result | `### **Expected Result**` | Yes | The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns." |
| Actual Result | `### **Actual Result**` | Yes | The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped. |
| Environment / Version | `### **Environment / Version**` | **No -- MISSING** | N/A |
| Attachments | `### **Attachments**` | Yes | None. |

### Optional Sections

| Template Section | Heading Format | Present in ACME-500 | Content |
|---|---|---|---|
| Root Cause | `### **Root Cause**` | No | N/A |
| Suggested Fix | `### **Suggested Fix**` | No | N/A |

### Missing Required Section

The **Environment / Version** section is missing from the bug description. Per the skill process, this should be flagged:

> Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md.

**Note:** For this eval, we proceed with the remaining steps using the available information. The Affects Version/s field on the issue itself is already set to `0.9.0`, which provides partial version context despite the missing description section.

## Parsed Content for Downstream Steps

### Issue Description
When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `), the plan-feature skill's convention conformance analysis fails to match the heading and silently skips the convention. No warning is logged. The generated task description omits the convention that should have been included.

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
The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.

### Attachments
None.
