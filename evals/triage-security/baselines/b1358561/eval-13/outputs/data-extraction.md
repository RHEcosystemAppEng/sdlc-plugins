# TC-8001 — Step 1 Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval constraints: no Jira MCP, no `git show`, no WebFetch. Issue data comes from `vuln-issue-standard.md`, matrix data from `security-matrix-mock.md`, and configuration from `claude-md-security-config.md`.

## Step 0: Configuration validation

| Item | Value |
|------|-------|
| Repository Registry | present (rhtpa-backend) |
| Jira Configuration | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | present (`mcp__<instance>__<tool>`, serena_backend) |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Jira version prefix | `RHTPA` |
| Vulnerability issue type ID | `10024` |
| Component label pattern | `pscomponent:` |
| VEX Justification field | `customfield_12345` |
| Upstream Affected Component field | not configured, so Step 4.3 and Step 7 are skipped |
| ProdSec Jira account ID | not configured, so @mentions are omitted |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`. Coordination Guidance is omitted for backward compatibility) |

Result: all required sections are present, so triage proceeds.

## Step 0.3: Matrix staleness check

Both streams have `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-27, so the matrix is **152 days old**, past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (152 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

For this eval I chose **Proceed anyway** and used the supplied matrix. Any release after 2.2.4 / 2.1.1 is not represented.

## Step 0.8: Assign and transition (planned, not executed)

- `jira.user_info()` returns the current account. `jira.edit_issue(TC-8001, assignee=<current-user>)`.
- `jira.get_transitions(TC-8001)`: pick the transition whose target is "Assigned". The status is `New`, so the transition applies.

## Step 1: Parsed CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Issue type / status | Vulnerability / New |
| CVE ID | **CVE-2026-31812** (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | **RHTPA 2.0.0** (no 2.0.x stream exists, so this value is wrong) |
| Vulnerable library | **quinn-proto** |
| Ecosystem | **Cargo** (Rust crate). Source dependency category |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") |
| Fixed version | **0.11.14** |
| CVSS / severity | 7.5 (High). DoS (panic on excessive stream count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html |
| Due date | 2026-07-15 (already past) |
| Assignee | Unassigned |
| Security level | none shown in the issue data (re-read live before task creation) |
| Existing comments | none |

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (`rhtpa-release.0.4.z`).
- Issue stream scope: **2.2.x (scoped)**. Affects Versions correction and standard (Depend) remediation are limited to 2.2.x. Other affected streams go through Case A (cross-stream comment + preemptive tasks).

### Deployment context

- Component maps to source repo `rhtpa-backend` (Cargo repository `backend` in Ecosystem Mappings). Deployment context defaults to `upstream`. The Deployment Context column is absent, so the Coordination Guidance subsection is omitted.

## Step 1.5: External CVE enrichment

MITRE (`cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV (`api.osv.dev/v1/vulns/CVE-2026-31812`) were **not queried** because external calls are forbidden in this eval. This is handled as "both unavailable":

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed** (Jira description, consistent with RUSTSEC reference).

## Step 1.7: Embargo check

Skipped. No Embargo policy URL is configured, even though CVSS 7.5 is above the 7.0 threshold.
