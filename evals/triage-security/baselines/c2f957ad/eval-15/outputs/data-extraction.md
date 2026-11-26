# Step 1 — Data Extraction for TC-8001

## Step 0 — Configuration extracted (from claude-md-security-config-prodsec.md)

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
| ProdSec Jira account ID | 557058:prodsec-mock-account-id |
| Upstream Affected Component custom field | not configured (Step 4.3 and Step 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend); no Deployment Context column, so it defaults to `upstream` |

All required sections are present (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration). Validation passed.

**Step 0.3 (matrix staleness):** `Last-Updated: 2026-06-28T10:00:00Z` is older than 14 days. In an interactive run the engineer would be asked to Refresh, Proceed, or Stop. For this eval the run proceeds with the supplied mock matrix.

**Step 0.8:** In an interactive run, TC-8001 (status New, Unassigned) would be assigned to the current user and moved to Assigned. Not executed in this eval.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| CVE ID | CVE-2026-31812 (label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Status | New |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to 2.2.x. Steps 3 and 4 apply to this stream only. Other affected streams go through Case A.

## Ecosystem Detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (lock file `Cargo.lock`, repository `backend`).
- Category: **source dependency**, which means 2 remediation tasks per stream.

## Deployment Context

- Affected repository: rhtpa-backend. No Deployment Context column exists, so it defaults to **upstream**.

## Step 1.5 — External CVE Enrichment

External tools were not called in this eval. MITRE and OSV were treated as unavailable, so the run falls back to the Jira description's threshold (fixed in 0.11.14).
> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

## Step 1.7 — Embargo Check

Skipped because no Embargo policy URL is configured.
