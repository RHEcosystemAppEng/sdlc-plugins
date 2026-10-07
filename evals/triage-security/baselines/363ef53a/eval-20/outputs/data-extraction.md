# Step 1 -- Data Extraction

## Source Issue

- **Key**: TC-8001
- **Issue Type**: Vulnerability
- **Status**: New

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2`
- Mapped stream: **2.2.x**
- Match: The suffix maps to the `2.2.x` row in the Version Streams table (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

**Issue stream scope**: 2.2.x (scoped issue -- Steps 3-4 will apply to the 2.2.x stream; Case A cross-stream check will evaluate impact on 2.1.x)

## Ecosystem Detection

- **Library**: quinn-proto
- **Ecosystem**: Cargo (Rust crate)
- **Category**: Source dependency
- **Remediation task count per stream**: 2 (upstream backport or dependency bump + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`

The Cargo ecosystem is listed in both streams' Ecosystem Mappings tables in security-matrix-mock.md, confirming it is a supported ecosystem.

## Deployment Context Lookup

- **Affected repository** (from component label `pscomponent:org/rhtpa-server`): rhtpa-backend
- **Source Repositories table match**: rhtpa-backend
- **Deployment context**: upstream (Deployment Context column absent -- defaulting to `upstream` per skill rules)

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions field contains **RHTPA 2.0.0**, but no `2.0.x` stream exists in the Version Streams configuration. The configured streams are 2.1.x and 2.2.x. The issue is scoped to `[rhtpa-2.2]`, which maps to the 2.2.x stream. The Affects Versions will need correction in Step 3 based on version impact analysis results.

## Verification Notes

- All critical fields (CVE ID, library, affected range) were successfully parsed. No missing fields that would require engineer input.
- The Affects Versions value (RHTPA 2.0.0) does not correspond to any configured version stream -- this is expected for PSIRT-created issues and will be corrected in Step 3.
