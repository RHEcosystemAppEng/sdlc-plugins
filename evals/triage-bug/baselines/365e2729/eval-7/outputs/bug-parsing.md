# Step 0 / Step 1 — Configuration Validation and Bug Parsing: ACME-520

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | `acme-backend` (Rust backend service), Serena instance `serena_backend`, path `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key: `ACME`; Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Present | No Serena MCP servers configured — fall back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md`; Bug-to-Task link type: `Blocks` |

All required configuration is present. Proceeding.

## Step 1 — Fetch Bug

Simulated `jira.get_issue("ACME-520")` (not called; data taken from bug-issue-persistence-impact.md).

### Issue type validation

- Issue type: Bug, `issuetype.id` = `10020`
- Configured Bug issue type ID = `10020`
- Result: **match** — proceed.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-520 |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Status | New |
| Labels | `reported-by-user` |
| Component | `risk-engine` |
| Affects Version/s | (none) — `affectsVersions` field is **not populated** (Step 4.5 will not need keep/replace/augment prompt) |

### Template headings used for parsing (bug-template-mock.md)

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`,
`### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

### Parsed Required Sections

#### Description (`### **Issue Description**`) — PRESENT

The `compute_risk_score()` function in the risk engine divides by total dependencies
instead of vulnerable dependencies, producing inflated risk scores for all assessments.

#### Steps to Reproduce (`### **Steps to Reproduce**`) — PRESENT

1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

#### Expected Result (`### **Expected Result**`) — PRESENT

The risk score should be `5 / 100 = 0.05` (vulnerable / total).

#### Actual Result (`### **Actual Result**`) — PRESENT

The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.

#### Environment / Version (`### **Environment / Version**`) — PRESENT

Not specified.

(Note: section is present but contains no version identifier — this will trigger the
Affects Version gap flag in Step 4.5.6.)

#### Attachments (`### **Attachments**`) — PRESENT

None.

### Parsed Optional Sections

| Section | Status |
|---|---|
| Root Cause | Absent — no prior analysis from reporter |
| Suggested Fix | Absent — no proposed solution from reporter |

### Completeness check

All required sections are present. No missing sections — investigation can proceed.
