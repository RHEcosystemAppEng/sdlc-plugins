# Triage TC-8001: Steps 0 to 1 (Configuration and Data Extraction)

> Eval mode: Jira MCP, `git show` and WebFetch were not called. The data comes from
> the supplied fixtures (`vuln-issue-standard.md`, `security-matrix-mock.md`,
> `claude-md-security-config.md`).

## Step 0.6: Fullsend Mode Detection

`FULLSEND_OUTPUT_DIR` is not set, so the skill runs in **interactive mode** (the
simulated confirmations are recorded below).

## Step 0: Validate Project Configuration

| Required section | Status | Value(s) |
|---|---|---|
| Repository Registry | Present | rhtpa-backend (serena_backend) |
| Jira Configuration | Present | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<serena-instance>__<tool>` naming convention |
| Security Configuration / Product Lifecycle | Present | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| Security Configuration / Version Streams | Present | 2.1.x → `rhtpa-release.0.3.z`, 2.2.x → `rhtpa-release.0.4.z` |
| Security Configuration / Source Repositories | Present | rhtpa-backend → `https://github.com/rhtpa/rhtpa-backend` |

Optional fields:

| Optional field | Status |
|---|---|
| VEX Justification custom field | `customfield_12345` (configured) |
| Upstream Affected Component custom field | Not configured, so Step 4.3 and Step 7 are skipped |
| PS Component / Stream custom fields | Not configured |
| ProdSec contact email / Jira account ID | Not configured, so @mentions are skipped silently |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |

### Source Repositories: deployment context parsing

The Source Repositories table has these columns: `Repository | URL | Local Path`.
**It has no `Deployment Context` column.** For backward compatibility, every
repository defaults to `upstream`:

| Repository | URL | Deployment Context |
|---|---|---|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | `upstream` (defaulted: no Deployment Context column) |

The missing column is not an error, and triage continues normally. Because the column
does not exist, the Step 8 remediation tasks will **omit the Coordination Guidance
subsection entirely**, as `remediation-templates.md` (Coordination Guidance) requires.

## Step 0.3: Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-06) | Result |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | 131 days | Stale (> 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 131 days | Stale (> 14 days) |

> Security matrix for stream **2.1.x** / **2.2.x** was last updated on 2026-06-28
> (131 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now, 2. Proceed anyway, 3. Stop

Simulated engineer choice: **2. Proceed anyway** (eval fixture data is authoritative).

## Step 0.8: Assign and Transition to Assigned

Status is `New`. Proposed actions: assign TC-8001 to the current user, then transition
to `Assigned` using the dynamically discovered transition. These are simulated only,
and no Jira call was made.

## Step 1: Data Extraction

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Vulnerability type | Denial of service (panic from an unbounded number of streams in a STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 | `duedate` field (already past as of 2026-11-06) |
| Status | New | Issue |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both
  streams' Ecosystem Mappings (`Cargo.lock`, repository `backend`).
- Category: **source dependency**, which means 2 remediation tasks per stream.

### Deployment context lookup

- Affected source repository: `rhtpa-backend` (the `backend` repository in Ecosystem Mappings).
- Deployment context: **`upstream`**. This is the default because the Source
  Repositories table has no Deployment Context column. It is recorded for Step 8, but no
  Coordination Guidance subsection will be generated (backward-compatibility rule).

## Step 1.5: External CVE Data Enrichment

The MITRE CVE API and OSV.dev were not queried (eval constraint: no external tools).
The result is treated as "unavailable" for both:

> ⚠ External CVE databases unavailable. Using Jira description data only.
> Fix threshold confidence is reduced.

Effective fix threshold: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed**.

## Step 1.7: Embargo Check

Skipped: no Embargo policy URL is configured.
