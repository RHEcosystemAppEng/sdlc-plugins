# Step 1 – Data Extraction: TC-8001

Mode: interactive (FULLSEND_OUTPUT_DIR not set). Eval run: Jira, git, and WebFetch calls are simulated from the provided mock files. Nothing was sent to an external service.

## Step 0 – Configuration Validation (summary)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | https://example.com/security/embargo-policy (configured, so Step 1.7 is active) |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec Jira account ID | not configured (no @mentions) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). There is no Deployment Context column, so it defaults to `upstream`. |

All required sections are present, so the configuration is valid.

## Step 0.3 – Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-23) | Status |
|--------|--------------|------------------------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 148 days | STALE (threshold: 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 148 days | STALE (threshold: 14 days) |

> Security matrix for stream **2.1.x** / **2.2.x** was last updated on 2026-06-28 (148 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now, 2. Proceed anyway, 3. Stop

Eval assumption: **Proceed anyway**, using the provided mock matrix. Any 2.1.x/2.2.x releases after 2026-06-28 are not covered by this analysis.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field (does not match any configured stream, see Step 3) |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Vulnerability class | Denial of service (panic from unbounded stream-state allocation via STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-23) | `duedate` |
| Assignee | Unassigned (Step 0.8 would assign to the current user and move to Assigned) | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

- Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which is configured (Konflux repo `rhtpa-release.0.4.z`).
- Issue stream scope: **2.2.x** (scoped issue).

## Ecosystem Detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. It is listed in both streams' Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`).
- Category: **Source dependency**, so each stream gets 2 remediation tasks.

## Deployment Context

- Affected repository: rhtpa-backend (backend). It defaults to `upstream` because the Deployment Context column is absent. Because the column is absent, the Coordination Guidance subsection is left out of the remediation tasks (backward-compatibility rule).

## Step 1.5 – External CVE Data Enrichment

The MITRE CVE API and OSV.dev were not queried, per the eval instruction not to call external tools.

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed** (from the Jira description).
