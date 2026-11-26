# Step 1 – Data Extraction: TC-8001

## Step 0 – Configuration Validation

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| ProdSec contact email | prodsec-team@example.com |
| ProdSec Jira account ID | 557058:prodsec-mock-account-id |
| Upstream Affected Component field | not configured (Steps 4.3, 7, 7.5.3 dedup skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (deployment context: upstream, the default because the column is absent) |

All required sections are present, so triage can proceed.

## Step 0.3 – Matrix Staleness Check

Both stream matrices carry `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. That is about 151 days before today (2026-11-26), well past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (151 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval run: **Proceed anyway** with the current matrix data. Caveat: any 2.1.x or 2.2.x release after 2026-06-28 is not covered.

## Step 0.8 – Assign and Transition

Proposed (not executed in this eval): assign TC-8001 to the current user and transition it from New to Assigned.

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Issue type / Status | Vulnerability / New |
| Reporter | psirt-analyst (account ID: `557058:psirt-analyst-mock-id`) |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` (summary suffix) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate), a source dependency |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past) |
| Existing comments | none |
| Assignee | Unassigned |

## Stream Scope Resolution

- The summary suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 4 apply only to 2.2.x versions. Any other affected stream goes through Case A cross-stream handling.

## Deployment Context

- Affected repository: rhtpa-backend (Cargo `backend` in the Ecosystem Mappings).
- Deployment context: `upstream` (the default, because the Source Repositories table has no Deployment Context column).

## Step 1.5 – External CVE Data Enrichment

The MITRE CVE API and OSV.dev were not queried, because this eval forbids external calls. Both count as **unavailable**:

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 affected; 0.11.14 fixed** (from the Jira description).

## Step 1.7 – Embargo Check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise meet the threshold.
