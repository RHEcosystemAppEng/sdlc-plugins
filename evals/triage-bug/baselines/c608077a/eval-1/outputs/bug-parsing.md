# Step 0 / Step 1 — Configuration Validation, Bug Fetch, and Description Parsing (ACME-500)

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present (1 entry) | `acme-backend` — Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key: **ACME**; Cloud ID: **mock-cloud-id-for-eval** |
| Code Intelligence | Present | No Serena MCP servers configured — fall back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID: **10020**; Bug template path: **docs/templates/bug-template.md** (eval fixture: bug-template-mock.md); Bug-to-Task link type: **Blocks** |

Result: configuration is complete. Proceed.

## Step 0.5 — Jira Access

Eval mode: no Jira MCP / REST calls are made. All Jira operations are simulated and written to files.

## Step 1 — Fetch Bug (simulated `jira.get_issue("ACME-500")`)

### Issue type validation

- Issue `issuetype.id`: **10020** (Bug)
- Bug Configuration `Bug issue type ID`: **10020**
- Result: **MATCH** — ACME-500 is a Bug. Proceed.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| webUrl | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | `reported-by-user` |
| Component | `sdlc-workflow` |
| Affects Version/s | `0.9.0` — **already populated** (`affectsVersions` non-empty; Step 4.5.1 would prompt Keep / Replace / Augment) |

### Heading formats (from bug template — Required / Optional Sections tables)

| Section | Heading format | Required? |
|---|---|---|
| Description | `### **Issue Description**` | Required |
| Steps to reproduce | `### **Steps to Reproduce**` | Required |
| Expected Result | `### **Expected Result**` | Required |
| Actual Result | `### **Actual Result**` | Required |
| Environment / Version | `### **Environment / Version**` | Required (template) |
| Attachments | `### **Attachments**` | Required (template) |
| Root Cause | `### **Root Cause**` | Optional |
| Suggested Fix | `### **Suggested Fix**` | Optional |

### Parsed sections

#### Description (`### **Issue Description**`) — FOUND

> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
> the plan-feature skill's convention conformance analysis fails to match the heading and silently
> skips the convention. No warning is logged. The generated task description omits the convention
> that should have been included.

#### Steps to Reproduce (`### **Steps to Reproduce**`) — FOUND

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result (`### **Expected Result**`) — FOUND

> The generated task's Implementation Notes should include:
> "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."

#### Actual Result (`### **Actual Result**`) — FOUND

> The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
> No warning or error is shown — the convention is silently dropped.

#### Attachments (`### **Attachments**`) — FOUND

> None.

#### Environment / Version (`### **Environment / Version**`) — NOT FOUND as a description heading

The description has no `### **Environment / Version**` heading. However, the version
information is available from the issue's `Affects Version/s` field (`0.9.0`), and the
Component field (`sdlc-workflow`) identifies the environment. Because the four core
triage sections (Description, Steps to Reproduce, Expected Result, Actual Result) are all
present and the version is recoverable from structured metadata, triage proceeds. A
recommendation is included in the root cause comment that the reporter add an
Environment / Version section for template conformance.

> Note: under a strict reading of the template, a missing Environment / Version section
> would trigger the Step 1 stop rule ("Bug ACME-500 is missing required sections:
> Environment / Version. The bug description does not follow the template at
> docs/templates/bug-template.md."). It is recorded here so the user can decide; this
> eval run continues because the information is present in the Affects Version/s field.

#### Root Cause (optional) — not present
#### Suggested Fix (optional) — not present

### Summary

| Section | Result |
|---|---|
| Description | Extracted |
| Steps to Reproduce | Extracted |
| Expected Result | Extracted |
| Actual Result | Extracted |
| Attachments | Extracted ("None.") |
| Environment / Version | Heading absent; version `0.9.0` taken from Affects Version/s field |
| Root Cause / Suggested Fix | Not provided by reporter |
