# TC-8020 — Data Extraction (Steps 0 – 1.7)

## Step 0 – Configuration validation

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | `mcp__<instance>__<tool>` convention present | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification field | customfield_12345 | Configured (not used, since the issue is affected) |
| Upstream Affected Component field | Not configured in Security Configuration | Skip Step 4.3 (cross-CVE overlap), Step 7 (concurrent triage), Step 7.5.3 (dedup) |
| ProdSec contact / account ID | Not configured | @mentions in correction comments skipped |
| Embargo policy URL | Not configured | Skip Step 1.7 |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column) | Context defaults to `upstream`. Coordination Guidance is omitted because the column is absent (backward compatibility) |

## Step 0.3 – Matrix staleness check

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, which makes it **151 days old**. That is more than the 14-day threshold.

> Security matrix for stream **2.1.x** / **2.2.x** was last updated on 2026-06-28
> (151 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval assumption: **Proceed anyway**, using the current matrix. Any 2.2.x releases after 2.2.4 are not covered.

## Step 0.6 – Mode detection
`FULLSEND_OUTPUT_DIR` is absent, so this runs in **interactive mode**. Jira mutations below are proposals, written to files instead of executed.

## Step 0.8 – Assign and transition (proposed)
- Assign TC-8020 to the current user (`jira.user_info()` account ID).
- Status is New. Transition to **Assigned** using the dynamically discovered transition.

## Step 1 – Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Status | New |
| CVE ID | CVE-2026-55123 (label and summary agree) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | tokio |
| Stream field (customfield_10832) | rhtpa-2.2 |
| Product version (PSIRT suffix) | `[rhtpa-2.2]` |
| Affects Versions (current Jira) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio (Rust crate) |
| Ecosystem | Cargo (source dependency, so 2 tasks per stream) |
| Affected range | < 1.42.0 ("versions before 1.42.0") |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Vulnerability | Use-after-free when a spawned task is aborted while holding a borrowed reference. Can cause memory corruption and possible code execution |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp (also RUSTSEC-2026-0088) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 (**already past**, 103 days overdue) |
| Assignee | Unassigned |
| Existing links / comments | None / None |
| Affected repository | rhtpa-backend (Cargo ecosystem, `backend` column) |
| Deployment context | upstream (default, column absent) |

### Stream scope resolution
- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x. Steps 3 and 4 are scoped to 2.2.x, and Case A cross-stream handling applies to the other streams.

## Step 1.5 – External CVE enrichment
MITRE and OSV were not queried, per eval constraints. Proceeding with the Jira description threshold (< 1.42.0, fixed 1.42.0).
> External CVE databases were not available, so only Jira description data is used. Confidence in the fix threshold is lower.

## Step 1.7 – Embargo check
Skipped because no Embargo policy URL is configured. The CVSS is 8.1, which would otherwise trigger the gate.
