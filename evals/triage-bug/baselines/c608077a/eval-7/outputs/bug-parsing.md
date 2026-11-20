# Step 0 / Step 1 — Configuration Validation and Bug Parsing (ACME-520)

## Step 0 — Configuration validation

Source: project CLAUDE.md (`claude-md-bug-config.md`)

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present (1 entry) | `acme-backend` — Rust backend service — Serena: `serena_backend` — Path: `/home/dev/repos/acme-backend` |
| Jira Configuration | Present | Project key: `ACME`; Cloud ID: `mock-cloud-id-for-eval` |
| Code Intelligence | Present | No Serena MCP servers configured, so investigation falls back to Read/Grep/Glob |
| Bug Configuration | Present | Bug issue type ID: `10020`; Bug template path: `docs/templates/bug-template.md`; Bug-to-Task link type: `Blocks` |

Result: the configuration is valid, so the skill proceeds.

## Step 0.5 — Jira access

This is an eval run, so no Jira MCP or REST calls are made. The skill would call `jira.get_issue("ACME-520")`. Here the issue content comes from `bug-issue-persistence-impact.md`.

## Step 1 — Fetch Bug

### Issue type validation

- Issue `issuetype.id`: `10020` (Bug)
- Configured Bug issue type ID: `10020`
- Result: **match**. Proceeding.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-520 |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Status | New |
| Labels | `reported-by-user` |
| Component | `risk-engine` |
| Affects Version/s | (none). The `versions` field is **not populated**, so Step 4.5 does not need the keep/replace/augment prompt. |

### Template heading formats used for parsing

Template: `docs/templates/bug-template.md` (mock: `bug-template-mock.md`)

| Section | Heading format | Kind |
|---|---|---|
| Description | `### **Issue Description**` | Required |
| Steps to reproduce | `### **Steps to Reproduce**` | Required |
| Expected Result | `### **Expected Result**` | Required |
| Actual Result | `### **Actual Result**` | Required |
| Environment / Version | `### **Environment / Version**` | Required |
| Attachments | `### **Attachments**` | Required (template) |
| Root Cause | `### **Root Cause**` | Optional |
| Suggested Fix | `### **Suggested Fix**` | Optional |

### Parsed sections

#### Description (Required): present

> The `compute_risk_score()` function in the risk engine divides by total dependencies
> instead of vulnerable dependencies, producing inflated risk scores for all assessments.

#### Steps to Reproduce (Required): present

1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable.
2. Create a risk assessment for the ingested SBOM.
3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`.
4. Inspect the `risk_score` field.

#### Expected Result (Required): present

> The risk score should be `5 / 100 = 0.05` (vulnerable / total).

#### Actual Result (Required): present

> The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and
> denominator are swapped.

#### Environment / Version (Required): present

> Not specified.

The section exists but contains no version identifier. Step 4.5 treats this as a gap.

#### Attachments (Required by template): present

> None.

#### Root Cause (Optional): absent

#### Suggested Fix (Optional): absent

### Completeness check

All required sections are present, so no missing sections are reported and the skill proceeds to investigation.

Note: the summary says "wrong denominator". The Actual Result is more precise: the numerator and denominator are **swapped**. The function computes `total / vulnerable` instead of `vulnerable / total`.
