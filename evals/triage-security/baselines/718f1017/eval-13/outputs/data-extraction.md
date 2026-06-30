# Step 1 - Data Extraction for TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels: `CVE-2026-31812`; summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `rhtpa-2.2` -> stream `2.2.x`
2. Matched to Version Streams table: stream `2.2.x` corresponds to Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.4.z`
3. **Issue stream scope: 2.2.x** -- Steps 3-7 are scoped to this stream only. Cross-stream impact on 2.1.x is handled via Case B.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

- **Ecosystem**: Cargo
- **Repository**: backend
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z`

This is a **source dependency** ecosystem. Remediation will require two tasks per affected stream: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).

## Step 1.7 - Embargo Check

CVE-2026-31812 has a CVSS score of 7.5 (High severity), which meets the embargo check threshold (CVSS >= 7.0). However, the Security Configuration does not include an Embargo policy URL. **Step 1.7 is skipped** -- no embargo policy URL configured.
