# TC-8001 Triage — Step 0 / Step 1 Data Extraction

_Simulated run: no Jira MCP, git, or external calls were made. All values come from the
provided eval input files (vuln-issue-standard.md, security-matrix-mock.md,
claude-md-security-config.md)._

## Step 0.6 – Mode

`FULLSEND_OUTPUT_DIR` not set → **interactive mode** (Step 0.7 skipped).

## Step 0 – Configuration Validation

| Section | Status | Values |
|---|---|---|
| Repository Registry | Present | rhtpa-backend (serena_backend) |
| Jira Configuration | Present | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<serena-instance>__<tool>` |
| Security Configuration → Product Lifecycle | Present | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| VEX Justification custom field (optional) | Configured | `customfield_12345` |
| Upstream Affected Component / PS Component / Stream fields (optional) | Not configured | Step 4.3 and Step 7 skipped |
| ProdSec contact / Jira account ID (optional) | Not configured | @mentions skipped silently |
| Embargo policy URL (optional) | Not configured | Step 1.7 skipped |
| Version Streams | Present | 2.1.x → `git.example.com/rhtpa/rhtpa-release.0.3.z`; 2.2.x → `git.example.com/rhtpa/rhtpa-release.0.4.z` |
| Source Repositories | Present | 1 entry (see below) |

### Source Repositories mapping — Deployment Context

The Source Repositories table has columns `Repository | URL | Local Path`. **The
Deployment Context column is absent.** Per Step 0 backward-compatibility rule, all
repositories default to `upstream`:

| Repository | URL | Deployment Context |
|---|---|---|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | `upstream` (defaulted — column absent) |

Because the column is absent, Step 8 omits the `### Coordination Guidance` subsection from
all remediation task descriptions (remediation-templates.md, Coordination Guidance:
"When the Deployment Context column is absent ... omit the coordination guidance
entirely"). Triage otherwise proceeds normally; the missing column is not an error.

## Step 0.3 – Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-23) | Result |
|---|---|---|---|
| 2.1.x / 2.2.x (shared mock file) | 2026-06-28T10:00:00Z | 148 days | **Stale (> 14 days)** — would prompt engineer: Refresh now / Proceed anyway / Stop. Simulated choice: **Proceed anyway** (eval data is the matrix of record). |

## Step 0.8 – Assign and Transition

Issue status is `New`, Unassigned → would assign to current user and transition to
`Assigned` (dynamic transition discovery). Not executed (simulation).

## Step 1 – Parsed CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Affected repository | rhtpa-backend (Cargo `backend` repo in Ecosystem Mappings) | Component → backend source repo |
| Deployment context | `upstream` (default — no Deployment Context column) | Source Repositories mapping |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (scoped) | Suffix `rhtpa-2.2` → Version Stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (source dependency → 2 tasks per stream) | Rust crate; Cargo row in Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High) | Description |
| Vulnerability | DoS — panic on excessive stream count in STREAMS frame | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote link / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote link |
| Due date | 2026-07-15 | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Step 1.5 – External Enrichment

MITRE and OSV.dev not queried (eval forbids external calls) → treated as unavailable:

> "External CVE databases unavailable — using Jira description data only. Fix threshold
> confidence is reduced."

Fix threshold used: **quinn-proto < 0.11.14**.

## Step 1.7 – Embargo Check

CVSS 7.5 meets threshold, but no Embargo policy URL is configured → step skipped silently.

## Step 2 – Version Impact Analysis (simulated `git show <tag>:Cargo.lock`)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |
| dev stream | — | branch HEAD | not determined | — | Requires Jira unreleased-version discovery (Step 2.2) — not available in simulation |

Dependency chain (Step 2.3.5): manifest data not provided in the eval inputs; direct vs
transitive classification not determinable — remediation tasks include both approaches.
Profile: assumed production runtime (QUIC transport), no dev-dependency evidence.

Upstream fix status (Step 2.5): upstream branch HEAD lock files not provided.

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | release/0.3.z | not verified (all released tags 0.11.9) | Not confirmed → upstream backport |
| 2.2.x | Cargo | release/0.4.z | not verified (tags v0.4.11, v0.4.12 already ship 0.11.14) | Fix present on branch per released tags → dependency-bump variant |

## Step 3 – Affects Versions Correction

PSIRT value `RHTPA 2.0.0` is wrong (no 2.0.x stream; 2.0.0 not in matrix). Issue is
scoped to 2.2.x → proposed Affects Versions: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
(IDs via dynamic version discovery). Requires engineer confirmation.

## Steps 4–7

- Step 4: sibling JQL for `CVE-2026-31812` not executable in simulation; assume no 2.1.x
  sibling CVE Jira exists → 2.1.x handled via preemptive tasks (Case A).
- Step 4.3 / Step 7: skipped (Upstream Affected Component field not configured).
- Step 5: lifecycle page not fetched; 2.1.x and 2.2.x assumed in support.
- Step 6: no resolved siblings known → not already fixed.
- Step 7.5: release Jira (e.g., `RHTPA 2.2.5 CVE triage`) would be found/created with
  individual confirmation; keys unknown in simulation.

## Outcome

Case A (scoped issue, 2.1.x also affected) + Case B (2.2.x affected). See remediation.md.
