# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-520)

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | `acme-backend` — Rust backend service — Serena: `serena_backend` — `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key: `ACME`; Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Present | States no Serena MCP servers are configured; fall back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md`; Bug-to-Task link type: `Blocks` |

Result: configuration is complete, so triage continues.

## Step 0.5 — Jira Access

Simulated for the eval: no MCP or REST calls were made. The issue data comes from `bug-issue-persistence-impact.md`.

## Step 1 — Fetch Bug

### Issue type validation

- Issue `issuetype.id`: `10020` (Bug)
- Configured Bug issue type ID: `10020`
- Result: **match**. The issue is a Bug, so triage continues.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-520 |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Status | New |
| Labels | `reported-by-user` |
| Component | `risk-engine` |
| Affects Version/s | (none). The `versions` field is **not populated**, so Step 4.5 does not run the keep/replace/augment prompt. |

### Template headings used (from bug-template-mock.md)

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`, `### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

### Parsed Required Sections

#### Description (`### **Issue Description**`)
The `compute_risk_score()` function in the risk engine divides by total dependencies instead of vulnerable dependencies, producing inflated risk scores for all assessments.

#### Steps to Reproduce (`### **Steps to Reproduce**`)
1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

#### Expected Result (`### **Expected Result**`)
The risk score should be `5 / 100 = 0.05` (vulnerable / total).

#### Actual Result (`### **Actual Result**`)
The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped.

#### Environment / Version (`### **Environment / Version**`)
Not specified.

#### Attachments (`### **Attachments**`)
None.

### Parsed Optional Sections

- **Root Cause**: not present
- **Suggested Fix**: not present

### Completeness check

All required sections are present, so triage continues.

Note: the Environment / Version section is present but has no version value ("Not specified"). Step 4.5 will flag this gap.
