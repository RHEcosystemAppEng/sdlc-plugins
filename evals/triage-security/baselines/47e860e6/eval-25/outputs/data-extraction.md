# Step 1 – Data Extraction: TC-8040

> Source: `vuln-issue-standard.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links` output).
> No Jira MCP, REST, or git calls were made. Note: the mock issue file lists key `TC-8001`;
> the triage target given for this eval is **TC-8040**, and the mock content is used as that issue's data.

## Pre-step context

| Check | Result |
|---|---|
| Mode (Step 0.6) | Interactive (`FULLSEND_OUTPUT_DIR` absent) |
| Step 0 – Configuration | Valid. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present |
| Jira version prefix | `RHTPA` |
| Vulnerability issue type ID | `10024` |
| Component label pattern | `pscomponent:` |
| VEX Justification field | `customfield_12345` |
| Embargo policy URL | Not configured, so Step 1.7 would be skipped |
| Upstream Affected Component field | Not configured, so Steps 4.3 and 7 would be skipped |
| Step 0.3 – Matrix staleness | `Last-Updated: 2026-06-28T10:00:00Z` is 129 days old, past the 14-day threshold. In a live run the engineer would be asked to choose Refresh / Proceed / Stop. This does not affect the ecosystem result below |
| Step 0.8 – Assign / transition | Simulated only. No Jira mutation was performed |

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8040 | Invocation argument |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Issue summary |
| Status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-31812 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary bracket suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream scope resolution

| Item | Result |
|---|---|
| Suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Scope | **Scoped** to the single stream 2.2.x |
| Observation | The PSIRT Affects Versions value (`RHTPA 2.0.0`) does not belong to the 2.2.x stream. Step 3 would normally correct this, but triage stops before Step 2 (see below) |

## Deployment context lookup

The Source Repositories table has no Deployment Context column, so the context defaults to **`upstream`** for backward compatibility. The component `org/rhtpa-server` maps to the `backend` repository (`rhtpa-backend`).

## Ecosystem detection

| Item | Result |
|---|---|
| **Detected ecosystem** | **Go modules** (resolution given for this eval scenario) |
| Ecosystems supported by stream 2.1.x (`rhtpa-release.0.3.z`) Ecosystem Mappings | Cargo, RPM |
| Ecosystems supported by stream 2.2.x (`rhtpa-release.0.4.z`) Ecosystem Mappings | Cargo, RPM |
| Listed in the in-scope stream's (2.2.x) Ecosystem Mappings? | **No** |
| Listed in any configured stream's mappings? | **No** |
| Classification table category | None. Go modules has no row (not a configured source dependency or system package ecosystem) |
| Lock file / check command | **None configured.** No `go.sum` / `go.mod` mapping exists, so no `git show` evidence can be gathered |
| **Outcome** | **UNSUPPORTED ECOSYSTEM. Automated triage stops here** (see `unsupported-ecosystem.md`) |

The skill does not substitute another ecosystem's mapping (for example Cargo's `Cargo.lock`) and does not invent dependency versions. Steps 1.5 through 8 are not run: no version impact table, no Affects Versions correction, no remediation tasks, no close recommendation, and no Jira mutations.
