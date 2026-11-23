# Step 1 – Data Extraction: TC-8021

Execution mode: **interactive** (`FULLSEND_OUTPUT_DIR` is absent, so Step 0.6 detects interactive mode and Step 0.7 is skipped).
Source: mock Jira issue `vuln-issue-preemptive-reconciliation.md`. The skill would normally call `jira.get_issue` and `jira.get_issue_remote_links`; in this eval it reads the mock file and makes no Jira calls.

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend (serena_backend) | Present |
| Project key | TC | Present |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | Present |
| Code Intelligence | `mcp__<serena-instance>__<tool>` convention | Present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | Present |
| Jira version prefix | RHTPA | Present |
| Vulnerability issue type ID | 10024 | Present |
| Component label pattern | `pscomponent:` | Present |
| VEX Justification custom field | customfield_12345 | Present (optional) |
| Upstream Affected Component / PS Component / Stream custom fields | Not configured in Security Configuration | Optional field missing, so Step 4.3 and Step 7 are skipped |
| ProdSec contact / Jira account ID | Not configured | No @mentions |
| Embargo policy URL | Not configured | Step 1.7 skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z | Present |
| Source Repositories | rhtpa-backend (no Deployment Context column) | Present, context defaults to `upstream` |

Configuration is valid, so triage proceeds.

## Step 0.3 – Matrix Staleness Check

- `security-matrix-mock.md` has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`.
- Today is 2026-11-23, so the matrix is **148 days old**, well past the 14-day threshold.
- **Warning to the engineer:** "Security matrix for streams 2.1.x / 2.2.x was last updated on 2026-06-28 (148 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop."
- For this eval the run assumes **Proceed anyway**. The stale matrix has no effect on the Step 4.4 reconciliation result.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Status is **New**, so the proposal is to assign TC-8021 to the current user and transition it to **Assigned**. The transition would be discovered dynamically with `get_transitions`.
- Nothing was executed because this eval forbids Jira calls.

## Extracted CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | **CVE-2026-55123** | Label `CVE-2026-55123` and summary |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] | Issue |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 | `versions` field |
| Vulnerable library | **tokio** | Description and customfield_10632 |
| Affected version range | **< 1.42.0** ("versions before 1.42.0") | Description |
| Fixed version | **1.42.0** | Description |
| CVSS / Severity | 8.1 (High) | Description |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp (also RUSTSEC-2026-0088) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote links |
| Due date | 2026-08-15 (already past as of 2026-11-23) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue |
| Existing issue links | None | Issue |
| customfield_10632 (Upstream Affected Component) | tokio | Custom field |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server | Custom field |
| customfield_10832 (Stream) | rhtpa-2.1 | Custom field |

All critical fields (CVE ID, library, affected range) were parsed, so no engineer input is needed.

## Stream Scope Resolution

- Suffix `[rhtpa-2.1]` maps to stream **2.1.x**, which matches the configured Version Streams row (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.3.z`).
- **Issue stream scope: 2.1.x (scoped).** Steps 3, 4 and 8 are limited to this stream. Supported versions in the matrix for this stream are 2.1.0 (backend `v0.3.8`) and 2.1.1 (backend `v0.3.12`).

## Ecosystem Detection

- tokio is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the 2.1.x Ecosystem Mappings: lock file `Cargo.lock` in `backend`, upstream branch `release/0.3.z`.
- Category: **source dependency**. If remediation were needed, that means 2 tasks per stream (upstream backport or dependency bump, plus downstream propagation).

## Deployment Context

- Affected repository: rhtpa-backend (the `backend` component). The Source Repositories table has no Deployment Context column, so the context defaults to **`upstream`**.

## Step 1.5 – External CVE Data Enrichment

- The skill would query `https://cveawg.mitre.org/api/cve/CVE-2026-55123` and `https://api.osv.dev/v1/vulns/CVE-2026-55123`. External calls are forbidden in this eval, so both sources count as **unavailable**.
- "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
- Fix threshold used: **tokio 1.42.0** (affected when < 1.42.0).

## Step 1.7 – Embargo Check

- CVSS 8.1 is above the threshold, but no Embargo policy URL is configured, so this step is **skipped**.

## Step 2 – Version Impact Analysis (note)

- The mock lock-file data in `security-matrix-mock.md` has tables for quinn-proto, serde_json, h2, criterion, rustls and openssl-libs. It has **no tokio data** for `v0.3.8` or `v0.3.12`.
- The skill says "Do NOT fabricate data", so no tokio version is claimed here. In a real run this would be `git show v0.3.8:Cargo.lock` and `git show v0.3.12:Cargo.lock` in the backend repo. The table below gives the impact as PSIRT asserted it. Prior cross-stream triage of TC-8020, which created TC-8022 for rhtpa-2.1, also found 2.1.x affected. Both need confirmation from lock-file evidence.

| Version | Build | backend tag | tokio version | Affected (< 1.42.0)? |
|---|---|---|---|---|
| RHTPA 2.1.0 | 0.3.8 | `v0.3.8` | Not in mock data (requires `git show v0.3.8:Cargo.lock`) | Presumed YES (PSIRT plus prior TC-8020 cross-stream analysis) |
| RHTPA 2.1.1 | 0.3.12 | `v0.3.12` | Not in mock data (requires `git show v0.3.12:Cargo.lock`) | Presumed YES (PSIRT plus prior TC-8020 cross-stream analysis) |

Out of scope for this issue: 2.2.x (tracked by companion TC-8020 [rhtpa-2.2]).

## Step 3 – Affects Versions Correction

- Current: [RHTPA 2.1.0, RHTPA 2.1.1]. Proposed for stream 2.1.x: [RHTPA 2.1.0, RHTPA 2.1.1].
- The current values already match the stream-scoped impact, so **no correction** is proposed. This depends on lock-file confirmation; if tokio at either tag turns out to be >= 1.42.0, that version would be removed.
