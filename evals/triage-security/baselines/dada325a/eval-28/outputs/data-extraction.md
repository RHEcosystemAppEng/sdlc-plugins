# Step 1 – Data Extraction: TC-8060

_Source: fixture `vuln-issue-transitive.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`). No Jira calls were made._

## Step 0 – Configuration Validation (from `claude-md-security-config.md`)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 cross-CVE overlap and Step 7 concurrent-triage detection are skipped) |
| Embargo policy URL | not configured (Step 1.7 is skipped) |
| ProdSec contact / account ID | not configured (no @mentions of ProdSec) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). No Deployment Context column, so it defaults to `upstream` |

Result: all required sections are present, so the skill can proceed.

## Step 0.3 – Matrix Staleness Check

| Stream | Last-Updated | Age (as of 2026-11-06) | Status |
|--------|--------------|------------------------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 131 days | STALE (over the 14-day threshold) |
| 2.2.x | 2026-06-28T10:00:00Z | 131 days | STALE (over the 14-day threshold) |

> Warning: The security matrix for streams 2.1.x and 2.2.x was last updated on 2026-06-28 (131 days ago), so it may not list recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval decision: **Proceed anyway** with the current matrix. No refresh is possible in this environment.

## Step 0.6 – Mode

`FULLSEND_OUTPUT_DIR` is absent, so this run uses interactive mode. All Jira mutations below are written as proposals and none are executed.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8060 | Issue |
| Issue status | New (so full triage runs) | Issue status |
| CVE ID | CVE-2026-99010 | Label `CVE-2026-99010` and summary |
| Summary | CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2] | Issue summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate) | Description |
| Ecosystem | Cargo (source dependency, so 2 remediation tasks per stream) | Library + Ecosystem Mappings |
| Affected version range | `< 0.4.5` ("versions before 0.4.5") | Description |
| Fixed version | 0.4.5 | Description |
| Severity / CVSS | 7.5 (High) | Description |
| Vulnerability class | Denial of service: unbounded CONTINUATION frames per HEADERS frame cause memory exhaustion | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | none provided (no GHSA link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 | Remote links |
| Due date | 2026-08-15 (**already past** as of 2026-11-06) | `duedate` |
| Assignee | Unassigned | Issue |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) | Issue (used for the mandatory @mention in the post-triage summary) |
| Existing comments | none | Comment history |
| Affected repository | rhtpa-backend (Cargo `backend`) | Ecosystem Mappings Repository column |
| Deployment context | `upstream` (default; column absent, so the Coordination Guidance subsection is omitted) | Source Repositories |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to stream `2.2.x`, which **matches** the configured Version Stream `2.2.x` (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3–8 only act on 2.2.x. Other streams are checked only for Case A cross-stream impact.

## Step 0.8 – Assign and Transition (proposed, not executed)

- `jira.edit_issue(TC-8060, assignee=<current-user>)`
- Issue status is New, so the proposal is to transition to **Assigned**. The transition is discovered dynamically with `get_transitions`.

## Step 1.5 – External CVE Data Enrichment

The MITRE CVE API and OSV.dev were **not queried** because the eval constraint forbids external calls. This is handled the same way as "both external APIs unavailable":

> Warning: External CVE databases unavailable. Using Jira description data only, so confidence in the fix threshold is reduced.

**Fix threshold used for Step 2.3:** h2 `< 0.4.5` (fixed in 0.4.5).

## Step 1.7 – Embargo Check

Skipped because no Embargo policy URL is configured. The CVSS of 7.5 would otherwise meet the threshold.
