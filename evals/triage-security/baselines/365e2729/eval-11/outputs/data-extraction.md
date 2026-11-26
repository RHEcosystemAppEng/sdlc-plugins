# Step 1 – Data Extraction: TC-8021

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation: no Jira MCP or `git show` calls were made. All data comes from the provided input files.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured in Security Configuration (the issue carries customfield_10632/10669/10832, but the config doesn't declare them). Step 4.3 and Step 7 are skipped. |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| ProdSec contact / account ID | Not configured, so no @mentions |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so triage can proceed.

## Step 0.3 – Matrix staleness

Matrix `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, which makes it **151 days old** (the threshold is 14 days). A staleness warning would be shown with the options Refresh now / Proceed anyway / Stop. For this eval I treat the answer as "Proceed anyway".

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 | Issue |
| CVE ID | CVE-2026-55123 | Label + summary |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] | Issue |
| Status | New | Issue (full triage path) |
| Affected component | `pscomponent:org/rhtpa-server` | Label (matches `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.1.0, RHTPA 2.1.1 | `versions` field |
| Vulnerable library | tokio | Description / customfield_10632 |
| Affected version range | < 1.42.0 ("versions before 1.42.0") | Description |
| Fixed version | 1.42.0 | Description |
| CVSS / severity | 8.1 (High) | Description |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp (also RUSTSEC-2026-0088) | Remote link / references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote link |
| Due date | 2026-08-15 | `duedate` (already past as of 2026-11-26) |
| Assignee | Unassigned | Issue (Step 0.8 would assign it to the current user and transition New → Assigned) |
| Existing issue links | None | Issue |
| Existing comments | None | Issue |

## Stream scope resolution

- Suffix `[rhtpa-2.1]` maps to stream **2.1.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.3.z`). The stream custom field also says `rhtpa-2.1`.
- The issue is **scoped** to 2.1.x. Steps 3, 4 and 8 apply to the 2.1.x stream only.
- In-scope supported versions per the matrix: 2.1.0 (backend `v0.3.8`) and 2.1.1 (backend `v0.3.12`).

## Ecosystem detection

- tokio is a Rust crate, so the ecosystem is **Cargo** (listed in the 2.1.x Ecosystem Mappings: backend, `Cargo.lock`, upstream branch `release/0.3.z`).
- Category: **source dependency**. Normal remediation would be 2 tasks per stream: an upstream backport or dependency bump, plus downstream propagation.
- Deployment context for rhtpa-backend: `upstream` (default).

## Step 1.5 / 1.7

- External enrichment (MITRE / OSV) was not queried because external calls are forbidden in this eval. I fall back to the Jira description threshold (< 1.42.0, fixed 1.42.0), with reduced confidence noted.
- Embargo check: CVSS 8.1 meets the threshold, but no Embargo policy URL is configured, so the step is skipped.

## Step 2 – Version impact evidence gap

The mock lock-file data in security-matrix-mock.md has **no tokio entries** (only quinn-proto, serde_json, h2, criterion, rustls and openssl-libs). Under the "Do NOT fabricate data" rule, I can't assert tokio versions for `v0.3.8` / `v0.3.12`. In a real run, `git show v0.3.8:Cargo.lock` / `git show v0.3.12:Cargo.lock` would supply them.

| Version | Stream | backend tag | tokio version | Affected (< 1.42.0)? |
|---|---|---|---|---|
| 2.1.0 | 2.1.x | v0.3.8 | not available in mock data | Unverified (PSIRT claims YES) |
| 2.1.1 | 2.1.x | v0.3.12 | not available in mock data | Unverified (PSIRT claims YES) |
| 2.2.0–2.2.4 | 2.2.x | v0.4.5…v0.4.12 | not available in mock data | Out of scope (tracked by TC-8020) |

Indirect evidence: TC-8022 already exists. A prior triage of TC-8020 created it after lock-file analysis found 2.1.x affected, which supports PSIRT's Affects Versions (RHTPA 2.1.0, 2.1.1). Step 3 therefore proposes **no Affects Versions change**, pending confirmation with real lock-file output.
