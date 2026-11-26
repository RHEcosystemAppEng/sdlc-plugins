# Step 1 – Data Extraction: TC-8021

Source: `vuln-issue-standard.md` (mock Jira issue), plus the task statement for
`customfield_10632`. No Jira, WebFetch, or git calls were made.

> Note: the mock issue file shows the key as `TC-8001`. The task names the issue
> `TC-8021`, so this triage uses `TC-8021` everywhere (including the Step 7
> `key != TC-8021` exclusion). All other issue data comes from the mock file.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 (configured, per the task's assumption) |
| ProdSec contact / account ID | Not configured, so @mentions are skipped |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend. There is no Deployment Context column, so it defaults to `upstream` |

Mode: interactive (no `FULLSEND_OUTPUT_DIR`), simulated through file outputs.

### Step 0.3 – Matrix Staleness Check

`security-matrix-mock.md` shows `Last-Updated: 2026-06-28T10:00:00Z`. Today is
2026-11-26, so the matrix is **151 days old**. The threshold is 14 days, so the
matrix is **STALE**. In a live run the engineer would choose Refresh / Proceed /
Stop. For this eval, triage continues with the current matrix, and the staleness is
flagged as a confidence caveat: releases after 2.2.4 / 2.1.1 may be missing.

## Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8021 |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New |
| Affected component | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Impact | Denial of service: a panic caused by too many streams in a STREAMS frame |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past as of 2026-11-26) |
| Assignee | Unassigned |
| Existing comments | None |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

The suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x**
(rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.

## Ecosystem Detection

quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both
streams' Ecosystem Mappings (lock file `Cargo.lock`, repo `backend`). Cargo is a
source dependency, so it gets 2 remediation tasks per affected stream.

## Deployment Context

The repository is rhtpa-backend. The Source Repositories table has no Deployment
Context column, so the context is `upstream`.

## Step 1.5 – External CVE Data Enrichment

MITRE and OSV were not queried, because external calls are not allowed in this
eval. Under the skill's "unavailable" rule:

> External CVE databases unavailable — using Jira description data only. Fix
> threshold confidence is reduced.

Fix threshold used: **0.11.14** (affected: < 0.11.14).

## Step 1.7 – Embargo Check

No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.5
would otherwise have triggered the gate.

## Step 0.8 – Assign / Transition (proposed, not executed)

- Assign TC-8021 to the current user.
- Transition New -> Assigned, with the transition discovered dynamically.

## Step 2 – Version Impact Analysis (simulated lock-file data from the matrix mock)

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside this issue's scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside this issue's scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | backend retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |
| dev stream | — | branch HEAD | not available | unknown | Step 2.2 requires a Jira unreleased-version lookup, which was not performed |

Dependency chain (2.3.5): the mock data cannot confirm whether quinn-proto is direct
or transitive in `backend` (it is most likely transitive via `quinn`). The
remediation task should document this chain.

Upstream fix status (2.5), not verified by `git show` against branch HEAD:

| Stream | Upstream Branch | Evidence | Fixed? |
|---|---|---|---|
| 2.2.x | release/0.4.z | Released tags v0.4.11 and v0.4.12 already ship 0.11.14 | Likely YES (HEAD not inspected) |
| 2.1.x | release/0.3.z | Last tag v0.3.12 ships 0.11.9 | Unknown at HEAD; likely NO |

## Step 3 – Affects Versions Correction (proposed)

`Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

RHTPA 2.0.0 is not a supported version. The proposal is scoped to stream 2.2.x
because of the issue suffix. The 2.1.x versions belong to a sibling or companion
issue. Jira version IDs must be discovered dynamically.
