# TC-8001 — Step 0 / Step 1 Data Extraction

## Step 0 — Configuration Validation (claude-md-security-config-embargo.md)

All required sections present: Repository Registry, Jira Configuration, Code Intelligence,
Security Configuration (Product Lifecycle, Version Streams, Source Repositories). Proceeding.

| Config field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| **Embargo policy URL** (optional) | **https://example.com/security/embargo-policy** — present, extracted; Step 1.7 is enabled |
| Upstream Affected Component field | not configured — Steps 4.3 and 7 skipped |
| ProdSec contact / account ID | not configured — skipped silently |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`; coordination guidance omitted for backward compatibility) |

Optional fields that are absent did not cause an error. The Embargo policy URL is an optional
field. It is present here, so it was extracted without changing how the other fields are validated.

## Step 0.3 — Matrix Staleness Check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-04, so the matrix is **129 days old**.
That is past the 14-day threshold. Warning presented:

> Security matrix for streams **2.1.x / 2.2.x** was last updated on 2026-06-28 (129 days ago).
> The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Simulated engineer choice: **Proceed anyway**. This is an eval, and no refresh is possible.

## Step 0.6 — Mode: interactive (FULLSEND_OUTPUT_DIR absent)

## Step 1 — Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8001 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| Severity | CVSS 7.5 (High) |
| Vulnerability type | Denial of service (panic on excessive STREAMS frame stream count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned. Step 0.8 would assign it to the current user and transition it to Assigned after confirmation. Not executed in this eval. |
| Existing comments | none |

### Stream scope resolution
Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which is configured, so the issue is **scoped** to 2.2.x.

### Ecosystem
quinn-proto is a Rust crate, so the ecosystem is **Cargo**. It is a source dependency, which means 2 tasks per stream. Cargo is listed in both streams' Ecosystem Mappings.

### Deployment context
Repository rhtpa-backend ("backend"). The Source Repositories table has no Deployment Context column, so the context defaults to `upstream`. Coordination guidance is omitted because the column is absent.

## Step 1.5 — External CVE Enrichment
MITRE and OSV were not queried, because the eval forbids external calls. The skill treats both
sources as unavailable:

> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.**
