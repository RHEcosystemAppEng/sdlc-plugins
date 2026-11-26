# Step 1 – Data Extraction: TC-8020

> Note: The mock issue file (`vuln-issue-standard.md`) lists its key as `TC-8001`.
> The task directs triage of **TC-8020**; that key is used throughout. All other
> issue data is taken from the mock file.

## Preliminary steps

| Step | Result |
|------|--------|
| 0 – Validate Configuration | PASS. Repository Registry, Jira Configuration (TC, Cloud ID 2b9e35e3-...), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are present. |
| 0 – Extracted config | Project key `TC`; Jira version prefix `RHTPA`; Vulnerability issue type ID `10024`; Component label pattern `pscomponent:`; VEX Justification field `customfield_12345`; **Upstream Affected Component field `customfield_10632`** (assumed configured per task instruction); Embargo policy URL: not configured; ProdSec contact/account ID: not configured. |
| 0.3 – Matrix Staleness | WARNING. `Last-Updated: 2026-06-28T10:00:00Z` is 151 days old (threshold 14 days) for both 2.1.x and 2.2.x. The engineer would be offered Refresh / Proceed / Stop. For this eval, proceeding with the current matrix. |
| 0.6 – Fullsend Mode | Interactive mode (`FULLSEND_OUTPUT_DIR` absent). Step 0.7 skipped. |
| 0.8 – Assign/Transition | Would assign TC-8020 to current user and transition New -> Assigned (simulated, no Jira call). |

## Extracted fields

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8020 | Task input |
| CVE ID | CVE-2026-31812 | Label + summary |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Summary |
| Status | New | Issue |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Upstream Affected Component (customfield_10632) | `quinn-proto` | Custom field (per task) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability class | Denial of service (panic on excessive STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote link |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote link |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 (already past as of 2026-11-26) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` -> stream **2.2.x** (matches Version Streams table row
  `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue is **stream-scoped** to 2.2.x. Stream 2.1.x is outside scope (Case A
  cross-stream handling applies if affected).

## Ecosystem detection

- quinn-proto is a Rust crate -> **Cargo** (listed in both streams' Ecosystem
  Mappings; lock file `Cargo.lock`, repository `backend`).
- Category: **Source dependency** -> 2 remediation tasks per stream (upstream
  backport or dependency bump + downstream propagation).

## Deployment context

- Affected repository: rhtpa-backend. The Source Repositories table has no
  Deployment Context column -> default `upstream`.

## Step 1.5 – External CVE Data Enrichment

Not executed (external calls prohibited in this eval). Fallback per skill: use Jira
description data; fix-threshold confidence reduced.

> External CVE databases unavailable — using Jira description data only. Fix
> threshold confidence is reduced.

Fix threshold used: **0.11.14** (affected: < 0.11.14).

## Step 1.7 – Embargo Check

Skipped: no Embargo policy URL configured in Security Configuration (CVSS 7.5 would
otherwise have triggered the gate).

## Step 2 – Version Impact Analysis (simulated lock file data)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? |
|--------|---------|-------------|-------------|-----------------------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | YES |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

- Development stream: not determinable without Jira unreleased-version lookup
  (Step 2.2); no dev-stream data in the mock. Latest 2.2.x release already ships
  0.11.14, so `release/0.4.z` HEAD is expected to carry the fix (Step 2.5:
  fix available upstream in 2.2.x). No evidence that `release/0.3.z` carries it.

## Steps 3–6 summary

- **Step 3 – Affects Versions correction** (scoped to 2.2.x): PSIRT value
  `RHTPA 2.0.0` is wrong (no 2.0.x stream configured). Proposed:
  RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2. Remove RHTPA 2.0.0.
- **Step 4 – Duplicates/siblings/overlap**: no sibling data provided; assumed none.
- **Step 5 – Lifecycle**: lifecycle page not queried; assumed all listed versions supported.
- **Step 6 – Already fixed**: no resolved siblings; proceed.
