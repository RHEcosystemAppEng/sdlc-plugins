# Step 0 / Step 1 – Configuration Validation and Bug Parsing (ACME-511)

## Step 0 – Configuration Validation

Source: `claude-md-bug-config.md`

| Required section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present (1 entry) | acme-backend, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key: `ACME`, Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Present | No Serena MCP servers configured, so investigation falls back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID: `10020`, Bug template path: `docs/templates/bug-template.md`, Bug-to-Task link type: `Blocks` |

Result: configuration is valid, so triage proceeds.

## Step 1 – Fetch Bug

### Issue type validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **match**. The issue is a Bug, so triage proceeds.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-511 |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Status | New |
| Labels | `reported-by-user` |
| Component | sdlc-workflow |
| Affects Version/s | (none). The `versions` field is **not populated**, so Step 4.5.1 does not apply and Step 4.5 starts at sub-step 4.5.2 |

### Template heading formats (from bug template)

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`,
`### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

### Parsed Required Sections

#### Description (`### **Issue Description**`)

When a user enables dark mode via the settings panel and then closes and reopens the
browser, the application reverts to light mode. The preference is not persisted.

#### Steps to Reproduce (`### **Steps to Reproduce**`)

1. Open the application in a browser.
2. Navigate to Settings > Appearance.
3. Toggle "Dark Mode" to ON.
4. Close the browser completely.
5. Reopen the browser and navigate back to the application.

#### Expected Result (`### **Expected Result**`)

The application should load in dark mode, matching the user's last preference.

#### Actual Result (`### **Actual Result**`)

The application loads in light mode. The dark mode toggle is reset to OFF.

#### Environment / Version (`### **Environment / Version**`)

> Not sure which version — using whatever is deployed on staging.

- The heading is present, so the required-section check passes.
- The content is **vague**. It has no explicit version number, no product-prefixed version,
  and no "version X.Y.Z" pattern. It only names a deployment environment ("staging").
- This content goes to Step 4.5.2. See `version-resolution.md`.

#### Attachments (`### **Attachments**`)

None.

### Parsed Optional Sections

- **Root Cause**: not present. The reporter gave no prior analysis.
- **Suggested Fix**: not present.

### Required-section check

All required sections are present: Issue Description, Steps to Reproduce, Expected Result,
Actual Result, Environment / Version, and Attachments. **No missing sections**, so
triage proceeds.
