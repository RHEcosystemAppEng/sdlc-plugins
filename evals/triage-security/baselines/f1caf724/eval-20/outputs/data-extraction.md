# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

### Stream Scope Resolution

The issue summary contains a stream suffix: `[rhtpa-2.2]`

1. **Parsed suffix**: `rhtpa-2.2` maps to stream `2.2.x`
2. **Matched stream**: 2.2.x (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
3. **Issue stream scope**: **Scoped to 2.2.x**

This is a stream-scoped issue. Steps 3-4 will apply to the 2.2.x stream, and Case A cross-stream impact will be checked for the 2.1.x stream.

### Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z` (for 2.2.x stream)
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

### Deployment Context Lookup

- **Affected repository**: rhtpa-backend (from component label `pscomponent:org/rhtpa-server`)
- **Deployment context**: `upstream` (default -- no explicit Deployment Context column in Source Repositories table)

### Affects Versions Mismatch

The PSIRT-assigned Affects Versions field contains **RHTPA 2.0.0**, but:

- No `2.0.x` version stream is configured in Security Configuration
- The configured streams are **2.1.x** and **2.2.x** only
- The issue summary suffix `[rhtpa-2.2]` indicates the issue targets the 2.2.x stream

This is a clear Affects Versions mismatch that Step 3 (Affects Versions Correction) would need to address based on the version impact analysis from Step 2.

### Version Impact Preview (from Mock Lock File Data)

Using the quinn-proto version data from the security matrix mock:

| Stream | Version | Build Tag | quinn-proto Version | Fixed (>= 0.11.14) | Affected |
|--------|---------|-----------|---------------------|---------------------|----------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | No | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | No | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | No | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | No | YES |
| 2.2.x | 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | No | YES (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | Yes | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | Yes | NO |

**Summary**: quinn-proto < 0.11.14 is vulnerable. Versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, and 2.2.2 ship vulnerable versions (0.11.9 or 0.11.12). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are NOT affected.

### Critical Fields Verification

All critical fields were successfully parsed:

- [x] CVE ID: CVE-2026-31812
- [x] Vulnerable library: quinn-proto
- [x] Affected version range: < 0.11.14
- [x] Fixed version: 0.11.14

No missing critical fields -- triage can proceed to Step 1.5 (External CVE Data Enrichment).
