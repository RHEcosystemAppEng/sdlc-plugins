# TC-8060 — Step 1 Data Extraction

Skill: `/sdlc-workflow:triage-security` (interactive mode — `FULLSEND_OUTPUT_DIR` absent; eval run with no Jira, git, or WebFetch calls, so the fixture files stand in for those reads)

## Step 0 — Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured, so Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| ProdSec contact / account ID | not configured, so @mentions are skipped |
| Version Streams | 2.1.x → `git.example.com/rhtpa/rhtpa-release.0.3.z`; 2.2.x → `git.example.com/rhtpa/rhtpa-release.0.4.z` |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Result: all required sections are present (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration). Proceed.

## Step 0.3 — Matrix staleness check

| Stream | Last-Updated | Age (as of 2026-11-03) | Status |
|--------|--------------|------------------------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 128 days | STALE (threshold 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 128 days | STALE (threshold 14 days) |

> Security matrix for stream **2.2.x** was last updated on 2026-06-28 (128 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval decision: **Proceed anyway**, using the mock matrix. Before the version impact table is relied on, the engineer should check that no 2.2.x release after 2.2.4 is missing from the matrix.

## Step 0.8 — Assign and transition (proposed, not executed)

- Assign TC-8060 to the current user. It is currently Unassigned.
- Status is **New**, so transition to **Assigned**, with the transition ID found dynamically through `get_transitions`.

## Step 1 — Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8060 | Issue |
| Status | New (full triage path) | Issue |
| CVE ID | CVE-2026-99010 | Label + summary |
| Summary | CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-server`, which maps to source repo `rhtpa-backend` (matrix repo column `backend`) | Labels |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate) | Description |
| Affected version range | < 0.4.5 ("versions before 0.4.5") | Description |
| Fixed version | 0.4.5 | Description |
| Severity | CVSS 7.5 (High), DoS / memory exhaustion | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | none (no GHSA link present) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 | Remote links |
| Due date | 2026-08-15 (**past due** as of 2026-11-03) | `duedate` |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) | Issue (used for the post-triage @mention) |
| Assignee | Unassigned | Issue |
| Existing comments | none | Issue |

All critical fields (CVE ID, library, affected range) were parsed. Execution continues.

### Stream scope resolution

| Suffix | Parsed stream | Configured? | Scope |
|--------|---------------|-------------|-------|
| `[rhtpa-2.2]` | 2.2.x | Yes (`rhtpa-release.0.4.z`) | **Scoped to 2.2.x** |

Steps 2–8 are scoped to the 2.2.x stream. 2.1.x is still analyzed for the cross-stream check (Case A).

### Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | **Cargo** (h2 is a Rust crate) |
| Listed in stream Ecosystem Mappings? | Yes (Cargo → `backend`, `Cargo.lock`, upstream branch `release/0.4.z`) |
| Category | Source dependency, so 2 remediation tasks per stream |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock \| grep -A2 'name = "h2"'` |

### Deployment context

`rhtpa-backend` has no Deployment Context column in Source Repositories. Its context defaults to `upstream`. Because the column is absent (backward compatibility), the Coordination Guidance subsection is **left out** of the remediation tasks, as `remediation-templates.md` requires.

## Step 1.5 — External CVE enrichment

MITRE (`cveawg.mitre.org/api/cve/CVE-2026-99010`) and OSV.dev (`api.osv.dev/v1/vulns/CVE-2026-99010`) were **not queried** because this eval forbids external calls. Both sources count as unavailable.

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used in Step 2.3: **h2 < 0.4.5 affected; 0.4.5 fixed** (from the Jira description).

## Step 1.7 — Embargo check

Skipped: no Embargo policy URL is configured. CVSS 7.5 would otherwise meet the threshold of 7.0 or higher.
