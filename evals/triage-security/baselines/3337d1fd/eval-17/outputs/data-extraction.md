# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

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

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

The issue is **scoped** to stream 2.2.x. Steps 3-4 will apply only to 2.2.x versions. However, all streams (2.1.x and 2.2.x) are analyzed in Step 2 for cross-stream impact detection (Case B).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings tables in the security matrix, the relevant ecosystem is **Cargo**:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` (2.2.x) / `release/0.3.z` (2.1.x) |

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories without a Deployment Context column. Per backward compatibility rules, the deployment context defaults to `upstream`. Coordination guidance subsection will be omitted from remediation tasks since the Deployment Context column is absent.

## Affects Versions Mismatch Flag

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but no 2.0.x stream exists in the Security Configuration. This is incorrect and will need correction in Step 3 based on lock file evidence from Step 2.
