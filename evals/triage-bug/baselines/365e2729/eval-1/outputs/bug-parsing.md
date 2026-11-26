# Step 0 / Step 1 — Configuration Validation and Bug Parsing: ACME-500

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | `acme-backend` — Serena instance `serena_backend`, Path `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key: `ACME`; Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Present | "No Serena MCP servers are configured" — fall back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md` (mock: bug-template-mock.md); Bug-to-Task link type: `Blocks` |

All required configuration is present. Continuing to Step 1.

## Step 1 — Fetch Bug (simulated `jira.get_issue("ACME-500")`)

### Issue type validation

- Issue `issuetype.id`: **10020** (Bug)
- Bug Configuration `Bug issue type ID`: **10020**
- Result: **MATCH**. ACME-500 is a Bug. Continuing.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | `reported-by-user` |
| Component | `sdlc-workflow` |
| Affects Version/s | `0.9.0` — **already populated** (Step 4.5.1 must ask Keep / Replace / Augment) |

### Heading formats (from the bug template)

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`,
`### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

### Parsed Required Sections

#### Description (`### **Issue Description**`) — FOUND

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce (`### **Steps to Reproduce**`) — FOUND

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result (`### **Expected Result**`) — FOUND

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result (`### **Actual Result**`) — FOUND

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

#### Environment / Version (`### **Environment / Version**`) — NOT FOUND IN DESCRIPTION

There is no `### **Environment / Version**` heading in the description. Version information
is available from the Jira **Affects Version/s** field (`0.9.0`) and the Component field
(`sdlc-workflow`).

#### Attachments (`### **Attachments**`) — FOUND

None.

### Parsed Optional Sections

- Root Cause (`### **Root Cause**`): not present
- Suggested Fix (`### **Suggested Fix**`): not present

### Validation outcome

The four core required sections (Description, Steps to Reproduce, Expected Result,
Actual Result) and Attachments were all extracted using the template heading formats.

**Deviation flag:** the template's `### **Environment / Version**` heading is missing. Under a
strict reading of the Step 1 stop rule the skill would halt with:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description
> does not follow the template at docs/templates/bug-template.md."

For this eval run, triage continues: the missing information is already captured in the
structured Affects Version/s field (`0.9.0`), and that gap does not stop root-cause
investigation. A real run should either stop here or ask the reporter to add the section.
