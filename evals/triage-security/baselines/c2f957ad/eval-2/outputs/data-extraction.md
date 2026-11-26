# Data Extraction — TC-8002

Skill: `sdlc-workflow/triage-security` (interactive mode; `FULLSEND_OUTPUT_DIR` absent).
Eval mode: no Jira MCP, `git show`, WebFetch, or other external calls were made. All data
comes from the provided mock input files.

## Step 0 — Configuration Validation

Source: `claude-md-security-config.md`

| Required section | Present | Values |
|---|---|---|
| Repository Registry | Yes | rhtpa-backend (serena_backend) |
| Jira Configuration | Yes | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Yes | `mcp__<serena-instance>__<tool>` convention, instance `serena_backend` |
| Security Configuration / Product Lifecycle | Yes | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| Security Configuration / Version Streams | Yes | `2.1.x` -> rhtpa-release.0.3.z; `2.2.x` -> rhtpa-release.0.4.z |
| Security Configuration / Source Repositories | Yes | rhtpa-backend -> https://github.com/rhtpa/rhtpa-backend |

Optional fields:

| Field | Value |
|---|---|
| VEX Justification custom field | `customfield_12345` (configured) |
| Upstream Affected Component custom field | Not configured -> Steps 4.3, 7 and 7.5.3 are skipped |
| PS Component / Stream custom fields | Not configured |
| ProdSec contact email / Jira account ID | Not configured -> no ProdSec @mentions |
| Embargo policy URL | Not configured -> Step 1.7 skipped |
| Deployment Context column (Source Repositories) | Absent -> defaults to `upstream` |

Result: configuration is valid; proceed.

## Step 0.3 — Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-26) | Status |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | ~151 days | STALE (> 14-day threshold) |
| 2.2.x | 2026-06-28T10:00:00Z | ~151 days | STALE (> 14-day threshold) |

Warning that would be shown to the engineer:

> Security matrix for stream **2.2.x** (and **2.1.x**) was last updated on 2026-06-28
> (151 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval assumption: **Proceed anyway** (the mock matrix is the only data available; refresh
would require `git` access to the Konflux release repos). Releases after 2.2.4 (2026-05-04),
if any, are not covered by this analysis.

## Step 0.8 — Assign and Transition (proposed, not executed)

- Issue status is `New`, assignee is `Unassigned`.
- Proposed: assign TC-8002 to the current user and transition to `Assigned`.

## Step 1 — Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8002 |
| Issue type | Vulnerability |
| Status | New |
| CVE ID | CVE-2026-28940 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | `< 1.0.135` ("versions before 1.0.135") |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | None in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0019.html |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 (already past as of 2026-11-26) |
| Existing comments | None |
| Reporter | Not present in mock data. The post-triage summary needs the reporter's account ID for the required @mention, so it would come from the live `jira.get_issue` response |

All critical fields (CVE ID, library, affected range) were parsed successfully.

### Stream scope resolution

- Summary suffix `[rhtpa-2.2]` -> stream **2.2.x**, which matches a configured Version Stream
  (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue is **scoped** to stream 2.2.x.

### Ecosystem detection

- `serde_json` is a Rust crate, so the ecosystem is **Cargo**.
- Cargo appears in both streams' Ecosystem Mappings (repository `backend`, lock file
  `Cargo.lock`, check command `git show <tag>:Cargo.lock`).
- Category: source dependency.

### Deployment context

- Component `org/rhtpa-server` maps to the backend repository (`rhtpa-backend`).
- The Source Repositories table has no Deployment Context column, so it defaults to `upstream`.

## Step 1.5 — External CVE Data Enrichment

- The MITRE CVE API and OSV.dev were **not queried** because external calls are prohibited in this eval.
- Treated as "both external APIs unavailable":

  > External CVE databases unavailable. Using Jira description data only.
  > Fix threshold confidence is reduced.

- Fix threshold used for Step 2: **serde_json < 1.0.135 is vulnerable; 1.0.135 is fixed**
  (from the Jira description, consistent with the GHSA and RUSTSEC references listed).

## Step 1.7 — Embargo Check

Skipped. No Embargo policy URL is configured, and CVSS 5.3 (Medium) is below the 7.0 threshold anyway.
