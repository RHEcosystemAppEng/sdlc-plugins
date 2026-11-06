# TC-8001 — Step 1 Data Extraction

Skill: `/sdlc-workflow:triage-security` (interactive mode; eval simulation — no Jira MCP, git, or external calls were made)

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
| Embargo policy URL | _(not configured — Step 1.7 skipped)_ |
| Upstream Affected Component field | _(not configured — Steps 4.3 / 7 skipped)_ |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |

### Source Repositories mapping (parsed from Security Configuration)

The Deployment Context column is **present**, so values come from the table. The `upstream` default was not needed.

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Issue status | New (full triage path) | Issue `status` |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Affected repository | rhtpa-backend (backend) | Component → Ecosystem Mappings `Repository` = `backend` → Source Repositories `rhtpa-backend` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field (**mismatch**: no 2.0.x stream exists, see Step 3) |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (source dependency) | Library is a Rust crate; Cargo listed in both streams' Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High). Denial of Service (panic via excessive STREAMS frame count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description references |
| Due date | 2026-07-15 | Issue `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue comments |
| **Deployment context** | **customer-shipped** | Source Repositories lookup for `rhtpa-backend` |

### Deployment context lookup result

- Affected repository resolved: **rhtpa-backend**
- Found in Source Repositories table: **yes**
- Deployment Context: **`customer-shipped`**
- Effect: Step 8 remediation tasks must include a `### Coordination Guidance` subsection in Implementation Notes, using the customer-shipped text. That text covers Product Security coordination, CVE assignment, advisory preparation, and formal disclosure through a security advisory with explicit CVE-to-component mapping.

### Stream scope resolution

- Summary suffix `[rhtpa-2.2]` → stream **2.2.x** (matches configured Version Stream `rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x. Other streams (2.1.x) are checked for cross-stream impact (Case A).

### Ecosystem classification

- Cargo → **Source dependency** → 2 remediation tasks per affected stream (upstream backport or dependency bump, plus downstream propagation).

## Step 1.5 — External Enrichment (simulated)

MITRE and OSV were not queried (eval restriction). The Jira description data is used as the fix threshold: **affected < 0.11.14, fixed 0.11.14**. Confidence is reduced because nothing external cross-checked it.

## Step 1.7 — Embargo Check

Skipped: no Embargo policy URL is configured. CVSS 7.5 would otherwise have triggered the gate.

## Step 0.3 — Matrix Staleness

Matrix `Last-Updated: 2026-06-28T10:00:00Z`. As of today (2026-11-06) it is about 131 days old, which is over the 14-day threshold. In interactive mode the engineer would be offered Refresh / Proceed / Stop. This simulation proceeds with the current matrix.

## Step 2 — Version Impact (from mock lock file data)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build | backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | out of issue scope |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | out of issue scope |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | fixed |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | fixed |

Dependency type (direct or transitive): cannot be determined from the mock data because no Cargo.lock dependency chain was provided. Recorded as "to be confirmed by implementer".

Upstream fix status (Step 2.5): branch HEAD lock files were not provided. Tag evidence shows `release/0.4.z` has shipped 0.11.14 since `v0.4.11`, so the fix is on the 2.2.x upstream line. `release/0.3.z` has no tag with a fixed version (all 0.11.9), so it is treated as **not fixed upstream**.

## Step 3 — Affects Versions Correction (proposed)

- Current: RHTPA 2.0.0. This is wrong: there is no 2.0.x stream, and PSIRT assigned it at scan time.
- Proposed (scoped to 2.2.x): **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
- 2.1.0 and 2.1.1 are affected but outside this issue's scope. They are reported through the cross-stream comment (Case A), not added to this issue.
