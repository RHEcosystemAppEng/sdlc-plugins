# Step 1 – Data Extraction: TC-8051

> Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval run: Jira MCP was not called.
> The data below was parsed from the mock issue fixture (`vuln-issue-feature-gated.md`).

## Step 0 – Configuration (validated)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 (configured) |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Upstream Affected Component field | not configured, so Steps 4.3 and 7 are skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

## Step 0.3 – Matrix Staleness Check

The security matrix has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. That is **128 days**
before today (2026-11-03), well past the 14-day threshold.

> Security matrix for stream **2.2.x** (and 2.1.x) was last updated on 2026-06-28
> (128 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now**: re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway**: continue triage with the current matrix
> 3. **Stop**: halt triage so I can investigate

For this eval, triage proceeds with the current matrix (option 2). Any 2.2.x
release after 2.2.4 (2026-05-04) is NOT covered by this analysis.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8051 |
| Summary | CVE-2026-99002 rustls - Certificate validation bypass [rhtpa-2.2] |
| Status | New (full triage path) |
| CVE ID | CVE-2026-99002 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Affected repository | rhtpa-backend (`backend` in the matrix) |
| Deployment context | upstream (default, because the Source Repositories table has no Deployment Context column) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Ecosystem | Cargo (Rust crate), a source dependency, so 2 remediation tasks per stream if remediation proceeds |
| Affected version range | < 0.23.5 ("versions before 0.23.5") |
| Fixed version | 0.23.5 |
| Severity | CVSS 8.1 (High) |
| Vulnerability | Improper server certificate validation with custom certificate verifiers (MITM) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | none provided (no GHSA link) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 (already past as of 2026-11-03) |
| Assignee | Unassigned (Step 0.8 would assign to the current user and transition New to Assigned; not executed in this eval) |
| Existing comments | none |

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (rhtpa-release.0.4.z), which matches a configured Version Stream |
| Issue stream scope | **Scoped to 2.2.x** |

## Step 1.5 – External CVE Data Enrichment

The eval constraints did not allow MITRE CVE API or OSV.dev queries, so both external
sources are treated as unavailable.

> ⚠ External CVE databases unavailable. Using Jira description data only.
> Fix threshold confidence is reduced.

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 0.23.5 | 0.23.5 |
| MITRE CVE API | unavailable | unavailable |
| OSV.dev | unavailable | unavailable |

**Fix threshold used for Step 2:** rustls < 0.23.5 is vulnerable. 0.23.5 is fixed.

## Step 1.7 – Embargo Check

No Embargo policy URL is configured in Security Configuration, so this step was skipped
silently. CVSS 8.1 would otherwise have triggered the gate.
