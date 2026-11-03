# TC-8001: Data Extraction (Step 1), Re-run

Execution mode: **interactive** (`FULLSEND_OUTPUT_DIR` is not set; Step 0.6). Step 0.7 is skipped.
No Jira, git or WebFetch calls were made. All data comes from the provided mock files.

## Step 0: Configuration validation (from claude-md-security-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend | OK |
| Project key / Cloud ID | TC / 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | serena_backend | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification field | customfield_12345 | Configured |
| Upstream Affected Component / PS Component / Stream fields | not configured | Steps 4.3 and 7 are skipped |
| ProdSec contact / account ID | not configured | No @mentions |
| Embargo policy URL | not configured | Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column) | Defaults to `upstream` |

## Step 0.3: Matrix staleness check

- `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-03, so the matrix is **128 days old**. The threshold is 14 days.
- Warning: the matrix may not reflect releases made after 2026-06-28. An interactive run would offer Refresh / Proceed / Stop. Refreshing only writes the local `security-matrix.md`, never Jira. For this eval the run continues with the current matrix ("Proceed anyway").

## Step 0.8 and status-aware handling

- Current status: **In Progress**. This is later than Assigned, so the transition to Assigned is **skipped**.
- Status-aware warning: "This issue is already in `In Progress`. It may be actively worked on." The run continues so the earlier triage can be checked.
- Assignee: engineer-a@example.com is already set. This assumes the re-run is done by the same engineer, so re-assigning changes nothing (see idempotency-check.md).

## Step 1: Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Stream scope | **2.2.x** (scoped) | `[rhtpa-2.2]` maps to Version Streams row 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field (set by the earlier run) |
| Vulnerable library | **quinn-proto** | Description |
| Ecosystem | Cargo (source dependency, 2 tasks per stream) | Rust crate; Cargo row in the 2.2.x Ecosystem Mappings |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock` | Matrix Ecosystem Mappings |
| Upstream branch | `release/0.4.z` | Matrix Ecosystem Mappings |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| Severity | CVSS 7.5 (High) | Description |
| Vulnerability class | DoS (panic on excessive STREAMS frame stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-03) | `duedate` |
| Deployment context | upstream (default, column absent) | Source Repositories |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | Issue |
| Status | **In Progress** | Issue |
| Assignee | engineer-a@example.com | Issue |
| Custom fields on issue | cf_10632 = quinn-proto; cf_10669 = pscomponent:org/rhtpa-server; cf_10832 = rhtpa-2.2 | Issue |
| Existing issue links | Depend: TC-8100 (upstream backport, In Progress); Depend: TC-8101 (downstream propagation, Open, blocked by TC-8100) | Issue links |
| Existing comments | (1) `[sdlc-workflow] Description digest: sha256-md:a1b2...a1b2` (2026-07-01T10:00Z); (2) Post-triage summary with Comment Footnote (v0.11.1, 2026-07-01T10:01Z) | Comment history |

All critical fields (CVE ID, library, affected range) were parsed, so the run does not stop at Step 1.

## Step 1.5: External enrichment

No external calls are allowed in this eval, so MITRE and OSV are treated as unavailable.
> External CVE databases unavailable. Using Jira description data only. Confidence in the fix threshold is reduced.

Fix threshold used: **0.11.14** (from the Jira description).

## Step 1.7: Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise have triggered the gate.

## Step 2: Version impact (scope 2.2.x, simulated `git show` data from the mock)

| Version | Backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES |
| RHTPA 2.2.2 | v0.4.8 (backend retag of 2.2.1) | 0.11.12 (same as 2.2.1) | **YES** |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO |

Outside scope (2.1.x, for Case A awareness): RHTPA 2.1.0 (v0.3.8) and 2.1.1 (v0.3.12) both ship 0.11.9, so both are **YES**.

Step 2.2 (development stream through unreleased Jira versions) and branch-HEAD checks could not run without Jira or git. Step 2.5: the matrix data shows `release/0.4.z` has shipped quinn-proto 0.11.14 since v0.4.11 (RHTPA 2.2.3).
