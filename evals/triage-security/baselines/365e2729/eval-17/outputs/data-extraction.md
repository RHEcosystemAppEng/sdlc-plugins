# TC-8001 — Triage: Configuration and Data Extraction

Mode: **interactive** (`FULLSEND_OUTPUT_DIR` not set; Step 0.7 skipped).
Eval simulation: no Jira MCP, `git show` or WebFetch calls were made. All data comes from the provided input files.

## Step 0 – Validate Project Configuration

Every required section is present in `claude-md-security-config-embargo.md`:

| Section | Status |
|---|---|
| Repository Registry | Present (rhtpa-backend) |
| Jira Configuration | Present (Project key, Cloud ID) |
| Code Intelligence | Present (serena_backend) |
| Security Configuration → Product Lifecycle | Present |
| Security Configuration → Version Streams | Present (2 streams) |
| Security Configuration → Source Repositories | Present (1 repo) |

Extracted configuration values:

| Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field (optional) | customfield_12345 |
| **Embargo policy URL (optional)** | **https://example.com/security/embargo-policy** (configured, so Step 1.7 is active) |
| Upstream Affected Component field (optional) | Not configured. Step 4.3 and Step 7 are skipped |
| PS Component / Stream custom fields (optional) | Not configured |
| ProdSec contact email / Jira account ID (optional) | Not configured. @mentions skipped silently |
| Version Streams | 2.1.x → git.example.com/rhtpa/rhtpa-release.0.3.z; 2.2.x → git.example.com/rhtpa/rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend, deployment context: `upstream` (default, because the Deployment Context column is absent) |

Missing optional fields are not errors. Extraction ran without raising any.

## Step 0.3 – Matrix Staleness Check

- Matrix `Last-Updated`: 2026-06-28T10:00:00Z. Today is 2026-11-26, so the matrix is **151 days old**, well past the 14-day threshold.
- Warning shown to the engineer:

  > Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (151 days ago). The matrix may not reflect recent releases.
  > Options: 1. Refresh now  2. Proceed anyway  3. Stop

- Simulated engineer choice: **Proceed anyway**. This eval has no repo access for a refresh. Any 2.1.x/2.2.x releases after 2026-06-28 are not reflected below.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Assign TC-8001 to the current user. Transition New → Assigned through dynamically discovered transitions. Both need engineer confirmation.

## Step 1 – Data Extraction

| Field | Value |
|---|---|
| Issue key | TC-8001 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` → rhtpa-backend (backend) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS / Severity | 7.5 (High) |
| Vulnerability type | Denial of service (panic on an excessive STREAMS frame) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | None |

### Stream scope resolution

- Summary suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (rhtpa-release.0.4.z).
- Issue type: **scoped** to 2.2.x. Other affected streams go through Case A, the cross-stream/preemptive path.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo appears in both streams' Ecosystem Mappings.
- Category: source dependency. Remediation is 2 tasks per stream (upstream backport or dependency bump, plus downstream propagation).

### Deployment context

- rhtpa-backend: `upstream` (default, because the Source Repositories table has no Deployment Context column). Following remediation-templates.md, no Coordination Guidance subsection is added when the column is absent.

## Step 1.5 – External CVE Data Enrichment

The MITRE CVE API and OSV.dev were **not queried** because the eval forbids external calls. Both are treated as unavailable:

> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.** This comes from the Jira description.
