# Step 0 / Step 1 — Configuration Validation and Bug Parsing: ACME-520

## Step 0 — Project Configuration (from claude-md-bug-config.md)

| Check | Result |
|---|---|
| `## Repository Registry` | Present — 1 entry: `acme-backend` (Rust backend service, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`) |
| `## Jira Configuration` | Present — Project key `ACME`, Cloud ID `mock-cloud-id-for-eval` |
| `## Code Intelligence` | Present — states "No Serena MCP servers are configured" (so Read/Grep/Glob fallback is used, despite the registry listing `serena_backend`) |
| `## Bug Configuration` | Present — Bug issue type ID `10020`, Bug template path `docs/templates/bug-template.md`, Bug-to-Task link type `Blocks` |

Configuration is complete. Proceeding.

Extracted values:
- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md (mock: bug-template-mock.md)
- **Bug-to-Task link type**: Blocks

## Step 0.5 — Jira Access

Eval mode: no Jira MCP or REST calls are made. All Jira operations are written to the output files.

## Step 1 — Fetch Bug

Would call: `jira.get_issue("ACME-520")` (simulated from bug-issue-persistence-impact.md)

### Issue type validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **Match** — issue is a Bug. Proceeding.

### Metadata

| Field | Value |
|---|---|
| Issue key | ACME-520 |
| Web URL | https://mock-jira.example.com/browse/ACME-520 |
| Summary | Risk scores are computed with wrong denominator, producing inflated values |
| Status | New |
| Labels | `reported-by-user` |
| Component | `risk-engine` |
| Affects Version/s | (none) — `versions` field is **not populated** (Step 4.5 will not take the keep/replace/augment branch) |

### Template heading formats (from bug template)

Required: `### **Issue Description**`, `### **Steps to Reproduce**`, `### **Expected Result**`, `### **Actual Result**`, `### **Environment / Version**`, `### **Attachments**`
Optional: `### **Root Cause**`, `### **Suggested Fix**`

### Parsed Required Sections

| Section | Present | Content |
|---|---|---|
| Description (`### **Issue Description**`) | Yes | The `compute_risk_score()` function in the risk engine divides by total dependencies instead of vulnerable dependencies, producing inflated risk scores for all assessments. |
| Steps to Reproduce | Yes | 1. Ingest an SBOM with 100 total dependencies, 5 of which are vulnerable. 2. Create a risk assessment for the ingested SBOM. 3. Retrieve the risk assessment via `GET /api/v2/assessments/{id}`. 4. Inspect the `risk_score` field. |
| Expected Result | Yes | The risk score should be `5 / 100 = 0.05` (vulnerable / total). |
| Actual Result | Yes | The risk score is `100 / 5 = 20.0` (total / vulnerable). The numerator and denominator are swapped. |
| Environment / Version | Yes | "Not specified." |
| Attachments | Yes | "None." |

All required sections are present — the bug follows the template. Proceeding to investigation.

### Parsed Optional Sections

| Section | Present | Content |
|---|---|---|
| Root Cause | No | — (reporter's Issue Description does hint at the cause: wrong denominator) |
| Suggested Fix | No | — |

### Notes for later steps

- **Environment / Version** contains no extractable version identifier ("Not specified.") — Step 4.5 will go straight to gap flagging (4.5.6).
- **Component** `risk-engine` narrows investigation to the risk module of `acme-backend`.
