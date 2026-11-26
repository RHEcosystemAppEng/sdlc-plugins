# Step 1 – Data Extraction: TC-8003

Source: mock Jira issue (`vuln-issue-duplicate.md`). No Jira MCP / REST calls were made (eval mode).

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 are skipped) |
| PS Component / Stream custom fields | not configured |
| ProdSec contact / Jira account ID | not configured (no @mentions) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present: Repository Registry, Jira Configuration, Code Intelligence, Security Configuration (Product Lifecycle, Version Streams, Source Repositories). Validation passes.

## Step 0.3 – Matrix Staleness Check

- `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the matrix is about 151 days old, over the 14-day threshold.
- **Warning:** the security matrix for streams 2.1.x and 2.2.x may be missing recent releases (the newest listed is 2.2.4, built 2026-05-04). Options: Refresh now / Proceed anyway / Stop. In this eval, triage **proceeds with the current matrix**. This does not change the outcome here because the result is a duplicate closure.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Status is `New` and the issue is unassigned. Proposed actions: assign to the current user, then transition to `Assigned`.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8003 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto (Rust crate) |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| Severity | CVSS 7.5 (High), DoS |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | none |
| Assignee | Unassigned |

All critical fields (CVE ID, library, affected range) were parsed successfully.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to stream 2.2.x.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo appears in the 2.2.x Ecosystem Mappings (lock file `Cargo.lock`, upstream branch `release/0.4.z`).
- Category: source dependency, which would mean 2 remediation tasks per stream if remediation were needed.

### Deployment context

- Affected repo: backend (rhtpa-backend). There is no Deployment Context column, so it defaults to `upstream`.

## Step 1.5 – External CVE Enrichment

- Not executed. External calls are prohibited in this eval. Jira description data is used as the fix threshold (< 0.11.14, fixed in 0.11.14), with reduced confidence noted.

## Step 1.7 – Embargo Check

- Skipped because no Embargo policy URL is configured. (CVSS 7.5 would otherwise meet the threshold.)

## Step 2 – Version Impact Analysis (simulated lock file data from security-matrix-mock.md)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? | Notes |
|--------|---------|-------------|-------------|-----------------------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | out of issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | out of issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version shipped |

- Development stream (Step 2.2): could not be determined because Jira was not queried for unreleased versions. Upstream branch `release/0.4.z` already ships 0.11.14 as of v0.4.11 (Step 2.5: the fix is available upstream).
- **In-scope (2.2.x) affected versions:** RHTPA 2.2.0, 2.2.1, 2.2.2.
- **Out-of-scope affected:** RHTPA 2.1.0, 2.1.1 (stream 2.1.x).

## Step 3 – Affects Versions Correction (assessment)

- Current: `[RHTPA 2.2.0]`. Lock-file-based proposal: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
- This correction is **superseded by the Step 4 duplicate finding**. TC-8003 will be closed as a Duplicate, so its Affects Versions are not edited. The correction is redirected to the surviving issue TC-7999 (see duplicate-check.md).
