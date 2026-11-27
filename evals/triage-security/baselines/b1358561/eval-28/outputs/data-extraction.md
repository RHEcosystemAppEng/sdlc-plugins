# TC-8060 — Step 1: Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval run: Jira and external calls are simulated from the fixture files. Nothing was written to Jira.

## Step 0: Configuration check

Source: `claude-md-security-config.md`

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | `mcp__<serena-instance>__<tool>`, serena_backend | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification custom field | customfield_12345 | Configured |
| Upstream Affected Component field | not configured | Steps 4.3 and 7 skipped |
| ProdSec Jira account ID / email | not configured | @mentions skipped |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) | OK. No Deployment Context column, so it defaults to `upstream` and coordination guidance is left out |

## Step 0.3: Matrix staleness

The matrix has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-27, so it is **152 days old**, past the 14-day threshold.

> Security matrix for streams **2.1.x / 2.2.x** was last updated on 2026-06-28 (152 days ago). The matrix may not show recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval decision: **proceed anyway** with the current matrix. No refresh was done because external tools are not allowed.

## Step 0.8: Assign and transition (proposed, not executed)

- Assign TC-8060 to the current user. It is currently Unassigned.
- Status is New. Transition it to Assigned, using a transition discovered dynamically with `get_transitions`.

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Jira key | TC-8060 | Issue |
| CVE ID | CVE-2026-99010 | Label `CVE-2026-99010` and the summary |
| Summary | CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2] | Issue |
| Status | New | Issue |
| Affected component | `pscomponent:org/rhtpa-server` (org/rhtpa-server) | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate) | Description |
| Affected version range | < 0.4.5 ("versions before 0.4.5") | Description |
| Fixed version | 0.4.5 | Description |
| CVSS / severity | 7.5 (High) | Description |
| Vulnerability type | Denial of service: memory exhaustion via unbounded CONTINUATION frames | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 (hyperium/h2#800) | Remote links |
| Advisory URL | none (no GHSA or advisory remote link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 | Remote links |
| Due date | 2026-08-15 (**already past** as of 2026-11-27) | `duedate` |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) | Issue |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream `2.2.x`. It matches the configured Version Stream `2.2.x` (git.example.com/rhtpa/rhtpa-release.0.4.z).
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 4 are limited to 2.2.x. Other streams are only considered for the Case A cross-stream check.

### Ecosystem detection

- h2 is a Rust crate, so the ecosystem is **Cargo**.
- Cargo appears in the 2.2.x Ecosystem Mappings: repo `backend`, lock file `Cargo.lock`, check `git show <tag>:Cargo.lock`, upstream branch `release/0.4.z`.
- Category: **source dependency**. That means 2 remediation tasks per affected stream: an upstream backport (or dependency bump) plus a downstream propagation task.

### Deployment context

- The affected repository is rhtpa-backend (`backend`). The Source Repositories table has no Deployment Context column, so it defaults to `upstream`. Under the backward-compatibility rule, the Coordination Guidance subsection is left out.

## Step 1.5: External CVE data enrichment

| Source | Affected range | Fixed version | Status |
|--------|----------------|---------------|--------|
| Jira description | < 0.4.5 | 0.4.5 | Parsed |
| MITRE CVE API | — | — | Not queried (eval forbids external calls), treated as unavailable |
| OSV.dev | — | — | Not queried (eval forbids external calls), treated as unavailable |

> External CVE databases unavailable. Using Jira description data only, so confidence in the fix threshold is reduced.

**Fix threshold used for Step 2.3: h2 < 0.4.5 is affected; 0.4.5 and later is fixed.**

## Step 1.7: Embargo check

Skipped silently because no Embargo policy URL is configured. For reference, CVSS 7.5 would have met the threshold.
