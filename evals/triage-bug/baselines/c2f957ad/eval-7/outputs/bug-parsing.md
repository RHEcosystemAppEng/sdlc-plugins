# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-520)

## Step 0 — Configuration Validation

Source: `claude-md-bug-config.md` (project CLAUDE.md)

| Required section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present (1 entry) | `acme-backend` — Rust backend service — Serena: `serena_backend` — Path: `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key: `ACME`; Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Present | No Serena MCP servers configured — fall back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md`; Bug-to-Task link type: `Blocks` |

Result: configuration is complete — proceed.

## Step 1 — Fetch Bug

(Simulated `jira.get_issue("ACME-520")` — data taken from `bug-issue-persistence-impact.md`.)

### Issue type validation

- Issue `issuetype.id`: `10020` (Bug)
- Configured Bug issue type ID: `10020`
- Result: **match** — issue is a Bug, proceed.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-520 |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Status | New |
| Labels | `reported-by-user` |
| Component | `risk-engine` |
| Affects Version/s | (none) — `affectsVersions` is **not populated** (Step 4.5 must not skip) |

### Parsed description sections

Heading formats taken from the bug template (`bug-template-mock.md`).

#### Required sections

| Section | Heading matched | Status |
|---|---|---|
| Description | `### **Issue Description**` | Present |
| Steps to Reproduce | `### **Steps to Reproduce**` | Present |
| Expected Result | `### **Expected Result**` | Present |
| Actual Result | `### **Actual Result**` | Present |
| Environment / Version | `### **Environment / Version**` | Present (content: "Not specified.") |
| Attachments | `### **Attachments**` | Present (content: "None.") |

All required sections are present — no missing-section stop condition.

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

(No extractable version identifier — this will trigger the Step 4.5.6 gap flag.)

**Attachments**

> None.

#### Optional sections

| Section | Status |
|---|---|
| Root Cause | Not present |
| Suggested Fix | Not present |
