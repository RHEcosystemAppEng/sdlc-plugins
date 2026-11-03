# Step 1 – Data Extraction: TC-8050

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Simulated eval — no Jira, git, or external calls were made; all data comes from the fixture files.

## Step 0 – Configuration validation

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| ProdSec contact / account ID | not configured (no @mentions) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). There is no Deployment Context column, so the default is `upstream`. Coordination guidance is left out of the tasks to keep older configs working. |

## Step 0.3 – Matrix staleness check

The security matrix says `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-03, so the matrix is **128 days old**, well past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (128 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

For this eval: **Proceed anyway**, using the fixture matrix. Any 2.2.x release after 2.2.4 is not in the matrix and has not been assessed.

## Step 0.8 – Assign and transition (proposed, not executed)

- Assign TC-8050 to the current triager.
- Move it from New to Assigned. Find the transition ID at runtime; do not hardcode it.

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8050 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-99001 (from the label and the summary) |
| Summary | CVE-2026-99001 criterion - Path traversal in benchmark output [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` → repository rhtpa-backend (Ecosystem Mappings repo: `backend`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion (Rust crate) |
| Ecosystem | Cargo (source dependency → 2 remediation tasks per stream) |
| Affected version range | < 0.5.2 ("versions before 0.5.2") |
| Fixed version | 0.5.2 |
| Severity | CVSS 5.3 (Medium) |
| Vulnerability | Path traversal: crafted benchmark names containing path separators let benchmark output files be written to arbitrary paths |
| Upstream fix PR | None in remote links |
| Advisory URL (GHSA) | None in remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 (already past) |
| Assignee | Unassigned |
| Existing comments | None |
| Deployment context | upstream (default; no column configured) |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x. Steps 3 and 4 cover only 2.2.x. Impact on 2.1.x is handled in Case A (cross-stream impact).

## Step 1.5 – External CVE data enrichment

This eval does not call MITRE or OSV.dev, which counts as "unavailable".

> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **criterion < 0.5.2 is affected, fixed in 0.5.2**.

## Step 1.7 – Embargo check

Skipped for two reasons: no Embargo policy URL is configured, and CVSS 5.3 is Moderate, below the 7.0 threshold.
