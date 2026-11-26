# Step 1 – Data Extraction: TC-8004

Mode: interactive (Step 0.6 — `FULLSEND_OUTPUT_DIR` absent). Eval run: no Jira MCP,
`git show`, or WebFetch calls were made; all data comes from the provided mock files.

## Step 0 – Configuration validation

| Section | Status | Values used |
|---|---|---|
| Repository Registry | Present | rhtpa-backend (serena_backend) |
| Jira Configuration | Present | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<serena-instance>__<tool>` |
| Security Configuration → Product Lifecycle | Present | Product pages `https://access.example.com/product-life-cycle/rhtpa`, version prefix `RHTPA`, Vulnerability issue type `10024`, component label pattern `pscomponent:`, VEX field `customfield_12345` |
| Security Configuration → Version Streams | Present | 2.1.x → `rhtpa-release.0.3.z`; 2.2.x → `rhtpa-release.0.4.z` |
| Security Configuration → Source Repositories | Present | rhtpa-backend → `https://github.com/rhtpa/rhtpa-backend` |

Optional fields that are **not configured** (and what that skips):

- Upstream Affected Component custom field → Step 4.3 (cross-CVE overlap), Step 7 (concurrent triage) and Step 7.5.3 (cross-CVE dedup) are skipped.
- PS Component / Stream custom fields → not used.
- ProdSec contact email / Jira account ID → no ProdSec @mention in comments.
- Embargo policy URL → Step 1.7 is skipped, even though CVSS is 7.5.
- Deployment Context column (Source Repositories) → defaults to `upstream` for metadata. Per `remediation-templates.md`, Coordination Guidance is **left out** of task descriptions because the column is absent.

## Step 0.3 – Matrix staleness check

| Stream | Last-Updated | Age (as of 2026-11-26) | Result |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | 151 days | **STALE** (threshold 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 151 days | **STALE** (threshold 14 days) |

> Security matrix for stream **2.1.x** / **2.2.x** was last updated on 2026-06-28
> (151 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval decision: **Proceed anyway** using the provided mock matrix. Releases after
2026-06-28 (for example a 2.1.2 or 2.2.5) would not appear in this analysis.

## Step 0.8 – Assign and transition (proposed, not executed)

- Assign TC-8004 to the current user (`jira.user_info()` → account ID).
- Issue status is **New** → transition to **Assigned** (transition discovered through `jira.get_transitions`).

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8004 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-33501 | Label + summary |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames | Issue |
| Affected component | `pscomponent:org/rhtpa-server` → repository rhtpa-backend (Cargo `backend` in matrix) | Label |
| Product version (PSIRT-claimed, summary suffix) | **None — no bracketed suffix** | Summary |
| Affects Versions (Jira field, current) | RHTPA 2.1.0, RHTPA 2.2.0 | `versions` |
| Vulnerable library | h2 (Rust crate) | Description |
| Affected version range | `< 0.4.8` ("versions before 0.4.8") | Description |
| Fixed version | 0.4.8 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 (also RUSTSEC-2026-0055) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 | Remote links |
| Due date | 2026-08-01 (**already past** as of 2026-11-26) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue |
| Note | Distinct from CVE-2024-2758 (httpd CONTINUATION flood) | Description |

All critical fields (CVE ID, library, affected range) were parsed, so triage continues.

## Stream scope resolution

- Summary has **no stream suffix** → the issue is **UNSCOPED**. It covers all configured streams (2.1.x and 2.2.x).
- Consequences:
  - Step 3 Affects Versions correction covers all affected versions across all streams.
  - Step 8 Case A (cross-stream proactive or preemptive remediation) does **not** apply.
  - Case B creates standard (non-preemptive) remediation tasks for **each affected stream**, linked with "Depend" to TC-8004.

## Ecosystem detection

- Library `h2` is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (`Cargo.lock`, `git show <tag>:Cargo.lock`).
- Category: **Source dependency**, so each affected stream gets 2 remediation tasks (upstream backport or dependency bump, plus downstream propagation).

## Deployment context

- rhtpa-backend has no Deployment Context column, so it defaults to `upstream`. Coordination Guidance is left out of task descriptions (backward-compatibility rule).

## Step 1.5 – External CVE data enrichment

| Source | Affected range | Fixed version | Status |
|---|---|---|---|
| Jira description | < 0.4.8 | 0.4.8 | Parsed |
| MITRE CVE API | — | — | Not queried (eval: no external calls) |
| OSV.dev | — | — | Not queried (eval: no external calls) |

> External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

**Fix threshold used for Step 2:** h2 `< 0.4.8` is affected; `>= 0.4.8` is fixed.

## Step 1.7 – Embargo check

Skipped: no Embargo policy URL is configured. CVSS 7.5 would otherwise meet the threshold.
