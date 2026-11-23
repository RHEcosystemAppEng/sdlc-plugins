# TC-8001 — Triage Data Extraction (Steps 0–2)

Mode: interactive (FULLSEND_OUTPUT_DIR absent). External calls (Jira MCP, git show,
WebFetch) were NOT executed for this eval; all data comes from the provided mock files.

## Step 0 — Configuration Validation

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | rhtpa-backend (serena_backend) |
| Jira Configuration | Present | Project key: TC; Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Code Intelligence | Present | `mcp__<serena-instance>__<tool>` convention |
| Security Configuration / Product Lifecycle | Present | Product pages URL: https://access.example.com/product-life-cycle/rhtpa; Jira version prefix: RHTPA; Vulnerability issue type ID: 10024; Component label pattern: `pscomponent:`; VEX Justification field: customfield_12345 |
| Security Configuration / Version Streams | Present | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Security Configuration / Source Repositories | Present (with Deployment Context column) | see mapping below |

Optional fields not configured (skipped silently): Upstream Affected Component field
(Step 4.3 and Step 7 skipped), PS Component field, Stream field, ProdSec contact email,
ProdSec Jira account ID, Embargo policy URL (Step 1.7 skipped).

### Source Repositories mapping (repository → { url, deployment_context })

| Repository | URL | Deployment Context |
|---|---|---|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

The Deployment Context column is present, so no `upstream` default was applied.

## Step 0.3 — Matrix Staleness Check

Matrix `Last-Updated: 2026-06-28T10:00:00Z`; today is 2026-11-23 → **148 days old**
(threshold 14 days).

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (148 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval assumption: engineer chose **Proceed anyway** (the supplied mock matrix is the
only available data).

## Step 1 — Parsed CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| Issue status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Affected repository | rhtpa-backend | Component → Repository Registry / Ecosystem Mappings (`backend`) |
| **Deployment context** | **customer-shipped** | Source Repositories lookup for `rhtpa-backend` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → RHTPA 2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / severity | 7.5 (High) — DoS (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-23) | `duedate` |
| Assignee | Unassigned (Step 0.8 would assign to current user and transition New → Assigned) | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

### Stream scope resolution

- Summary suffix `[rhtpa-2.2]` → stream **2.2.x** (matches configured Version Stream
  `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue is **scoped** to 2.2.x. Stream 2.1.x is outside scope (cross-stream handling
  via Case A).

### Ecosystem detection

- quinn-proto is a Rust crate → **Cargo** (present in both streams' Ecosystem Mappings).
- Category: **Source dependency** → 2 remediation tasks per stream (upstream backport
  or dependency bump + downstream propagation).

### Deployment context lookup

| Affected repository | Found in Source Repositories? | Deployment context | Used in |
|---|---|---|---|
| rhtpa-backend | Yes | **customer-shipped** | Step 8 — Coordination Guidance in every remediation task's Implementation Notes |

## Step 1.5 — External CVE Data Enrichment

MITRE and OSV queries were not executed (eval forbids external calls). Treated as
unavailable:

> External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 affected; 0.11.14 fixed**.

## Step 1.7 — Embargo Check

No Embargo policy URL configured → skipped (CVSS 7.5 would otherwise trigger the gate).

## Step 2 — Version Impact Analysis

Lock file data taken from the mock `git show <tag>:Cargo.lock` output in
security-matrix-mock.md. Development stream (Step 2.2) could not be determined: no
Jira unreleased-version data was supplied and 2.2.x is the latest stream (no forward
pointer), so no separate dev-stream HEAD row is included.

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |

### Dependency chain (Step 2.3.5)

Dependency chain for quinn-proto:
  Type: not determinable from supplied data (no Cargo.toml / full Cargo.lock graph in
  mock). quinn-proto is commonly pulled in transitively via `quinn` (e.g. reqwest
  `http3`), but this must be confirmed from the manifest before implementation.
  Profile: assumed production (no evidence of dev/build-only scope) → no
  `dev-dependency` label, priority not overridden.

### Upstream fix status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | release/0.3.z | not available (latest release tag v0.3.12 = 0.11.9) | Not confirmed → treat as NOT fixed |
| 2.2.x | Cargo | release/0.4.z | not available (released tags v0.4.11/v0.4.12 = 0.11.14) | YES (fix already shipped in 2.2.3) |

## Step 3 — Affects Versions Correction (proposed)

- Current: RHTPA 2.0.0 (no 2.0.x stream exists; not supported by lock file evidence).
- Proposed (scoped to 2.2.x): **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**.
- Remove RHTPA 2.0.0. Version IDs to be discovered dynamically via
  `getJiraIssueTypeMetaWithFields` (not executed).

## Steps 4–7 (summary)

- Step 4: sibling JQL search for `labels = CVE-2026-31812` not executed; assumed no
  2.1.x sibling CVE Jira exists → preemptive tasks for 2.1.x (Case A).
- Step 5: lifecycle check not executed; all listed versions treated as supported.
- Step 6: no resolved siblings known.
- Step 7: skipped (Upstream Affected Component field not configured).
- Step 7.5: release Jira lookup not executed; release Epic/Task linking to be performed
  for non-preemptive tasks only if found/created.
