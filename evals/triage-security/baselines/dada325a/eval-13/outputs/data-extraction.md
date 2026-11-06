# TC-8001: Step 1 Data Extraction

Mode: **interactive**. `FULLSEND_OUTPUT_DIR` is not set (Step 0.6). This is an eval
run, so nothing was sent to Jira, git, or the web. All data below was read from
the provided mock files.

## Step 0: Configuration Validation

| Check | Result |
|---|---|
| Repository Registry | Present (rhtpa-backend, serena_backend) |
| Jira Configuration | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present (`mcp__<instance>__<tool>`) |
| Security Configuration / Product Lifecycle | Product pages URL, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| VEX Justification custom field | `customfield_12345` |
| Upstream Affected Component / PS Component / Stream fields | **Not configured**, so Steps 4.3, 7 and 7.5.3 are skipped |
| ProdSec contact / Jira account ID | Not configured, so @mentions are omitted |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`) |
| Source Repositories | rhtpa-backend (`https://github.com/rhtpa/rhtpa-backend`). There is **no Deployment Context column**, so the context defaults to `upstream` and coordination guidance is left out of task descriptions (backward-compatibility rule) |

Configuration is valid, so triage continues.

## Step 0.3: Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-06) | Status |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | 131 days | **STALE** (over 14-day threshold) |
| 2.2.x | 2026-06-28T10:00:00Z | 131 days | **STALE** (over 14-day threshold) |

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (131 days ago). The matrix may not reflect recent releases (e.g. a 2.2.5 or 2.1.2 build).
> Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Simulated engineer choice: **Proceed anyway**, since the eval provides only this matrix data.
Any release after 2026-06-28 is missing from this analysis.

## Step 0.8: Assign and Transition (planned)

- `jira.user_info()` returns the current user's account ID
- `jira.edit_issue(TC-8001, assignee=<current-user>)`
- `jira.get_transitions(TC-8001)`, then pick the transition whose target status is "Assigned". Status is `New`, so transition to Assigned.

## Step 1: Extracted CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| Issue status | New (full triage path) | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` + summary |
| Affected component | `pscomponent:org/rhtpa-server` (org/rhtpa-server) | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` maps to stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | **RHTPA 2.0.0** (no 2.0.x stream exists, so this is wrong) | `versions` field |
| Vulnerable library | **quinn-proto** | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Vulnerability class | DoS: panic from an unbounded number of streams in a QUIC STREAMS frame | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already past** as of 2026-11-06) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream `2.2.x`, which matches the Version Streams table row `2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z`.
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 4 are scoped to 2.2.x. Other affected streams go through Case A.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. It is listed in both streams' Ecosystem Mappings (`Cargo.lock`, repo `backend`).
- Classification: **source dependency**, so each stream gets 2 remediation tasks (upstream backport or dependency bump, plus downstream propagation).

### Deployment context lookup

- Affected repository: rhtpa-backend (Ecosystem Mappings repo `backend`).
- The Source Repositories table has no Deployment Context column, so the context defaults to `upstream`. Coordination guidance is omitted per `remediation-templates.md`, because the column is absent.

## Step 1.5: External CVE Data Enrichment

The MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev
(`https://api.osv.dev/v1/vulns/CVE-2026-31812`) lookups were **not performed**,
because the eval forbids external calls. Both are treated as unavailable:

> External CVE databases unavailable. Using Jira description data only.
> Fix threshold confidence is reduced.

| Source | Affected range | Fixed version |
|---|---|---|
| Jira description | < 0.11.14 | 0.11.14 |
| MITRE CVE API | unavailable | unavailable |
| OSV.dev | unavailable | unavailable |

**Fix threshold used in Step 2: quinn-proto < 0.11.14 is affected; 0.11.14 is the fix.**

## Step 1.7: Embargo Check

Skipped. No Embargo policy URL is configured. The CVSS of 7.5 would otherwise
have triggered the gate.
