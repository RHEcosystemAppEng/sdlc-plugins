# TC-8001 — Data Extraction

> **Eval simulation.** No Jira MCP, REST, WebFetch, or `git show` calls were made.
> Every Jira operation below is a **proposed** action shown for engineer confirmation.
> None of them has been performed.

## Pre-flight (Steps 0, 0.3, 0.6)

- **Step 0.6, Fullsend mode detection:** `FULLSEND_OUTPUT_DIR` is not set, so this is **interactive mode**. Step 0.7 (Load Trusted Fullsend Input) applies only in sandbox mode and is skipped. The interactive confirmation gates stay in force.
- **Step 0, Configuration validation** (from `claude-md-security-config.md`): Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present. Validation **passes**.
  - Jira version prefix: `RHTPA`
  - Vulnerability issue type ID: `10024`
  - Component label pattern: `pscomponent:`
  - VEX Justification field: `customfield_12345` (configured)
  - Not configured: Upstream Affected Component field, PS Component field, Stream field, ProdSec contact or account ID, Embargo policy URL. The Source Repositories table has no Deployment Context column.
- **Step 0.3, Matrix staleness:** the matrix carries `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the matrix is **151 days old**, well past the 14-day threshold. The skill would warn and offer three choices: (1) Refresh now, (2) Proceed anyway, (3) Stop. This simulation assumes **Proceed anyway** and uses the supplied matrix. Releases after 2026-06-28 may be missing from the analysis.

---

## Step 0.7 / 0.8 — Early Assignment and Transition to Assigned

The task calls this the Step 0.7 early assignment. The skill's Quick Reference numbers it **Step 0.8**. It runs before data extraction so that concurrent-triage detection (Step 7) can see who is actively working the issue.

**Proposed actions** (interactive mode, each needs engineer confirmation; **NOT performed**):

1. **Retrieve current user:** `jira.user_info()` gets the current user's Jira account ID.
2. **Assign TC-8001 to the current user:**
   `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`
   The current assignee is *Unassigned*, so there is no conflict with another owner.
3. **Discover transitions dynamically:** `jira.get_transitions("TC-8001")`. Pick the transition whose target status name is `Assigned`. The TC Vulnerability workflow is Bugzilla-style and uses `ASSIGNED`. No transition ID is hardcoded.
4. **Transition TC-8001 New → Assigned:**
   `jira.transition_issue("TC-8001", <assigned-transition-id>)`
   The current status is **New**, so the transition applies and is not skipped.

Status-aware handling: the status is **New**, so the full triage path runs with no "already in progress" or "already closed" warning.

---

## Step 1 — Parsed CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` (component `org/rhtpa-server`) | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (current Jira field) | **RHTPA 2.0.0** (incorrect: no 2.0.x stream is configured) | `versions` field |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High), DoS via panic on excessive QUIC stream count | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links and description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already past** as of 2026-11-26) | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully, so no engineer input is needed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 4 limit their changes to 2.2.x. Step 2 still analyzes every stream. Any impact on 2.1.x is handled as cross-stream (Case A).

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Both streams list Cargo in their Ecosystem Mappings (`backend` repo, `Cargo.lock`).
- Category: **source dependency**, which means 2 remediation tasks per affected stream (upstream backport or dependency bump, plus downstream propagation).

### Deployment context lookup

- Affected source repository: `rhtpa-backend` (the matrix calls it `backend`).
- The Source Repositories table has no Deployment Context column, so the context defaults to `upstream` per Step 0. For backward compatibility, the remediation templates **omit** the Coordination Guidance subsection when the column is absent.

### Step 1.5 — External CVE enrichment (simulated)

The MITRE (`cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev (`api.osv.dev/v1/vulns/CVE-2026-31812`) lookups were **not executed** because external calls are disallowed in this eval. Following the "unavailable" path:

> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.**

### Step 1.7 — Embargo check

CVSS 7.5 meets the threshold of 7.0 or higher. However, **no Embargo policy URL is configured**, so Step 1.7 is skipped silently.
