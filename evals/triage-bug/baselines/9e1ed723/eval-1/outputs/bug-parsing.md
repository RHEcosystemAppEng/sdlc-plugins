# Step 0 / Step 1 — Configuration Validation and Bug Parsing: ACME-500

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Serena: serena_backend, Path: /home/dev/repos/acme-backend) | Present |
| Project key | ACME | Present |
| Cloud ID | mock-cloud-id-for-eval | Present |
| Code Intelligence | Present (states no Serena MCP servers configured) | Present |
| Bug issue type ID | 10020 | Present |
| Bug template path | docs/templates/bug-template.md (mocked by bug-template-mock.md) | Present |
| Bug-to-Task link type | Blocks | Present |

Configuration is valid; proceed.

## Step 1 — Issue Type Validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **Match** — issue is a Bug; triage continues.

## Metadata

| Field | Value |
|---|---|
| Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 (`versions` field **already populated** — Step 4.5 would prompt Keep/Replace/Augment) |

## Parsed Description Sections

Heading formats were taken from the template's Required/Optional Sections tables.

### Required Sections

| Section | Template heading | Found | 
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No — heading not present in description** |
| Attachments | `### **Attachments**` | Yes |

#### Description
When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce
1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result
The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result
The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

#### Environment / Version
**Missing from the description body.** The only version information available is the
issue's `Affects Version/s` metadata field: `0.9.0`.

#### Attachments
None.

### Optional Sections

| Section | Found |
|---|---|
| Root Cause (`### **Root Cause**`) | No (no prior reporter analysis) |
| Suggested Fix (`### **Suggested Fix**`) | No |

## Template Compliance Note

Strictly per Step 1 of the skill, a missing Required Section triggers:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not
> follow the template at docs/templates/bug-template.md."

and execution should stop. Because this eval run explicitly requests the full triage output
(Steps 1-5), and the missing information is recoverable from the populated `Affects Version/s`
field (0.9.0), triage continues below with this gap flagged. In a live run, the user would be
informed of the missing section (and a reporter could be asked to add it).
