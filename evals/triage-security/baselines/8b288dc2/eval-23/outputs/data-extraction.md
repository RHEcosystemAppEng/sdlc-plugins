# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |
| Deployment Context | **customer-shipped** |

## Deployment Context Lookup

Source repository `rhtpa-backend` was looked up in the Source Repositories table from Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

Result: **customer-shipped** -- this component is shipped to customers. This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions.

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams table.

This issue is **stream-scoped** to **2.2.x** only. Steps 3-4 will apply only to the 2.2.x stream.

## Version Impact Analysis

Using mock lock file data from the security matrix, the following version impact table was produced:

### Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | at fix version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | at fix version |

### Summary

- **2.2.x stream** (issue scope): versions 2.2.0, 2.2.1, and 2.2.2 are affected; versions 2.2.3 and 2.2.4 are not affected (ship quinn-proto 0.11.14, the fix version).
- **2.1.x stream** (out of scope but cross-stream impact): versions 2.1.0 and 2.1.1 are also affected (ship quinn-proto 0.11.9).
- The PSIRT-assigned Affects Versions of "RHTPA 2.0.0" is incorrect -- there is no 2.0.x stream configured. The correct Affects Versions for the 2.2.x stream scope are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2.
