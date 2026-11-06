# Step 1 – Data Extraction: TC-8021

Mode: interactive (no `FULLSEND_OUTPUT_DIR`). This is an eval, so nothing was sent to Jira or run through git. All values below come from the mock inputs.

## Step 0 – Configuration Validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not declared in Security Configuration. The issue does carry customfield_10632 / 10669 / 10832. |
| Embargo policy URL | Not configured. Step 1.7 is skipped. |
| ProdSec contact / account ID | Not configured. @mentions are skipped. |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so triage proceeds.

### Step 0.3 – Matrix Staleness

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-06, so the matrix is **131 days old**, well past the 14-day threshold. In a live run the engineer would be asked to pick Refresh / Proceed / Stop. For this eval, assume **Proceed anyway**.

## Extracted CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 | Issue |
| Status | New (full triage path) | Issue |
| CVE ID | CVE-2026-55123 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label / customfield_10669 |
| Product version (PSIRT-claimed) | `[rhtpa-2.1]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.1.0, RHTPA 2.1.1 | `versions` field |
| Vulnerable library | tokio | Description / customfield_10632 |
| Affected version range | < 1.42.0 ("versions before 1.42.0") | Description |
| Fixed version | 1.42.0 | Description |
| Vulnerability type | Use-after-free in task abort | Summary / description |
| CVSS | 8.1 (High) | Description |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0088.html | Description |
| Due date | 2026-08-15 (already past as of 2026-11-06) | `duedate` |
| Assignee | Unassigned. Step 0.8 would assign it to the triager and move it to Assigned. | Issue |
| Existing issue links | None | Issue |
| Existing comments | None | Issue |

## Stream Scope Resolution

- Suffix `[rhtpa-2.1]` maps to configured stream **2.1.x** (Konflux repo `rhtpa-release.0.3.z`, backend branch `release/0.3.z`).
- The Stream field (customfield_10832) is `rhtpa-2.1`, which agrees with the suffix.
- **Issue stream scope: 2.1.x (scoped).**
- Versions in scope: RHTPA 2.1.0 (backend `v0.3.8`) and RHTPA 2.1.1 (backend `v0.3.12`).

## Ecosystem Detection

- tokio is a Rust crate, so the ecosystem is **Cargo**. Cargo is a source dependency ecosystem, which normally means 2 remediation tasks per stream.
- Lock file: `Cargo.lock` in backend, read with `git show <tag>:Cargo.lock`.
- Deployment context: rhtpa-backend, defaulting to `upstream`.

## Step 1.5 / 1.7

- Step 1.5 (MITRE / OSV): not queried, because external calls are forbidden in this eval. Only the Jira description data is used: fix threshold 1.42.0. Confidence in the threshold is lower as a result.
- Step 1.7: CVSS 8.1 is above the 7.0 threshold, but no Embargo policy URL is configured, so the step is skipped silently.

## Step 2 – Version Impact Data Gap

The mock lock-file data covers quinn-proto, serde_json, h2, criterion, rustls and openssl-libs. It has **no tokio entries**. The skill's no-fabrication guardrail means tokio versions cannot be asserted for any tag.

| Version | Build | backend tag | tokio version | Affected (< 1.42.0)? |
|---|---|---|---|---|
| RHTPA 2.1.0 | 0.3.8 | v0.3.8 | not available in mock data | Unverified |
| RHTPA 2.1.1 | 0.3.12 | v0.3.12 | not available in mock data | Unverified |
| RHTPA 2.2.x (out of scope) | — | v0.4.5–v0.4.12 | not available in mock data | Unverified |

In a live run this would mean `git show v0.3.8:Cargo.lock | grep -A2 'name = "tokio"'` and the same for `v0.3.12`. Evidence that counts against the version being safe:

- PSIRT assigned RHTPA 2.1.0 and 2.1.1.
- A prior cross-stream triage of TC-8020 concluded that 2.1.x was affected and created preemptive task TC-8022.

For this eval, Affects Versions are **left unchanged** (RHTPA 2.1.0, RHTPA 2.1.1) until lock-file evidence confirms them. No correction is proposed.
