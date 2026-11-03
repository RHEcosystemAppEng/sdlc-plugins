# Step 1 – Data Extraction: TC-8001

## Step 0 – Configuration extracted (from claude-md-security-config-prodsec.md)

| Setting | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| ProdSec contact email | prodsec-team@example.com |
| ProdSec Jira account ID | 557058:prodsec-mock-account-id (used for the @mention in the Step 3 comment) |
| Upstream Affected Component field | not configured, so Steps 4.3 and 7 are skipped |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Step 0.3 matrix staleness: `Last-Updated: 2026-06-28T10:00:00Z` is more than 14 days before today (2026-11-03), so the matrix is stale. In an interactive run the engineer would get a choice of Refresh, Proceed or Stop. For this eval the triage proceeds with the current matrix.

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Status | New |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto (Rust crate) |
| Ecosystem | Cargo (source dependency, lock file `Cargo.lock`) |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | none |
| Deployment context (rhtpa-backend) | upstream (the default) |

## Stream Scope

The summary suffix `[rhtpa-2.2]` matches the configured Version Stream `2.2.x`, so the issue is **scoped** to 2.2.x.

## Step 1.5 – External enrichment

MITRE and OSV were not queried because this eval forbids external calls. The triage uses the Jira description data only.

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

## Step 1.7 – Embargo check

No Embargo policy URL is configured, so this step was skipped silently. The CVSS of 7.5 would otherwise have triggered the gate.
