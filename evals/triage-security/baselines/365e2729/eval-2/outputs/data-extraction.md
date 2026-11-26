# TC-8002 — Data Extraction (Step 0 – Step 1.7)

## Step 0 – Configuration Validation

Source: `claude-md-security-config.md` (mock project CLAUDE.md)

| Required section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | rhtpa-backend (serena_backend) |
| Jira Configuration | Present | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<serena-instance>__<tool>` convention |
| Security Configuration > Product Lifecycle | Present | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| Security Configuration > Version Streams | Present | `2.1.x` -> rhtpa-release.0.3.z; `2.2.x` -> rhtpa-release.0.4.z |
| Security Configuration > Source Repositories | Present | rhtpa-backend -> https://github.com/rhtpa/rhtpa-backend |

Optional configuration:

| Field | Value | Effect |
|---|---|---|
| VEX Justification custom field | `customfield_12345` | Set on a "Not a Bug" (not affected) closure |
| Upstream Affected Component custom field | not configured | Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped |
| PS Component / Stream custom fields | not configured | n/a |
| ProdSec contact email / Jira account ID | not configured | No ProdSec @mentions |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Deployment Context column | absent | rhtpa-backend defaults to `upstream` |

Configuration is valid, so triage continues.

## Step 0.3 – Matrix Staleness Check

| Stream | Last-Updated | Age (today 2026-11-26) | Result |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | 151 days | STALE (over the 14-day threshold) |
| 2.2.x | 2026-06-28T10:00:00Z | 151 days | STALE (over the 14-day threshold) |

> Security matrix for stream **2.1.x** / **2.2.x** was last updated on 2026-06-28
> (151 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval decision: **Proceed anyway**. Refreshing would require external git access, which this eval does not allow. Releases after 2.2.4 (2026-05-04) that are missing from the matrix are a known gap. The final triage comment should recommend refreshing the matrix.

## Step 0.6 / 0.7 – Mode

`FULLSEND_OUTPUT_DIR` is not set, so this is **interactive mode**. Step 0.7 does not apply.

## Step 0.8 – Assign and Transition (proposed; not executed)

- `jira.user_info()` -> current user account ID
- `jira.edit_issue("TC-8002", assignee=<current-user-account-id>)` (the issue is currently Unassigned)
- `jira.get_transitions("TC-8002")` -> choose the transition whose target status is "Assigned"
- `jira.transition_issue("TC-8002", <assigned-transition-id>)`, because the status is `New`

## Step 1 – Extracted CVE Data

Status-aware handling: the issue status is **New**, so full triage proceeds.

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8002 | Issue |
| CVE ID | **CVE-2026-28940** | Label `CVE-2026-28940` and summary |
| Affected component | `pscomponent:org/rhtpa-server` -> `org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | **serde_json** | Description |
| Affected version range | **< 1.0.135** ("versions before 1.0.135") | Description |
| Fixed version | **1.0.135** | Description |
| Severity | CVSS 5.3 (Medium) | Description |
| Vulnerability | Stack overflow (unbounded recursion) when deserializing deeply nested JSON. Fix adds a recursion limit (default 128). | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 | Remote links |
| Other reference | https://rustsec.org/advisories/RUSTSEC-2026-0019.html | Description references |
| Due date | 2026-07-30 (already past as of 2026-11-26) | `duedate` |
| Assignee | Unassigned | Issue |
| Reporter | not provided in the mock data | Needed for the summary-comment @mention |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (Konflux repo `rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x. Steps 2–8 still analyze every stream for cross-stream impact, but Affects Versions and remediation apply only to 2.2.x.

### Ecosystem detection

- `serde_json` is a Rust crate, so the ecosystem is **Cargo**.
- Cargo appears in the Ecosystem Mappings of both streams (lock file `Cargo.lock`, repository `backend`).
- Category: source dependency (2 tasks per stream if affected).

### Deployment context

- Affected repository: rhtpa-backend (backend). There is no Deployment Context column, so it defaults to **upstream**.

## Step 1.5 – External CVE Data Enrichment

The eval forbids external calls, so MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-28940`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-28940`) were not queried. Both are treated as **unavailable**:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

| Source | Affected range | Fixed version |
|---|---|---|
| Jira description | < 1.0.135 | 1.0.135 |
| MITRE CVE API | unavailable | — |
| OSV.dev | unavailable | — |

**Fix threshold used for Step 2: serde_json >= 1.0.135 is fixed.**

The conclusion does not depend much on this threshold. The lowest shipped version (1.0.137) is two patch releases above it, so a small disagreement between sources would not change the outcome.

## Step 1.7 – Embargo Check

Skipped. No Embargo policy URL is configured, and CVSS 5.3 (Medium) is below the 7.0 threshold anyway.
