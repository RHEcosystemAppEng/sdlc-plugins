# Step 0 / Step 1 — Configuration Validation and Bug Parsing: ACME-500

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Check | Result |
|---|---|
| Repository Registry | Present — `acme-backend` (Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`) |
| Jira Configuration | Present — Project key `ACME`, Cloud ID `mock-cloud-id-for-eval` |
| Code Intelligence | Present — notes that no Serena MCP servers are configured (Read/Grep/Glob fallback applies) |
| Bug Configuration | Present — Bug issue type ID `10020`, Bug template path `docs/templates/bug-template.md` (mocked by `bug-template-mock.md`), Bug-to-Task link type `Blocks` |

Configuration is valid. Continue.

## Step 1 — Fetch Bug (mocked `jira.get_issue(ACME-500)`)

### Issue type validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **Match.** Issue is a Bug.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| webUrl | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | `reported-by-user` |
| Component | sdlc-workflow |
| Affects Version/s | 0.9.0 (field **already populated**, so Step 4.5 would ask Keep / Replace / Augment) |

### Required sections (heading formats from bug template)

| Section | Template heading | Found? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No. Missing from the description.** |
| Attachments | `### **Attachments**` | Yes (content: "None.") |

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
No warning or error is shown. The convention is silently dropped.

#### Environment / Version
*(Section absent from the description.)* The only version information is the Jira
**Affects Version/s** field: `0.9.0`.

#### Attachments
None.

### Optional sections

| Section | Template heading | Found? |
|---|---|---|
| Root Cause | `### **Root Cause**` | No (no prior analysis from the reporter) |
| Suggested Fix | `### **Suggested Fix**` | No |

## Validation outcome

Strictly applied, Step 1 says the skill should stop here and tell the user:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not
> follow the template at docs/templates/bug-template.md."

**Eval handling:** the eval instructions ask for all four output artifacts, so triage
continues. The missing section has little effect: the bug is a deterministic text-parsing defect
and does not depend on the environment, and the version (`0.9.0`) is available from the
populated Affects Version/s field. In a live run, the reporter should be asked to add the
`### **Environment / Version**` section to the Bug description.
