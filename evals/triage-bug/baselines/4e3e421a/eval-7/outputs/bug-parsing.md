# Step 0 / Step 1 — Configuration Validation and Bug Parsing: ACME-520

## Step 0 — Project Configuration (from CLAUDE.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | `acme-backend` (Rust backend service, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`) | Present |
| Project key | `ACME` | Present |
| Cloud ID | `mock-cloud-id-for-eval` | Present |
| Code Intelligence | Section present (states no Serena MCP servers configured -> Read/Grep/Glob fallback) | Present |
| Bug issue type ID | `10020` | Present |
| Bug template path | `docs/templates/bug-template.md` | Present |
| Bug-to-Task link type | `Blocks` | Present |

All required configuration is present. Proceeding.

## Step 0.5 — Jira Access

Eval mode: no Jira MCP / REST calls are made. All Jira operations are simulated and written to files.

## Step 1 — Fetch Bug

### Issue type validation

- Issue `issuetype.id`: `10020` (Bug)
- Configured Bug issue type ID: `10020`
- Result: **match** — proceed.

### Metadata

| Field | Value |
|---|---|
| Key | ACME-520 |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Status | New |
| Labels | `reported-by-user` |
| Component | `risk-engine` |
| Affects Version/s | (none) — `versions` field is **not populated** (Step 4.5 will not need the keep/replace/augment prompt) |

### Parsed description sections (matched against template heading formats)

#### Required Sections

| Section | Template heading | Found |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | Yes (content: "Not specified.") |
| Attachments | `### **Attachments**` | Yes (content: "None.") |

**Description**

> The `compute_risk_score()` function in the risk engine divides by total dependencies
> instead of vulnerable dependencies, producing inflated risk scores for all assessments.

**Steps to Reproduce**

> 1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
> 2. Create a risk assessment for the ingested SBOM.
> 3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
> 4. Inspect the `risk_score` field.

**Expected Result**

> The risk score should be `5 / 100 = 0.05` (vulnerable / total).

**Actual Result**

> The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and
> denominator are swapped.

**Environment / Version**

> Not specified.

**Attachments**

> None.

#### Optional Sections

| Section | Found |
|---|---|
| Root Cause | Not present |
| Suggested Fix | Not present |

### Completeness check

All required sections are present. The bug report is complete and investigation can proceed.

Note: the Environment / Version section is present but contains no version identifier ("Not specified.") — this will trigger the Affects Version gap flag in Step 4.5.6.
