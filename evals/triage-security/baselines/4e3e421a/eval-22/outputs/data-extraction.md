# Step 1 – Data Extraction: TC-8021

Source: `vuln-issue-standard.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`).
No Jira MCP calls were made.

> Note: the mock issue file shows key `TC-8001`; the task identifies the issue as
> **TC-8021**. TC-8021 is used as the current issue key throughout (including the
> `key != TC-8021` exclusion in Step 7).

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (assumed configured per task instructions) |
| Embargo policy URL | not configured -> Step 1.7 skipped |
| ProdSec contact / account ID | not configured -> @mentions skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column -> defaults to `upstream`) |

All required sections present (Repository Registry, Jira Configuration, Code Intelligence,
Security Configuration with Product Lifecycle / Version Streams / Source Repositories).

## Step 0.3 – Matrix Staleness

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` vs. today 2026-11-03 = **128 days old**
(threshold 14 days). Warning would be raised for both streams with options
Refresh / Proceed anyway / Stop. For this eval, proceeding with the current matrix.

## Extracted Fields

| Field | Value |
|---|---|
| Issue key | TC-8021 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS / Severity | 7.5 (High) – Denial of Service (panic on excessive stream count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned (Step 0.8 would assign to current user and transition New -> Assigned) |
| Existing comments | none |

## Stream Scope

Summary suffix `[rhtpa-2.2]` -> stream **2.2.x** (matches configured Version Stream).
Issue is **scoped** to 2.2.x.

## Ecosystem

quinn-proto is a Rust crate -> **Cargo** (listed in both streams' Ecosystem Mappings).
Category: source dependency -> 2 remediation tasks per stream.
Lock file: `Cargo.lock` in backend repo; deployment context: `upstream` (default).

## Step 1.5 – External Enrichment

Not queried (no external calls permitted in this eval). Using Jira description data:
fix threshold `< 0.11.14`, fixed in `0.11.14` (reduced confidence noted).

## Step 1.7 – Embargo Check

Skipped: no Embargo policy URL configured (CVSS 7.5 would otherwise trigger the gate).

## Step 2 – Version Impact Analysis (simulated lock file data from security-matrix-mock.md)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | YES |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

Development stream (Step 2.2): no unreleased-version data available in the eval inputs; not assessed.

## Step 3 – Affects Versions Correction (proposed)

PSIRT value `RHTPA 2.0.0` is wrong (no 2.0.x stream exists). Scoped to 2.2.x, the corrected
Affects Versions are: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**. (2.1.0 / 2.1.1 are affected
but out of this issue's scope; handled via cross-stream logic in Step 8 Case A.)
