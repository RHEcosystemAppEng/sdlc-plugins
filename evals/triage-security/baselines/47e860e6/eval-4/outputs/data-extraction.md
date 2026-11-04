# TC-8004 — Step 1: Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation: Jira/git/WebFetch calls are not executed; the input files stand in for those responses.

## Step 0 — Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | not configured (so Steps 4.3 and 7 are skipped) |
| ProdSec contact / account ID | not configured (no @mention) |
| Embargo policy URL | not configured (so Step 1.7 is skipped) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). No Deployment Context column, so it defaults to `upstream` and Coordination Guidance is omitted per the template's backward-compat rule |

All required sections are present, so triage proceeds.

## Step 0.3 — Matrix staleness

The matrix carries `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, so it is about 129 days old (threshold 14 days). **Warning: the matrix is stale and may not reflect recent releases.** The options are Refresh / Proceed / Stop. For this eval we proceed with the current matrix. A refresh is recommended before the Jira mutations are applied.

## Step 0.8 — Assign / transition

Status is New and the issue is unassigned. Proposed: assign TC-8004 to the current user and transition it to Assigned, with the target resolved from the live `get_transitions` list (e.g. `ASSIGNED`). This needs confirmation and is not executed in the eval.

## Extracted fields

| Field | Value |
|---|---|
| Issue key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| CVE ID | CVE-2026-33501 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | **None (no bracketed stream suffix)** |
| Stream scope | **Unscoped**. It covers all configured streams (2.1.x and 2.2.x) |
| Affects Versions (Jira, current) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 (Rust crate) |
| Ecosystem | Cargo (source dependency, so 2 remediation tasks per affected stream) |
| Affected version range | < 0.4.8 ("versions before 0.4.8") |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 (also RUSTSEC-2026-0055) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 (already past as of 2026-11-04) |
| Status / Assignee | New / Unassigned |
| Existing comments | none |
| Affected source repo / deployment context | rhtpa-backend (Cargo ecosystem mapping: `backend`) / upstream (default) |

Note: the description says this CVE is distinct from CVE-2024-2758 (the httpd CONTINUATION flood). This CVE is specific to the Rust h2 crate's header-block accumulation.

## Step 1.5 — External enrichment

The MITRE CVE API and OSV.dev were not queried (eval constraint: no external calls). Treated as unavailable, so the Jira description threshold is used: **affected < 0.4.8, fixed 0.4.8**.
> Warning: external CVE databases unavailable. Using Jira description data only, so confidence in the fix threshold is reduced.

## Step 1.7 — Embargo check

Skipped. No Embargo policy URL is configured, even though CVSS 7.5 is above the threshold.
