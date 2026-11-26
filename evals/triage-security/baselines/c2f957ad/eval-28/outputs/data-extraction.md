# TC-8060 — Step 1: Data Extraction

Simulated triage. No Jira MCP, `git show`, WebFetch, or other external calls were made. All data comes from the eval fixtures:
- `evals/triage-security/files/vuln-issue-transitive.md` (Jira issue mock)
- `evals/triage-security/files/security-matrix-mock.md` (supportability matrix mock)
- `evals/triage-security/files/claude-md-security-config.md` (project CLAUDE.md mock)

## Pre-flight (Steps 0 – 0.8)

| Step | Result |
|------|--------|
| 0.6 Fullsend mode detection | Interactive mode (`FULLSEND_OUTPUT_DIR` not set). Steps 0.7 and the Fullsend serialization rules do not apply. |
| 0 Configuration validation | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present. |
| 0 Extracted config | Jira version prefix `RHTPA`; Vulnerability issue type ID `10024`; component label pattern `pscomponent:`; Product pages URL `https://access.example.com/product-life-cycle/rhtpa`; VEX Justification field `customfield_12345`. Not configured: Upstream Affected Component field, PS Component field, Stream field, ProdSec email or account ID, Embargo policy URL. |
| 0.3 Matrix staleness | WARNING. The matrix `Last-Updated` is `2026-06-28T10:00:00Z`, which is **151 days** before today (2026-11-26) and over the 14-day threshold. In a live run the engineer would choose Refresh / Proceed / Stop. For this eval: **Proceed anyway** with the current matrix. |
| 0.5 Jira access | Not exercised (simulated). |
| 0.8 Assign + transition | Proposed only: assign TC-8060 to the current user and transition New → Assigned. Not executed. |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Jira issue key | TC-8060 | Issue key |
| CVE ID | CVE-2026-99010 | Label `CVE-2026-99010` and the summary |
| Summary | CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2] | Summary |
| Status | New | Status field (full triage path) |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary bracket suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate) | Description |
| Affected version range | `< 0.4.5` ("versions before 0.4.5") | Description |
| Fixed version | 0.4.5 | Description |
| Severity / CVSS | 7.5 (High) | Description |
| Vulnerability type | Denial of service: memory exhaustion from unbounded CONTINUATION frames per HEADERS frame | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | _(none; no GHSA link present)_ | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 | Remote links |
| Due date | 2026-08-15 | `duedate` field |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) | Reporter field (used for the mandatory @mention in the post-triage summary) |
| Assignee | Unassigned | Assignee field |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed. No engineer input is needed.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`, local `/home/dev/repos/rhtpa-release.0.4.z`) |
| Scope | **Scoped**: Steps 3, 4, and 8 apply only to the 2.2.x stream. Other streams are checked only for cross-stream impact (Case A). |

## Ecosystem Detection

| Item | Value |
|------|-------|
| Ecosystem | **Cargo** (h2 is a Rust crate; listed in the 2.2.x Ecosystem Mappings) |
| Category | Source dependency: 2 remediation tasks per affected stream |
| Repository | backend (`rhtpa-backend`, https://github.com/rhtpa/rhtpa-backend) |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock` |
| Upstream branch (2.2.x) | `release/0.4.z` |

## Deployment Context

The Source Repositories table has no Deployment Context column (older format). `rhtpa-backend` therefore defaults to `upstream`. Because the column is absent, the remediation templates say to **omit** the Coordination Guidance subsection from task descriptions.

## Step 1.5 – External CVE Data Enrichment

The MITRE CVE API and OSV.dev were **not queried**, because the eval forbids external calls. They are treated as unavailable:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **h2 < 0.4.5 is affected; 0.4.5 is fixed** (from the Jira description).

## Step 1.7 – Embargo Check

Skipped. No Embargo policy URL is configured in Security Configuration, even though the CVSS of 7.5 would otherwise trigger the gate.
