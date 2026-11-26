# TC-8001 — Data Extraction

> **Simulation notice:** This is an eval run. No Jira MCP, REST API, `git show`, or
> WebFetch call was made. Every Jira operation below is a **proposed** action that would
> run only after explicit engineer confirmation. No Jira operation has been performed.

## Pre-flight (Steps 0 – 0.6)

| Step | Result |
|------|--------|
| 0.6 Fullsend Mode Detection | `FULLSEND_OUTPUT_DIR` is absent, so this is **interactive mode** (the normal confirmation-gated workflow applies) |
| 0.7 Load Trusted Fullsend Input | Skipped (sandbox mode only) |
| 0 Validate Configuration | Pass: Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present |
| 0.3 Matrix Staleness Check | **Warning:** both stream matrices have `Last-Updated: 2026-06-28T10:00:00Z`, which is **151 days old** (threshold 14 days). The engineer would choose: 1. Refresh now, 2. Proceed anyway, 3. Stop. *This simulation proceeds with the current matrix (option 2).* |
| 0.5 Jira Access | Not initialized (simulation) |

Extracted Security Configuration:

| Setting | Value |
|---------|-------|
| Jira version prefix | `RHTPA` |
| Vulnerability issue type ID | `10024` |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | `customfield_12345` |
| Upstream Affected Component / PS Component / Stream fields | **Not configured**, so Steps 4.3, 7, and 7.5.3 are skipped |
| ProdSec contact / Jira account ID | Not configured (no @mentions) |
| Embargo policy URL | Not configured (Step 1.7 skipped) |
| Version Streams | `2.1.x` → `rhtpa-release.0.3.z`; `2.2.x` → `rhtpa-release.0.4.z` |
| Source Repositories | `rhtpa-backend` (https://github.com/rhtpa/rhtpa-backend). There is no Deployment Context column, so the context defaults to `upstream` |

---

## Early Assignment Actions (skill Step 0.8, called "Step 0.7" in the eval task)

TC-8001 is currently **Unassigned** in status **New**. Before data extraction, the skill
assigns the issue and moves it to Assigned. The proposed actions (awaiting confirmation,
**not performed**) are:

1. **Retrieve the current user's account ID**
   ```
   jira.user_info()  →  <current-user-account-id>
   ```
2. **Assign TC-8001 to the current user**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   This runs regardless of status, so the active triager is always recorded.
3. **Discover the Assigned transition dynamically.** No transition ID is hardcoded,
   because Vulnerability issues use a Bugzilla-style workflow (`ASSIGNED`, `POST`, `MODIFIED`, ...).
   ```
   jira.get_transitions("TC-8001")  →  select transition whose target status is "Assigned"
   ```
4. **Transition TC-8001 from New to Assigned.** The issue is in `New`, so the
   transition is required.
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

Status-aware handling: the status is `New`, so full triage proceeds with no warning.

---

## Step 1 — Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` → `org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (scoped) | `[rhtpa-2.2]` matches Version Stream `2.2.x` |
| Affects Versions (Jira field) | `RHTPA 2.0.0` (**suspect:** no 2.0.x stream is configured) | `versions` field |
| Vulnerable library | **quinn-proto** | Description |
| Ecosystem | **Cargo** (Rust crate) → source dependency, 2 remediation tasks per stream | Library + Ecosystem Mappings |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High) | Description |
| Vulnerability type | Denial of service (panic from an unbounded STREAMS frame stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already past** as of 2026-11-26) | `duedate` |
| Existing comments | None | Comment history |
| Assignee | Unassigned (the Step 0.8 assignment is proposed above) | Issue |
| Affected repository / deployment context | `rhtpa-backend` (Ecosystem Mappings repo `backend`) / `upstream` (default, because the column is absent) | Source Repositories |

All critical fields (CVE ID, library, affected range) parsed successfully.

### Step 1.5 — External CVE Data Enrichment

The MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev
(`https://api.osv.dev/v1/vulns/CVE-2026-31812`) lookups were **not executed**, because
external tools are disabled for this eval.

> ⚠ External CVE databases unavailable. Using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 is vulnerable; 0.11.14 is fixed.**

### Step 1.7 — Embargo Check

Skipped silently: no Embargo policy URL is configured. CVSS 7.5 would otherwise meet
the ≥ 7.0 trigger.
