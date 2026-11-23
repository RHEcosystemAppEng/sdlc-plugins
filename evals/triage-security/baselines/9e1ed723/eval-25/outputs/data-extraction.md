# Step 1 – Data Extraction: TC-8040

> Simulated triage. No Jira MCP, git, or WebFetch calls were made. The data comes from
> the mock issue file `vuln-issue-standard.md`. Note: the mock file records the issue key
> as **TC-8001**, but this eval asks for **TC-8040**. This document uses TC-8040 as the
> invocation target.

## Pre-steps (summary)

| Step | Result |
|------|--------|
| 0.6 Fullsend Mode Detection | Interactive mode (`FULLSEND_OUTPUT_DIR` not set); Steps 0.7 and Fullsend serialization skipped |
| 0 Validate Configuration | PASS. Repository Registry, Jira Configuration, Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present |
| 0.3 Matrix Staleness Check | WARNING. `Last-Updated: 2026-06-28T10:00:00Z` is 148 days old (threshold is 14 days) for streams 2.1.x and 2.2.x. In a live run the engineer would choose Refresh / Proceed / Stop. Simulated choice: Proceed |
| 0.5 Jira Access | Simulated (no live calls) |
| 0.8 Assign / Transition | Simulated only. Status is New, so a live run would assign the issue to the current user and move it to Assigned |

### Extracted configuration

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured (Steps 4.3 and 7 would be skipped) |
| Embargo policy URL | Not configured (Step 1.7 would be skipped) |
| ProdSec contact / account ID | Not configured |
| Version Streams | 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`) |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend, deployment context `upstream` (default, because the Deployment Context column is absent) |

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8040 (mock file says TC-8001) | Invocation |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Summary |
| Status | New | Status field |
| Affected component | `pscomponent:org/rhtpa-server` → `org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary bracket suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description references |
| Due date | 2026-07-15 | `duedate` field |
| Assignee | Unassigned | Assignee field |
| Existing comments | None | Comment history |
| Deployment context | `upstream` (default) | Source Repositories lookup |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Matched Version Stream | **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Issue stream scope | Scoped to 2.2.x |

Observation for later steps: the PSIRT-assigned Affects Version (RHTPA 2.0.0) does not
match the 2.2 stream scope. Step 3 would normally correct this, but triage stops before
reaching Step 3 (see below).

## Ecosystem detection

| Item | Value |
|------|-------|
| **Detected ecosystem** | **Go modules** (as the eval scenario specifies) |
| Ecosystems in the 2.2.x Ecosystem Mappings table | Cargo, RPM |
| Ecosystems in the 2.1.x Ecosystem Mappings table | Cargo, RPM |
| Listed in Ecosystem Mappings? | **No** |
| Ecosystem classification category | None. Go modules has no row in the classification table (Source dependency: Cargo, npm; System package: RPM) |
| Lock file / check command | None configured for Go modules (no `go.sum`/`go.mod` mapping in any stream) |
| **Result** | **UNSUPPORTED ECOSYSTEM. Automated triage stops here.** |

Note: the library name (quinn-proto) and the RUSTSEC reference would normally indicate
Cargo. This simulation follows the eval's instruction that detection resolves to Go
modules.

## Disposition

The skill says that when the detected ecosystem is not in the stream's Ecosystem Mappings
table, it must inform the user and stop automated triage for that ecosystem. The
following steps were **not** executed:

- 1.5 External CVE Data Enrichment
- 1.7 Embargo Check (would be skipped anyway, since no Embargo policy URL is configured)
- 2 Version Impact Analysis (there is no lock file or check command for Go modules)
- 3 Affects Versions Correction
- 4 to 7.5 Duplicate, Lifecycle, Already-Fixed, Concurrent, and Release Jira checks
- 8 Remediation (no task structure is defined for Go modules)
- Post-Triage Summary (no `ai-cve-triaged` label and no summary comment)

No Jira mutations were proposed or performed. See `unsupported-ecosystem.md` for the
notification shown to the user.
