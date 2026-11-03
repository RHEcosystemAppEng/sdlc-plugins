# Step 1 – Data Extraction: TC-8001

Mode: interactive (`FULLSEND_OUTPUT_DIR` not set). Jira was not called. Data comes from the mock issue in `vuln-issue-standard.md`.

## Step 0 – Configuration (from claude-md-security-config-embargo.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | https://example.com/security/embargo-policy (configured, so Step 1.7 runs) |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec contact / account ID | not configured (no @mentions) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). There is no Deployment Context column, so the context defaults to `upstream` |

## Step 0.3 – Matrix Staleness Check

> Security matrix `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` was last updated on **2026-06-28**, which is **128 days ago** (today is 2026-11-03). The 14-day threshold is exceeded, so the matrix may not reflect recent releases.
>
> Options: 1. Refresh now · 2. Proceed anyway · 3. Stop

For this eval the analysis goes ahead with the current matrix (option 2, simulated). Any 2.2.x or 2.1.x release made after 2026-06-28 is not covered.

## Step 0.8 – Assign / Transition (proposed, not executed)

- Assign TC-8001 to the current user (currently Unassigned).
- Move TC-8001 from New to Assigned. The transition ID would be found with `get_transitions`.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New | Issue (full triage path) |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field (does not match the suffix; see Step 3) |
| Vulnerable library | quinn-proto (Rust crate) | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Vulnerability type | Denial of service (panic from an unbounded number of streams in a STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-03) | `duedate` |
| Existing comments | None | Comment history |
| Assignee | Unassigned | Issue |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

- The suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x. Case A (cross-stream impact) applies if other streams are affected.

## Ecosystem Detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings.
- Category: **source dependency**. That means two tasks per affected stream: an upstream backport or dependency bump, plus a downstream propagation task.
- Lock file: `Cargo.lock` in repository `backend` (rhtpa-backend). Check command: `git show <tag>:Cargo.lock`.

## Deployment Context

- `org/rhtpa-server` maps to the rhtpa-backend (`backend`) repository.
- The Source Repositories table has no Deployment Context column. The context therefore defaults to `upstream` (Step 0 backward compatibility). Under `remediation-templates.md`, the Coordination Guidance subsection is left out of task descriptions when the column is absent.

## Step 1.5 – External CVE Data Enrichment

The MITRE (`cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev (`api.osv.dev/v1/vulns/CVE-2026-31812`) lookups were **not performed**, because this eval allows no external calls.

> External CVE databases unavailable: using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 affected, fixed in 0.11.14** (from the Jira description). The severity is CVSS 7.5 (High), from the description.
