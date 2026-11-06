# Step 1 – Data Extraction: TC-8030

Source: mock Jira issue (`vuln-issue-enrichment.md`). No live Jira calls were made.

## Pre-flight (Steps 0 – 0.8)

| Check | Result |
|-------|--------|
| Step 0.6 Mode | Interactive (eval). `FULLSEND_OUTPUT_DIR` is not set |
| Step 0 Configuration | PASS. Repository Registry, Jira Configuration (TC, Cloud ID 2b9e35e3-...), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 (configured) |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Upstream Affected Component field | Not configured, so Steps 4.3 and 7 are skipped |
| ProdSec Jira account ID | Not configured, so @mentions are omitted |
| Deployment Context column | Absent from Source Repositories. Defaults to `upstream`. Per the template rules, the Coordination Guidance subsection is omitted |
| Step 0.3 Matrix staleness | WARNING. `Last-Updated: 2026-06-28T10:00:00Z` is 131 days old (today is 2026-11-06), which exceeds the 14-day threshold. Options are Refresh / Proceed / Stop. For the eval we chose **Proceed anyway** with the current matrix. Newer 2.1.x/2.2.x releases may be missing |
| Step 0.8 Assign/transition | Would assign TC-8030 to the current user and transition New to Assigned. Not executed (eval) |
| Status-aware handling | Status = New, so full triage runs |

## Extracted Fields

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Label `CVE-2026-48901` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate, hyperium/h2) | Description |
| Affected version range | "versions prior to the fix". **Imprecise: no parseable threshold** | Description |
| Fixed version | "see advisory". **Imprecise: no parseable version** | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability | HTTP/2 CONTINUATION flood. Unbounded CONTINUATION frames after HEADERS cause excessive memory and CPU use (DoS) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p (also RUSTSEC-2026-0089: https://rustsec.org/advisories/RUSTSEC-2026-0089.html) | Remote links / description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 (**already past** as of 2026-11-06) | `duedate` |
| Assignee | Unassigned | Issue |
| Status | New | Issue |
| Existing comments | None | Comment history |

## Critical Field Assessment

- CVE ID: parsed.
- Library: parsed (`h2`).
- Affected range: **not precisely parseable from the Jira description.** Normally the skill would stop here and ask the engineer. Step 1.5 always queries external CVE databases, and both MITRE and OSV.dev return a precise, consistent threshold (`< 0.4.8`, fixed `0.4.8`). That threshold fills the gap; see `enrichment.md`. The engineer should still confirm it.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which matches Version Streams row `2.2.x`: `git.example.com/rhtpa/rhtpa-release.0.4.z`.
- **Issue stream scope: 2.2.x (scoped).** Step 3 corrections apply to 2.2.x only. The 2.1.x stream is treated as cross-stream (Case A).

## Ecosystem Detection

- h2 is a Rust crate, so the ecosystem is **Cargo**, listed in both streams' Ecosystem Mappings (`backend`, `Cargo.lock`, `git show <tag>:Cargo.lock`).
- Category: **source dependency**. That means 2 remediation tasks per affected stream (upstream backport or dependency bump, plus downstream propagation).

## Deployment Context

- Affected source repo: `rhtpa-backend` (Ecosystem Mappings repository `backend`; component `org/rhtpa-server`).
- The Source Repositories table has no Deployment Context column, so the context defaults to `upstream` for backward compatibility. The Coordination Guidance subsection is omitted from task descriptions, as the template rules require.
