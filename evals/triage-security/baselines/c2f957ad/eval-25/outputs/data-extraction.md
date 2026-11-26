# Step 1 – Data Extraction: TC-8040

> Source: `vuln-issue-standard.md` (simulated `jira.get_issue` / `jira.get_issue_remote_links`
> output). Note: the mock issue file is keyed `TC-8001`; the triage target given for this run
> is `TC-8040`. The data is treated as the content of TC-8040.

## Pre-steps

- **Step 0.6 – Mode detection:** interactive mode (`FULLSEND_OUTPUT_DIR` not set). Step 0.7 skipped.
- **Step 0 – Configuration:** `claude-md-security-config.md` has all required sections
  (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration with
  Product Lifecycle, Version Streams, Source Repositories). Validation passed.
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Jira version prefix: RHTPA
  - Vulnerability issue type ID: 10024
  - Component label pattern: `pscomponent:`
  - VEX Justification custom field: customfield_12345
  - Product pages URL: https://access.example.com/product-life-cycle/rhtpa
  - Upstream Affected Component / PS Component / Stream fields: not configured
  - ProdSec contact / account ID: not configured
  - Embargo policy URL: not configured (Step 1.7 would be skipped)
  - Version Streams: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
  - Source Repositories: rhtpa-backend (https://github.com/rhtpa/rhtpa-backend); no Deployment
    Context column, so it defaults to `upstream`
- **Step 0.3 – Matrix staleness:** `Last-Updated: 2026-06-28T10:00:00Z` is about 151 days before
  today (2026-11-26), which is past the 14-day limit. In a live run the engineer would be warned
  and asked to choose Refresh / Proceed / Stop.
- **Step 0.5 / 0.8 – Jira access, assignment, transition:** not run (no external calls in
  this eval).

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8040 | Invocation argument |
| Status | New | Issue status (full triage path) |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / severity | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description references |
| Due date | 2026-07-15 | `duedate` field |
| Assignee | Unassigned | Issue field |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`, which maps to configured stream **2.2.x**
  (git.example.com/rhtpa/rhtpa-release.0.4.z)
- **Issue stream scope: 2.2.x (scoped)**
- The PSIRT Affects Versions value (RHTPA 2.0.0) does not belong to the 2.2.x stream.
  This would be checked for correction in Step 3 if triage continued.

## Ecosystem Detection

| Item | Value |
|------|-------|
| **Detected ecosystem** | **Go modules** (detection result fixed by the eval instructions) |
| Ecosystems in 2.1.x Ecosystem Mappings | Cargo, RPM |
| Ecosystems in 2.2.x Ecosystem Mappings | Cargo, RPM |
| Listed in in-scope stream (2.2.x) mappings? | **No** |
| Listed in any configured stream mappings? | **No** |
| Ecosystem classification category | None. Go modules is not in the classification table (Source dependency: Cargo, npm; System package: RPM) |
| Lock file / check command | None configured (no `go.sum` / `go.mod` mapping exists) |
| **Result** | **UNSUPPORTED ECOSYSTEM. Automated triage stops for this ecosystem.** |

Note: the library name (quinn-proto, a Rust crate) and the RUSTSEC reference would normally
point to Cargo. This run follows the eval instruction that detection resolves to Go modules.

## Deployment Context

- Component `org/rhtpa-server` does not match any entry in the Source Repositories table
  (only `rhtpa-backend` is listed), so it defaults to **`upstream`**.
- The Source Repositories table has no Deployment Context column, so all repos default to
  `upstream` anyway.

## Triage Status

Ecosystem detection in Step 1 returned an ecosystem that is not supported. Under the skill's
Ecosystem detection rule, the user is told and automated triage **stops** for this ecosystem.
None of the following ran: Step 1.5 (external enrichment), Step 1.7, Step 2 (version impact /
lock file inspection), Steps 3–8 (Affects Versions correction, duplicate checks, lifecycle,
already-fixed, concurrent triage, release Jira, remediation). No Jira mutations were proposed
or made. See `unsupported-ecosystem.md`.
