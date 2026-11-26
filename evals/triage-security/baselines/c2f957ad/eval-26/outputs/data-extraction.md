# TC-8050 — Step 1 Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation: no Jira MCP, git, or WebFetch calls were made; all data comes from the fixture files.

## Step 0 — Configuration validation

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 are skipped) |
| Embargo policy URL | not configured (Step 1.7 is skipped) |
| ProdSec contact / account ID | not configured (no @mentions) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so triage proceeds.

## Step 0.3 — Matrix staleness check

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the matrix is **151 days old**, well past the 14-day threshold. The skill would warn the engineer here and offer three choices: Refresh now, Proceed anyway, or Stop. For this eval, triage continues with the current mock matrix ("Proceed anyway").

## Parsed CVE data

| Field | Value |
|---|---|
| Issue key | TC-8050 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-99001 (from label and summary) |
| Summary | CVE-2026-99001 criterion - Path traversal in benchmark output [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion (Rust crate) |
| Affected version range | < 0.5.2 ("versions before 0.5.2") |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | none in remote links |
| Advisory URL | none (no GHSA link) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Assignee | Unassigned. Step 0.8 would assign it to the current user and move it to Assigned. |
| Existing comments | none |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which is a configured stream (rhtpa-release.0.4.z).
- The issue is **scoped** to 2.2.x. The 2.1.x stream is out of scope and is handled through Case A (cross-stream).

## Ecosystem detection

- criterion is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the Ecosystem Mappings for both streams.
- Category: source dependency. Each stream gets two remediation tasks.

## Deployment context

- The affected repo is the backend (rhtpa-backend). The Source Repositories table has no Deployment Context column, so the context defaults to `upstream`.
- For backward compatibility, Coordination Guidance is left out of the task descriptions.

## Step 1.5 — External CVE enrichment

MITRE and OSV were not queried in this eval simulation.
> "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."

Fix threshold in use: **criterion < 0.5.2, fixed in 0.5.2** (from the Jira description).

## Step 1.7 — Embargo check

Skipped for two reasons: no Embargo policy URL is configured, and CVSS 5.3 is below the 7.0 threshold.
