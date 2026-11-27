# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-520)

## Step 0 — Configuration Validation

Source: `claude-md-bug-config.md` (project CLAUDE.md)

| Section | Present | Extracted values |
|---|---|---|
| Repository Registry | Yes | `acme-backend` — Rust backend service — Serena: `serena_backend` — Path: `/home/dev/repos/acme-backend` |
| Jira Configuration | Yes | Project key: `ACME`; Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Yes | Naming convention section present (no live Serena servers; Read/Grep/Glob fallback applies) |
| Bug Configuration | Yes | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md` (mock: `bug-template-mock.md`); Bug-to-Task link type: `Blocks` |

Result: configuration complete — proceed.

## Step 1 — Fetch Bug (simulated `jira.get_issue("ACME-520")`)

### Issue type validation

- Issue `issuetype.id`: `10020` (Bug)
- Configured Bug issue type ID: `10020`
- Result: **match** — proceed.

### Metadata

| Field | Value |
|---|---|
| Key | ACME-520 |
| webUrl | https://mock-jira.example.com/browse/ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Status | New |
| Labels | `reported-by-user` |
| Component | `risk-engine` |
| Affects Version/s | (none) — `versions` field NOT populated (Step 4.5 will not need keep/replace/augment prompt) |

### Template headings (from bug template)

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`,
`### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

### Parsed Required Sections

**Description** (`### **Issue Description**`)
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

### Parsed Optional Sections

- **Root Cause**: not present
- **Suggested Fix**: not present

### Completeness check

All required sections present (Description, Steps to Reproduce, Expected Result,
Actual Result, Environment / Version, Attachments). No missing sections — proceed to
investigation.

Note: the Environment / Version section contains no version identifier ("Not specified."),
which will trigger the Affects Version gap flag in Step 4.5.6.
