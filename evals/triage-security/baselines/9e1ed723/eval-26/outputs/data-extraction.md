# Step 1 – Data Extraction: TC-8050

## Step 0 – Configuration validation

Source: `claude-md-security-config.md` (mock project CLAUDE.md)

| Check | Result |
|---|---|
| Repository Registry | PASS — `rhtpa-backend` (serena_backend) |
| Jira Configuration | PASS — Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | PASS — `mcp__<serena-instance>__<tool>` convention present |
| Security Configuration / Product Lifecycle | PASS — Product pages URL, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| VEX Justification custom field | Configured — `customfield_12345` |
| Version Streams | PASS — `2.1.x` (rhtpa-release.0.3.z), `2.2.x` (rhtpa-release.0.4.z) |
| Source Repositories | PASS — `rhtpa-backend` (no Deployment Context column → defaults to `upstream`) |
| Optional fields not configured | Upstream Affected Component, PS Component, Stream field, ProdSec email/account ID, Embargo policy URL |

Step 0.3 (matrix staleness): matrix `Last-Updated: 2026-06-28T10:00:00Z`. Relative to
the eval date (2026-11-23) this is older than the 14-day threshold; in an interactive run
the engineer would be offered Refresh / Proceed / Stop. For this eval, proceeding with the
supplied mock matrix.

Step 0.6: `FULLSEND_OUTPUT_DIR` absent → interactive mode (simulated; no Jira writes performed).

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8050 | Issue |
| Issue status | New (proceed with full triage) | Issue `status` |
| CVE ID | CVE-2026-99001 | Label `CVE-2026-99001` and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → RHTPA 2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | criterion (Rust crate) | Description |
| Affected version range | < 0.5.2 ("versions before 0.5.2") | Description |
| Fixed version | 0.5.2 | Description |
| CVSS / Severity | 5.3 (Medium) | Description |
| Vulnerability summary | Path traversal in benchmark output — crafted benchmark names containing path separators allow writing benchmark output files to arbitrary paths | Description |
| Upstream fix PR | None in remote links | Remote links |
| Advisory URL | None (no GHSA/advisory link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 | Remote links |
| Due date | 2026-08-01 | Issue `duedate` |
| Assignee | Unassigned (Step 0.8 would assign to current user and transition New → Assigned) | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream scope resolution

| Item | Value |
|---|---|
| Summary suffix | `[rhtpa-2.2]` |
| Parsed stream | `2.2.x` |
| Matching Version Stream | `2.2.x` → `git.example.com/rhtpa/rhtpa-release.0.4.z` (`/home/dev/repos/rhtpa-release.0.4.z`) |
| Issue stream scope | **Scoped to 2.2.x** |

Steps 3–8 are scoped to the 2.2.x stream. Other streams (2.1.x) are analyzed only for
cross-stream impact reporting (Case A).

## Ecosystem detection

| Item | Value |
|---|---|
| Ecosystem | **Cargo** (criterion is a Rust crate; backend Cargo mapping exists in the 2.2.x Ecosystem Mappings) |
| Category | Source dependency |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock` |
| Repository | backend (rhtpa-backend) |
| Upstream branch (2.2.x) | `release/0.4.z` |
| Remediation tasks per stream | 2 (upstream backport or dependency bump + downstream propagation) |

## Deployment context

`rhtpa-backend` found in Source Repositories; the table has no Deployment Context column
(backward compatibility) → deployment context defaults to `upstream`. Per
remediation-templates.md, the Coordination Guidance subsection is omitted when the column
is absent.

## Step 1.5 – External CVE data enrichment

MITRE CVE API and OSV.dev were **not queried** (eval constraint: no external tools).
Treated as unavailable:

> External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used for Step 2.3: **criterion < 0.5.2 affected; 0.5.2 fixed** (Jira description).

## Step 1.7 – Embargo check

Skipped — no Embargo policy URL configured (and CVSS 5.3 Medium is below the 7.0 threshold).
