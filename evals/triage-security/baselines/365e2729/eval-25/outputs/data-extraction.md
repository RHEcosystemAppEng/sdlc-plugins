# Step 1 – Data Extraction: TC-8040

> Execution mode: **interactive** (`FULLSEND_OUTPUT_DIR` absent — Step 0.6). Step 0.7 skipped.
> No Jira MCP, `git show`, or WebFetch calls were made (eval constraint). Data is taken from
> the provided mock files.
>
> Note: the task names the issue **TC-8040**. The mock issue file shows key `TC-8001`. This
> report uses TC-8040 as the invocation target and the mock file's contents as its data.

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (1 entry) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | present (serena_backend) | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification custom field | customfield_12345 | configured |
| Upstream Affected Component field | not configured | Steps 4.3 / 7 would be skipped |
| Embargo policy URL | not configured | Step 1.7 would be skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column, so defaults to `upstream`) | OK |

## Step 0.3 – Matrix Staleness Check

- Matrix `Last-Updated`: `2026-06-28T10:00:00Z`
- Today: 2026-11-26, so the matrix is **151 days old**, past the 14-day threshold.
- The skill would warn and offer **Refresh now / Proceed anyway / Stop**. For this eval,
  assume the engineer chose **Proceed anyway**.

## Step 0.8 – Assign and Transition (simulated only)

The issue is in `New` status. The skill would propose assigning it to the current user and
transitioning it to `Assigned`, after confirmation. Not executed.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8040 | Invocation argument |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Summary |
| Status | New | Status field |
| CVE ID | **CVE-2026-31812** | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` (component: `org/rhtpa-server`) | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary bracket suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | **quinn-proto** | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| CVSS / severity | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Assignee | Unassigned | Assignee field |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).**
- Observation for later steps: the Jira Affects Versions value (RHTPA 2.0.0) does not belong to
  any configured stream. Step 3 would correct it, but triage stops before Step 3 (see below).

## Ecosystem Detection

| Item | Result |
|------|--------|
| Detected ecosystem | **Go modules** (resolved as given by the eval scenario) |
| Stream checked | 2.2.x (issue scope). 2.1.x also checked for completeness |
| Ecosystem Mappings in 2.2.x `security-matrix.md` | Cargo, RPM |
| Ecosystem Mappings in 2.1.x `security-matrix.md` | Cargo, RPM |
| Listed in Ecosystem Mappings? | **No** |
| Category in classification table | **None.** Go modules is not classified as a source dependency (Cargo, npm) or system package (RPM) ecosystem |
| Lock file / check command | **Not available.** No mapping row exists, so there is no lock file path (e.g. `go.sum`/`go.mod`) or check command to run |
| Result | **UNSUPPORTED ECOSYSTEM.** Automated triage stops for this ecosystem |

Note: the library name (quinn-proto, a Rust crate, with a RUSTSEC advisory) would normally
resolve to Cargo. The eval scenario says to assume Go modules, so this report uses that result.
The engineer should confirm the ecosystem during manual assessment.

## Deployment Context

- Component `org/rhtpa-server` has no exact match in the Source Repositories table (only
  `rhtpa-backend`). The skill falls back to **`upstream`**. The Source Repositories table has
  no Deployment Context column, which also means `upstream` by default.

## Steps Not Executed

Because the ecosystem is unsupported, the skill stops before these steps:
- Step 1.5 (MITRE/OSV enrichment): not run
- Step 1.7 (embargo): would have been skipped anyway (no embargo URL configured)
- Step 2 (version impact analysis / lock file inspection): **not run**
- Steps 3–8 (Affects Versions correction, duplicates, lifecycle, already-fixed, concurrent
  triage, release Jira, remediation): **not run**
- No Jira mutations proposed or performed. The `ai-cve-triaged` label is **not** added.
