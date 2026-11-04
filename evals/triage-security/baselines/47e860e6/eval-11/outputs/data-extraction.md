# Step 1: Data Extraction for TC-8021

Mode: interactive. `FULLSEND_OUTPUT_DIR` is not set, so Steps 0.6 and 0.7 are skipped. This is an eval simulation. No Jira, git, or WebFetch calls were made. All data comes from the provided mock files.

## Step 0: Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured in Security Configuration. Steps 4.3 and 7 are skipped. |
| Embargo policy URL | Not configured. Step 1.7 is skipped. |
| ProdSec contact / account ID | Not configured. @mentions are skipped silently. |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so triage proceeds.

## Step 0.3: Matrix staleness

The matrix says `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, so the matrix is about 129 days old, which is past the 14-day threshold. **Staleness warning**: the engineer would choose Refresh, Proceed, or Stop. For this eval, triage proceeds with the current matrix.

## Step 0.8: Assign and transition (proposed, not executed)

- Assign TC-8021 to the current user.
- The issue status is `New`, so transition it to the target named "Assigned" (`ASSIGNED`). The transition ID is looked up from the live workflow.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8021 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-55123 (from the label and the summary) |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT suffix) | `[rhtpa-2.1]` |
| Affects Versions (Jira) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected range | < 1.42.0 ("versions before 1.42.0") |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp (plus RUSTSEC-2026-0088) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 (already past) |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |
| Existing issue links | none |
| Existing comments | none |

## Stream scope resolution

The suffix `[rhtpa-2.1]` maps to the configured stream **2.1.x** (rhtpa-release.0.3.z, backend branch `release/0.3.z`). The issue is **scoped** to 2.1.x, which covers versions 2.1.0 (backend `v0.3.8`) and 2.1.1 (backend `v0.3.12`).

## Ecosystem detection

tokio is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the 2.1.x Ecosystem Mappings (backend, `Cargo.lock`). Its category is a source dependency, so the remediation shape per stream is 2 tasks: a dependency bump or upstream backport, plus downstream propagation.

## Deployment context

The affected repository is rhtpa-backend, which defaults to `upstream`.

## Step 1.5: External enrichment

This was not executed because external calls are disabled in the eval. The Jira description data is used alone: threshold < 1.42.0, fixed in 1.42.0. **Confidence is reduced** because external CVE databases were unavailable.

## Step 1.7: Embargo

No Embargo policy URL is configured, so this step is skipped, even though CVSS 8.1 would meet the threshold.

## Step 2: Version impact (data gap)

The mock lock-file data has no **tokio** section. It covers only quinn-proto, serde_json, h2, criterion, rustls, and openssl-libs. The skill does not allow fabricating dependency versions, so the tokio version at `v0.3.8` and `v0.3.12` is **unverified**:

| Version | Build | backend tag | tokio version | Affected? |
|---|---|---|---|---|
| 2.1.0 | 0.3.8 | v0.3.8 | not available (`git show v0.3.8:Cargo.lock` not simulated) | Unverified |
| 2.1.1 | 0.3.12 | v0.3.12 | not available | Unverified |
| 2.2.x (outside scope) | — | v0.4.5 to v0.4.12 | not available | Unverified (tracked by TC-8020) |

In a real run, the skill would stop here and ask the engineer to provide the lock data or confirm access to the repo. For this eval, the analysis goes on to the Step 4.4 reconciliation, which depends only on Jira state. The PSIRT Affects Versions (2.1.0, 2.1.1) are kept as they are until lock evidence confirms them. Step 3 proposes no correction without evidence.
