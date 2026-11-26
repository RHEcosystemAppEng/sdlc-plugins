# Step 1 – Data Extraction: TC-8021

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation, so no Jira, git, or WebFetch calls were made. All data comes from the provided mock files.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured, so Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped |
| ProdSec contact / account ID | Not configured, so no ProdSec @mentions |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration). Validation passed.

## Step 0.3 – Matrix Staleness Check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-26, so the matrix is **151 days old**, well past the 14-day threshold. In a live run the engineer would be asked to choose Refresh now, Proceed anyway, or Stop. For this eval, the analysis proceeds with the current matrix and records the staleness warning.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Assign TC-8021 to the current user. It is currently Unassigned.
- Transition New to Assigned. The transition is discovered dynamically through `get_transitions`.

## Extracted CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 | Issue |
| CVE ID | CVE-2026-55123 | Label + summary |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] | Issue |
| Status | New | Issue (full triage path) |
| Affected component | `pscomponent:org/rhtpa-server` | Label |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.1.0, RHTPA 2.1.1 | `versions` field |
| Vulnerable library | tokio (Rust crate) | Description |
| Affected version range | < 1.42.0 | Description |
| Fixed version | 1.42.0 | Description |
| CVSS | 8.1 (High) | Description |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp | Remote link |
| Additional advisory | https://rustsec.org/advisories/RUSTSEC-2026-0088.html | Description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote link |
| Due date | 2026-08-15 (already passed as of 2026-11-26) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing issue links | None | Issue |
| Existing comments | None | Issue |
| Custom fields present on issue | customfield_10632 = tokio; customfield_10669 = pscomponent:org/rhtpa-server; customfield_10832 = rhtpa-2.1 | Issue (these field IDs are not configured in Security Configuration) |

## Stream Scope Resolution

- Suffix `[rhtpa-2.1]` maps to the configured Version Stream **2.1.x** (rhtpa-release.0.3.z).
- The issue is **scoped**. Steps 3, 4, and 8 apply only to stream 2.1.x (RHTPA 2.1.0 and 2.1.1).

## Ecosystem Detection

- tokio is a Rust crate, so the ecosystem is **Cargo**. The 2.1.x Ecosystem Mappings list Cargo with `Cargo.lock` in `backend` and upstream branch `release/0.3.z`.
- Category: **source dependency**, which normally yields 2 remediation tasks per stream (upstream backport or dependency bump, plus downstream propagation).
- Deployment context: rhtpa-backend defaults to `upstream` because no Deployment Context column exists.

## Step 1.5 – External Enrichment

The MITRE and OSV queries were not run (eval constraint, no external tools). The Jira description data (< 1.42.0, fixed 1.42.0) is used, with this note: "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."

## Step 1.7 – Embargo Check

Skipped. No Embargo policy URL is configured, even though CVSS 8.1 meets the severity threshold.

## Step 2 – Version Impact Analysis (2.1.x scope)

| Version | Build | backend tag | tokio version | Affected? |
|---|---|---|---|---|
| RHTPA 2.1.0 | 0.3.8 | v0.3.8 | **Not available in mock lock data** | Unverified |
| RHTPA 2.1.1 | 0.3.12 | v0.3.12 | **Not available in mock lock data** | Unverified |

The mock lock data contains quinn-proto, serde_json, h2, criterion, rustls, and openssl-libs, but **not tokio**. Under the "Do NOT fabricate data" guardrail, no tokio version is invented. In a live run the skill would execute `git show v0.3.8:Cargo.lock` and `git show v0.3.12:Cargo.lock` and ask the engineer if those reads failed.

This gap does not change the Step 4.4 outcome. TC-8022 already exists as the remediation vehicle for this CVE and stream ("bump tokio to 1.42.0 (rhtpa-2.1)"). Prior cross-stream triage of TC-8020 identified 2.1.x as affected. PSIRT's Affects Versions (RHTPA 2.1.0, 2.1.1) match the full 2.1.x stream and are kept unchanged, pending lock-file confirmation.

Out-of-scope stream 2.2.x is tracked by sibling TC-8020 ([rhtpa-2.2]).

## Step 3 – Affects Versions

Current: [RHTPA 2.1.0, RHTPA 2.1.1]. These are already scoped correctly to stream 2.1.x, so no correction is proposed. The evidence caveat above applies.
