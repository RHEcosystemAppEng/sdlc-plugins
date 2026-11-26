# Triage Data Extraction: TC-8001

Skill: `/sdlc-workflow:triage-security` (interactive mode, simulated: no Jira, git, or WebFetch calls were made)

## Step 0: Configuration Validation

All required sections are present in the project CLAUDE.md (`claude-md-security-config-deploy-ctx.md`):

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| ProdSec Jira account ID | not configured (no @mentions) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |

### Source Repositories mapping (includes Deployment Context)

The Deployment Context column is present, so values come straight from the table. The `upstream` default is not used.

| Repository | URL | Deployment Context |
|---|---|---|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

## Step 0.3: Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-26) | Status |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | 151 days | STALE (threshold 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 151 days | STALE (threshold 14 days) |

> Both security matrices were last updated on 2026-06-28, 151 days ago, so they may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.
> For this eval the triage continues on the current matrix (option 2).

## Step 1: Parsed CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8001 |
| Issue type / Status | Vulnerability / New |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` (summary suffix) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Vulnerability class | Denial of service (panic on excessive stream count in a STREAMS frame) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html |
| Due date | 2026-07-15 (already past as of 2026-11-26) |
| Assignee | Unassigned (Step 0.8 would assign it to the current user and move it to Assigned) |
| Existing comments | none |
| Ecosystem | Cargo (Rust crate). Category: source dependency, so 2 tasks per stream |
| Affected repository | rhtpa-backend (`backend` in the Ecosystem Mappings; lock file `Cargo.lock`) |
| **Deployment context** | **customer-shipped**, looked up from Source Repositories for `rhtpa-backend` |

The critical fields (CVE ID, library, affected range) all parsed, so there is no blocker.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (rhtpa-release.0.4.z), which is a configured stream.
- **Issue stream scope: 2.2.x (scoped).** Stream 2.1.x is outside this issue's scope and is handled through Case A, cross-stream impact.

### Deployment context lookup

| Affected repository | Found in Source Repositories? | Deployment Context | Source |
|---|---|---|---|
| rhtpa-backend | Yes | **customer-shipped** | Deployment Context column in the CLAUDE.md Source Repositories table |

Step 8 uses this value. Each remediation task's Implementation Notes gets a customer-shipped `### Coordination Guidance` subsection.

## Step 1.5: External CVE Data Enrichment

The MITRE and OSV.dev lookups were not run, because this eval forbids external calls.
> External CVE databases unavailable. Using Jira description data only, so confidence in the fix threshold is reduced.

Fix threshold used: **< 0.11.14** (from the Jira description).

## Step 1.7: Embargo Check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise trigger the gate.

## Step 2: Version Impact Analysis

Lock file data comes from the simulated `git show <tag>:Cargo.lock` output in `security-matrix-mock.md`.

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |

No development stream could be determined. Unreleased Jira versions (Step 2.2) need a Jira query, and no branch HEAD lock data was provided.

Dependency chain: the mock data does not include the manifest or dependency-tree evidence needed to say whether quinn-proto is direct or transitive in `backend`. It is usually transitive through `quinn`, but that is unverified, so both remediation approaches stay in the task templates. No evidence shows it is dev-only.

### Upstream fix status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Evidence | Fixed? |
|---|---|---|---|---|
| 2.2.x | Cargo | release/0.4.z | Released tags v0.4.11 and v0.4.12 already ship 0.11.14. Branch HEAD was not read directly. | YES (inferred from released tags) |
| 2.1.x | Cargo | release/0.3.z | Latest tag v0.3.12 ships 0.11.9. Branch HEAD was not read directly. | NO (per available evidence) |

## Step 3: Affects Versions Correction (proposed)

| | Versions |
|---|---|
| Current (PSIRT) | RHTPA 2.0.0 |
| Proposed (scoped to 2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

RHTPA 2.0.0 is not a configured stream, and no lock evidence supports it. 2.2.3 and 2.2.4 ship the fixed 0.11.14.

## Steps 4-7 (summary)

- Step 4 (sibling and duplicate search for CVE-2026-31812 `[rhtpa-2.1]`): needs JQL and was not run. The proposal below assumes no 2.1.x sibling exists, so 2.1.x gets preemptive tasks.
- Step 5 (lifecycle): needs the product pages URL and was not run.
- Step 6 (already fixed): no resolved siblings are known. Within 2.2.x the fix already shipped in 2.2.3.
- Step 7 (concurrent triage): skipped because the Upstream Affected Component field is not configured.
