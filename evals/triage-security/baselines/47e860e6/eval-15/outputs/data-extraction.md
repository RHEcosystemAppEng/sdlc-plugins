# Step 1 – Data Extraction: TC-8001

Mode: interactive (simulated; `FULLSEND_OUTPUT_DIR` absent). Source: mock Jira issue data (vuln-issue-standard.md).

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) |
| Assignee | Unassigned |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` -> stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (Rust crate) -- source dependency (2 tasks per stream) |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| Severity | CVSS 7.5 (High) -- DoS |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | none |
| Deployment context | upstream (Source Repositories table has no Deployment Context column -> default) |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` -> stream `2.2.x`, which matches a configured Version Stream (rhtpa-release.0.4.z).
- Issue is **scoped** to stream **2.2.x**.

## Configuration notes (Step 0)

- Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Jira version prefix RHTPA, Vulnerability issue type 10024, VEX field customfield_12345.
- ProdSec contact email: prodsec-team@example.com; ProdSec Jira account ID: 557058:prodsec-mock-account-id (used for @mention in Step 3).
- Upstream Affected Component field not configured -> Steps 4.3 and 7 skipped. Embargo policy URL not configured -> Step 1.7 skipped.

## Step 1.5 – External enrichment

Not executed (eval forbids external calls). Proceeding with Jira description data only:
"External CVE databases unavailable -- using Jira description data only. Fix threshold confidence is reduced." Fix threshold used: 0.11.14.

## Step 0.3 – Matrix staleness

Matrix Last-Updated 2026-06-28T10:00:00Z, more than 14 days before today (2026-11-04, ~129 days). Staleness warning would be raised; for this eval we proceed with the current matrix.
