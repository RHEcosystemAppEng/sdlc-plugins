# Step 1 – Data Extraction: TC-8020

> Source: simulated Jira issue data from `vuln-issue-standard.md` (no Jira MCP call made).
> Note: the mock file header shows key `TC-8001`; the task specifies the issue under
> triage is **TC-8020**. TC-8020 is used throughout this triage.

## Step 0 – Configuration validated

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 (configured, per task assumption) |
| Embargo policy URL | not configured → Step 1.7 skipped |
| ProdSec Jira account ID | not configured → no @mentions |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`) |

Step 0.3 (matrix staleness): matrix `Last-Updated: 2026-06-28T10:00:00Z` is far older
than 14 days relative to today (2026-11-27, ~152 days). In interactive mode the engineer
would be offered Refresh / Proceed / Stop; for this eval we proceed with the supplied matrix
and flag the staleness.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| Status | New (full triage path) |
| Assignee | Unassigned (Step 0.8 would assign to current user and transition to Assigned) |
| CVE ID | CVE-2026-31812 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | `quinn-proto` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Vulnerability type | Denial of service (panic on excessive STREAMS frame stream count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | none |

## Stream scope resolution

Summary suffix `[rhtpa-2.2]` → stream **2.2.x** (matches configured Version Stream
`git.example.com/rhtpa/rhtpa-release.0.4.z`). Issue is **scoped** to 2.2.x.

## Ecosystem detection

quinn-proto is a Rust crate → **Cargo** (listed in both streams' Ecosystem Mappings:
repository `backend`, lock file `Cargo.lock`). Category: source dependency → 2
remediation tasks per affected stream.

## Deployment context

Affected repository rhtpa-backend → deployment context `upstream` (default; column absent).

## Step 1.5 – External enrichment

MITRE / OSV queries not executed (external calls prohibited in this eval). Fix threshold
from Jira description is used: **< 0.11.14, fixed in 0.11.14**. Confidence noted as
reduced (no cross-validation).

## Step 1.7 – Embargo check

Skipped: no Embargo policy URL configured (CVSS 7.5 would otherwise trigger the gate).

## Step 2 – Version impact (from mock lock file data)

| Version | Stream | Backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |

Development stream: no unreleased Jira version data available (Step 2.2 not simulatable);
not assessed. Upstream branch HEAD (`release/0.4.z`, `release/0.3.z`) lock data was not
provided, so Step 2.5 upstream fix status is **unverified** (not fabricated). Released tags
v0.4.11+ already ship 0.11.14, which suggests but does not prove `release/0.4.z` is fixed.

## Step 3 – Affects Versions correction (proposed, not executed)

`Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
(RHTPA 2.0.0 does not exist in any supported stream; scoped to 2.2.x.)
