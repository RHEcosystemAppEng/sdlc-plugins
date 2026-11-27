# TC-8050 — Step 1 Data Extraction

Mode: **interactive** (`FULLSEND_OUTPUT_DIR` not set). Jira was not called. All data comes from the mock issue fixture (`vuln-issue-dev-dependency.md`).

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | `mcp__<serena-instance>__<tool>` naming present | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification custom field | customfield_12345 | Configured (optional) |
| Upstream Affected Component field | not configured | Steps 4.3 and 7 skipped |
| Embargo policy URL | not configured | Step 1.7 skipped |
| ProdSec contact / account ID | not configured | @mentions skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column) | Defaults to `upstream`; coordination guidance omitted (backward compatibility) |

## Step 0.3 – Matrix Staleness Check

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-27, so it is **152 days old**, past the 14-day threshold.

> Security matrix for streams **2.1.x / 2.2.x** was last updated on 2026-06-28 (152 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

In this eval, triage **proceeds anyway** using the mock matrix. Releases after 2.2.4 (if any) are not covered.

## Step 0.8 – Assign and Transition (simulated, not executed)

Proposed: assign TC-8050 to the current user and move it from **New** to **Assigned**. Engineer confirmation is required first.

## Step 1 – Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8050 | Issue |
| Issue status | New | Issue (full triage path) |
| CVE ID | CVE-2026-99001 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Affected repository | rhtpa-backend (`backend` workspace, Cargo) | Component + ecosystem mapping |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | criterion (Rust crate) | Description |
| Affected version range | < 0.5.2 ("versions before 0.5.2") | Description |
| Fixed version | 0.5.2 | Description |
| CVSS / severity | 5.3 (Medium) | Description |
| Vulnerability summary | Path traversal in benchmark output: crafted benchmark names containing path separators can write output files to arbitrary paths | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL | none (no GHSA link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 | Remote links |
| Due date | 2026-08-01 (already past) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z).
- **Issue stream scope: 2.2.x (scoped).** Steps 3, 4 and 8 apply only to 2.2.x. Any impact on 2.1.x is handled as cross-stream impact (Case A).

### Ecosystem detection

- criterion is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the Ecosystem Mappings for both streams (`Cargo.lock`, repository `backend`).
- Category: **source dependency**, which means 2 remediation tasks per stream.

### Deployment context

- rhtpa-backend: the Source Repositories table has no Deployment Context column, so the default is `upstream`. Per the backward-compatibility rule, the Coordination Guidance subsection is omitted.

## Step 1.5 – External CVE Data Enrichment (simulated)

The MITRE CVE API and OSV.dev were **not queried** because external calls are prohibited in this eval. Both are treated as unavailable:

> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **criterion < 0.5.2 is affected; 0.5.2 is fixed.**

## Step 1.7 – Embargo Check

No embargo policy URL is configured, and CVSS 5.3 is below the 7.0 threshold. **Step skipped.**
