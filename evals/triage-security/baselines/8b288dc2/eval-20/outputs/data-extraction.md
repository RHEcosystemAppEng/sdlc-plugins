# Step 1 -- Data Extraction

## Issue: TC-8001

Parsed from the Vulnerability issue fields, description, labels, and remote links.

## Extracted CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`), summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text ("quinn-proto crate before version 0.11.14") |
| Affected version range | < 0.11.14 | Description text ("versions before 0.11.14") |
| Fixed version | 0.11.14 | Description text ("fixed in 0.11.14") |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

- **Issue stream scope**: 2.2.x (scoped to a single stream)
- Steps 3-4 will apply to the 2.2.x stream only; cross-stream impact on 2.1.x will be handled via Case B if affected.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z` (for the 2.2.x stream)

The Cargo ecosystem means remediation will require **two tasks** per affected stream: an upstream backport task (source repo fix) and a downstream propagation subtask (Konflux release repo update).

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` source repository. The Source Repositories table in CLAUDE.md does not include a Deployment Context column (backward compatibility). Per Step 0 instructions, the deployment context defaults to **`upstream`**.

## Affects Versions Mismatch (Preliminary)

The Jira Affects Versions field is set to `RHTPA 2.0.0`, but:
- The issue is scoped to the **2.2.x** stream (per summary suffix `[rhtpa-2.2]`).
- There is no `2.0.x` stream configured in Version Streams.
- This mismatch will be corrected in Step 3 (Affects Versions Correction) after the version impact analysis in Step 2 determines which specific versions actually ship a vulnerable version of quinn-proto.
