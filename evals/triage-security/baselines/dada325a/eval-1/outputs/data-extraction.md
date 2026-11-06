# TC-8001 — Data Extraction

> **Simulation notice:** This is an eval run. No Jira MCP call, REST call, `git show`,
> or WebFetch was made. Every Jira operation below is a **proposed** action that needs
> engineer confirmation. None of them has been performed.

## Pre-flight

- **Step 0.6 (Fullsend mode detection):** `FULLSEND_OUTPUT_DIR` is not set, so the
  skill runs in **interactive mode**.
- **Step 0.7 (trusted Fullsend input):** skipped because the skill is in interactive mode.
- **Step 0 (configuration):** `claude-md-security-config.md` passes. It contains the
  Repository Registry, Jira Configuration (Project key `TC`, Cloud ID
  `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration.
  Security Configuration includes the Product Lifecycle section (prefix `RHTPA`,
  Vulnerability type `10024`, label pattern `pscomponent:`, VEX field
  `customfield_12345`), 2 Version Streams and 1 Source Repository.
  - Optional fields that are **not configured**: Upstream Affected Component field,
    PS Component field, Stream field, ProdSec contact/account ID, Embargo policy URL.
  - The Source Repositories table has **no Deployment Context column**. The repository
    defaults to `upstream`, and remediation tasks leave out Coordination Guidance (the
    rule for older config files).
- **Step 0.3 (matrix staleness):** the matrix says `Last-Updated: 2026-06-28T10:00:00Z`.
  Today is 2026-11-06, so it is **131 days old**, well past the 14-day threshold.
  > Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
  > (131 days ago). The matrix may not reflect recent releases.
  > Options: 1. Refresh now  2. Proceed anyway  3. Stop
  - For this eval we chose **Proceed anyway**. Any 2.1.x or 2.2.x release made after
    2026-06-28 is missing from the analysis.

## Early assignment actions (the skill numbers this Step 0.8; the task calls it Step 0.7)

The task names the early assignment step "Step 0.7". In the current `SKILL.md`,
Step 0.7 is "Load Trusted Fullsend Input" (skipped here). The assign-and-transition
step is **Step 0.8 – Assign and Transition to Assigned**. It runs before Step 1.

Proposed actions, each waiting for engineer confirmation:

| # | Action | Call (not executed) | Notes |
|---|--------|---------------------|-------|
| 1 | Get the current user's account ID | `jira.user_info()` | Gives `<current-user-account-id>`. No ID is assumed. |
| 2 | Assign TC-8001 to the current user | `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)` | The issue is now **Unassigned**. |
| 3 | Look up the available transitions | `jira.get_transitions("TC-8001")` | Choose the transition whose target status is **Assigned** (`ASSIGNED` in the TC Vulnerability workflow). No transition ID is hardcoded. |
| 4 | Move TC-8001 from **New** to **Assigned** | `jira.transition_issue("TC-8001", <assigned-transition-id>)` | The status is now **New**, so the transition applies and is not skipped. |

Status check: the issue is **New**, so full triage proceeds. No in-progress or closed
warning is needed.

## Step 1 — Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and the summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | **RHTPA 2.0.0** | `versions` field |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High), denial of service (panic from unbounded stream allocation) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links and description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already overdue**, 114 days before today) | `duedate` |
| Status / Assignee | New / Unassigned (Step 0.8 changes both after confirmation) | Issue |
| Existing comments | None | Comment history |

### Stream scope resolution

- The suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (Konflux repo
  `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- The issue is **scoped to 2.2.x**. Steps 3 and 4 apply to 2.2.x versions only.
  Other affected streams go to Case A (cross-stream impact).

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo** (a source dependency).
- Both streams list Cargo in their Ecosystem Mappings: repository `backend`, lock file
  `Cargo.lock`.
- Remediation shape is **2 tasks per stream**: upstream backport (or dependency bump)
  plus downstream propagation.

### Deployment context

- Affected repository: `rhtpa-backend` (Ecosystem Mappings repository `backend`).
  Its deployment context defaults to **upstream** because the column is absent.

### Step 1.5 — External CVE data enrichment

- MITRE (`cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev were **not queried**
  because this eval does not allow external calls. Both sources count as unavailable.
  > External CVE databases unavailable. Using Jira description data only.
  > Fix threshold confidence is reduced.
- Effective fix threshold: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.**

### Step 1.7 — Embargo check

- No Embargo policy URL is configured, so this step is skipped silently. The CVSS
  score of 7.5 would otherwise trigger the gate.
