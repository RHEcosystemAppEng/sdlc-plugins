# Step 1 – Data Extraction: TC-8021

Mode: interactive (FULLSEND_OUTPUT_DIR not set). Jira was not called for this eval; all values below come from the provided mock issue file.

## Step 0 – Configuration check (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured, so Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped |
| ProdSec contact / account ID | Not configured, so no @mentions |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so triage continues.

## Step 0.3 – Matrix staleness

The `security-matrix.md` timestamp is `2026-06-28T10:00:00Z`. Today is 2026-11-03, so the matrix is **128 days old** (threshold 14 days).

> Security matrix for stream **2.1.x** (and 2.2.x) was last updated on 2026-06-28 (128 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

For this eval the run proceeds with the current matrix (option 2) and records the warning.

## Step 0.8 – Assign / transition (proposed, not executed)

- Assign TC-8021 to the current user.
- Status is `New`, so transition it to `Assigned` through the dynamically discovered transition.

## Extracted fields

| Field | Value |
|---|---|
| Issue key | TC-8021 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Status | New |
| CVE ID | CVE-2026-55123 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| PSIRT-claimed product version | `[rhtpa-2.1]` |
| Affects Versions (Jira) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio (Rust crate) |
| Affected version range | versions before 1.42.0 (`< 1.42.0`) |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp (also RUSTSEC-2026-0088) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 (already past as of 2026-11-03) |
| Existing comments | none |
| Existing issue links | none |
| Custom fields on issue | customfield_10632 = tokio, customfield_10669 = pscomponent:org/rhtpa-server, customfield_10832 = rhtpa-2.1 (present on the issue, but these field IDs are not configured in Security Configuration) |

## Stream scope resolution

- Suffix `[rhtpa-2.1]` maps to configured stream **2.1.x** (Konflux repo `rhtpa-release.0.3.z`).
- The issue is **scoped** to 2.1.x (versions 2.1.0 and 2.1.1).

## Ecosystem detection

- tokio is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in the 2.1.x Ecosystem Mappings with lock file `Cargo.lock` and upstream branch `release/0.3.z`.
- Category: source dependency, which normally means 2 remediation tasks per stream.
- Deployment context for rhtpa-backend is `upstream` (default).

## Step 1.5 – External enrichment

MITRE and OSV were not queried, because external calls are forbidden in this eval. The Jira description threshold (`< 1.42.0`, fixed in 1.42.0) is used, at reduced confidence:

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

## Step 1.7 – Embargo check

CVSS 8.1 meets the severity threshold, but no Embargo policy URL is configured, so this step is skipped silently.

## Step 2 – Version impact analysis (limitation)

The mock lock-file data in `security-matrix-mock.md` has entries for quinn-proto, serde_json, h2, criterion, rustls and openssl-libs. It has **no tokio entries** for any tag. Under the no-fabrication rule, tokio versions are not assumed:

| Version | Backend tag | tokio version | Affected (< 1.42.0)? |
|---|---|---|---|
| 2.1.0 | v0.3.8 | not in provided data | UNVERIFIED |
| 2.1.1 | v0.3.12 | not in provided data | UNVERIFIED |
| 2.2.0 | v0.4.5 | not in provided data | UNVERIFIED |
| 2.2.1 | v0.4.8 | not in provided data | UNVERIFIED |
| 2.2.2 | v0.4.9 (retag of v0.4.8) | same as 2.2.1 | same as 2.2.1 |
| 2.2.3 | v0.4.11 | not in provided data | UNVERIFIED |
| 2.2.4 | v0.4.12 | not in provided data | UNVERIFIED |

In a real run the next command is `git show v0.3.8:Cargo.lock` / `git show v0.3.12:Cargo.lock` (grep `name = "tokio"`). The skill would ask the engineer for that evidence before confirming the impact table. Two pieces of prior evidence suggest 2.1.x is affected: PSIRT assigned RHTPA 2.1.0/2.1.1, and an earlier triage (TC-8020) created a preemptive 2.1.x remediation task (TC-8022). Neither replaces lock-file evidence.

## Step 3 – Affects Versions

Current: [RHTPA 2.1.0, RHTPA 2.1.1]. These are within the 2.1.x scope and match the full 2.1.x supportability matrix. No correction is proposed until lock-file evidence is reviewed. If the evidence confirms both versions ship tokio < 1.42.0, the field is already correct.
