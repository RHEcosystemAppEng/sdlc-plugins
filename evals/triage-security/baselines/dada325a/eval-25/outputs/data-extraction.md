# Step 1 – Data Extraction: TC-8040

> Simulated triage (eval). No Jira MCP, REST API, `git show`, or WebFetch calls were made.
> Issue data comes from `vuln-issue-standard.md`, which records the key as `TC-8001`; this
> triage is run against the requested key **TC-8040** using that mock content.

## Pre-steps (simulated)

| Step | Result |
|------|--------|
| 0.6 Fullsend Mode Detection | `FULLSEND_OUTPUT_DIR` not set, so interactive mode |
| 0 Validate Configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present |
| 0.3 Matrix Staleness Check | Both streams show `Last-Updated: 2026-06-28T10:00:00Z`, which is 131 days old as of 2026-11-06 and over the 14-day threshold. In a live run the engineer would be warned and offered Refresh / Proceed / Stop. This does not matter here because triage stops in Step 1 |
| 0.5 Jira Access | Not run (eval) |
| 0.8 Assign and Transition | Not run (eval). In a live run, TC-8040 would be assigned to the current user and moved New -> Assigned |

### Extracted configuration

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured (Steps 4.3 and 7 would be skipped) |
| Embargo policy URL | Not configured (Step 1.7 would be skipped) |
| Version Streams | 2.1.x -> git.example.com/rhtpa/rhtpa-release.0.3.z; 2.2.x -> git.example.com/rhtpa/rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend -> https://github.com/rhtpa/rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8040 |
| Issue type / Status | Vulnerability / New |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Vulnerability class | Denial of service (panic from unbounded stream allocation) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0042.html |
| Due date | 2026-07-15 (already past as of 2026-11-06) |
| Assignee | Unassigned |
| Existing comments | None |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream scope resolution

| Item | Result |
|------|--------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z) |
| Scope | **Scoped** to 2.2.x |
| Note | The Jira Affects Versions value (RHTPA 2.0.0) does not belong to the 2.2.x stream, and no 2.0.x stream is configured. Step 3 would normally correct this, but triage does not get that far (see below) |

## Ecosystem detection

| Item | Result |
|------|--------|
| Detected ecosystem | **Go modules** (resolved per eval instruction) |
| Ecosystems supported in stream 2.1.x (`rhtpa-release.0.3.z`) | Cargo (`Cargo.lock`), RPM (`rpms.lock.yaml`) |
| Ecosystems supported in stream 2.2.x (`rhtpa-release.0.4.z`) | Cargo (`Cargo.lock`), RPM (`rpms.lock.yaml`) |
| Listed in Ecosystem Mappings? | **No.** Go modules is not in either stream's table |
| Classification (source dependency / system package) | Undefined. Go modules is not in the skill's ecosystem classification table |
| Lock file / check command | None configured (no `go.sum` / `go.mod` mapping exists) |
| **Result** | **UNSUPPORTED ECOSYSTEM. Automated triage stops here** |

## Deployment context

| Item | Result |
|------|--------|
| Affected repository | rhtpa-backend (the only configured source repository; component `org/rhtpa-server`) |
| Deployment context | `upstream` (default; no Deployment Context column) |

## Triage status

Automated triage **stopped at Step 1 (Ecosystem detection)** because Go modules is not
supported. These steps were **not** run: 1.5 (External CVE enrichment), 1.7 (Embargo),
2 (Version Impact Analysis), 3 (Affects Versions correction), 4 to 7.5, and 8 (Remediation).
No Jira mutations were proposed or performed. The `ai-cve-triaged` label is **not** added,
because the issue has not been triaged. See `unsupported-ecosystem.md` for the notification
shown to the user.
