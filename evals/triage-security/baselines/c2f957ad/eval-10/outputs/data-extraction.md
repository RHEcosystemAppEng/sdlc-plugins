# Step 1 – Data Extraction: TC-8020

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
| Embargo policy URL | not configured (Step 1.7 skipped) |
| ProdSec Jira account ID | not configured (no ProdSec @mentions) |
| Version Streams | 2.1.x → `git.example.com/rhtpa/rhtpa-release.0.3.z`; 2.2.x → `git.example.com/rhtpa/rhtpa-release.0.4.z` |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections exist: Repository Registry, Jira Configuration, Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories).

## Step 0.3 – Matrix staleness check

Both stream matrices carry `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-26, so the matrices are **151 days old**. The threshold is 14 days, so they are **STALE**.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (151 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval decision: **Proceed anyway** with the current matrix. The task said not to run external tools, so no refresh was possible.

## Step 0.8 – Assign / transition (proposed, not executed)

- Assign TC-8020 to the current user. It is currently Unassigned.
- Transition New → Assigned. Discover the transition dynamically through `get_transitions`.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| Issue type / status | Vulnerability / New |
| CVE ID | CVE-2026-55123 (from the label and the summary) |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Ecosystem | Cargo (Rust crate), a **source dependency**, so 2 tasks per stream |
| Affected version range | < 1.42.0 ("versions before 1.42.0") |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Vulnerability | Use-after-free when a spawned task is aborted while holding a borrowed reference. Can cause memory corruption and potential code execution |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0088.html |
| Due date | 2026-08-15 (**already past**: today is 2026-11-26) |
| Assignee | Unassigned |
| Existing comments | none |
| Existing issue links | none |
| Custom fields | Upstream Affected Component (customfield_10632) = tokio; PS Component (customfield_10669) = pscomponent:org/rhtpa-server; Stream (customfield_10832) = rhtpa-2.2 |
| Affected repository | rhtpa-backend (Cargo ecosystem, repository `backend`) |
| Deployment context | `upstream` (default, because the Deployment Context column is absent) |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (`rhtpa-release.0.4.z`).
- The issue is **scoped** to stream 2.2.x. Case A (cross-stream impact) applies if other streams are affected.

## Step 1.5 – External CVE data enrichment

The eval forbade external calls, so MITRE and OSV.dev were not queried.
> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

The fix threshold used for the analysis is **tokio < 1.42.0, fixed in 1.42.0**. The threshold given in the task prompt agrees.

## Step 1.7 – Embargo check

Severity is CVSS 8.1 (High), which is above the threshold. No Embargo policy URL is configured, so this step was **skipped silently**.
