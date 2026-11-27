# TC-8001 — Data Extraction

> **Simulation notice:** This is an eval run. No Jira MCP, REST API, `git show`, WebFetch,
> or any other external call was made. All Jira operations below are **proposed only**.
> None of them has been performed.

## Mode and configuration

- **Step 0.6 (Fullsend mode detection):** `FULLSEND_OUTPUT_DIR` is not set, so this runs in
  **interactive mode**. Step 0.7 (trusted Fullsend input) does not apply.
- **Step 0 (configuration validation):** read from `claude-md-security-config.md`. It passes:
  Repository Registry (rhtpa-backend), Jira Configuration (Project key `TC`, Cloud ID
  `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence (serena_backend), and Security
  Configuration (Product Lifecycle, Version Streams 2.1.x/2.2.x, Source Repositories).
  - Jira version prefix: `RHTPA`
  - Vulnerability issue type ID: `10024`
  - Component label pattern: `pscomponent:`
  - VEX Justification field: `customfield_12345`
  - Product pages URL: `https://access.example.com/product-life-cycle/rhtpa`
  - Not configured: Upstream Affected Component field, PS Component field, Stream field,
    ProdSec email/account ID, Embargo policy URL, Deployment Context column.
- **Step 0.3 (matrix staleness):** the matrix has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`.
  Today is 2026-11-27, so it is **152 days old**, well past the 14-day threshold.
  > Security matrix for streams **2.1.x / 2.2.x** was last updated on 2026-06-28 (152 days ago).
  > The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

  For this eval, I chose **Proceed anyway** with the supplied matrix. Any 2.1.x/2.2.x release
  after 2026-05-04 (2.2.4) is missing from this analysis.

## Early assignment actions (task's "Step 0.7"; the skill numbers this Step 0.8)

The task calls this Step 0.7. In the current SKILL.md, Step 0.7 is the Fullsend trusted-input
loader, and "Assign and Transition to Assigned" is **Step 0.8**. These are the actions that step
would take. All are **proposed, not performed**:

| # | Operation (interactive) | Target | Detail | Status |
|---|---|---|---|---|
| 1 | `jira.user_info()` | — | Get the current user's Jira account ID | Proposed, not executed |
| 2 | `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)` | TC-8001 | Assign the CVE issue to the current user. It is currently **Unassigned**. | Proposed, not executed |
| 3 | `jira.get_transitions(TC-8001)` | TC-8001 | Find the transition dynamically by choosing the one whose target status is `Assigned` (e.g. `ASSIGNED`). No hardcoded ID. | Proposed, not executed |
| 4 | `jira.transition_issue(TC-8001, <assigned-transition-id>)` | TC-8001 | Move **New → Assigned**. This applies because the current status is `New`. | Proposed, not executed |

Status-aware handling: the issue is in **New**, so full triage proceeds with no warning.

## Step 0.5 — Jira access

Skipped for the eval. Issue data comes from `vuln-issue-standard.md`, not `jira.get_issue` or
`jira.get_issue_remote_links`.

## Step 1 — Parsed CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and the summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | **RHTPA 2.0.0** | `versions` field |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High), DoS (panic on an excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already passed** as of 2026-11-27) | `duedate` |
| Status | New | Issue |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |
| Reporter | Not in the mock data. The live `jira.get_issue` read would supply it for the post-triage @mention. | — |
| Security level | Not in the mock data. The live read would supply it, and it would be copied onto every created Task. | — |

All critical fields (CVE ID, library, affected range) parsed without problems.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x**
  (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Stream 2.1.x is outside this issue's scope. It is
  handled through Case A cross-stream logic.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. It is listed in both streams'
  Ecosystem Mappings (`backend`, `Cargo.lock`, `git show <tag>:Cargo.lock`).
- Category: **source dependency**, so each stream gets 2 remediation tasks. Those are either
  upstream backport + downstream propagation, or dependency bump + downstream propagation.

### Deployment context

- Ecosystem Mappings repository `backend` corresponds to Source Repository **rhtpa-backend**
  (https://github.com/rhtpa/rhtpa-backend).
- The Source Repositories table has no Deployment Context column. Step 1 would default this to
  `upstream`, but `remediation-templates.md` says to **omit** Coordination Guidance when the
  column is absent (backward compatibility). Remediation tasks therefore leave that subsection
  out.

## Step 1.5 — External CVE data enrichment

MITRE (`cveawg.mitre.org`) and OSV.dev were **not queried** because this eval forbids external
calls. Both sources count as unavailable:

> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold
> confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed** (Jira description).

## Step 1.7 — Embargo check

No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.5 would otherwise
meet the threshold.
