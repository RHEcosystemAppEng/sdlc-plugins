# Step 1 – Data Extraction: TC-8040

> Simulated triage. No Jira MCP, `git show`, or external calls were made. Data comes
> from the mock issue (`vuln-issue-standard.md`), the mock matrix
> (`security-matrix-mock.md`), and the mock project CLAUDE.md
> (`claude-md-security-config.md`).
>
> Note: the task names the issue **TC-8040**, but the mock issue file shows key
> `TC-8001`. This triage treats TC-8040 as the invocation target and uses the mock
> file's contents as its issue data.

## Preceding steps (summary)

| Step | Result |
|------|--------|
| 0 – Validate Configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present. |
| 0.3 – Matrix Staleness Check | WARNING. `Last-Updated: 2026-06-28T10:00:00Z` is 128 days old (today is 2026-11-03), which is over the 14-day threshold. In a live run the engineer would be asked to pick Refresh now / Proceed anyway / Stop. |
| 0.6 – Fullsend Mode Detection | Interactive mode (`FULLSEND_OUTPUT_DIR` not set). |
| 0.8 – Assign / Transition | Skipped in this simulation (no Jira calls). It would assign the issue to the current user and move it from New to Assigned. |

## Extracted configuration

| Field | Value |
|-------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 would be skipped) |
| Embargo policy URL | not configured (Step 1.7 would be skipped) |
| Version Streams | 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`) |
| Source Repositories | rhtpa-backend: https://github.com/rhtpa/rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8040 (mock file key: TC-8001) | Task / issue data |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Summary |
| Status | New | Issue status |
| CVE ID | CVE-2026-31812 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary bracket suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field (does not match the claimed 2.2 stream; would be checked in Step 3) |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description references |
| Due date | 2026-07-15 | `duedate` field |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream scope resolution

| Item | Result |
|------|--------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Scope | **Scoped**: only stream 2.2.x would be analyzed |

## Deployment context

| Item | Result |
|------|--------|
| Affected repository | Component `org/rhtpa-server`. It has no exact match in the Source Repositories table (only `rhtpa-backend` is listed). |
| Deployment context | `upstream` (default: the table has no Deployment Context column, and the repo is not listed) |

## Ecosystem detection

| Item | Result |
|------|--------|
| **Detected ecosystem** | **Go modules** (per the eval override for Step 1) |
| Ecosystems in stream 2.2.x Ecosystem Mappings | Cargo, RPM |
| Ecosystems in stream 2.1.x Ecosystem Mappings | Cargo, RPM |
| Listed in Ecosystem Mappings? | **No** |
| Classification (source dependency / system package) | **Undefined.** Go modules is not in the ecosystem classification table. |
| Lock file / check command | **None configured** (a Go triage would need e.g. `go.sum` / `go.mod`, but no mapping exists) |
| **Outcome** | **UNSUPPORTED ECOSYSTEM. Automated triage stops here.** See `unsupported-ecosystem.md`. |

Note: the library name `quinn-proto` and the RUSTSEC reference would normally point to
Cargo. This eval says to treat detection as resolving to Go modules, so the unsupported
path applies.

## Steps not executed

Detecting an unsupported ecosystem stops automated triage. So Steps 1.5 (External
CVE Enrichment), 1.7 (Embargo Check), 2 (Version Impact Analysis), 3 (Affects
Versions Correction), 4–6, 7, 7.5, and 8 (Remediation) were **not** run. No version
impact table was built and no dependency versions were inferred. No Jira mutations
were proposed or made: no Affects Versions change, no `ai-cve-triaged` label, no
remediation tasks, and no comments.
