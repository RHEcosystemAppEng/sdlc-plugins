# Step 1 – Data Extraction: TC-8051

**Mode:** Interactive (`FULLSEND_OUTPUT_DIR` not set). For this eval, Jira MCP, `git show`, and WebFetch were not called. All data comes from the fixture files.

## Step 0 – Configuration Validation

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 (configured) |
| Upstream Affected Component field | not configured, so Step 4.3 and Step 7 are skipped |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required Security Configuration sections are present.

## Step 0.3 – Matrix Staleness Check

The security matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the matrix is **151 days old**, well past the 14-day threshold.

> Security matrix for stream **2.1.x / 2.2.x** was last updated on 2026-06-28 (151 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

For this eval the triage takes option 2 (**Proceed anyway**) with the fixture matrix.

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8051 | Issue |
| Issue status | New (full triage path) | Issue |
| CVE ID | CVE-2026-99002 | Label `CVE-2026-99002` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Affected repository | rhtpa-backend (`backend` in the security matrix) | Component plus Ecosystem Mappings |
| Deployment context | upstream (default, because the column is absent) | Source Repositories |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (matches Version Streams row `rhtpa-release.0.4.z`) | Stream scope resolution |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | rustls | Description |
| Ecosystem | Cargo (source dependency, Rust crate) | Library name plus Ecosystem Mappings |
| Affected version range | < 0.23.5 ("versions before 0.23.5") | Description |
| Fixed version | 0.23.5 | Description |
| CVSS | 8.1 (High) | Description |
| Vulnerability summary | Certificate validation bypass: improper server certificate validation with custom certificate verifiers allows MITM with an invalid chain | Summary and description |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 (rustls/rustls#2100) | Remote links |
| Advisory URL | none (no GHSA link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 | Remote links |
| Due date | 2026-08-01 (already past) | `duedate` |
| Assignee | Unassigned. Step 0.8 would assign the current user and move New to Assigned after confirmation; not done in this eval | Issue |
| Existing comments | none | Comments |

All critical fields (CVE ID, library, affected range) were parsed. No input from the engineer is needed.

## Step 1.5 – External CVE Data Enrichment

The MITRE (`cveawg.mitre.org/api/cve/CVE-2026-99002`) and OSV.dev (`api.osv.dev/v1/vulns/CVE-2026-99002`) lookups were **not called** because this eval forbids external calls.

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

**Fix threshold used:** rustls < 0.23.5 (fixed in 0.23.5), taken from the Jira description.

## Step 1.7 – Embargo Check

CVSS 8.1 meets the threshold (>= 7.0), but no Embargo policy URL is configured, so this step is skipped silently.
