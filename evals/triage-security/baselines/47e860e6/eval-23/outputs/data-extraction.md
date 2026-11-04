# TC-8001 — Step 1 Data Extraction (triage-security)

> Eval mode: Jira MCP, `git show`, MITRE/OSV and lifecycle lookups were **not** called.
> All values below come from the provided mock files (`vuln-issue-standard.md`,
> `security-matrix-mock.md`, `claude-md-security-config-deploy-ctx.md`).
> Execution mode: interactive (`FULLSEND_OUTPUT_DIR` not set). Steps 0.6/0.7 therefore leave the interactive workflow unchanged.

## Step 0 — Configuration validated

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec contact / account ID | not configured (no @mention) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → `rhtpa-release.0.3.z`; 2.2.x → `rhtpa-release.0.4.z` |
| Source Repositories mapping | `rhtpa-backend` → { url: https://github.com/rhtpa/rhtpa-backend, deployment_context: **customer-shipped** } |

The Source Repositories table **includes** the Deployment Context column, so the backward-compatible `upstream` default does not apply.

## Step 0.3 — Matrix staleness check

| Stream | Last-Updated | Age (as of 2026-11-04) | Result |
|--------|--------------|------------------------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 129 days | **STALE** (more than 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 129 days | **STALE** (more than 14 days) |

> Security matrix for both streams was last updated on 2026-06-28 (129 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now / 2. Proceed anyway / 3. Stop.

Eval decision: **Proceed anyway** (the matrix cannot be refreshed without external access). Versions released after 2026-06-28 (for example a 2.2.5) would be missing from this analysis.

## Step 0.8 — Assign and transition

Proposed (not executed): assign TC-8001 to the current triager. The issue is in **New**, so transition it to **Assigned** using the transition discovered dynamically through `get_transitions`.

## Step 1 — Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` → `org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 (**incorrect**: no 2.0.x stream exists) | `versions` field |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High), DoS (panic on excessive STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-04) | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed. Nothing needs to be supplied by the engineer.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` → matches configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 4 are limited to 2.2.x. Other affected streams are handled through Case A (cross-stream).

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (`Cargo.lock`, `git show <tag>:Cargo.lock`).
- Classification: **source dependency**, which means 2 remediation tasks per stream.

### Deployment context lookup

| Step | Result |
|------|--------|
| Affected component | `org/rhtpa-server` |
| Source repo that builds it | `backend` (the only source column in the Supportability Matrix and the Cargo `Repository` in Ecosystem Mappings) → **rhtpa-backend** in Source Repositories |
| Found in Source Repositories table? | **Yes** |
| Deployment Context column present? | **Yes** |
| **Deployment context** | **`customer-shipped`** |
| Fallback applied? | No (the `upstream` default applies only when the repo is missing or the column is absent) |

Recorded for Step 8: every remediation task's Implementation Notes gets the **customer-shipped** Coordination Guidance (Product Security coordination for CVE assignment, advisory preparation, and formal disclosure through a security advisory with explicit CVE-to-component mapping).

## Step 1.5 — External CVE enrichment

MITRE CVE API and OSV.dev were **not queried** (eval restriction), so they are treated as unavailable.

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14, fixed in 0.11.14** (Jira description, consistent with RUSTSEC-2026-0042 reference).

## Step 1.7 — Embargo check

No Embargo policy URL is configured, so the step is skipped silently. (CVSS 7.5 would otherwise have triggered the gate.)

## Step 2 — Version impact (simulated `git show <tag>:Cargo.lock` from mock data)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | **YES** | outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | **YES** | outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | v0.4.8 | — | **YES** | same as 2.2.1 (backend retag, so the lock file check was skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version shipped |
| dev stream | — | branch HEAD | not determined | — | Step 2.2 needs Jira unreleased versions, which were not queried. No development stream was identified. |

Dependency chain (Step 2.3.5): the mock provides only lock file versions, not `Cargo.toml` manifests, so direct vs transitive could not be confirmed. quinn-proto is normally pulled in transitively (for example `backend → reqwest/quinn → quinn-proto`). Treat it as **transitive (unverified)** and production scope, because it is a runtime QUIC dependency and is not a dev-dependency. `/implement-task` must confirm this.

Upstream fix status (Step 2.5; HEAD was not inspected, inferred from the latest released tags):

| Stream | Ecosystem | Upstream Branch | Latest evidence | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | v0.4.11 / v0.4.12 ship 0.11.14 | YES (likely; confirm at HEAD) |
| 2.1.x | Cargo | release/0.3.z | v0.3.12 ships 0.11.9 | NO (no evidence of fix) |

## Step 3 — Affects Versions correction (scoped to 2.2.x)

`Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

RHTPA 2.0.0 does not exist in any configured stream. The 2.1.x versions are excluded because they are outside this issue's scope. Version IDs must be discovered at runtime (not executed).

## Steps 4–7 summary

- Step 4: Sibling JQL was not executed. In this eval no siblings are assumed, so there is no duplicate, and 2.1.x has no CVE Jira of its own, which leads to Case A preemptive tasks. Step 4.3 was skipped because the Upstream Affected Component field is not configured.
- Step 5: The lifecycle page was not fetched. 2.1.x and 2.2.x are assumed to be supported (needs verification).
- Step 6: No resolved siblings, so the issue proceeds to Step 8.
- Step 7: Skipped because the Upstream Affected Component field is not configured.
- Step 7.5: The release Epic/Task (for example "RHTPA 2.2.5 Release Tasks" / "RHTPA 2.2.5 CVE triage") would be found or created with individual confirmation. Placeholder keys are used.

## Outcome

**Case A + Case B.** The issue is scoped to 2.2.x, 2.2.x is affected (2.2.0–2.2.2), and 2.1.x is also affected. See `remediation.md`.
