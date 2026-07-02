# Step 1 -- Data Extraction

## Issue: TC-8040

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | None |

## Ecosystem Detection

Detected ecosystem: **Go modules**

The vulnerable library `quinn-proto` was resolved to the **Go modules** ecosystem based on the library name and component context.

### Ecosystem Mappings Check

The Ecosystem Mappings tables in `security-matrix.md` for both configured streams (2.1.x and 2.2.x) list the following supported ecosystems:

| Ecosystem | Supported |
|-----------|-----------|
| Cargo | Yes |
| RPM | Yes |
| Go modules | **No -- not listed** |

**Result**: Go modules is not present in any stream's Ecosystem Mappings table. Automated triage cannot proceed -- the skill does not have a configured lock file path or check command for this ecosystem.

## Stream Scope Resolution

The summary suffix `[rhtpa-2.2]` maps to the **2.2.x** stream, which is configured in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Deployment Context

Repository `rhtpa-backend` found in Source Repositories table. Deployment context defaults to `upstream` (no Deployment Context column present).
