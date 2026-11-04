# Step 1 – Data Extraction: TC-8020

> Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation, so no Jira, WebFetch, or git calls were made.
> All data comes from the provided input files.
>
> Note: the mock issue file shows key `TC-8001`. The task targets **TC-8020**, so this
> triage uses TC-8020 as the issue key. All other fields come from the mock file.

## Step 0 – Configuration validation (claude-md-security-config.md)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key / Cloud ID | TC / 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | present (`mcp__<instance>__<tool>`) | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification field | customfield_12345 | configured |
| Upstream Affected Component field | customfield_10632 | configured (per eval assumption) |
| PS Component field | — | not configured |
| Stream field | — | not configured |
| ProdSec contact / Jira account ID | — | not configured (no @mentions) |
| Embargo policy URL | — | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) | OK |

## Step 0.3 – Matrix staleness

- Matrix `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, so the matrix is **129 days old**, well past the 14-day threshold.
- Warning: "Security matrix was last updated on 2026-06-28 (129 days ago). The matrix may not reflect recent releases. Options: Refresh now / Proceed anyway / Stop."
- Eval assumption: **Proceed anyway** with the provided matrix. Any release after 2.2.4 is not represented.

## Step 0.8 – Assign and transition (simulated, not executed)

- Proposed: assign TC-8020 to the current user, then transition New to the workflow's "Assigned" target (e.g. `ASSIGNED`), found dynamically via `get_transitions`.

## Extracted fields

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8020 | task input |
| CVE ID | CVE-2026-31812 | label + summary |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | summary |
| Status | New | issue |
| Affected component | `pscomponent:org/rhtpa-server` | label matching `pscomponent:` |
| Upstream Affected Component (customfield_10632) | quinn-proto | task input |
| PSIRT-claimed product version | `[rhtpa-2.2]` | summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto (Rust crate) | description |
| Affected version range | < 0.11.14 | description |
| Fixed version | 0.11.14 | description |
| CVSS / severity | 7.5 (High), DoS | description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | remote link / references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | remote link |
| Due date | 2026-07-15 (already past as of 2026-11-04) | `duedate` |
| Assignee | Unassigned | issue |
| Existing comments | none | issue |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z).
- The issue is **scoped** to 2.2.x.

## Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo** (listed in both streams' Ecosystem Mappings: repo `backend`, lock file `Cargo.lock`).
- Category: **source dependency**, which means 2 remediation tasks per stream.
- Deployment context of rhtpa-backend: `upstream` (default, because the column is absent).

## Step 1.5 – External enrichment

- MITRE / OSV were not queried (eval forbids external calls). Fix threshold comes from the Jira description only: **< 0.11.14, fixed in 0.11.14**. Confidence is reduced.

## Step 1.7 – Embargo check

- Skipped. No Embargo policy URL is configured, even though CVSS 7.5 is at or above 7.0.

## Step 2 – Version impact analysis (simulated `git show <tag>:Cargo.lock` data)

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | latest release, fixed |

- Development stream (2.2): no unreleased Jira version data was provided, so it was not assessed.
- Dependency chain (2.3.5) and upstream branch HEAD (2.5, `release/0.4.z` / `release/0.3.z`): no simulated data was provided, so they were **not verified**. The latest 2.2.x pinned tag (v0.4.12) already ships 0.11.14. That is evidence that the fix landed on the 0.4.z line, but it is not a HEAD read.

## Step 3 – Affects Versions correction (proposed, scoped to 2.2.x)

- Current: `[RHTPA 2.0.0]` (wrong, because no 2.0 stream exists).
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
- 2.1.0 and 2.1.1 are affected, but they belong to the 2.1.x stream and are excluded from this scoped issue.
- Jira version IDs would come from `getJiraIssueTypeMetaWithFields`. Nothing was executed.
