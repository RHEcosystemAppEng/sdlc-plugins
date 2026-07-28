# Step 1 – Bug Parsing: ACME-500

## Configuration Validation (Step 0)

From `claude-md-bug-config.md`:
- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md (resolved to `bug-template-mock.md` for this eval)
- **Bug-to-Task link type**: Blocks
- **Repository Registry**: acme-backend → `/home/dev/repos/acme-backend`
- **Code Intelligence**: No Serena MCP servers configured — fallback to Read/Grep/Glob

All required configuration sections are present. Proceeding.

---

## Issue Metadata

| Field            | Value                                                          |
|------------------|----------------------------------------------------------------|
| Key              | ACME-500                                                       |
| Summary          | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Issue Type       | Bug (ID: 10020)                                                |
| Status           | New                                                            |
| Labels           | reported-by-user                                               |
| Component        | sdlc-workflow                                                  |
| Affects Version/s | **0.9.0** (already populated — recorded for Step 4.5)        |
| Web URL          | https://mock-jira.example.com/browse/ACME-500                  |

### Issue Type Validation

Bug Configuration specifies Bug issue type ID: `10020`.
Bug issue reports issue type ID: `10020`.
**Match confirmed.** Issue is a Bug. Proceeding.

---

## Bug Template — Required and Optional Sections

From `bug-template-mock.md`:

### Required Sections

| Section              | Heading Format                    |
|----------------------|-----------------------------------|
| Description          | `### **Issue Description**`       |
| Steps to reproduce   | `### **Steps to Reproduce**`      |
| Expected Result      | `### **Expected Result**`         |
| Actual Result        | `### **Actual Result**`           |
| Environment / Version | `### **Environment / Version**`  |
| Attachments          | `### **Attachments**`             |

### Optional Sections

| Section       | Heading Format           |
|---------------|--------------------------|
| Root Cause    | `### **Root Cause**`     |
| Suggested Fix | `### **Suggested Fix**`  |

---

## Parsed Description Sections

### Present Required Sections

#### Issue Description
> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

#### Steps to Reproduce
1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result
> The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result
> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown — the convention is silently dropped.

#### Attachments
> None.

---

### Missing Required Sections

| Section              | Status  | Notes |
|----------------------|---------|-------|
| Environment / Version | **MISSING** | The `### **Environment / Version**` heading is absent from the bug description body. Under normal skill execution this would halt triage with a message to the user. However, the `Affects Version/s` metadata field IS populated (value: `0.9.0`), which will be used in Step 4.5.1. Proceeding for eval purposes. |

### Optional Sections
- **Root Cause**: Not present (reporter did not provide prior analysis)
- **Suggested Fix**: Not present

---

## Metadata Summary for Later Steps

| Extracted Field         | Value                                      |
|-------------------------|--------------------------------------------|
| affectsVersions         | `["0.9.0"]` — **already populated**       |
| Component               | sdlc-workflow → investigation target: `plugins/sdlc-workflow/` |
| Labels                  | reported-by-user                           |
| Environment/Version     | Section absent from description; version sourced from metadata field |
| Root Cause (reporter)   | None                                       |
| Suggested Fix           | None                                       |
