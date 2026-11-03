# TC-8001 — Step 1 Data Extraction

Mode: interactive (eval simulation — `FULLSEND_OUTPUT_DIR` not set). No Jira MCP, git, or
WebFetch calls were made. All data comes from the eval input files.

## Step 0 — Configuration Validation (summary)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |

### Source Repositories mapping (parsed from Security Configuration)

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

The Deployment Context column is present, so the backward-compatibility default (`upstream`)
does not apply.

## Step 0.3 — Matrix Staleness Check

The security matrix has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-03, so
the matrix is **128 days old**, well past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (128 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now, 2. Proceed anyway, 3. Stop

Eval assumption: **Proceed anyway** with the current matrix. Newer 2.1.x/2.2.x releases may
exist that are not covered below.

## Step 1 — Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New (full triage path) | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` + summary |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field (does not match the suffix; corrected in Step 3) |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity / CVSS | 7.5 (High) | Description |
| Vulnerability type | DoS (panic on excessive STREAMS frame stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past) | `duedate` |
| Assignee | Unassigned (Step 0.8 would assign to the current user and move it to Assigned) | Issue |
| Existing comments | none | Issue |

All critical fields (CVE ID, library, affected range) parsed successfully.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (rhtpa-release.0.4.z).
- Issue is **scoped** to 2.2.x. Other affected streams are handled through Case A (cross-stream).

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo** (listed in both streams' Ecosystem Mappings).
- Category: **Source dependency**. Lock file is `Cargo.lock` in repository `backend`.

### Deployment context lookup

| Item | Value |
|------|-------|
| Affected component label | `pscomponent:org/rhtpa-server` |
| Affected source repository | rhtpa-backend (the `backend` repo in Ecosystem Mappings, the only configured Source Repository and the Cargo repo for the server image) |
| Found in Source Repositories table? | Yes |
| **Deployment context** | **customer-shipped** |
| Default applied? | No (`upstream` default not needed) |
| Downstream use | Step 8 adds customer-shipped Coordination Guidance to the remediation task Implementation Notes |

## Step 1.5 — External CVE Data Enrichment

Not run (the eval forbids external calls). MITRE and OSV were treated as unavailable:

> External CVE databases unavailable — using Jira description data only. Fix threshold
> confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14, fixed in 0.11.14**.

## Step 1.7 — Embargo Check

CVSS 7.5 meets the threshold, but no Embargo policy URL is configured, so the step was skipped.

## Step 2 — Version Impact Analysis (from the simulated `git show <tag>:Cargo.lock` data)

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |
| dev stream | — | branch HEAD | not available | — | no unreleased Jira version data in the eval inputs |

Dependency type: not determinable without `Cargo.toml` and `cargo tree`. quinn-proto usually
comes in transitively through `quinn` (quinn → quinn-proto). Treated as **transitive**, pending
verification.

Upstream fix status (Step 2.5):

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | ≥ 0.11.14 (released tags v0.4.11 and v0.4.12 already ship 0.11.14) | YES |
| 2.1.x | Cargo | release/0.3.z | not verified (latest tag v0.3.12 = 0.11.9) | Assumed NO |

## Step 3 — Affects Versions Correction (proposed)

- Current: RHTPA 2.0.0, which is wrong. 2.0.x is not a configured stream and does not match the `[rhtpa-2.2]` suffix.
- Proposed (scoped to 2.2.x): **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
- Remove: RHTPA 2.0.0
- Version IDs would come from dynamic discovery (`getJiraIssueTypeMetaWithFields`).
- The 2.1.x impact is reported through a cross-stream comment and preemptive tasks, not added to this scoped issue.
