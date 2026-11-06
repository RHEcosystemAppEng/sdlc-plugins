# Step 1 – Data Extraction: TC-8003

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Simulated eval: no Jira, WebFetch, or `git show` calls were made. Issue data comes from `vuln-issue-duplicate.md`, config from `claude-md-security-config.md`, and matrix/lock-file data from `security-matrix-mock.md`.

## Step 0 – Configuration Validation

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | present, naming convention `mcp__<serena-instance>__<tool>` | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification field | customfield_12345 | configured (optional) |
| Upstream Affected Component / PS Component / Stream fields | not configured | Steps 4.3, 7, 7.5.3 skipped |
| ProdSec contact / account ID | not configured | @mentions omitted |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) | OK |

## Step 0.3 – Matrix Staleness Check

Both streams' matrix says `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-06, so the matrix is **131 days old**, well past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (131 days ago). It may be missing recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval assumption: **Proceed anyway**. A stale matrix does not change the duplicate decision below, but versions released after 2026-06-28 are not covered by this analysis.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Assign TC-8003 to the current user.
- Status is `New`, so the proposal is to transition it to `Assigned` using a transition found at runtime.

## Extracted Fields

| Field | Value |
|-------|-------|
| Issue key | TC-8003 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Repository (deployment context) | rhtpa-backend (`upstream`, the default) |
| PSIRT-claimed product version | `[rhtpa-2.2]` |
| Stream scope | **2.2.x** (scoped; suffix matches a configured stream) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (source dependency, so 2 tasks per stream if remediation is needed) |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Impact | DoS (panic from an unbounded STREAMS frame count) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0042.html |
| Due date | 2026-07-15 (already past) |
| Assignee | Unassigned |
| Existing comments | none |

All critical fields (CVE ID, library, affected range) were parsed.

## Step 1.5 – External CVE Data Enrichment

MITRE and OSV.dev were not queried because this eval forbids external calls. I fell back to the Jira description data:

> External CVE databases unavailable: using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **0.11.14**.

## Step 1.7 – Embargo Check

Skipped: no Embargo policy URL is configured. CVSS 7.5 would otherwise meet the threshold.

## Step 2 – Version Impact Analysis (simulated lock-file data, Cargo.lock at pinned tags)

| Stream | Version | Build | backend tag | quinn-proto | Affected (< 0.11.14)? | Notes |
|--------|---------|-------|-------------|-------------|------------------------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | **YES** | |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | **YES** | |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 | — | **YES** | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | fixed |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | fixed |

- Development stream (Step 2.2): no Jira unreleased-version data was given and no Jira query was allowed, so it was not determined. The latest 2.2.x release (2.2.4) already ships 0.11.14, and 2.2.x is the latest stream.
- Upstream fix status (Step 2.5): `release/0.4.z` already ships quinn-proto 0.11.14 as of v0.4.11. On 2.1.x (`release/0.3.z`), the last shipped tag v0.3.12 still has 0.11.9.

## Step 3 – Affects Versions Correction (scoped to 2.2.x)

- Current: [RHTPA 2.2.0]
- Evidence-based for 2.2.x: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
- The current value is correct but incomplete. **The correction is not applied to TC-8003**: Step 4 finds that TC-8003 is a duplicate and will be closed, so changing its versions would not help. The correction is instead recommended for the canonical issue TC-7999 (see duplicate-check.md).
- Jira version IDs would be looked up at runtime with `getJiraIssueTypeMetaWithFields` (not done in the eval).
