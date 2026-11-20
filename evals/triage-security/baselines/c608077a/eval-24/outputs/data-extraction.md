# TC-8001 — Triage Data Extraction (Step 0 – Step 2)

> Eval mode: no Jira MCP, `git show`, WebFetch or other external calls were made.
> Issue data comes from `vuln-issue-standard.md`, configuration from
> `claude-md-security-config.md`, and lock file data from the "Mock Lock File Data"
> section of `security-matrix-mock.md` (stands in for `git show <tag>:Cargo.lock`).

## Step 0 – Configuration Validation

| Section | Status | Values extracted |
|---|---|---|
| Repository Registry | Present | rhtpa-backend (Rust backend service, serena_backend) |
| Jira Configuration | Present | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<instance>__<tool>`; serena_backend |
| Security Config – Product Lifecycle | Present | Product pages `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type `10024`, Component label pattern `pscomponent:`, VEX Justification field `customfield_12345` |
| Security Config – Version Streams | Present | 2.1.x → `rhtpa-release.0.3.z`; 2.2.x → `rhtpa-release.0.4.z` |
| Security Config – Source Repositories | Present (**no Deployment Context column**) | rhtpa-backend → `https://github.com/rhtpa/rhtpa-backend` |

Optional fields not configured (dependent behavior skipped): Upstream Affected
Component field (Step 4.3 cross-CVE overlap and Step 7 concurrent triage skipped),
PS Component field, Stream field, ProdSec contact email, ProdSec Jira account ID (no
@mentions in correction comments), Embargo policy URL (Step 1.7 skipped).

### Source Repositories mapping (backward compatibility)

The Source Repositories table has only the `Repository | URL | Local Path` columns,
with no `Deployment Context` column. Per Step 0 (constraint §1.78), every repository
**defaults to `upstream`**:

| Repository | URL | Deployment Context |
|---|---|---|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | `upstream` (defaulted, column absent) |

## Step 0.3 – Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-20) | Result |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | 145 days | **STALE** (> 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 145 days | **STALE** (> 14 days) |

Warning shown to the engineer: the matrix may be missing releases after 2.2.4 /
2.1.1. Options are Refresh now, Proceed anyway, or Stop. For this eval run:
**Proceed anyway**. Both streams share one mock file, so they share one timestamp.

## Step 0.6 / 0.7 – Mode

`FULLSEND_OUTPUT_DIR` is not set, so this is **interactive mode**. Step 0.7 is skipped.

## Step 0.8 – Assign and Transition (proposed, not executed)

- Assign TC-8001 to the current user.
- Transition New → Assigned, using a transition ID found at runtime.

## Step 1 – Parsed CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| Status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High), DoS | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-20) | `duedate` |
| Existing comments | None | Comment history |
| Ecosystem | Cargo (Rust crate), listed in both streams' Ecosystem Mappings | Library and Ecosystem Mappings |
| Ecosystem category | Source dependency, so 2 remediation tasks per stream | Classification table |
| Affected source repository | backend / rhtpa-backend | Ecosystem Mappings `Repository` column |
| Deployment context | `upstream` (defaulted, Deployment Context column absent) | Step 0 mapping |

All critical fields (CVE ID, library, affected range) were parsed successfully.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which is in the Version Streams table.
- **Issue stream scope: 2.2.x (scoped).** Steps 3, 4 and 8 apply to 2.2.x. Other
  streams that are affected fall under Case A (cross-stream impact).

### Affects Versions mismatch (flagged for Step 3)

PSIRT set **RHTPA 2.0.0**. No 2.0.x stream is configured, and the issue is scoped to
2.2.x, so this value is wrong. Step 3 corrects it.

## Step 1.5 – External CVE Data Enrichment

The MITRE and OSV.dev queries were not run in this eval because external calls are
not allowed. Both sources are treated as unavailable:

> External CVE databases unavailable. Using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed**.

## Step 1.7 – Embargo Check

No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.5 would
otherwise meet the threshold.

## Step 2 – Version Impact Analysis

### 2.2 Development stream

No unreleased Jira versions could be retrieved because there was no Jira access. No
development stream (branch HEAD) row is included. 2.2.x is the latest stream per its
forward pointer.

### 2.4 Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Build | Pinned tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | outside issue scope |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | outside issue scope |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | |

### 2.3.5 Dependency chain

Manifest (`Cargo.toml`) data is not in the mock, so the dependency type (direct or
transitive) and full chain could not be traced. quinn-proto usually comes in
transitively through `quinn`, for example `backend → (reqwest http3 / quinn) → quinn →
quinn-proto`. **This needs checking before implementation.** The remediation tasks
include both the direct and transitive approaches. Profile is assumed to be production
(QUIC transport is a runtime dependency), so the `dev-dependency` label does not apply.

### 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | `release/0.3.z` | not verified; latest tag `v0.3.12` = 0.11.9 | **NO** (assumed) |
| 2.2.x | Cargo | `release/0.4.z` | ≥ 0.11.14 (tags `v0.4.11` and `v0.4.12` ship 0.11.14) | **YES** |

### Summary of impact

- **In scope (2.2.x):** 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and 2.2.4 are
  already fixed: the current Konflux pin `v0.4.12` ships quinn-proto 0.11.14.
- **Cross-stream (2.1.x):** 2.1.0 and 2.1.1 are affected. No upstream fix is on
  `release/0.3.z`. This is Case A.

## Step 3 – Affects Versions Correction (proposed)

| Current | Proposed |
|---|---|
| RHTPA 2.0.0 | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

Version IDs must be found at runtime with `getJiraIssueTypeMetaWithFields`. 2.1.x
versions are left out because the issue is scoped to 2.2.x. They go in the
cross-stream comment instead. A correction comment with the Comment Footnote will be
posted. There is no ProdSec @mention because no ProdSec account ID is configured.

## Steps 4–7 (eval limitations)

- **Step 4 (siblings/duplicates):** The JQL search for `labels = CVE-2026-31812` was
  not run. Assumption: no sibling issue for stream 2.1.x exists. 4.3 is skipped because
  Upstream Affected Component is not configured. 4.4 found no preemptive tasks to
  reconcile (assumed).
- **Step 5 (lifecycle):** Product pages were not queried. 2.1.x and 2.2.x are assumed
  to be supported. **This must be verified before creating the 2.1.x tasks.**
- **Step 6 (already fixed):** No resolved siblings are known. Within 2.2.x the fix
  already shipped in 2.2.3 (`v0.4.11`).
- **Step 7 (concurrent triage):** Skipped because Upstream Affected Component is not
  configured.
- **Step 7.5 (release Jira):** The default target release for 2.1.x is **RHTPA 2.1.2**,
  the next patch after 2.1.1. Find or create the "RHTPA 2.1.2 Release Tasks" Epic and
  the "RHTPA 2.1.2 CVE triage" Task. Each needs separate confirmation. Preemptive tasks
  are not linked to release Jira.
