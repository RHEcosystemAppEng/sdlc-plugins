# TC-8002 — Data Extraction (Step 0 – Step 1.7)

## Step 0 – Configuration Validation

Source: `claude-md-security-config.md`, the mock project CLAUDE.md.

| Required section | Present | Values extracted |
|---|---|---|
| Repository Registry | Yes | rhtpa-backend (serena_backend) |
| Jira Configuration | Yes | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Yes | `mcp__<serena-instance>__<tool>` naming convention |
| Security Configuration / Product Lifecycle | Yes | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| Security Configuration / Version Streams | Yes | 2.1.x → `rhtpa-release.0.3.z`, 2.2.x → `rhtpa-release.0.4.z` |
| Security Configuration / Source Repositories | Yes | rhtpa-backend → `https://github.com/rhtpa/rhtpa-backend` |

Optional fields:

| Field | Status |
|---|---|
| VEX Justification custom field | Configured: `customfield_12345` |
| Upstream Affected Component custom field | Not configured. Step 4.3 and Step 7 are skipped |
| PS Component / Stream custom fields | Not configured |
| ProdSec contact email / Jira account ID | Not configured. @mentions are omitted |
| Embargo policy URL | Not configured. Step 1.7 is skipped |
| Deployment Context column | Absent. rhtpa-backend defaults to `upstream` |

The configuration is complete, so triage continues.

## Step 0.3 – Matrix Staleness Check

- The matrix contains `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`.
- Today is 2026-11-03, so the matrix is **128 days old**. The threshold is 14 days.
- **Warning:** The security matrices for streams **2.1.x** and **2.2.x** were last updated on 2026-06-28, 128 days ago, and may not reflect recent releases. For example, 2.2.5+ or a 2.3/3.0 stream may exist and be missing from the matrix. Options: (1) refresh now, (2) proceed anyway, (3) stop.
- Eval mode cannot prompt the engineer, so this triage **proceeds with the current matrix** (option 2). The outcome records the staleness caveat.

## Step 0.6 / 0.7 – Mode Detection

`FULLSEND_OUTPUT_DIR` is not set, so this is interactive mode, simulated. Step 0.7 (trusted input bundle) is skipped.

## Step 0.8 – Assign and Transition (proposed only, not executed)

- Issue status is `New` and the issue is unassigned.
- Proposed: `jira.user_info()`, then `jira.edit_issue(TC-8002, assignee=<current-user>)`, then `jira.get_transitions(TC-8002)` to find the transition whose target is "Assigned", then transition the issue.
- Status-aware handling: the status is `New`, so the full triage path applies.

## Step 1 – Extracted CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8002 | Issue |
| CVE ID | **CVE-2026-28940** | Label `CVE-2026-28940` and summary |
| Affected component | `pscomponent:org/rhtpa-server` → repository rhtpa-backend (`backend` column in matrix) | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | **serde_json** | Description |
| Affected version range | **< 1.0.135** ("versions before 1.0.135") | Description |
| Fixed version | **1.0.135** | Description |
| Severity | CVSS 5.3 (Medium) | Description |
| Vulnerability | Stack overflow from unbounded recursion when deserializing deeply nested JSON. The fix adds a recursion limit, default 128. | Description |
| Upstream fix PR | None (no GitHub PR remote link) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0019.html | Description references |
| Due date | 2026-07-30 (**already past**, today is 2026-11-03) | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | None | Comment history |
| Reporter | Not present in mock data. The post-triage summary needs the reporter's account ID for its @mention | — |

All critical fields (CVE ID, library, affected range) were parsed, so no engineer input is needed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (`rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3, 4, and 8 apply to the 2.2.x stream. 2.1.x is still analyzed for cross-stream impact (Case A).

### Ecosystem detection

- serde_json is a Rust crate, so the ecosystem is **Cargo**. It is listed in the Ecosystem Mappings for both streams.
- Category: source dependency. If the issue were affected, each stream would get 2 tasks.
- Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`.

### Deployment context

- rhtpa-backend has no Deployment Context column, so it defaults to **upstream**.

## Step 1.5 – External CVE Data Enrichment

- The eval forbids external calls, so the MITRE CVE API (`https://cveawg.mitre.org/api/cve/CVE-2026-28940`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-28940`) were **not queried**. This is treated as "Unavailable".
- **Warning:** External CVE databases are unavailable, so this triage uses Jira description data only and fix-threshold confidence is reduced.
- Fix threshold used: **serde_json < 1.0.135 is vulnerable, and 1.0.135 is the fix.**
- The lowest shipped serde_json version in this analysis is 1.0.137. Even if MITRE or OSV moved the threshold up by a couple of patch versions, the conclusion would hold up to 1.0.137. A real run should still cross-validate.

## Step 1.7 – Embargo Check

- **Skipped** because no Embargo policy URL is configured. It would be skipped anyway because CVSS 5.3 is below the 7.0 threshold.
