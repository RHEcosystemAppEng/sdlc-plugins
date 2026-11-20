# Step 1 – Data Extraction — TC-8001

Source: `vuln-issue-standard.md` (mock Jira issue and remote links). Configuration source:
`claude-md-security-config.md` (Jira version prefix `RHTPA`, component label pattern
`pscomponent:`). No Jira MCP calls were made.

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue key |
| Issue type / Status | Vulnerability / New | Issue fields |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary text (they match) |
| Affected component | `pscomponent:org/rhtpa-server` (component `org/rhtpa-server`) | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `rhtpa-2.2`, which maps to stream **2.2.x** | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto (Rust crate) | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability class | Denial of service (panic from an unbounded number of streams in a STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042: https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links / description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Assignee | Unassigned | Issue fields |
| Existing comments | None | Issue comment history |

All critical fields (CVE ID, library, affected range) were parsed. No input from the
engineer is needed to fill gaps.

## Stream scope resolution

- Summary suffix: `[rhtpa-2.2]`, which maps to stream `2.2.x`.
- Configured Version Streams: `2.1.x` (rhtpa-release.0.3.z) and `2.2.x` (rhtpa-release.0.4.z).
- The suffix matches a configured stream, so the issue is **scoped to 2.2.x**.
  Steps 2–8 analyze only the 2.2.x stream for this issue. The 2.1.x stream is checked
  only for cross-stream impact.

## Discrepancy flagged for Step 3

The Jira **Affects Versions** field is `RHTPA 2.0.0`. This does not match the
PSIRT-claimed stream `2.2.x` from the summary suffix, and no `2.0.x` stream is
configured. Step 3 must correct Affects Versions based on the version impact analysis
for the 2.2.x stream.

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | Cargo (quinn-proto is a Rust crate) |
| Supported in matrix? | Yes. Cargo is listed in the 2.2.x (and 2.1.x) Ecosystem Mappings |
| Category | Source dependency: 2 remediation tasks per affected stream (upstream backport + downstream propagation), or dependency bump + downstream propagation if upstream already ships the fix |
| Lock file / check command | `Cargo.lock` via `git show <tag>:Cargo.lock` in repo `backend`; 2.2.x upstream branch `release/0.4.z` |

## Deployment context

The affected component `org/rhtpa-server` maps to the backend source repository
(`rhtpa-backend`). The Source Repositories table has no Deployment Context column, so
the context defaults to **`upstream`**.
