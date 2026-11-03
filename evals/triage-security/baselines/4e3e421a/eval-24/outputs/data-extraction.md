# TC-8001 — Triage Data Extraction (Step 0 to Step 2)

Mode: interactive (`FULLSEND_OUTPUT_DIR` not set). Eval run, so no Jira, git, or WebFetch calls were made. All values below come from the provided mock files.

## Step 0 — Configuration Validation

| Section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present | rhtpa-backend |
| Jira Configuration | Present | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | serena_backend (rhtpa-backend) |
| Security Configuration / Product Lifecycle | Present | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:`, VEX Justification field `customfield_12345` |
| Security Configuration / Version Streams | Present | 2.1.x → `git.example.com/rhtpa/rhtpa-release.0.3.z`; 2.2.x → `git.example.com/rhtpa/rhtpa-release.0.4.z` |
| Security Configuration / Source Repositories | Present | rhtpa-backend → `https://github.com/rhtpa/rhtpa-backend` |

Optional fields that are not configured: Upstream Affected Component field (so Steps 4.3 and 7 are skipped), PS Component field, Stream field, ProdSec contact email, ProdSec Jira account ID (no @mentions), Embargo policy URL (so Step 1.7 is skipped).

**Deployment context:** the Source Repositories table has **no Deployment Context column**. For backward compatibility every repo defaults to `upstream`, so rhtpa-backend is `upstream`. Because the column is missing, remediation tasks **leave out the Coordination Guidance subsection** (remediation-templates.md, "Coordination Guidance").

## Step 0.3 — Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-03) | Result |
|---|---|---|---|
| 2.1.x | 2026-06-28T10:00:00Z | 128 days | STALE (threshold 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 128 days | STALE (threshold 14 days) |

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (128 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval decision: **Proceed anyway** with the current matrix. Any release after 2026-06-28 is not covered by this analysis.

## Step 1 — Parsed CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| Issue status | New (full triage path) | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` → rhtpa-server image (backend source: rhtpa-backend) | Label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (Rust crate), a source dependency (2 tasks per stream) | Library and Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High), DoS (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links and description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Assignee | Unassigned. Step 0.8 would assign it to the current user and transition New → Assigned (not executed in eval) | Issue |
| Existing comments | None | Issue |
| Deployment context | `upstream` (default, because the Deployment Context column is absent) | Source Repositories |

**Stream scope:** `[rhtpa-2.2]` matches configured stream `2.2.x`, so the issue is **scoped to 2.2.x**.

## Step 1.5 — External CVE Enrichment

MITRE and OSV were not queried (eval constraint: no external tools). Fallback rule:

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold in use: quinn-proto **< 0.11.14**, fixed in **0.11.14**.

## Step 1.7 — Embargo Check

CVSS 7.5 is at or above the 7.0 threshold, but no Embargo policy URL is configured, so this step is skipped.

## Step 2 — Version Impact Analysis

Simulated `git show <tag>:Cargo.lock` output comes from the mock lock file data. Development stream: no unreleased Jira version data is available and no stream beyond 2.2.x is configured, so no development stream was detected.

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag of 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fix shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fix shipped |

Dependency chain (Step 2.3.5): quinn-proto is in `Cargo.lock` of rhtpa-backend (workspace). Direct vs transitive status and profile **were not determined**, because no `Cargo.toml` or `cargo tree` evidence was provided. quinn-proto usually arrives transitively through `quinn`, so the remediation tasks cover both approaches. Nothing suggests it is dev-only, so it is treated as a production dependency.

### Step 2.5 — Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | release/0.3.z | not available (no branch HEAD data; last tag v0.3.12 = 0.11.9) | NO (assumed, must be verified) |
| 2.2.x | Cargo | release/0.4.z | not read directly; tags v0.4.11 and v0.4.12 on this branch already ship 0.11.14 | YES (from tag evidence) |

## Step 3 — Affects Versions Correction (proposed, not executed)

| | Value |
|---|---|
| Current | RHTPA 2.0.0 |
| Proposed (scoped to 2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Rationale | RHTPA 2.0.0 is not a supported stream in the matrix. Lock file evidence shows 2.2.0 through 2.2.2 ship quinn-proto 0.11.9 or 0.11.12 (< 0.11.14). 2.2.3 and 2.2.4 ship 0.11.14 and are not affected. |

Jira version IDs would come from `getJiraIssueTypeMetaWithFields`. No IDs are hardcoded.

## Steps 4 to 7 — Summary

- **Step 4 (siblings/duplicates):** the JQL for other `CVE-2026-31812` issues was not run (eval). This analysis assumes no sibling issue exists for stream 2.1.x, so preemptive tasks are planned for 2.1.x. Step 4.3 is skipped because the Upstream Affected Component field is not configured.
- **Step 5 (lifecycle):** the product pages were not fetched. 2.1.x and 2.2.x are assumed in support because both appear in the configured Version Streams. This needs verification.
- **Step 6 (already fixed):** no resolved sibling issues are known. For 2.2.x, releases 2.2.3 and later already ship the fix.
- **Step 7 (concurrent triage):** skipped because the Upstream Affected Component field is not configured.
- **Step 7.5 (release Jira):** would find or create "RHTPA 2.2.x Release Tasks" and "RHTPA <version> CVE triage" for each affected stream. Not executed in eval.

## Step 8 — Outcome

**Case A + Case B.** The issue is scoped to 2.2.x, and 2.2.x is affected (Case B: 2 tasks). Stream 2.1.x, outside the scope, is also affected (Case A: post a cross-stream comment and create 2 preemptive tasks). See `remediation.md`.
