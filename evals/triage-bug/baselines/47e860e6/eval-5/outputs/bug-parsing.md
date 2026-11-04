# Step 0 / Step 1 – Configuration Validation and Bug Parsing: ACME-511

## Step 0 – Project Configuration Validation

Source: `claude-md-bug-config.md` (project CLAUDE.md)

| Required section | Status | Values extracted |
|---|---|---|
| Repository Registry | Present (1 entry) | acme-backend, Rust backend service, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key `ACME`, Cloud ID `mock-cloud-id-for-eval` |
| Code Intelligence | Present | Says "No Serena MCP servers are configured" (this conflicts with the registry listing `serena_backend`. I treat code intelligence as unavailable and fall back to Read/Grep/Glob.) |
| Bug Configuration | Present | Bug issue type ID `10020`, Bug template path `docs/templates/bug-template.md` (mocked by `bug-template-mock.md`), Bug-to-Task link type `Blocks` |

Result: the configuration is complete, so triage proceeds.

## Step 0.5 – Jira Access

For this eval, Jira MCP is not called. The issue contents come from `bug-issue-no-version.md`, and every Jira write is recorded in these output files.

## Step 1 – Fetch Bug

### Issue type validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **match**, so triage proceeds.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-511 |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Status | New |
| Labels | `reported-by-user` |
| Component | sdlc-workflow |
| Affects Version/s | (none). The `versions` field is **not populated**, so Step 4.5.1 (keep/replace/augment) does not apply and Step 4.5 starts at 4.5.2. |

### Parsed description sections (matched against template heading formats)

| Template section | Heading format | Found? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | Yes (present, but it contains no version identifier) |
| Attachments | `### **Attachments**` | Yes ("None.") |
| Root Cause (optional) | `### **Root Cause**` | Not present |
| Suggested Fix (optional) | `### **Suggested Fix**` | Not present |

All required sections are present, so the bug is not rejected as incomplete.

#### Description
> When a user enables dark mode via the settings panel and then closes and reopens the
> browser, the application reverts to light mode. The preference is not persisted.

#### Steps to Reproduce
1. Open the application in a browser.
2. Navigate to Settings > Appearance.
3. Toggle "Dark Mode" to ON.
4. Close the browser completely.
5. Reopen the browser and navigate back to the application.

#### Expected Result
> The application should load in dark mode, matching the user's last preference.

#### Actual Result
> The application loads in light mode. The dark mode toggle is reset to OFF.

#### Environment / Version
> Not sure which version — using whatever is deployed on staging.

Notes:
- The section heading is present, so there is no missing-section failure.
- The content is vague. It has no explicit version number, no product-prefixed version, and no "version X.Y.Z" pattern. The only environment hint is "staging", which names a deployment target, not a release.
- Step 4.5.2 therefore extracts **no version**. See `version-resolution.md`.

#### Attachments
> None.

#### Root Cause (optional)
Not provided by the reporter.

#### Suggested Fix (optional)
Not provided by the reporter.
