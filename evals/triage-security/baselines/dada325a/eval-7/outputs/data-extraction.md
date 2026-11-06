# TC-8006 — Step 1 Data Extraction

Skill: `/sdlc-workflow:triage-security` (interactive mode; `FULLSEND_OUTPUT_DIR` absent).
Eval simulation: no Jira MCP, git, or WebFetch calls were made. All values come from the provided mock files.

## Step 0 — Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3, Step 7, and Step 7.5.3 dedup get skipped) |
| PS Component / Stream fields | not configured |
| ProdSec account ID / email | not configured (no @mentions) |
| Embargo policy URL | not configured (Step 1.7 gets skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

Every required section is present, so validation passes.

## Step 0.3 — Matrix staleness

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-06, which makes it about 131 days old, well past the 14-day threshold. That applies to both streams. In a live run the skill would offer: Refresh now / Proceed anyway / Stop. For this eval the triage proceeds on the current matrix and records the warning.

## Extracted fields

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8006 | Issue |
| CVE ID | CVE-2026-31812 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label |
| PSIRT-claimed product version | `[rhtpa-2.1]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.1.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Other reference | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 | `duedate` |
| Status | New (full triage path) | Issue |
| Assignee | Unassigned (Step 0.8 would assign to the current user and move it to Assigned) | Issue |
| Existing comments | none | Comments |
| Existing issue links | **Related → TC-8001** (link ID 1990401, outward: TC-8006 → TC-8001) | `issuelinks` |

## Stream scope resolution

- Suffix `[rhtpa-2.1]` maps to stream **2.1.x**, which is in the Version Streams table (rhtpa-release.0.3.z).
- The **issue is scoped to stream 2.1.x**.

## Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**, which counts as a source dependency.
- Lock file: `Cargo.lock` in the backend repo (from the Ecosystem Mappings in both streams).
- Remediation shape: 2 tasks per stream.
- Deployment context for rhtpa-backend: `upstream` (default).

## Step 1.5 — External enrichment (simulated)

MITRE and OSV were not queried, as the eval requires. The fix threshold from the Jira description (< 0.11.14, fixed in 0.11.14) is used and marked as reduced confidence.

## Step 1.7 — Embargo check

No Embargo policy URL is configured, so this step is skipped silently even though CVSS is 7.5.

## Step 2 — Version impact (from the mock lock-file data)

Released versions, quinn-proto at the pinned backend tag:

| Stream | Version | Backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| 2.1.x ← (this issue) | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x ← (this issue) | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 | YES |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

The development stream and upstream branch HEAD checks (Steps 2.2 and 2.5) need Jira and git access, so they were not simulated.

## Step 3 — Affects Versions correction (scoped to 2.1.x)

- Current: `[RHTPA 2.1.0]` → Proposed: `[RHTPA 2.1.0, RHTPA 2.1.1]`. The current value is correct but incomplete, because 2.1.1 also ships quinn-proto 0.11.9.
- The 2.2.x versions are left off this issue because sibling TC-8001 tracks them.
- In a live run this needs engineer confirmation plus a correction comment with the Comment Footnote.
