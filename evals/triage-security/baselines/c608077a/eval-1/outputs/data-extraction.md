# TC-8001 — Data Extraction

> **Simulation notice:** This is an eval run. No Jira MCP, REST API, `git show`, WebFetch,
> or other external call was made. Every Jira operation below is a **proposed** action
> that needs engineer confirmation. None of them was performed. All data comes from
> the supplied fixture files (`vuln-issue-standard.md`, `security-matrix-mock.md`,
> `claude-md-security-config.md`).

## Pre-flight (Steps 0 – 0.6)

| Step | Result |
|------|--------|
| 0 – Validate configuration | PASS. Repository Registry (rhtpa-backend), Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present. Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, component label pattern `pscomponent:`, VEX Justification field `customfield_12345`. **Not configured:** Upstream Affected Component / PS Component / Stream custom fields, ProdSec contact/account ID, Embargo policy URL. The Source Repositories table has no Deployment Context column, so the backward-compatible default applies. |
| 0.3 – Matrix staleness | **WARNING.** The matrix `Last-Updated` is `2026-06-28T10:00:00Z`. On 2026-11-20 that is **145 days old**, well past the 14-day threshold. In a live run the engineer would choose Refresh now / Proceed anyway / Stop. For this eval the triage **proceeds with the supplied matrix**. Releases after 2.1.1 (2.1.x) or 2.2.4 (2.2.x) may be missing. |
| 0.5 – Jira access | Not initialised (eval: no external calls). |
| 0.6 – Fullsend mode detection | `FULLSEND_OUTPUT_DIR` is absent, so **interactive mode** applies. Step 0.7 (Load Trusted Fullsend Input) is sandbox-only and is skipped. |

## Early assignment actions (Step 0.8, called "Step 0.7" in the task prompt)

The task prompt calls this "Step 0.7". In the skill, Step 0.7 is the Fullsend trusted-input
load (skipped in interactive mode). "Assign and Transition to Assigned" is Step 0.8 and runs
before Step 1. These actions are **proposed only**. None was executed.

| # | Proposed Jira operation | Detail |
|---|-------------------------|--------|
| 1 | `jira.user_info()` | Get the current user's Jira account ID. |
| 2 | `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)` | Assign TC-8001 (currently **Unassigned**) to the current user. |
| 3 | `jira.get_transitions("TC-8001")` | Find the transition dynamically. Pick the one whose target status is "Assigned" (TC Vulnerability workflow name `ASSIGNED`). Do not hardcode a transition ID. |
| 4 | `jira.transition_issue("TC-8001", <assigned-transition-id>)` | The current status is **New**, so the transition applies: New → Assigned. |

Purpose: show right away who is triaging the issue, and let Step 7 detect concurrent triage
reliably. Each operation needs engineer confirmation before it runs.

## Step 1 — Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server`, which maps to repository **rhtpa-backend** | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | **RHTPA 2.0.0** | `versions` field |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High); impact is denial of service (panic on excessive STREAMS frame stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already past** as of 2026-11-20) | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | None | Comment history |
| Reporter | Not present in fixture. Needed later for the post-triage summary @mention. | — |

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Stream 2.1.x is outside this issue's scope and is handled through Case A (cross-stream).

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`).
- Category: **source dependency**, so each affected stream gets 2 remediation tasks.

### Deployment context

- rhtpa-backend is in Source Repositories with no Deployment Context column, so it defaults to `upstream` (backward compatibility).
- Per `remediation-templates.md`, Coordination Guidance is **omitted** from task descriptions when the column is absent.

## Step 1.5 — External CVE data enrichment

MITRE CVE API and OSV.dev were **not queried** (eval constraint). Following the "both
unavailable" rule:

> ⚠ External CVE databases unavailable. Using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.**

## Step 1.7 — Embargo check

No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.5 would
otherwise meet the threshold.
