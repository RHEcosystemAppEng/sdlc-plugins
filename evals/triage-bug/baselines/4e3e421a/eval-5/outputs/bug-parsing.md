# Step 0 / Step 1 – Configuration Validation and Bug Parsing: ACME-511

## Step 0 – Configuration Validation (from claude-md-bug-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (Rust backend service, Serena: serena_backend, Path: /home/dev/repos/acme-backend) | Present |
| Project key | ACME | Present |
| Cloud ID | mock-cloud-id-for-eval | Present |
| Code Intelligence | Present (no Serena MCP servers configured, so Read/Grep/Glob fallback applies) | Present |
| Bug issue type ID | 10020 | Present |
| Bug template path | docs/templates/bug-template.md (eval mock: bug-template-mock.md) | Present |
| Bug-to-Task link type | Blocks | Present |

Configuration is complete, so triage continues.

## Step 1 – Fetch Bug (simulated, no Jira call)

### Issue type validation

- Issue `issuetype.id` = **10020** (Bug)
- Configured Bug issue type ID = **10020**
- Result: **Match**. The issue is a Bug.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-511 |
| Web URL | https://mock-jira.example.com/browse/ACME-511 |
| Summary | Dark mode toggle does not persist across browser sessions |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | (none). The `versions` field is **not populated**. Step 4.5.1 is skipped and resolution starts at 4.5.2. |

### Parsed description sections

Headings were matched against the template's Required/Optional Sections tables.

#### Required sections

| Template Section | Heading Matched | Found |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | Yes |
| Attachments | `### **Attachments**` | Yes |

**Description**
> When a user enables dark mode via the settings panel and then closes and reopens the
> browser, the application reverts to light mode. The preference is not persisted.

**Steps to Reproduce**
1. Open the application in a browser.
2. Navigate to Settings > Appearance.
3. Toggle "Dark Mode" to ON.
4. Close the browser completely.
5. Reopen the browser and navigate back to the application.

**Expected Result**
> The application should load in dark mode, matching the user's last preference.

**Actual Result**
> The application loads in light mode. The dark mode toggle is reset to OFF.

**Environment / Version**
> Not sure which version — using whatever is deployed on staging.

- The section is present, but it has **no version identifier**: no explicit version number, no product-prefixed version, and no "version X.Y.Z" pattern. The text is vague ("not sure which version", "whatever is deployed on staging"). Step 4.5 handles this.

**Attachments**
> None.

#### Optional sections

| Section | Present | Content |
|---|---|---|
| Root Cause | No | — |
| Suggested Fix | No | — |

### Completeness result

All required sections are present, so the bug is structurally complete and triage continues.
The Environment / Version section has content but no usable version information.
