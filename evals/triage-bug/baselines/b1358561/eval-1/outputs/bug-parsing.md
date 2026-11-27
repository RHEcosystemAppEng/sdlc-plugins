# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-500)

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | `acme-backend` (Rust backend service), Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key: `ACME`; Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Present | No Serena MCP servers are configured, so investigation falls back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md` (mocked by `bug-template-mock.md`); Bug-to-Task link type: `Blocks` |

Result: the configuration is valid, so triage continues.

## Step 0.5 — Jira Access

The eval says not to use Jira, so no MCP or REST call was made. Every Jira operation below is simulated and written to a file.

## Step 1 — Fetch Bug: `jira.get_issue("ACME-500")` (simulated from bug-issue-standard.md)

### Issue type validation

- Issue `issuetype.id`: **10020** (Bug)
- Bug Configuration `Bug issue type ID`: **10020**
- Result: **the IDs match.** ACME-500 is a Bug, so triage continues.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| webUrl | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | `reported-by-user` |
| Component | `sdlc-workflow` |
| Affects Version/s | `0.9.0`. The `affectsVersions` field is **already populated**, so Step 4.5.1 will ask the user to Keep, Replace, or Augment it. |

### Parsed description sections (heading formats from bug-template-mock.md)

#### Required Sections

**Description** (heading `### **Issue Description**`): FOUND
> When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `), the plan-feature skill's convention conformance analysis fails to match the heading and silently skips the convention. No warning is logged. The generated task description omits the convention that should have been included.

**Steps to Reproduce** (heading `### **Steps to Reproduce**`): FOUND
> 1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
>    ```
>    ## Migration Patterns  
>    Add Index::create() for all FK columns.
>    ```
> 2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
> 3. Inspect the generated task's Implementation Notes.

**Expected Result** (heading `### **Expected Result**`): FOUND
> The generated task's Implementation Notes should include:
> > Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

**Actual Result** (heading `### **Actual Result**`): FOUND
> The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.

**Attachments** (heading `### **Attachments**`, required by the mock template): FOUND
> None.

**Environment / Version** (heading `### **Environment / Version**`): **NOT FOUND in the description body**
> This heading does not appear in the description. The version is only in the Jira **Affects Version/s** field (`0.9.0`).

#### Optional Sections

| Section | Heading | Status |
|---|---|---|
| Root Cause | `### **Root Cause**` | Not present. The reporter gave no prior analysis. |
| Suggested Fix | `### **Suggested Fix**` | Not present |

### Validation note on Environment / Version

The current SKILL.md lists five required sections: Description, Steps to Reproduce, Expected Result, Actual Result, and Environment / Version. A strict reading would make the skill stop here with this message:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

All four core sections are present: Description, Steps to Reproduce, Expected Result and Actual Result. The version is also set in the Affects Version/s field (`0.9.0`). This eval asks for the full triage of ACME-500, so the analysis continues and treats the Affects Version/s field as the Environment / Version information. In a live run, the gap above would be reported to the user.
