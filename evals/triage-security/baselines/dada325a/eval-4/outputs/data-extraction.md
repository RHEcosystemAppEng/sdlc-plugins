# TC-8004 — Step 1 Data Extraction

Skill: `/sdlc-workflow:triage-security` (interactive mode — `FULLSEND_OUTPUT_DIR` absent)
Source: mock Jira issue (`vuln-issue-split.md`), no live Jira calls made.

## Step 0 – Configuration Validation

| Item | Value | Status |
|------|-------|--------|
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification custom field | customfield_12345 | Configured (only used on Not-a-Bug closures) |
| Upstream Affected Component field | not configured | Steps 4.3, 7, 7.5.3 skipped |
| ProdSec Jira account ID | not configured | @mentions omitted |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`; coordination guidance omitted per backward-compat rule) | OK |

## Step 0.3 – Matrix Staleness Check

Both stream matrices carry `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is
2026-11-06, so the matrices are **131 days old** (threshold 14 days).

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (131 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval decision: **Proceed anyway** (matrix refresh not possible without external tools).
Any 2.1.x / 2.2.x release after 2026-06-28 would not appear in this analysis.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Status is `New` → propose assign to current user and transition to `Assigned`
  (transition discovered dynamically via `get_transitions`).

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Status | New |
| CVE ID | CVE-2026-33501 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | **none — no bracketed stream suffix** |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 (Rust crate) |
| Ecosystem | Cargo (source dependency → 2 remediation tasks per affected stream) |
| Affected version range | < 0.4.8 ("versions before 0.4.8") |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0055.html |
| Due date | 2026-08-01 (already past as of 2026-11-06) |
| Assignee | Unassigned |
| Existing comments | none |
| Affected repository | rhtpa-backend (Cargo ecosystem row → Repository `backend`) |
| Deployment context | `upstream` (default — column absent) |

## Stream Scope Resolution

The summary has **no stream suffix in brackets** → the issue is **UNSCOPED** and covers
all configured streams (2.1.x and 2.2.x). Consequences:

- Step 2 analyzes every version in both streams.
- Step 3 Affects Versions correction includes affected versions across all streams.
- Step 8 Case A (cross-stream preemptive remediation) does **not** apply; Case B creates
  standard (non-preemptive, `Depend`-linked) remediation tasks for each affected stream only.

## Step 1.5 – External CVE Data Enrichment

MITRE CVE API and OSV.dev were not queried (eval forbids external calls).

> External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used for Step 2: **h2 < 0.4.8 is vulnerable; 0.4.8+ is fixed.**

## Step 1.7 – Embargo Check

Skipped — no Embargo policy URL configured (CVSS 7.5 would otherwise trigger the gate).
