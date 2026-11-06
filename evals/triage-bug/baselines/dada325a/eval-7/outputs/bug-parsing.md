# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-520)

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Check | Result |
|---|---|
| Repository Registry | Present — `acme-backend` (Rust backend service), Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | Present — Project key `ACME`, Cloud ID `mock-cloud-id-for-eval` |
| Code Intelligence | Present — notes that no Serena MCP servers are configured (fallback to Read/Grep/Glob) |
| Bug Configuration | Present — Bug issue type ID `10020`, Bug template path `docs/templates/bug-template.md`, Bug-to-Task link type `Blocks` |

All required configuration is present. Proceeding.

## Step 0.5 — Jira Access

Not exercised (eval mode: no MCP / REST calls). All Jira operations are recorded to files instead.

## Step 1 — Fetch Bug

### Issue type validation

- Issue `issuetype.id`: `10020` (Bug)
- Configured Bug issue type ID: `10020`
- Result: **match** — issue is a Bug; triage continues.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-520 |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Status | New |
| Labels | `reported-by-user` |
| Component | `risk-engine` |
| Affects Version/s | (none) — `versions` field is **not** populated (Step 4.5 will not need the keep/replace/augment prompt) |

### Parsed description sections (matched against template headings)

#### Required sections

| Section | Template heading | Present |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | Yes (content: "Not specified.") |
| Attachments | `### **Attachments**` | Yes (content: "None.") |

No required sections are missing.

**Description**

> The `compute_risk_score()` function in the risk engine divides by total dependencies
> instead of vulnerable dependencies, producing inflated risk scores for all assessments.

**Steps to Reproduce**

1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

**Expected Result**

> The risk score should be `5 / 100 = 0.05` (vulnerable / total).

**Actual Result**

> The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and
> denominator are swapped.

**Environment / Version**

> Not specified.

**Attachments**

> None.

#### Optional sections

| Section | Template heading | Present |
|---|---|---|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

No prior root cause analysis or suggested fix from the reporter.
