# TC-8001 — Data Extraction

> Eval run: no Jira MCP, REST, `git show`, or WebFetch calls were made. Every Jira
> operation below is a **proposed** action waiting for engineer confirmation. None
> of them has been performed.

## Step 0.7 (SKILL.md numbers this Step 0.8): Early assignment

Step 0.6 found no `FULLSEND_OUTPUT_DIR`, so this run uses **interactive mode**. Step 0.7
(Load Trusted Fullsend Input) applies only to sandbox mode and is skipped. The early
assignment therefore follows the interactive procedure.

Current issue state (from the mock issue): **Status = New**, **Assignee = Unassigned**.

Proposed actions, in order (each one needs engineer confirmation; none has been run):

1. **Get the current user's account ID**
   ```
   jira.user_info()
   ```
2. **Assign TC-8001 to the current user**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
3. **Look up the available transitions** (no hardcoded transition ID or name.
   Vulnerability issues use a Bugzilla-style workflow such as `ASSIGNED`, `POST`, `MODIFIED`)
   ```
   jira.get_transitions("TC-8001")
   ```
   Pick the transition whose target status name matches "Assigned" (case-insensitive,
   for example `ASSIGNED`).
4. **Move TC-8001 from New to Assigned**
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```
   The issue is in **New**, so this transition applies. If it were already in Assigned
   or a later status, this step would be skipped and only the assignment would run.

Purpose: shows right away who is triaging the issue, and lets Step 7 (concurrent
triage detection) see that the issue is actively being worked.

## Pre-steps (context)

- **Step 0: Configuration check.** Passed. Repository Registry, Jira Configuration
  (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence,
  and Security Configuration are all present. The Security Configuration includes
  Product Lifecycle (URL, prefix `RHTPA`, Vulnerability type `10024`, label pattern
  `pscomponent:`), 2 Version Streams, and 1 Source Repository.
  - VEX Justification field: `customfield_12345` (configured)
  - Not configured: Upstream Affected Component field, PS Component field, Stream field,
    ProdSec contact/account ID, Embargo policy URL
- **Step 0.3: Matrix staleness.** **STALE.** Both stream matrices carry
  `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, which is **129 days** ago
  and over the 14-day threshold. The engineer should choose one of: (1) Refresh now,
  (2) Proceed anyway, (3) Stop. This eval continues with the current matrix (option 2).
  The tables below may therefore miss any 2.1.x or 2.2.x releases after 2026-06-28.
- **Step 0.5: Jira access.** Not set up in this eval. No calls were made.

## Step 1: Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | **RHTPA 2.0.0** | `versions` field |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High), DoS (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already past**) | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | None | Issue |

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x**
  (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **The issue is scoped to stream 2.2.x.** Steps 3, 4, and 8 are scoped to that stream.
  Any impact on 2.1.x is handled as cross-stream impact (Case A).

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both
  streams' Ecosystem Mappings (repository `backend`, lock file `Cargo.lock`).
- Category: **source dependency**, so there are 2 remediation tasks per affected stream.

### Deployment context

- The affected repository is `rhtpa-backend` (the `backend` mapping). The Source
  Repositories table has **no Deployment Context column**. For backward compatibility,
  the context defaults to `upstream`, and the Coordination Guidance subsection is
  left out of task descriptions, as `remediation-templates.md` requires.

### Step 1.5: External CVE data enrichment

MITRE (`cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev were **not queried**
because this eval allows no external calls.
> External CVE databases unavailable. Using Jira description data only.
> Fix-threshold confidence is lower. Threshold used: quinn-proto **< 0.11.14**, fixed in
> **0.11.14**.

### Step 1.7: Embargo check

No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.5 would
otherwise trigger the gate.
