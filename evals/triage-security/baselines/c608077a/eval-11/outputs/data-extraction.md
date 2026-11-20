# TC-8021 — Step 1 Data Extraction

Mode: interactive (simulated). `FULLSEND_OUTPUT_DIR` is not set. Jira, git, and WebFetch were **not** called. All data comes from the eval input files.

## Step 0 – Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured in Security Configuration (the issue does carry customfield_10632 / 10669 / 10832 values) |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| ProdSec contact / account ID | Not configured, so no @mentions |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so validation passes.

## Step 0.3 – Matrix staleness

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-20, so it is **145 days old**, well past the 14-day threshold. In an interactive run the engineer would be offered Refresh / Proceed / Stop. For this eval we assume **Proceed anyway** and note the staleness.

## Step 0.8 – Assign / transition (proposed, not executed)

- Assign TC-8021 to the current triager.
- Transition New → Assigned. The transition ID would be found dynamically.

## Extracted fields

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 | Issue |
| CVE ID | CVE-2026-55123 | Label + summary |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] | Issue |
| Status | New | Issue |
| Affected component | `pscomponent:org/rhtpa-server` | Label / customfield_10669 |
| Upstream Affected Component | tokio | customfield_10632 |
| Stream field | rhtpa-2.1 | customfield_10832 |
| PSIRT-claimed stream (suffix) | `[rhtpa-2.1]` | Summary |
| Affects Versions (Jira) | RHTPA 2.1.0, RHTPA 2.1.1 | `versions` |
| Vulnerable library | tokio (Rust crate) | Description |
| Affected range | < 1.42.0 ("versions before 1.42.0") | Description |
| Fixed version | 1.42.0 | Description |
| CVSS | 8.1 (High) | Description |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote link |
| Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp, https://rustsec.org/advisories/RUSTSEC-2026-0088.html | Remote link / references |
| CVE record | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote link |
| Due date | 2026-08-15 (**already past** as of 2026-11-20) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing issue links | None | Issue |
| Existing comments | None | Issue |

## Stream scope resolution

- Suffix `[rhtpa-2.1]` maps to the configured stream **2.1.x** (Konflux repo `rhtpa-release.0.3.z`, versions 2.1.0 / 2.1.1).
- The issue is **scoped** to 2.1.x. Steps 3, 4, and 8 apply only to this stream.

## Ecosystem detection

- tokio is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the 2.1.x Ecosystem Mappings: backend, `Cargo.lock`, upstream branch `release/0.3.z`.
- Category: **source dependency**, which normally means 2 remediation tasks per stream (bump or backport, plus downstream propagation).
- Deployment context for rhtpa-backend: `upstream` (default).

## Step 1.5 – External enrichment

MITRE and OSV were not queried because external calls are forbidden in this eval. Treated as "unavailable", so the Jira description threshold is used: **fixed in 1.42.0, affected < 1.42.0**.

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

## Step 1.7 – Embargo

Skipped. No Embargo policy URL is configured, even though CVSS 8.1 would meet the threshold.

## Step 2 – Version impact (data gap)

Pinned tags for 2.1.x are `v0.3.8` (2.1.0) and `v0.3.12` (2.1.1). The mock lock-file data has **no tokio section**. It only covers quinn-proto, serde_json, h2, criterion, rustls, and openssl-libs. Under the "do not fabricate" rule, tokio versions cannot be stated:

| Version | Tag | tokio version | Affected (< 1.42.0)? |
|---|---|---|---|
| 2.1.0 | v0.3.8 | not available in the mock data (would come from `git show v0.3.8:Cargo.lock`) | Unverified |
| 2.1.1 | v0.3.12 | not available in the mock data | Unverified |
| 2.2.x (out of scope) | v0.4.5–v0.4.12 | not available in the mock data | Unverified (tracked by TC-8020) |

The PSIRT Affects Versions (2.1.0, 2.1.1) are kept **unchanged and unverified** pending a real lock-file check. That means no Step 3 correction is proposed. The Step 4.4 reconciliation does not depend on these lock-file values. It depends on the CVE label and stream match.
