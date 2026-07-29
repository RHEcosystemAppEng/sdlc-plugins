# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will be scoped to this stream only. Cross-stream impact on other streams (e.g., 2.1.x) will be handled via Case A in Step 8.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. No Deployment Context column is present in the configuration (backward compatibility), so the default context is `upstream`.

## Affects Versions Discrepancy (Preliminary)

PSIRT assigned `RHTPA 2.0.0` as the Affects Version, but no `2.0.x` stream exists in the Version Streams configuration. The configured streams are `2.1.x` and `2.2.x`. This will be corrected in Step 3 after the version impact analysis is complete.
