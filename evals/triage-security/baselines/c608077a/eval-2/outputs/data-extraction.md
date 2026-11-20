# TC-8002 — Data Extraction (Step 0 – Step 1.7)

Skill: `sdlc-workflow:triage-security` (interactive mode; `FULLSEND_OUTPUT_DIR` not set).
Eval constraint: no Jira MCP, `git show`, WebFetch or other external calls. Every value
below comes from the supplied input files (mock Jira issue, mock security matrix, mock
CLAUDE.md).

## Step 0 – Project Configuration validation

| Required section | Present | Values extracted |
|---|---|---|
| Repository Registry | Yes | rhtpa-backend (Rust backend service, Serena `serena_backend`) |
| Jira Configuration | Yes | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Yes | Naming convention `mcp__<serena-instance>__<tool>` |
| Security Configuration / Product Lifecycle | Yes | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| Security Configuration / Version Streams | Yes | 2.1.x → `rhtpa-release.0.3.z`; 2.2.x → `rhtpa-release.0.4.z` |
| Security Configuration / Source Repositories | Yes | rhtpa-backend → `https://github.com/rhtpa/rhtpa-backend` |

Optional fields:

| Field | Status | Effect |
|---|---|---|
| VEX Justification custom field | `customfield_12345` | Gets set when the issue is closed as Not a Bug |
| Upstream Affected Component / PS Component / Stream fields | Not configured | Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped |
| ProdSec contact email / Jira account ID | Not configured | No ProdSec @mention in comments |
| Embargo policy URL | Not configured | Step 1.7 skipped |
| Deployment Context column | Absent | rhtpa-backend defaults to `upstream` |

Result: the configuration is valid, so triage continues.

## Step 0.3 – Matrix staleness check

| Stream | Last-Updated | Age on 2026-11-20 | Status |
|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | 2026-06-28T10:00:00Z | 145 days | STALE (threshold is 14 days) |
| 2.2.x (rhtpa-release.0.4.z) | 2026-06-28T10:00:00Z | 145 days | STALE (threshold is 14 days) |

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (145 days ago). It may not reflect recent releases. Options: 1. Refresh now,
> 2. Proceed anyway, 3. Stop.

Eval decision: **Proceed anyway**. A refresh needs git access, which this eval does not
allow. This does not change the outcome. Every listed version already ships a
serde_json release above the fix threshold, and serde_json only moved forward between
builds (1.0.137 → 1.0.138 → 1.0.139). A newer build would most likely not go back below
1.0.135. The engineer should still refresh the matrix before the next triage.

## Step 0.8 – Assign and transition (proposed, not executed)

- Proposed: `jira.user_info()`, then `jira.edit_issue(TC-8002, assignee=<current-user>)`
- Proposed: `jira.get_transitions(TC-8002)`, then a transition to the status named "Assigned"
  (the current status is **New**, so the transition applies)

## Step 1 – Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8002 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | **CVE-2026-28940** | Label `CVE-2026-28940` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | **serde_json** | Description |
| Affected version range | **< 1.0.135** ("versions before 1.0.135") | Description |
| Fixed version | **1.0.135** | Description |
| Vulnerability | Stack overflow from unbounded recursion when deserializing deeply nested JSON (DoS / process crash) | Description |
| Fix summary | Configurable recursion limit, default 128 nesting levels | Description |
| CVSS | 5.3 (Medium) | Description |
| Upstream fix PR | None in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 | Remote links |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0019.html | Description |
| Due date | 2026-07-30 (already past on 2026-11-20) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comments |

All critical fields (CVE ID, library, affected range) were parsed. No engineer input is
needed.

### Stream scope resolution

- Summary suffix: `[rhtpa-2.2]` → stream **2.2.x**
- Matches the configured Version Stream `2.2.x` (`git.example.com/rhtpa/rhtpa-release.0.4.z`)
- **Issue stream scope: 2.2.x (scoped)**. Steps 3 and 4 are limited to 2.2.x. Step 2
  still analyzes every stream so that cross-stream impact can be detected.

### Ecosystem detection

- serde_json is a Rust crate, so the ecosystem is **Cargo**
- Cargo appears in both streams' Ecosystem Mappings (repository `backend`, lock file
  `Cargo.lock`, check command `git show <tag>:Cargo.lock`)
- Category: **Source dependency** (2 remediation tasks per affected stream if any stream
  were affected)

### Deployment context

- The component maps to repository rhtpa-backend (the `backend` source in the matrix)
- The Source Repositories table has no Deployment Context column, so the context
  defaults to **upstream**

## Step 1.5 – External CVE data enrichment

| Source | Query (not executed) | Result |
|---|---|---|
| MITRE CVE API | `https://cveawg.mitre.org/api/cve/CVE-2026-28940` | Not queried (eval forbids external calls) |
| OSV.dev | `https://api.osv.dev/v1/vulns/CVE-2026-28940` | Not queried (eval forbids external calls) |

> ⚠ External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

**Fix threshold used for Step 2:** serde_json `< 1.0.135` is affected; `>= 1.0.135` is
fixed. Lower confidence matters little here. The lowest shipped version (1.0.137) sits
two patch releases above the threshold, so a small disagreement between external
sources would not change the result.

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured, and CVSS 5.3 (Medium) is below the
7.0 trigger threshold anyway.
