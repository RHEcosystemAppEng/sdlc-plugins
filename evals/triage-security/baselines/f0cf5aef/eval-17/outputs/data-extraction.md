# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8001

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
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings in the security matrix, this falls under the **Cargo** ecosystem.

- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories with URL `https://github.com/rhtpa/rhtpa-backend`. No Deployment Context column is present, so the default context is `upstream`.

## Validation Notes

- All critical fields (CVE ID, library, affected range, fixed version) were successfully parsed.
- The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) does not correspond to any configured version stream (no 2.0.x stream exists). This will be corrected in Step 3 based on lock file evidence from Step 2.
