# Step 1 – Data Extraction: TC-8051

## Pre-flight

- **Step 0 (Configuration):** passed. Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, component label pattern `pscomponent:`, VEX Justification custom field `customfield_12345`. Version Streams: `2.1.x` (rhtpa-release.0.3.z) and `2.2.x` (rhtpa-release.0.4.z). Source repository: `rhtpa-backend`.
  - Optional fields not configured: Upstream Affected Component field, PS Component field, Stream field, ProdSec contact or account ID, Embargo policy URL.
- **Step 0.3 (Matrix staleness):** the matrix says `Last-Updated: 2026-06-28T10:00:00Z`, which is **129 days old** as of 2026-11-04. That is past the 14-day threshold. The engineer would normally choose Refresh, Proceed or Stop here. For this eval, triage proceeds with the current matrix.
- **Step 0.6 (Mode):** interactive mode (`FULLSEND_OUTPUT_DIR` not set).
- **Step 0.8 (Assign / transition):** proposed only, not run. Assign TC-8051 to the current user and move it from New to Assigned.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8051 |
| Summary | CVE-2026-99002 rustls - Certificate validation bypass [rhtpa-2.2] |
| Status | New (full triage path) |
| CVE ID | CVE-2026-99002 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls (Rust crate) |
| Affected version range | < 0.23.5 ("versions before 0.23.5") |
| Fixed version | 0.23.5 |
| CVSS / Severity | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | None (no GHSA or advisory remote link) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 (already past as of 2026-11-04) |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Scope | **Scoped**. Steps 3–8 cover the 2.2.x stream only. |

## Ecosystem Detection

| Item | Value |
|------|-------|
| Ecosystem | Cargo (Rust crate) |
| Listed in the stream's Ecosystem Mappings? | Yes. 2.2.x: Cargo / backend / `Cargo.lock` / `git show <tag>:Cargo.lock` / upstream branch `release/0.4.z` |
| Category | Source dependency: 2 remediation tasks per stream if remediation goes ahead |

## Deployment Context

| Item | Value |
|------|-------|
| Affected repository | rhtpa-backend (the backend component; label `org/rhtpa-server`) |
| Deployment context | `upstream` (default, because the Source Repositories table has no Deployment Context column) |

## Step 1.5 – External CVE Data Enrichment

The MITRE CVE API and OSV.dev were **not queried** because this eval does not allow external calls. With both sources unavailable, the Jira description data is used as is:

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

**Fix threshold used for Step 2:** rustls < 0.23.5 is affected; 0.23.5 is fixed.

## Step 1.7 – Embargo Check

Skipped. No Embargo policy URL is configured in Security Configuration. CVSS 8.1 would otherwise have met the threshold of 7.0 or higher.
