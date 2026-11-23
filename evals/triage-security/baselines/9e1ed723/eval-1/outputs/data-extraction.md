# TC-8001 — Data Extraction

> Eval run: no Jira MCP, REST, `git show`, or WebFetch calls were made. Every action
> below is a **proposed** action that waits for engineer confirmation. No Jira
> operation has been performed.

## Pre-flight (Steps 0 – 0.6)

| Check | Result |
|---|---|
| Step 0 – Project Configuration | Present: Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, Security Configuration (Product Lifecycle, Version Streams, Source Repositories). Proceed. |
| Jira version prefix | `RHTPA` |
| Vulnerability issue type ID | `10024` |
| Component label pattern | `pscomponent:` |
| VEX Justification field | `customfield_12345` (configured) |
| Upstream Affected Component / PS Component / Stream fields | **Not configured**: Step 4.3, Step 7, and Step 7.5.3 dedup will be skipped |
| ProdSec email / Jira account ID | Not configured: no @mentions in correction or overlap comments |
| Embargo policy URL | Not configured: Step 1.7 skipped |
| Source Repositories → Deployment Context column | Column is absent. Step 0 defaults the context to `upstream`, but per `remediation-templates.md` (backward compatibility) the Coordination Guidance subsection is left out of task descriptions |
| Step 0.3 – Matrix staleness | `Last-Updated: 2026-06-28T10:00:00Z` is **148 days old** (threshold is 14). **Warning:** the matrix may not reflect recent releases. Options: 1) Refresh now, 2) Proceed anyway, 3) Stop. For this eval, assumed **Proceed anyway**. A refresh is recommended before any Jira write. |
| Step 0.5 – Jira access | Not initialized (eval: no external calls) |
| Step 0.6 – Fullsend mode | `FULLSEND_OUTPUT_DIR` is absent, so this is **interactive mode** (Fullsend Step 0.7 trusted-input load does not apply) |

## Early assignment and transition to Assigned (task "Step 0.7" = SKILL.md Step 0.8)

This runs before data extraction, so the issue shows right away that someone is
triaging it, and so Step 7 concurrent-triage detection can see the work.

Current issue state (from the mock issue): **Status: New**, **Assignee: Unassigned**.

Proposed actions, which require engineer confirmation. **None of these was performed:**

1. **Get the current user's account ID**
   `jira.user_info()` → `<current-user-account-id>`
2. **Assign TC-8001 to the current user**
   `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`
   The issue is currently Unassigned, so it would not replace another owner.
3. **Find the Assigned transition dynamically**
   `jira.get_transitions("TC-8001")`. Pick the transition whose target status name
   is `Assigned` (TC Vulnerability workflow: `ASSIGNED`). The transition ID is not
   hardcoded.
4. **Move TC-8001 from New to Assigned**
   `jira.transition_issue("TC-8001", <assigned-transition-id>)`
   This applies because the issue is in **New**. If it were already Assigned or later,
   the transition would be skipped and only the assignment would be applied.

Status-aware handling: the status is **New**, so the full triage path applies with no
warning.

## Step 1 – Parsed CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix in brackets |
| Issue stream scope | **2.2.x** (scoped) | Suffix `[rhtpa-2.2]` maps to Version Stream `2.2.x` (`git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Affects Versions (Jira field) | **RHTPA 2.0.0** | `versions` field. No 2.0.x stream exists in the matrix, so this is suspect |
| Vulnerable library | **quinn-proto** | Description |
| Ecosystem | **Cargo** (Rust crate). It is in the stream's Ecosystem Mappings, so it is supported. Category: source dependency (2 tasks per stream) | Library and Ecosystem Mappings |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High), DoS | Description |
| Affected repository | `backend` (Ecosystem Mappings Repository for Cargo), which is `rhtpa-backend` (https://github.com/rhtpa/rhtpa-backend) | Matrix and Source Repositories |
| Deployment context | `upstream` (default: no Deployment Context column) | Source Repositories |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042: https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links and description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already past** as of 2026-11-23) | `duedate` |
| Existing comments | None | Comment history |
| Reporter | Not in the mock data. Needed for the post-triage summary @mention; read it from `jira.get_issue` at run time | — |

All critical fields (CVE ID, library, affected range) parsed. Nothing is missing.

### Step 1.5 – External CVE enrichment

MITRE (`cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev
(`api.osv.dev/v1/vulns/CVE-2026-31812`) were **not queried** because this eval allows
no external calls. Both sources are treated as unavailable:

> External CVE databases unavailable. Using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 affected; 0.11.14 fixed**.

### Step 1.7 – Embargo check

Skipped: no Embargo policy URL is configured. CVSS 7.5 would otherwise meet the
>= 7.0 threshold for the warning gate.
