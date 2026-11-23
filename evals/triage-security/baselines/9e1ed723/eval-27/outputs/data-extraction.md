# Step 1 – Data Extraction: TC-8051

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval run — Jira MCP not called; data parsed from fixture `vuln-issue-feature-gated.md`.

## Step 0 – Configuration validation

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 (configured) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (deployment context column absent, defaults to `upstream`) |

All required sections present. Validation passed.

## Step 0.3 – Matrix staleness check

Security matrix `Last-Updated: 2026-06-28T10:00:00Z` is **148 days old** (today 2026-11-23), past the 14-day threshold.

> Security matrix for stream **2.2.x** was last updated on 2026-06-28 (148 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

Eval assumption: **Proceed anyway** (fixture matrix is the only available data).

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8051 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-99002 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → RHTPA 2.2 |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Ecosystem | Cargo (source dependency) |
| Affected version range | versions before 0.23.5 (`< 0.23.5`) |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 (rustls/rustls#2100) |
| Advisory URL | none (no GHSA/advisory remote link) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Assignee | Unassigned (Step 0.8 would self-assign and transition to Assigned — not executed in eval) |
| Existing comments | none |
| Deployment context | upstream (default; rhtpa-backend has no Deployment Context column) |

## Stream scope resolution

| Item | Value |
|---|---|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z) |
| Scope | **Scoped** — Steps 2–8 scoped to 2.2.x; 2.1.x checked only for cross-stream impact (Case A) |

## Step 1.5 – External CVE enrichment

MITRE CVE API and OSV.dev not queried (eval: no external calls).

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2.3: **rustls < 0.23.5 affected; 0.23.5 fixed**.

## Step 1.7 – Embargo check

Skipped — no Embargo policy URL configured in Security Configuration (CVSS 8.1 would otherwise trigger the gate).
