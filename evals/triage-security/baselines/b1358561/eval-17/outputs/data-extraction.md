# Step 1 – Data Extraction: TC-8001

Source: mock Jira issue (`vuln-issue-standard.md`). No Jira MCP calls were made; the data
below was parsed from the provided issue file.

## Step 0 – Configuration Validation (from claude-md-security-config-embargo.md)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | Present |
| Project key | TC | Present |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | Present |
| Code Intelligence | `mcp__<serena-instance>__<tool>` naming convention | Present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | Present |
| Jira version prefix | RHTPA | Present |
| Vulnerability issue type ID | 10024 | Present |
| Component label pattern | `pscomponent:` | Present |
| VEX Justification custom field | customfield_12345 | Present (optional) |
| Embargo policy URL | https://example.com/security/embargo-policy | Present (optional), so Step 1.7 is active |
| Upstream Affected Component field | not configured | Steps 4.3 and 7 are skipped |
| ProdSec Jira account ID | not configured | Skip @mentions |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | Present |
| Source Repositories | rhtpa-backend | Present. No Deployment Context column, so it defaults to `upstream`. Coordination guidance is omitted (backward compatibility rule). |

Configuration is valid. Triage can proceed.

## Step 0.3 – Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-27) | Result |
|--------|--------------|------------------------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 152 days | STALE (threshold is 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 152 days | STALE (threshold is 14 days) |

> Security matrix for stream **2.1.x** / **2.2.x** was last updated on 2026-06-28
> (152 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now**: re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway**: continue triage with the current matrix
> 3. **Stop**: halt triage so I can investigate

In this eval there is no engineer to answer, and repository access is not allowed, so the
analysis continues with the current matrix (option 2). Any release after 2.2.4
(2026-05-04) is missing from this analysis.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Issue type / Status | Vulnerability / New | Issue. Status is New, so full triage applies. |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field. **Suspect: there is no 2.0.x stream in the configuration.** |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Vulnerability class | Denial of service (panic on an excessive STREAMS frame stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 (**already passed** as of 2026-11-27) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to stream `2.2.x`, which is in the Version Streams table
  (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 4 are limited to 2.2.x. Other
  affected streams are handled through Case A (cross-stream impact).

## Ecosystem Detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both
  streams' Ecosystem Mappings (repository `backend`, lock file `Cargo.lock`).
- Category: **Source dependency**. Each affected stream gets 2 remediation tasks
  (upstream backport or dependency bump, plus downstream propagation).

## Deployment Context

- Affected repository: rhtpa-backend (`backend`). Its deployment context is `upstream`
  by default, because the Source Repositories table has no Deployment Context column.
  The Coordination Guidance subsection is therefore omitted from task descriptions.

## Step 0.8 – Assignment (proposed, not executed)

- Proposed: assign TC-8001 to the current user and transition New to Assigned.
  This is not executed because Jira is out of scope for this eval.

## Step 1.5 – External CVE Data Enrichment

- MITRE CVE API and OSV.dev were **not queried**, because external calls are forbidden
  in this eval. This is treated as "both external sources unavailable":

> ⚠ External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

- Fix threshold used for Step 2: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed**
  (from the Jira description).
