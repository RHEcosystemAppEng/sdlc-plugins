# Step 1 – Data Extraction: TC-8020

> Source: `vuln-issue-standard.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`).
> Note: the mock file header shows key `TC-8001`; the task prompt names the issue as **TC-8020**.
> TC-8020 is used throughout, as the prompt directs.

## Step 0 – Configuration validation (from `claude-md-security-config.md`)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | present |
| Project key | TC | present |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | present |
| Code Intelligence | `mcp__<instance>__<tool>`; serena_backend | present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | present |
| Jira version prefix | RHTPA | present |
| Vulnerability issue type ID | 10024 | present |
| Component label pattern | `pscomponent:` | present |
| VEX Justification field | customfield_12345 | present (optional) |
| Upstream Affected Component field | customfield_10632 | assumed configured (per task instruction) |
| PS Component / Stream fields | not configured | Step 4.3 would be skipped. Step 7 only needs the Upstream Affected Component field. |
| ProdSec contact / account ID | not configured | @mentions skipped |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | present |
| Source Repositories | rhtpa-backend (no Deployment Context column, so `upstream` is used) | present |

Mode: interactive (no `FULLSEND_OUTPUT_DIR`). Jira and git calls are simulated from the mock files.

### Step 0.3 – Matrix staleness

Both stream matrices carry `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-20, so the matrices are **145 days old**, well past the 14-day threshold.

> Warning: the security matrices for streams **2.1.x** and **2.2.x** were last updated on 2026-06-28 (145 days ago). They may not show releases after RHTPA 2.2.4.
> Options: 1. Refresh now · 2. Proceed anyway · 3. Stop

Eval assumption: **Proceed anyway**, using the mock matrix as provided. This caveat is carried into the outcome.

### Step 0.8 – Assign / transition (simulated, not executed)
Proposed: assign TC-8020 to the current user, then transition New → Assigned (target found dynamically through `get_transitions`).

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8020 |
| Issue type / Status | Vulnerability / New |
| CVE ID | **CVE-2026-31812** (from the label and the summary) |
| Affected component (label) | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | **quinn-proto** |
| PSIRT-claimed product version (summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 (**wrong**: no 2.0.x stream exists) |
| Vulnerable library | **quinn-proto** |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") |
| Fixed version | **0.11.14** |
| CVSS / Severity | 7.5 (High) – DoS (panic from an excessive stream count) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (**already past** as of 2026-11-20) |
| Assignee | Unassigned |
| Existing comments | none |

## Stream scope resolution
- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`), which is a configured stream.
- The issue is **scoped** to 2.2.x. Stream 2.1.x is out of scope and can only be handled through Case A (cross-stream).

## Ecosystem detection
- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (repo: backend, lock file `Cargo.lock`).
- Category: **source dependency**, so each stream gets 2 remediation tasks.
- Deployment context for rhtpa-backend: `upstream` (default, because the column is absent).

## Step 1.5 – External enrichment (simulated)
No MITRE or OSV calls were made, per the task instructions. The Jira description threshold (< 0.11.14, fixed 0.11.14) is used. In a live run this would be cross-validated against the external sources.
Confidence note: fix-threshold confidence is reduced (Jira description data only).

## Step 1.7 – Embargo check
Skipped. No Embargo policy URL is configured, even though CVSS 7.5 would have met the threshold.

## Step 2 – Version impact (simulated `git show <tag>:Cargo.lock`, from the mock lock data)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? | Notes |
|--------|---------|-------------|-------------|-----------------------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | **YES** | out of scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | **YES** | out of scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | **YES** | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | **YES** | |
| 2.2.x | 2.2.2 | v0.4.8 | — | **YES** | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed |

- Development stream: no unreleased-version data was provided. 2.2.x is the latest stream, and its newer releases (v0.4.11 and later) already ship 0.11.14, so `release/0.4.z` HEAD is expected to be fixed. This was not verified by a HEAD read.
- Step 2.5 upstream fix status: `release/0.4.z` already ships 0.11.14 (from v0.4.11). For `release/0.3.z` no evidence of a fix is available; the last 2.1.x tag still ships 0.11.9.

## Step 3 – Affects Versions correction (proposed, scoped to 2.2.x)
`Current: [RHTPA 2.0.0]  ->  Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
(Version IDs would come from `getJiraIssueTypeMetaWithFields`. 2.2.3 and 2.2.4 are not affected.)

## Steps 4–6 (simulated, no data provided)
- Step 4: no sibling CVE-2026-31812 issues were supplied, so none are assumed. 4.3 is skipped (PS Component and Stream fields are not configured). 4.4: no preemptive tasks were supplied.
- Step 5: lifecycle page not fetched. 2.2.x is assumed supported.
- Step 6: no resolved siblings, so not already fixed.
