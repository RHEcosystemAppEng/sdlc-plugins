# Step 1 – Data Extraction: TC-8003

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Per eval instructions, no Jira MCP,
`git show`, or external calls were made; all values come from the provided input files.

## Step 0 – Configuration validation (claude-md-security-config.md)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | present |
| Project key | TC | present |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | present |
| Code Intelligence | `mcp__<serena-instance>__<tool>` naming convention | present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | present |
| Jira version prefix | RHTPA | present |
| Vulnerability issue type ID | 10024 | present |
| Component label pattern | `pscomponent:` | present |
| VEX Justification custom field | customfield_12345 | present (optional) |
| Upstream Affected Component field | not configured | Steps 4.3 and 7 skipped |
| ProdSec Jira account ID | not configured | @mentions skipped |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z | present |
| Source Repositories | rhtpa-backend (no Deployment Context column -> default `upstream`) | present |

Result: Security Configuration is complete; triage may proceed.

## Step 0.3 – Matrix staleness check

Matrix `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`; today is 2026-11-26, so the
matrix is **151 days old** (threshold 14 days).

> Security matrix for streams 2.1.x and 2.2.x was last updated on 2026-06-28
> (151 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval assumption: **Proceed anyway** with the supplied matrix. Staleness does not change
the duplicate outcome below.

## Step 0.8 – Assign and transition (proposed only)

TC-8003 is in **New** and unassigned. Proposed (needs confirmation): assign to the
current user and transition to Assigned. Not executed (no Jira access in this eval).

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8003 | Issue |
| Issue type | Vulnerability | Issue |
| Status | New | Issue |
| Assignee | Unassigned | Issue |
| CVE ID | CVE-2026-31812 | Label and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability class | Denial of service (panic on excessive stream count in STREAMS frame) | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 (already past) | `duedate` |
| Existing comments | none | Comments |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` -> stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Matches a configured Version Stream -> issue is **scoped** to 2.2.x.

## Ecosystem detection

- quinn-proto is a Rust crate -> ecosystem **Cargo** (listed in both streams' Ecosystem
  Mappings: repo `backend`, lock file `Cargo.lock`, upstream branches `release/0.3.z` /
  `release/0.4.z`).
- Category: source dependency (2 remediation tasks per stream if remediation were needed).
- Deployment context for rhtpa-backend: `upstream` (default; column absent).

## Step 1.5 – External enrichment

Not performed (eval forbids external calls). Falling back to Jira description data:

> External CVE databases unavailable – using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 affected; 0.11.14 fixed**.

## Step 1.7 – Embargo check

Skipped: no Embargo policy URL configured (CVSS 7.5 would otherwise trigger the gate).

## Step 2 – Version impact (from mock lock file data)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version |
| dev | — | — | — | not determined | no unreleased Jira version data available in eval (Step 2.2 requires Jira) |

Scoped to TC-8003's stream (2.2.x), the evidence-backed Affects Versions would be
**RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**. The PSIRT value (RHTPA 2.2.0 only) is
correct but incomplete. Stream 2.1.x is also affected (cross-stream impact).

Upstream fix (Step 2.5, inferred from released tags only): `release/0.4.z` already
ships 0.11.14 as of v0.4.11, so the 2.2.x fix is available upstream. Branch HEAD was
not inspected (no `git` access in eval).
