# Step 1 – Data Extraction: TC-8020

Source: `vuln-issue-standard.md` (mock Jira issue; simulated `jira.get_issue` + `jira.get_issue_remote_links`).

> Note: the mock issue file header says `TC-8001`; the eval task names the issue as **TC-8020**. TC-8020 is used as the
> current issue key throughout (including the `key != TC-8020` clause in Step 7 JQL).

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (per eval assumption: configured) |
| PS Component / Stream fields | Not configured |
| ProdSec contact / Jira account ID | Not configured (skip @mentions) |
| Embargo policy URL | Not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column -> defaults to `upstream`) |

All required sections present; configuration validation passes.

## Step 0.3 – Matrix Staleness

Both streams' matrix carries `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-06 -> **131 days old**, exceeding
the 14-day threshold. In an interactive run the engineer would be offered Refresh now / Proceed anyway / Stop. For this
eval, triage proceeds with the current matrix (the warning is recorded; versions released after 2026-06-28 may be missing).

## Step 0.8 – Assign / Transition (proposed, not executed)

Issue status is **New**, assignee Unassigned -> propose assign to current user and transition to Assigned. Not executed (no Jira calls in eval).

## Extracted CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New |
| CVE ID | CVE-2026-31812 (label + summary) |
| Affected component (label) | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| PSIRT-claimed product version | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) - DoS (panic via excessive STREAMS frame) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past as of 2026-11-06) |
| Existing comments | None |

### Stream scope resolution

Suffix `[rhtpa-2.2]` -> stream **2.2.x** (matches configured Version Stream `rhtpa-release.0.4.z`). Issue is **scoped**.

### Ecosystem detection

quinn-proto is a Rust crate -> **Cargo** (present in both streams' Ecosystem Mappings: `Cargo.lock` in `backend`).
Category: source dependency -> 2 remediation tasks per affected stream.

### Deployment context

rhtpa-backend -> `upstream` (default; no Deployment Context column).

## Step 1.5 – External enrichment

Not performed (no external calls allowed in eval). Using Jira description data only:
"External CVE databases unavailable - using Jira description data only. Fix threshold confidence is reduced."
Fix threshold used: **0.11.14**.

## Step 1.7 – Embargo check

CVSS 7.5 meets threshold, but no Embargo policy URL is configured -> step skipped.

## Step 2 – Version Impact Analysis (simulated lock-file data from security-matrix-mock.md)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |

- Development stream: not determinable in eval (no Jira unreleased-version data, no branch HEAD inspection).
- Step 2.5 upstream fix status: `release/0.4.z` released tags v0.4.11+ already ship 0.11.14, so the fix is
  already in the 2.2.x stream; `release/0.3.z` (2.1.x) has no evidence of a fix (latest tag ships 0.11.9). Branch HEADs not inspected.

## Step 3 – Affects Versions correction (proposed, not executed)

Scoped to 2.2.x: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
RHTPA 2.0.0 does not exist in the supportability matrix (PSIRT error). Jira version IDs would be discovered dynamically
via `getJiraIssueTypeMetaWithFields` (not available in eval).

## Steps 4–6

- Step 4 sibling/duplicate search: no sibling data supplied for this eval; no siblings assumed. 2.1.x is affected but no
  companion CVE Jira is known (relevant to Case A preemptive tasks).
- Step 4.3: skipped — PS Component and Stream custom fields are not configured (prerequisite).
- Step 5: lifecycle page not fetched; 2.2.x versions assumed supported.
- Step 6: no resolved siblings known -> not already fixed via sibling.
