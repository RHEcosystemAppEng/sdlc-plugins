# TC-8020 — Data Extraction (Steps 0 – 1.7)

## Step 0 – Configuration validation

Source: `claude-md-security-config.md` (project CLAUDE.md)

| Check | Result |
|---|---|
| Repository Registry | Present (rhtpa-backend, serena_backend) |
| Jira Configuration | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present (`mcp__<instance>__<tool>`) |
| Security Configuration → Product Lifecycle | Present |
| Security Configuration → Version Streams | 2 streams (2.1.x, 2.2.x) |
| Security Configuration → Source Repositories | 1 repo (rhtpa-backend) |

Extracted values:

| Setting | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | Not configured. Step 4.3 (cross-CVE overlap), Step 7 (concurrent triage) and Step 7.5.3 (cross-CVE dedup) are skipped |
| PS Component / Stream custom fields | Not configured in Security Configuration (the values are on the issue, but the skill does not use them) |
| ProdSec contact / Jira account ID | Not configured, so no ProdSec @mentions |
| Embargo policy URL | Not configured. Step 1.7 is skipped |
| Deployment Context column | Absent. rhtpa-backend defaults to `upstream`. Coordination Guidance is omitted from tasks, as the backward-compatibility rule requires |

Version Streams:

| Stream | Konflux Release Repo | Local Path |
|---|---|---|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Step 0.3 – Matrix staleness check

| Stream | Last-Updated | Age (as of 2026-11-20) | Status |
|---|---|---|---|
| 2.1.x / 2.2.x (shared mock file) | 2026-06-28T10:00:00Z | 145 days | **STALE** (threshold is 14 days) |

> The security matrix was last updated on 2026-06-28, 145 days ago. It may not list recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval assumption: **Proceed anyway** with the current matrix. The cross-stream impact data supplied for this task is used as the analysis input.

## Step 0.6 / 0.7 – Mode

`FULLSEND_OUTPUT_DIR` is not set, so the run is in **interactive mode**. Under the eval rules, no Jira or Git calls are made and all proposed mutations are written to files.

## Step 0.8 – Assign and transition (proposed, not executed)

- `jira.edit_issue(TC-8020, assignee=<current-user-account-id>)`
- Status is **New**, so the proposal is to transition to **Assigned** using the transition discovered at runtime with `get_transitions`.

## Step 1 – Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| Issue type / Status | Vulnerability / New |
| CVE ID | **CVE-2026-55123** (label and summary agree) |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | **tokio** (Rust crate) |
| Affected version range | **< 1.42.0** ("versions before 1.42.0") |
| Fixed version | **1.42.0** |
| CVSS | 8.1 (High) |
| Vulnerability | Use-after-free when a spawned task is aborted while it holds a borrowed reference. This can cause memory corruption and possibly code execution |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| Other advisory | https://rustsec.org/advisories/RUSTSEC-2026-0088.html |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 (**already past** as of 2026-11-20) |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.2 |
| Existing links | None |
| Existing comments | None |
| Assignee | Unassigned |

All critical fields (CVE ID, library, affected range) were parsed, so triage can continue.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `rhtpa-release.0.4.z`). It matches a configured Version Stream.
- **Issue stream scope: 2.2.x (scoped issue).** Steps 3 and 4 are scoped to 2.2.x, and Case A (cross-stream) applies to any other affected stream.

### Ecosystem detection

- tokio is a Rust crate, so the ecosystem is **Cargo**. Both streams list Cargo in Ecosystem Mappings: repository `backend`, lock file `Cargo.lock`.
- Classification: **Source dependency**, so each affected stream gets **2 remediation tasks** (upstream backport or dependency bump, plus downstream propagation).

### Deployment context

- Affected repository: rhtpa-backend (`backend` in Ecosystem Mappings). The Source Repositories table has no Deployment Context column, so the context defaults to `upstream` and Coordination Guidance is omitted.

## Step 1.5 – External CVE data enrichment

Not executed: external calls are forbidden in this eval. This is handled like the "both APIs unavailable" case:

> ⚠ External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **tokio < 1.42.0, fixed in 1.42.0** (Jira description, consistent with the provided cross-stream analysis).

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 8.1 would otherwise trigger the gate.
