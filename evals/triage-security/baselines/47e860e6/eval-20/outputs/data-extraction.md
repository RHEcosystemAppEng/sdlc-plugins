# Step 1 – Data Extraction (TC-8001)

Source: mock Jira issue (`vuln-issue-standard.md`), standing in for `jira.get_issue(TC-8001)` and `jira.get_issue_remote_links(TC-8001)`. No Jira calls were made.

Issue status: **New**, so full triage applies under the status-aware handling rules.

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary text (they match) |
| Affected component | `pscomponent:org/rhtpa-server` (component `org/rhtpa-server`) | Label matching the `pscomponent:` pattern |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / severity | 7.5 (High) | Description |
| Vulnerability type | Denial of service: panic from an unbounded number of streams in a QUIC STREAMS frame | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (GHSA-2026-qp73-x4mq) | Remote links |
| Additional advisory | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` field |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library and affected range) were parsed, so no engineer input is needed.

## Stream scope resolution

| Item | Value |
|---|---|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z) |
| Scope | **Scoped** to a single stream (2.2.x) |

The suffix matches a configured Version Stream. Steps 3 and 4 will be scoped to 2.2.x. Step 2 still checks every supported version, including 2.1.x, so that any cross-stream impact can be found (Case A).

## Affects Versions mismatch (preliminary)

PSIRT set Affects Versions to **RHTPA 2.0.0**. The issue is scoped to `rhtpa-2.2`, and no 2.0.x stream is configured. This field looks wrong and is a candidate for correction in Step 3, once Step 2 has produced the lock-file evidence.

## Ecosystem detection

| Item | Value |
|---|---|
| Ecosystem | **Cargo** (quinn-proto is a Rust crate) |
| Category | Source dependency: 2 remediation tasks per affected stream |
| Supported in Ecosystem Mappings | Yes (both streams list Cargo, `Cargo.lock`, `git show <tag>:Cargo.lock`) |
| Upstream branches | 2.1.x: `release/0.3.z`; 2.2.x: `release/0.4.z` |

## Deployment context

The component label `org/rhtpa-server` does not exactly match any repository name in the Source Repositories table. The only configured repository is `rhtpa-backend`, which is the `backend` repo in the matrix. The Source Repositories table has no Deployment Context column, so the deployment context defaults to **`upstream`**.

## External enrichment note (Step 1.5)

The task said not to call external tools, so I did not query the MITRE and OSV.dev APIs. Without them, the Jira description threshold (< 0.11.14, fixed in 0.11.14) is the working fix threshold, with reduced confidence.

## Embargo check note (Step 1.7)

The Security Configuration has no Embargo policy URL, so Step 1.7 is skipped even though CVSS is 7.5.
