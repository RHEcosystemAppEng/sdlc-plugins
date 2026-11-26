# TC-8020 — Data Extraction (Steps 0–1.7)

## Step 0 — Configuration validation

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | present (`mcp__<instance>__<tool>`) | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification custom field | customfield_12345 | configured |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z | OK |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) | OK |
| Deployment Context column | absent → default `upstream`; coordination guidance subsection omitted (backward compatibility rule) | note |
| Upstream Affected Component / PS Component / Stream fields | not configured in Security Configuration (values exist on the issue only) | Steps 4.3, 7, and 7.5.3 skipped |
| ProdSec contact / Jira account ID | not configured | @mentions skipped |
| Embargo policy URL | not configured | Step 1.7 skipped |

## Step 0.3 — Matrix staleness check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-23, so the matrix is **148 days old**, past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (148 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval mode: **Proceed anyway** with the current matrix. Releases after 2.2.4 may be missing from the analysis.

## Step 0.6 — Fullsend mode detection

`FULLSEND_OUTPUT_DIR` is absent, so this runs in **interactive mode**. The eval stands in for Jira and git with files.

## Step 0.8 — Assign and transition (proposed, not executed)

- `jira.edit_issue(TC-8020, assignee=<current-user>)`
- Status is **New**, so transition to **Assigned**. The transition is discovered dynamically with `get_transitions`.

## Step 1 — Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| Issue type / status | Vulnerability / New |
| CVE ID | CVE-2026-55123 (label + summary) |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 ("versions before 1.42.0") |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Vulnerability | Use-after-free when a spawned task is aborted while holding a borrowed reference, which can corrupt memory and may allow code execution |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0088.html |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 (**already past** as of 2026-11-23) |
| Assignee | Unassigned |
| Existing comments | none |
| Existing issue links | none |
| Custom fields on issue | customfield_10632 = tokio; customfield_10669 = pscomponent:org/rhtpa-server; customfield_10832 = rhtpa-2.2 |

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (`rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Affects Versions correction (Step 3) and Case B are limited to 2.2.x. Cross-stream handling (Case A) applies to other affected streams.

### Ecosystem detection

- tokio is a Rust crate, so the ecosystem is **Cargo**. It is listed in both streams' Ecosystem Mappings (`Cargo.lock`, repo `backend`).
- Category: **source dependency**, so **2 remediation tasks per affected stream** (upstream backport + downstream propagation).

### Deployment context

- Affected repository: rhtpa-backend. There is no Deployment Context column, so it defaults to `upstream`. Coordination guidance is omitted because the template says to drop that subsection when the column is absent.

## Step 1.5 — External CVE data enrichment

MITRE CVE API and OSV.dev were **not queried**, because the eval forbids external calls. Both are treated as unavailable.

> ⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **tokio < 1.42.0, fixed in 1.42.0** (from the Jira description).

## Step 1.7 — Embargo check

No embargo policy URL is configured, so this step was skipped. CVSS 8.1 would otherwise have triggered the gate.
