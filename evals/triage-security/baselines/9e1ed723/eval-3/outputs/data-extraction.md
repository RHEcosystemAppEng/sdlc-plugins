# Step 1 – Data Extraction: TC-8003

Execution mode: interactive (FULLSEND_OUTPUT_DIR absent). Jira reads were simulated from
`vuln-issue-duplicate.md`; no Jira MCP, WebFetch or `git show` calls were made.

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | `mcp__<serena-instance>__<tool>` convention present | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification custom field | customfield_12345 | configured (optional) |
| Upstream Affected Component field | not configured | Steps 4.3, 7, 7.5.3 dedup skipped |
| ProdSec Jira account ID | not configured | @mentions omitted |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column -> default `upstream`) | OK |

## Step 0.3 – Matrix Staleness Check

The matrix carries `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-23, so
it is **148 days old**, past the 14-day threshold. Normally the engineer would choose
Refresh / Proceed / Stop at this point. For this eval: **proceed with the current
matrix**. The warning is recorded here.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Assign TC-8003 to the current user. It is currently unassigned.
- Transition New -> Assigned.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8003 |
| Issue type / Status | Vulnerability / New |
| CVE ID | CVE-2026-31812 (label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS / Severity | 7.5 (High), DoS (panic on excessive STREAMS frame) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0042.html |
| Due date | 2026-07-15 (already passed as of 2026-11-23) |
| Assignee | Unassigned |
| Existing comments | none |

All critical fields (CVE ID, library, affected range) were parsed. Nothing is missing.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue stream scope: **2.2.x (scoped)**.

## Ecosystem Detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings.
- Category: source dependency. A remediation would need 2 tasks per stream (upstream backport or dependency bump, plus downstream propagation).
- Lock file: `Cargo.lock` in `backend`. Upstream branches: `release/0.4.z` (2.2.x) and `release/0.3.z` (2.1.x).
- Deployment context: rhtpa-backend, defaulting to `upstream`.

## Step 1.5 – External CVE Data Enrichment

The MITRE and OSV queries were not executed (no external calls allowed in this eval). The
Jira description is the only data source, so the fix threshold is **0.11.14** at reduced
confidence.

## Step 1.7 – Embargo Check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise have
triggered the gate.

## Step 2 – Version Impact Analysis (simulated lock-file data from security-matrix-mock.md)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Build | backend tag | quinn-proto | Affected? | Notes |
|---------|-------|-------------|-------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | out of TC-8003 scope (2.1.x) |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | out of TC-8003 scope (2.1.x) |
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 0.4.9 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | |

- Development stream: the unreleased Jira versions could not be queried, and the matrix has no development stream data. 2.2.x is the latest configured stream, and its latest release (2.2.4) already ships the fixed version.
- Upstream fix status for 2.2.x (`release/0.4.z`): v0.4.11 and later ship 0.11.14, which suggests the fix is already upstream. The branch HEAD was not inspected because `git show` is not permitted here.
- Affected versions in scope (2.2.x): **RHTPA 2.2.0, 2.2.1, 2.2.2**.
- Cross-stream: 2.1.x (2.1.0, 2.1.1) is also affected and needs its own tracker or a preemptive task.

## Step 3 – Affects Versions Correction (assessed, superseded by Step 4)

- Current: [RHTPA 2.2.0]. Evidence-based proposal for 2.2.x: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
- Step 4 finds that TC-8003 is a same-stream duplicate and should be closed. Correcting Affects Versions on an issue about to be closed adds no value, so this correction is **not recommended for TC-8003**. The gap is raised on the canonical issue TC-7999 instead (see duplicate-check.md).
