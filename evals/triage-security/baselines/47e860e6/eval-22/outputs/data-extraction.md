# Step 1 – Data Extraction: TC-8021

Mode: interactive (no `FULLSEND_OUTPUT_DIR`; Steps 0.6/0.7 → interactive, 0.7 skipped).
Source: `vuln-issue-standard.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`).

> Note: the mock issue file is labelled `TC-8001`; the eval task identifies the issue as
> **TC-8021**. TC-8021 is used as the current issue key throughout (including the
> `key != TC-8021` clause in Step 7). All other fields are taken from the mock file.

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
| Upstream Affected Component field | customfield_10632 (configured, per eval assumption) |
| PS Component field | not configured |
| Stream field | not configured |
| ProdSec contact / account ID | not configured (no @mentions) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`) |

All required sections (Repository Registry, Jira Configuration, Code Intelligence,
Security Configuration with Product Lifecycle / Version Streams / Source Repositories) are
present → proceed.

## Step 0.3 – Matrix staleness

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` vs today 2026-11-04 → **129 days old**
(threshold 14 days). Warning would be raised (Refresh / Proceed / Stop). For this eval,
proceeding with the current matrix, and noting that recent 2.1.x/2.2.x releases could be
missing.

## Step 0.8 – Assign/transition (simulated, not executed)

Status is `New`, assignee is Unassigned. Proposed: assign TC-8021 to the current user and
transition to Assigned (transition ID looked up at runtime). Requires engineer confirmation.

## Extracted fields

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 | Eval task |
| CVE ID | **CVE-2026-31812** | Label + summary |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Summary |
| Status | New | Status |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Upstream Affected Component (customfield_10632) | **quinn-proto** | Custom field (per eval) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | **quinn-proto** | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| CVSS / severity | 7.5 (High) – DoS | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote link / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote link |
| Due date | 2026-07-15 (already past as of 2026-11-04) | `duedate` |
| Existing comments | none | Comments |

All critical fields (CVE ID, library, affected range) were parsed, so there is no need to stop.

## Stream scope resolution

Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (rhtpa-release.0.4.z). The issue is
**scoped** to 2.2.x.

## Ecosystem detection

quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo appears in both streams'
Ecosystem Mappings (`Cargo.lock`, repository `backend`). Category: source dependency, which
means 2 remediation tasks per affected stream.

## Deployment context

Affected repository: rhtpa-backend. No Deployment Context column exists, so it defaults
to `upstream`.

## Step 1.5 – External enrichment

MITRE / OSV queries were not executed (the eval prohibits external calls). The Jira
description data is used only, so fix threshold confidence is reduced. Fix threshold used: **0.11.14**.

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise have triggered it.

## Step 2 – Version impact (simulated `git show <tag>:Cargo.lock`, using mock lock data)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | YES |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

Development stream: no unreleased Jira version data was available in this eval, so it could
not be evaluated (Step 2.2 not simulated).

Upstream fix status (Step 2.5): on `release/0.4.z`, the latest pinned tag v0.4.12 already
ships 0.11.14, so the fix is likely on the branch (branch HEAD was not inspected). On
`release/0.3.z`, the latest pinned tag v0.3.12 ships 0.11.9, so the fix has not been
confirmed upstream and a backport may be needed.

## Step 3 – Affects Versions correction (proposed, not executed)

Scoped to 2.2.x: `Current: [RHTPA 2.0.0]` → `Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
RHTPA 2.0.0 is wrong because no 2.0.x stream exists. Version IDs must come from
`getJiraIssueTypeMetaWithFields`. 2.1.x versions belong to a companion issue.
