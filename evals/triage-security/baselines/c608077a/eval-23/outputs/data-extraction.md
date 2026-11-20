# TC-8001 — Step 1 Data Extraction (simulated; no Jira/git calls made)

## Step 0 – Configuration extracted

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |

### Source Repositories mapping (Deployment Context column present)

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

## Parsed CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| CVE ID | CVE-2026-31812 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) — DoS (panic on excessive stream count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Status | New |
| Existing comments | none |
| Ecosystem | Cargo (source dependency → 2 tasks per stream) |
| Affected repository | rhtpa-backend (Cargo ecosystem mapping: Repository = backend) |
| **Deployment context** | **customer-shipped** (looked up from Source Repositories table, row `rhtpa-backend`) |

### Deployment context lookup

- Affected component `pscomponent:org/rhtpa-server` → Cargo ecosystem → Ecosystem Mappings Repository `backend` → Source Repository `rhtpa-backend`.
- Source Repositories table has a Deployment Context column; value for `rhtpa-backend` = `customer-shipped`.
- No default to `upstream` was needed (repository found, column present).
- Recorded for Step 8: every remediation task gets the **customer-shipped** Coordination Guidance subsection.

### Stream scope resolution

- Summary suffix `[rhtpa-2.2]` → stream **2.2.x** (matches configured Version Streams). Issue is **scoped** to 2.2.x.

### Notes

- Step 1.5 (MITRE/OSV) not executed per eval instructions (no external calls); Jira description threshold (< 0.11.14, fixed 0.11.14) used, with reduced confidence noted.
- Step 1.7 skipped: no Embargo policy URL configured (CVSS 7.5 would otherwise trigger the gate).
- Matrix staleness (Step 0.3): Last-Updated 2026-06-28 is >14 days before today (2026-11-20) — engineer would be warned; proceeding with mock matrix for this eval.

## Step 2 – Version impact (from mock lock-file data)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | out of issue scope (2.1.x) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | out of issue scope (2.1.x) |
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | |

Step 3: Affects Versions `RHTPA 2.0.0` is wrong (no 2.0.x stream; 2.0.0 not in matrix). Proposed correction for the scoped 2.2.x issue: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**.
