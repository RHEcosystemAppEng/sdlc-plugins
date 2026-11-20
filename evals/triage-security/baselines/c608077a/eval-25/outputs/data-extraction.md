# Step 1 – Data Extraction: TC-8040

> Simulated run. No Jira MCP, `git show`, or other external tools were called.
> Issue data comes from `vuln-issue-standard.md`, matrix data from `security-matrix-mock.md`,
> and project configuration from `claude-md-security-config.md`.
>
> Note: the task asks for **TC-8040**, but the mock issue file shows key `TC-8001`.
> The rest of the mock content is treated as the issue data for TC-8040.

## Step 0 – Configuration (from project CLAUDE.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary text |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | `< 0.11.14` (versions before 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High), DoS | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` field |
| Status | New | Issue status |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed, so extraction is complete.

## Stream Scope Resolution

| Item | Result |
|------|--------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (rhtpa-release.0.4.z), which is a configured Version Stream |
| Issue stream scope | **Scoped to 2.2.x** |

Observation: the Jira Affects Versions field (`RHTPA 2.0.0`) does not match the scoped
stream (2.2.x), and there is no 2.0.x stream configured. Step 4 would normally correct
this, but triage stops before then (see below).

## Ecosystem Detection

| Item | Result |
|------|--------|
| Detected ecosystem | **Go modules** (resolution given by the eval instructions) |
| Ecosystems configured in stream 2.2.x Ecosystem Mappings | Cargo (`Cargo.lock`), RPM (`rpms.lock.yaml`) |
| Ecosystems configured in stream 2.1.x Ecosystem Mappings | Cargo (`Cargo.lock`), RPM (`rpms.lock.yaml`) |
| Listed in Ecosystem Mappings? | **No.** Go modules is not configured in any stream |
| Classification category | None. Go modules is not in the ecosystem classification table (source dependency or system package) |
| Lock file / check command | None configured (no `go.sum` / `go.mod` mapping exists) |
| Outcome | **Unsupported ecosystem. Automated triage stops for this ecosystem.** See `unsupported-ecosystem.md` |

Note: from its name, library, and RUSTSEC reference, quinn-proto looks like a Rust crate
(Cargo). Go modules is used here only because the eval scenario requires it.

## Deployment Context

| Item | Result |
|------|--------|
| Affected repository | rhtpa-backend (the only configured source repository; component `org/rhtpa-server`) |
| Deployment context | `upstream` (default: the Source Repositories table does not specify a deployment context) |

## Steps Not Executed

Because the ecosystem is unsupported, the following steps were **not** run for this ecosystem:

- Step 1.5 External CVE enrichment (MITRE / OSV)
- Step 2 Version impact analysis (no lock file or check command to inspect)
- Steps 3–6 Jira triage operations (Affects Versions correction, duplicate and lifecycle checks)
- Steps 7 / 7.5 / 8 Concurrent-triage detection, release Jira, remediation task creation
- Post-triage `ai-cve-triaged` label and summary comment

No Jira changes were made.
