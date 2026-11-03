# TC-8004 — Step 1 Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation: no Jira MCP, git, or WebFetch calls were made. All data comes from the provided mock files.

## Step 0 — Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec Jira account ID | not configured (no @mention) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source repositories | rhtpa-backend (no Deployment Context column -> defaults to `upstream`; coordination guidance omitted per backward-compat rule) |

## Step 0.3 — Matrix staleness

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` — today is 2026-11-03, i.e. **128 days old** (threshold 14 days).

> WARNING: Security matrix for streams 2.1.x and 2.2.x was last updated on 2026-06-28 (128 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval assumption: **Proceed anyway** with the current matrix.

## Step 0.8 — Assign / transition (proposed, not executed)

- Assign TC-8004 to current user (currently Unassigned).
- Transition New -> Assigned (transition ID discovered dynamically).

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8004 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-33501 (label + summary) |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed suffix) | **none — unscoped** |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 (Rust crate) |
| Ecosystem | Cargo (source dependency -> 2 tasks per affected stream) |
| Affected version range | < 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS / severity | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 (also RUSTSEC-2026-0055) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 (already past as of 2026-11-03) |
| Existing comments | none |
| Reporter | not present in mock data (needed for post-triage @mention) |
| Affected repository / deployment context | rhtpa-backend (`backend` in Ecosystem Mappings) / `upstream` (default) |

## Stream scope resolution

Summary has **no bracketed stream suffix** -> issue is **unscoped** and covers all configured streams (2.1.x and 2.2.x). Steps 3–8 apply to all streams; Case A (cross-stream comment / preemptive tasks) does not apply.

## Step 1.5 — External enrichment

MITRE / OSV not queried (eval forbids external calls). Treated as unavailable:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **h2 < 0.4.8 vulnerable; >= 0.4.8 fixed.**

## Step 1.7 — Embargo check

Skipped: no Embargo policy URL configured (CVSS 7.5 would otherwise trigger the gate).
