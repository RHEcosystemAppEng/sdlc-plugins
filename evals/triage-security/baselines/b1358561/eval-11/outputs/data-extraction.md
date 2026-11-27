# TC-8021 — Step 1 Data Extraction (with Steps 0 / 0.3 / 0.6 / 1.5 / 1.7 context)

## Pre-flight

| Check | Result |
|---|---|
| Step 0.6 mode | Interactive (no `FULLSEND_OUTPUT_DIR`). Step 0.7 skipped. |
| Step 0 config | Valid. Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Jira version prefix `RHTPA`, Vulnerability issue type `10024`, component label pattern `pscomponent:`, VEX field `customfield_12345`. 2 Version Streams (2.1.x, 2.2.x), 1 Source Repository (rhtpa-backend). |
| Optional config | Upstream Affected Component, PS Component, and Stream custom fields are **not** set in Security Configuration. That means Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) get skipped, even though the issue carries values in those fields. No Embargo policy URL, ProdSec contact, or ProdSec account ID is configured. |
| Step 0.3 matrix staleness | `Last-Updated: 2026-06-28T10:00:00Z`, which is **152 days old** (today is 2026-11-27, threshold is 14 days). **Warning:** the matrix may not reflect recent releases. In a live run the engineer picks Refresh / Proceed / Stop. Here I continue as "Proceed anyway". |
| Step 0.8 assign/transition | Planned, not executed: assign TC-8021 to the current user and move it from New to Assigned. |
| Step 1.7 embargo | Skipped. No Embargo policy URL is configured (CVSS 8.1 would otherwise meet the threshold). |

## Extracted fields

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 | Issue |
| Status | New (proceed with full triage) | Issue |
| CVE ID | CVE-2026-55123 | Label and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label (pattern `pscomponent:`) and customfield_10669 |
| Upstream Affected Component | tokio | customfield_10632 |
| Stream (field) | rhtpa-2.1 | customfield_10832 |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.1.0, RHTPA 2.1.1 | `versions` field |
| Vulnerable library | tokio | Description |
| Affected range | < 1.42.0 ("versions before 1.42.0") | Description |
| Fixed version | 1.42.0 | Description |
| Severity | CVSS 8.1 (High) | Description |
| Vulnerability | Use-after-free when a spawned task is aborted while holding a borrowed reference | Description |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp, https://rustsec.org/advisories/RUSTSEC-2026-0088.html | Remote link and description refs |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote link |
| Due date | 2026-08-15 (already past as of 2026-11-27) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing issue links | None | Issue |
| Existing comments | None | Issue |

## Stream scope resolution

- Suffix `[rhtpa-2.1]` maps to configured stream **2.1.x**: Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.3.z`, local path `/home/dev/repos/rhtpa-release.0.3.z`.
- The issue is **scoped** to 2.1.x. Supported versions in scope (from the matrix): 2.1.0 (backend `v0.3.8`) and 2.1.1 (backend `v0.3.12`).

## Ecosystem and deployment context

- Ecosystem: **Cargo** (Rust crate `tokio`). It is listed in the 2.1.x Ecosystem Mappings: repo `backend`, lock file `Cargo.lock`, check `git show <tag>:Cargo.lock`, upstream branch `release/0.3.z`.
- Category: source dependency, so 2 tasks per stream (upstream backport or dependency bump, plus downstream propagation).
- Affected repository: rhtpa-backend. The Source Repositories table has no Deployment Context column, so the default is `upstream`.

## Step 1.5 – External enrichment

The eval forbids external calls, so MITRE and OSV were not queried. That counts as the "Unavailable" path:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **tokio < 1.42.0, fixed in 1.42.0**.

## Step 2 – Version impact note

The mock lock file data has no `tokio` rows (it covers only quinn-proto, serde_json, h2, criterion, rustls, and openssl-libs). Under the "do not fabricate" rule, the tokio version at `v0.3.8` and `v0.3.12` is **not determined**:

| Version | Build | backend tag | tokio | Affected? |
|---|---|---|---|---|
| 2.1.0 | 0.3.8 | v0.3.8 | not available in evidence | needs `git show v0.3.8:Cargo.lock` |
| 2.1.1 | 0.3.12 | v0.3.12 | not available in evidence | needs `git show v0.3.12:Cargo.lock` |

In a live run, Step 2 would block here and ask the engineer for this evidence. The Affects Versions correction (Step 3) therefore stays pending. The PSIRT values (RHTPA 2.1.0, 2.1.1) are kept unchanged for now, neither confirmed nor corrected. The existing preemptive task TC-8022 is supporting evidence that the 2.1.x stream was found affected during the earlier TC-8020 triage.
