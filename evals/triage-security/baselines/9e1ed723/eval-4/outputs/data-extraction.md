# Step 1 – Data Extraction: TC-8004

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Jira/external calls simulated from eval input files; no Jira MCP, git, or WebFetch calls were made.

## Step 0 – Configuration validation

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3, 7, 7.5.3 skipped) |
| ProdSec Jira account ID | not configured (no @mention) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column -> default `upstream`; coordination guidance omitted per backward-compat rule) |

All required sections present. Validation: PASS.

## Step 0.3 – Matrix staleness check

Matrix `Last-Updated: 2026-06-28T10:00:00Z`; today is 2026-11-23 (148 days, exceeds 14-day threshold).

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (148 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval assumption: **Proceed anyway** with the supplied matrix.

## Step 0.8 – Assign and transition

Proposed (requires confirmation): assign TC-8004 to current user; transition New -> Assigned (transition ID discovered dynamically via `get_transitions`).

## Extracted fields

| Field | Value |
|---|---|
| Issue key | TC-8004 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-33501 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | **none** - no bracketed stream suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 (Rust crate) |
| Affected version range | < 0.4.8 ("versions before 0.4.8") |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 (also RUSTSEC-2026-0055) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Existing comments | none |

## Stream scope resolution

Summary `CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames` has **no stream suffix** -> issue is **UNSCOPED**. All configured streams (2.1.x, 2.2.x) are analyzed; Affects Versions correction covers affected versions across all streams; Case A (cross-stream comment / preemptive tasks) does not apply; Case B creates remediation for every affected stream.

## Ecosystem detection

h2 is a Rust crate -> **Cargo** (present in both streams' Ecosystem Mappings, lock file `Cargo.lock`, repository `backend`). Category: **source dependency** -> 2 remediation tasks per affected stream.

## Deployment context

rhtpa-backend: Deployment Context column absent -> default `upstream`; per remediation-templates backward-compatibility rule the Coordination Guidance subsection is omitted.

## Step 1.5 – External CVE data enrichment

MITRE CVE API and OSV.dev not queried (external calls prohibited in this eval) -> treated as unavailable.

> External CVE databases unavailable - using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **h2 < 0.4.8 affected, 0.4.8 fixed**.

## Step 1.7 – Embargo check

Embargo policy URL not configured -> skipped (CVSS 7.5 would otherwise trigger the gate).
