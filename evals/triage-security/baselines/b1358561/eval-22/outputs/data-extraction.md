# Step 1 – Data Extraction: TC-8021

> Mode: interactive (`FULLSEND_OUTPUT_DIR` absent). No Jira MCP, git, or WebFetch calls were made.
> Issue data came from the provided mock file (`vuln-issue-standard.md`).
>
> **Key discrepancy:** the task names the issue **TC-8021**, but the mock issue file shows
> `**Key**: TC-8001`. This triage treats the file as the content of TC-8021, as the task
> instructs, and uses **TC-8021** in every JQL `key !=` clause and output. Flag this to the
> engineer before any real Jira mutation.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | present, naming convention `mcp__<instance>__<tool>` | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification field | customfield_12345 | configured |
| Upstream Affected Component field | customfield_10632 | configured (the task says to assume this) |
| PS Component field | not configured | Step 4.3 is skipped |
| Stream field | not configured | Step 4.3 is skipped |
| ProdSec contact / Jira account ID | not configured | @mentions skipped |
| Embargo policy URL | not configured | Step 1.7 is skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) | OK |

## Step 0.3 – Matrix staleness

The matrix carries `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-27, so the matrix is
**152 days old**, well past the 14-day threshold. **Warning:** the matrix may not list releases after
2.2.4 or 2.1.1. In an interactive run the engineer chooses Refresh, Proceed, or Stop. This eval
assumes **Proceed anyway** with the matrix as provided.

## Step 0.8 – Assign / transition (proposed, not executed)

- Assign TC-8021 to the current user.
- The issue is in status `New`, so transition it to `Assigned`. The transition ID is discovered with `get_transitions`.

## Extracted fields

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 (the mock file shows TC-8001) | task / issue |
| CVE ID | CVE-2026-31812 | label + summary |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | summary |
| Status | New | issue |
| Affected component | `pscomponent:org/rhtpa-server` | label |
| Upstream Affected Component (customfield_10632) | `quinn-proto` | custom field (given in the task) |
| PSIRT-claimed product version | `[rhtpa-2.2]` | summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 (wrong: no 2.0.x stream exists) | `versions` |
| Vulnerable library | quinn-proto | description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | description |
| Fixed version | 0.11.14 | description |
| CVSS | 7.5 (High) | description |
| Vulnerability class | DoS: panic from unbounded stream-state allocation via a STREAMS frame | description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | remote link |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | remote link |
| Other reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | description |
| Due date | 2026-07-15 (already past as of 2026-11-27) | `duedate` |
| Assignee | Unassigned | issue |
| Existing comments | none | issue |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream scope resolution

The suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x**
(`git.example.com/rhtpa/rhtpa-release.0.4.z`). The issue is **scoped to 2.2.x**.

## Ecosystem detection

quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings
(repository `backend`, lock file `Cargo.lock`). Its category is **source dependency**, which means 2 remediation
tasks per affected stream.

## Deployment context

rhtpa-backend has no Deployment Context column, so it defaults to **upstream**.

## Step 1.5 – External enrichment

The MITRE and OSV queries were **not executed** because the eval forbids external calls.
Warning: "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
The fix threshold used is **0.11.14** (affected range < 0.11.14).

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise have triggered the gate.

## Step 2 – Version impact (from the mock lock-file data)

| Version | Stream | Backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside this issue's scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside this issue's scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |
| dev stream | — | branch HEAD | unknown | unknown | No Jira unreleased-version data or HEAD lock data was provided, so it was not assessed |

Upstream fix status (Step 2.5): no data for branch HEAD of `release/0.4.z` or `release/0.3.z` was provided,
so it is **not verified**. The latest 2.2.x release tag (v0.4.12) already ships 0.11.14, which strongly
suggests `release/0.4.z` carries the fix, but per the no-fabrication rule this must be confirmed with
`git show release/0.4.z:Cargo.lock`. For 2.1.x, the last released tag (v0.3.12) still ships 0.11.9.

Dependency chain (Step 2.3.5): not determinable from the provided data (no Cargo.toml or manifest content).
Direct vs transitive classification and build profile still need to be checked.

## Step 3 – Affects Versions correction (proposed)

`Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (scoped to 2.2.x).
The Jira version IDs must be discovered with `getJiraIssueTypeMetaWithFields`. The 2.1.x versions belong to a companion issue.
