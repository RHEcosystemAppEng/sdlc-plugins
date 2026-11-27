# Step 1 – Data Extraction: TC-8030

Mode: interactive (FULLSEND_OUTPUT_DIR not set). Eval run, so Jira, git and WebFetch were not called. All values come from the mock fixtures.

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Check | Result |
|---|---|
| Repository Registry | PASS (rhtpa-backend, serena_backend) |
| Jira Configuration | PASS (Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432) |
| Code Intelligence | PASS (`mcp__<instance>__<tool>` naming convention) |
| Security Configuration / Product Lifecycle | PASS (Product pages URL, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:`) |
| Version Streams | PASS (2.1.x -> rhtpa-release.0.3.z, 2.2.x -> rhtpa-release.0.4.z) |
| Source Repositories | PASS (rhtpa-backend) |
| VEX Justification custom field | customfield_12345 (configured) |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Upstream Affected Component field | Not configured, so Steps 4.3 and 7 are skipped |
| ProdSec account ID | Not configured, so @mentions are skipped |
| Deployment Context column | Absent, so it defaults to `upstream` and Coordination Guidance is omitted (backward compatibility) |

## Step 0.3 – Matrix Staleness Check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-27, so the matrix is **152 days old** (threshold: 14 days).

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (152 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval decision: **Proceed anyway** using the provided matrix. Any release after 2.2.4 (2026-05-04) is missing from this analysis.

## Extracted Fields

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8030 | Issue |
| Status | New (full triage path) | Issue |
| CVE ID | CVE-2026-48901 | Label `CVE-2026-48901` + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (hyperium/h2, Rust crate) | Description |
| Affected version range (Jira) | "versions prior to the fix" (**imprecise, no numeric threshold**) | Description |
| Fixed version (Jira) | "see advisory" (**not stated**) | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability | HTTP/2 CONTINUATION flood: unbounded CONTINUATION frames after HEADERS cause excessive memory/CPU use (DoS) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| Additional advisory | https://rustsec.org/advisories/RUSTSEC-2026-0089.html | Description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 (already past as of 2026-11-27) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue |

### Critical field check

- CVE ID: present
- Library: present (h2)
- Affected range: **imprecise in Jira** ("versions prior to the fix"). The Jira prose alone gives no usable threshold. Step 1.5 is required to get one (see enrichment.md). If external data were also missing, the skill would stop here and ask the engineer for the range.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which matches the configured stream (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Stream 2.1.x is outside this issue's scope and is only handled as cross-stream impact (Case A).

## Ecosystem Detection

- h2 is a Rust crate, so the ecosystem is **Cargo**. It is listed in the Ecosystem Mappings for both streams (repo `backend`, lock file `Cargo.lock`).
- Category: **Source dependency**, which means 2 remediation tasks per affected stream.

## Deployment Context

- Affected repository: rhtpa-backend (`backend` in Ecosystem Mappings). The Source Repositories table has no Deployment Context column, so the default is `upstream`. Coordination Guidance is omitted per the backward-compatibility rule.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Assign TC-8030 to the current user, then transition New -> Assigned (transition discovered dynamically). Not executed in this eval.
