# Step 1 – Data Extraction: TC-8051

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 (configured) |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Mode: interactive (FULLSEND_OUTPUT_DIR not set). Every required Security Configuration section is present.

## Step 0.3 – Matrix staleness check

Both stream matrices have `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-06, so the matrices are **131 days old**, which is past the 14-day threshold.

> Security matrix for stream **2.1.x** and **2.2.x** was last updated on 2026-06-28 (131 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now / 2. Proceed anyway / 3. Stop

For this eval, triage continues with the current matrix (option 2).

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8051 | Issue |
| Issue status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-99002 | Label `CVE-2026-99002` and summary |
| Summary | CVE-2026-99002 rustls - Certificate validation bypass [rhtpa-2.2] | Issue summary |
| Affected component | `pscomponent:org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | rustls | Description |
| Affected version range | < 0.23.5 ("versions before 0.23.5") | Description |
| Fixed version | 0.23.5 | Description |
| CVSS | 8.1 (High) | Description |
| Vulnerability | Improper server certificate validation when custom certificate verifiers are used, which allows MITM with an invalid certificate chain | Description |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 (rustls/rustls#2100) | Remote links |
| Advisory URL | none provided (no GHSA link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 | Remote links |
| Due date | 2026-08-01 | `duedate` field |
| Assignee | Unassigned. Step 0.8 would assign it to the current user and move it to Assigned (simulated, not executed) | Issue |
| Existing comments | none | Comment history |

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (rhtpa-release.0.4.z) |
| Issue stream scope | **Scoped to 2.2.x**. Steps 3–8 are scoped to this stream; other streams are considered only for Case A cross-stream impact |

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | Cargo (Rust crate `rustls`) |
| Listed in stream Ecosystem Mappings? | Yes. Cargo / backend / `Cargo.lock` / `release/0.4.z` |
| Category | Source dependency (2 remediation tasks per stream if remediation proceeds) |
| Affected repository | backend (rhtpa-backend) |
| Deployment context | upstream (default; the Source Repositories table has no Deployment Context column) |

## Step 1.5 – External CVE data enrichment

The eval forbids external calls, so MITRE (`cveawg.mitre.org/api/cve/CVE-2026-99002`) and OSV.dev (`api.osv.dev/v1/vulns/CVE-2026-99002`) were not queried.

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **rustls < 0.23.5 is affected; fixed in 0.23.5** (from the Jira description).

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured, even though CVSS 8.1 is above the threshold.

All critical fields (CVE ID, library, affected range) were parsed, so triage proceeds to Step 2.
