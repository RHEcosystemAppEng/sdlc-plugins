# TC-8001 Triage: Data Extraction (Steps 0 to 2)

> Simulated run. No Jira MCP, `git show`, WebFetch or other external calls were made.
> Every value below comes from the provided input files: the mock issue, the mock
> security matrix with its simulated lock-file data, and the mock CLAUDE.md.

## Step 0.6: Mode detection

`FULLSEND_OUTPUT_DIR` is not set, so this is **interactive mode** and the standard workflow runs.

## Step 0: Configuration validation

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | rhtpa-backend (Serena: serena_backend) |
| Jira Configuration | Present | Project key: TC; Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Code Intelligence | Present | `mcp__<instance>__<tool>` naming convention |
| Security Configuration / Product Lifecycle | Present | Product pages URL: https://access.example.com/product-life-cycle/rhtpa; Jira version prefix: RHTPA; Vulnerability issue type ID: 10024; Component label pattern: `pscomponent:`; VEX Justification field: customfield_12345 |
| Security Configuration / Version Streams | Present | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Security Configuration / Source Repositories | Present, with a **Deployment Context** column | rhtpa-backend -> { url: https://github.com/rhtpa/rhtpa-backend, deployment_context: **customer-shipped** } |

These optional fields are not configured, so their steps are skipped:
- Upstream Affected Component field: not configured. Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped.
- PS Component and Stream fields: not configured.
- ProdSec contact email and Jira account ID: not configured, so comments carry no ProdSec @mention.
- Embargo policy URL: not configured, so Step 1.7 is skipped.

**Source Repositories mapping parsed in Step 0:**

| Repository | URL | Deployment Context |
|---|---|---|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | customer-shipped |

## Step 0.3: Matrix staleness check

| Stream | Last-Updated | Age on 2026-11-27 | Result |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | 152 days | **STALE** (threshold is 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 152 days | **STALE** (threshold is 14 days) |

> Warning: the security matrices for streams 2.1.x and 2.2.x were last updated on 2026-06-28,
> 152 days ago. They may not include recent releases. The options are: 1. Refresh now,
> 2. Proceed anyway, 3. Stop.
>
> This simulated run continued with **Proceed anyway**. Releases after 2026-06-28 (for example
> 2.2.5+) are not reflected below. Before applying any Jira changes, the engineer should
> refresh the matrix (setup Step 10.6).

## Step 0.8: Assign and transition (proposed, not executed)

- Proposal: assign TC-8001 to the current user.
- Proposal: transition TC-8001 from **New** to **Assigned**, using a transition discovered dynamically with `get_transitions`.

## Step 1: Parsed CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| Issue status | New, so full triage runs | Issue status |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server`, i.e. image `org/rhtpa-server` | Label matching `pscomponent:` |
| Affected repository | **rhtpa-backend** (Rust backend; Cargo `backend` repo in the Ecosystem Mappings) | Component, Ecosystem Mappings, Source Repositories |
| **Deployment context** | **customer-shipped** | Source Repositories table, Deployment Context column (row `rhtpa-backend`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, i.e. stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 (**incorrect**: no 2.0.x stream is configured or supported) | `versions` field |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| CVSS / severity | 7.5 (High). Impact: DoS (panic on an excessive stream count in a STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Other reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 (**already passed** as of 2026-11-27) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed, so triage does not stop here.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.
- Stream 2.1.x is outside this issue's scope. If it is affected, it is handled as cross-stream impact (Case A).

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Both streams list Cargo in their Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`).
- Category: **source dependency**, so each affected stream gets 2 remediation tasks.

### Deployment context lookup

| Affected repository | Found in Source Repositories? | Deployment Context | Result |
|---|---|---|---|
| rhtpa-backend | Yes | `customer-shipped` | Recorded for Step 8. Each remediation task gets the **customer-shipped** Coordination Guidance (Product Security coordination, CVE assignment, advisory preparation, formal disclosure, and release through a security advisory with explicit CVE-to-component mapping). |

The `upstream` default does not apply, because the repository is explicitly listed with a Deployment Context value.

## Step 1.5: External CVE data enrichment

The task forbids external calls, so MITRE (`cveawg.mitre.org`) and OSV.dev were **not queried**. Both are treated as unavailable.

> Warning: external CVE databases are unavailable, so only the Jira description data is used. Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.** The Jira description and RUSTSEC reference agree on this.

## Step 1.7: Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise have triggered the gate.

## Step 2: Version impact analysis

### 2.1 Matrix load and validation

Both stream matrices loaded. All required sections are present: Supportability Matrix, Ecosystem Mappings, Source Pinning Method, Forward Pointer. The Ecosystem Mappings columns match the template, so validation passes.

### 2.2 Development stream

No Jira version metadata (unreleased versions) is available in this simulated run. The latest configured stream is 2.2.x, which has no forward pointer. Branch HEAD of `release/0.4.z` could not be inspected, so no development-head row is reported.

### 2.3 / 2.4 Version impact table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14), based on simulated `git show <tag>:Cargo.lock` output:

| Stream | Version | Build | backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | **YES** | outside this issue's scope |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | **YES** | outside this issue's scope |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | **YES** | |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | **YES** | |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 | (retag) | **YES** | same as 2.2.1 (backend retag of v0.4.8) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | fixed version shipped |

Summary:
- **2.2.x (in scope):** 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and later already ship quinn-proto 0.11.14.
- **2.1.x (cross-stream):** every supported version (2.1.0, 2.1.1) is affected.

### 2.3.5 Dependency chain

```
Dependency chain for quinn-proto:
  backend (workspace) -> ... -> quinn-proto
  Type: NOT DETERMINED. The simulated data has no Cargo.toml/Cargo.lock dependency
        graph. quinn-proto is usually transitive (through quinn, e.g. via reqwest's
        http3 feature). Confirm with `cargo tree -i quinn-proto` at each pinned tag.
  Profile: assumed production (the component label names a shipped server image);
           not verified.
  Introduction point: present in every listed tag from v0.3.8 onward.
```

### 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Evidence | Fixed? |
|---|---|---|---|---|
| 2.2.x | Cargo | release/0.4.z | Tags v0.4.11 and v0.4.12, cut from this branch line, ship 0.11.14. Branch HEAD was not read. | YES (inferred from released tags; confirm at HEAD) |
| 2.1.x | Cargo | release/0.3.z | The latest tag v0.3.12 ships 0.11.9. Branch HEAD was not read. | NO evidence of a fix, so the **upstream backport** path applies |

## Step 3: Affects Versions correction (proposed, not executed)

The issue is scoped to stream 2.2.x.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

- RHTPA 2.0.0 is wrong: no 2.0.x stream exists, and PSIRT assigned it from scan time rather than lock-file evidence.
- 2.1.0 and 2.1.1 are excluded because they belong to the 2.1.x stream (a sibling or preemptive path).
- Jira version IDs must be discovered at runtime with `getJiraIssueTypeMetaWithFields`. They are not hardcoded here.

## Steps 4 to 7: Summary

- **Step 4:** a sibling JQL search was needed (`labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`) but not run. This run treats it as returning **no 2.1.x sibling**. If one exists, the 2.1.x preemptive tasks in remediation.md should not be created; link it with Related instead. Step 4.3 is skipped (field not configured).
- **Step 5:** lifecycle status needs the Product pages URL and was not checked. All matrix versions are assumed supported.
- **Step 6:** no resolved siblings are known, so there is no already-fixed detection from siblings.
- **Step 7:** skipped (Upstream Affected Component field not configured).
- **Step 7.5:** release Jira orchestration (`RHTPA <version> Release Tasks` Epic / `RHTPA <version> CVE triage` Task) needs Jira and was not run. The remediation tasks list the linking actions as pending.
