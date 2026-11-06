# TC-8050 — Step 1: Data Extraction

Skill: `/sdlc-workflow:triage-security` (interactive mode — `FULLSEND_OUTPUT_DIR` absent)
Source: mock Jira issue `vuln-issue-dev-dependency.md` (no live Jira calls made)

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) — no Deployment Context column, defaults to `upstream` |

All required sections present — validation passes.

## Step 0.3 – Matrix staleness check

Matrix `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-06, so the matrix is **131 days old**, which is past the 14-day threshold.

> Security matrix for stream **2.2.x** (and 2.1.x) was last updated on 2026-06-28 (131 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

For this eval I chose **Proceed anyway** and used the mock matrix as given.

## Step 0.8 – Assign / transition (proposed, not executed)

- Issue status is **New**, so the proposal is: assign TC-8050 to the current user and move it to **Assigned** using a transition discovered at runtime.

## Step 1 – Parsed CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8050 | Issue |
| CVE ID | CVE-2026-99001 | Label `CVE-2026-99001` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | criterion (Rust crate) | Description |
| Affected version range | < 0.5.2 ("versions before 0.5.2") | Description |
| Fixed version | 0.5.2 | Description |
| CVSS | 5.3 (Medium) | Description |
| Vulnerability summary | Path traversal: crafted benchmark names with path separators can write benchmark output files to arbitrary paths | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL (GHSA) | none in remote links | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 | Remote links |
| Due date | 2026-08-01 (already passed as of 2026-11-06) | `duedate` |
| Status | New | Issue |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comments |

All critical fields (CVE ID, library, affected range) were parsed. No engineer input needed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, configured as Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`.
- **Issue stream scope: 2.2.x (scoped).** Steps 3–8 are limited to 2.2.x. Other streams are handled through Case A (cross-stream impact).

### Ecosystem detection

- criterion is a Rust crate, so the ecosystem is **Cargo**. Cargo appears in the 2.2.x Ecosystem Mappings (`backend`, `Cargo.lock`, upstream branch `release/0.4.z`).
- Category: **Source dependency**, which means 2 remediation tasks per stream (upstream backport or dependency bump, plus downstream propagation).

### Deployment context

- Affected repository: rhtpa-backend (matrix column `backend`). The Source Repositories table has no Deployment Context column, so the default is `upstream`. Because the column is absent, remediation tasks leave out Coordination Guidance, as the backward-compatibility rule requires.

## Step 1.5 – External CVE data enrichment

MITRE (`cveawg.mitre.org/api/cve/CVE-2026-99001`) and OSV.dev were **not queried** because this eval forbids external calls.

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold in use: **criterion < 0.5.2 is affected; 0.5.2 is fixed** (from the Jira description).

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured, and CVSS 5.3 is below the 7.0 threshold in any case.
