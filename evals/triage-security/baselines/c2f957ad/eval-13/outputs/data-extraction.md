# TC-8001 — Step 1 Data Extraction

Simulated run: the issue was read from the mock file `vuln-issue-standard.md`.
No Jira MCP, REST, git, or WebFetch calls were made.

## Pre-flight (Steps 0 – 0.8)

| Step | Result |
|------|--------|
| 0 – Validate configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present. |
| 0 – Extracted config | Jira version prefix `RHTPA`; Vulnerability issue type ID `10024`; Component label pattern `pscomponent:`; Product pages URL `https://access.example.com/product-life-cycle/rhtpa`; VEX Justification field `customfield_12345`. Not configured: Upstream Affected Component field (so Steps 4.3 and 7 are skipped), ProdSec contact or account ID, and Embargo policy URL (so Step 1.7 is skipped). |
| 0.3 – Matrix staleness | WARNING. The matrix says `Last-Updated: 2026-06-28T10:00:00Z`, which is 151 days before today (2026-11-26). The limit is 14 days. In a real run the engineer would choose Refresh, Proceed, or Stop. For this eval I continued with the current matrix. |
| 0.6 – Fullsend detection | Interactive mode (`FULLSEND_OUTPUT_DIR` is not set). |
| 0.8 – Assign + transition | Planned, not run: assign TC-8001 to the current user and move it New -> Assigned. The transition is looked up at run time, not hard-coded. |

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` |
| Affected repository | rhtpa-backend (`backend` in Ecosystem Mappings) | Source Repositories / Ecosystem Mappings |
| Deployment context | Not configured. The Source Repositories table has no Deployment Context column. Step 0 defaults it to `upstream`, but because the column is missing, the Coordination Guidance subsection is left out of the task descriptions (backward compatibility). | Security Configuration |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix `[rhtpa-2.2]` |
| Issue stream scope | **2.2.x** (scoped) | `[rhtpa-2.2]` matches Version Stream `2.2.x` (`rhtpa-release.0.4.z`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field. This does not match the scope; corrected in Step 3. |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (source dependency, so 2 tasks per stream) | Rust crate, `Cargo.lock` mapping in the matrix |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High) | Description |
| Vulnerability | DoS: a panic caused by an unbounded number of streams in a QUIC STREAMS frame | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links / description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15. **Already past** as of 2026-11-26. | `duedate` |
| Existing comments | None | Comment history |
| Assignee | Unassigned | Issue |
| Reporter (for the summary @mention) | Not present in the mock data. Would come from the live issue's `reporter.accountId`. | Issue |
| Security level (to copy to tasks) | Not present in the mock data. Would come from a live `jira.get_issue`. | Issue |

All critical fields (CVE ID, library, affected range) were parsed. No engineer input was needed.

## Step 1.5 – External CVE data enrichment

| Source | Affected range | Fixed version | Status |
|--------|----------------|---------------|--------|
| Jira description | < 0.11.14 | 0.11.14 | Parsed |
| MITRE CVE API | — | — | Not queried (eval forbids external calls) |
| OSV.dev | — | — | Not queried (eval forbids external calls) |

> External CVE databases were unavailable, so only the Jira description data is used.
> Confidence in the fix threshold is lower.

Fix threshold used in Step 2: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.**

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured, even though CVSS 7.5 is at or above the 7.0 threshold.
