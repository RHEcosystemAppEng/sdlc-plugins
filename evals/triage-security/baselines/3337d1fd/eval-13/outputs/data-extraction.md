# Step 1 -- Data Extraction for TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | _(none)_ | Comment history |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 8 will be scoped to this stream. Other streams (2.1.x) will be checked for cross-stream impact (Case B).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. This maps to the **Cargo** ecosystem, which is configured in both streams' Ecosystem Mappings tables:

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x  | Cargo     | backend    | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| 2.2.x  | Cargo     | backend    | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Deployment Context Lookup

The Source Repositories table in the project CLAUDE.md does not include a Deployment Context column. Per backward compatibility rules, coordination guidance will be omitted from remediation task descriptions.

## Affects Versions Issue

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but no 2.0.x version stream is configured. This value is incorrect and will be corrected in Step 3 based on lock file evidence from the version impact analysis.
