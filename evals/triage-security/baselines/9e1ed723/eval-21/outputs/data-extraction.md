# Step 1 – Data Extraction: TC-8020

Execution mode: **interactive** (Step 0.6 — `FULLSEND_OUTPUT_DIR` absent). Jira, git, and
external lookups are simulated from the eval input files; no external calls were made.

> Note: the mock issue file lists its key as `TC-8001`; the eval task identifies the issue
> as **TC-8020**. TC-8020 is used throughout as the current issue key.

## Step 0 – Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 (assumed configured per eval instructions) |
| Embargo policy URL | not configured → Step 1.7 skipped |
| ProdSec contact / account ID | not configured → @mentions skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend (no Deployment Context column → default `upstream`) |

All required sections present (Repository Registry, Jira Configuration, Code Intelligence,
Security Configuration with Product Lifecycle / Version Streams / Source Repositories).

## Step 0.3 – Matrix staleness

Matrix `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-23 → ~148 days old, exceeding
the 14-day threshold. In a live run the engineer would be offered Refresh / Proceed / Stop.
For this eval, triage proceeds with the current matrix (**Proceed anyway**).

## Step 0.8 – Assign and transition

Issue status is `New`, assignee Unassigned. Proposed (not executed): assign TC-8020 to the
current user and transition to `Assigned`.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| CVE ID | CVE-2026-31812 (label + summary) |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New |
| Affected component | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Vulnerability type | Denial of service (panic via excessive STREAMS frame) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | none |

## Stream scope resolution

Suffix `[rhtpa-2.2]` → stream **2.2.x** (matches configured Version Stream). Issue is
**scoped** to 2.2.x.

## Ecosystem detection

quinn-proto is a Rust crate → **Cargo** (listed in both streams' Ecosystem Mappings).
Category: source dependency → 2 remediation tasks per affected stream.
Lock file: `Cargo.lock` in `backend` repository.

## Deployment context

Affected repository rhtpa-backend → deployment context `upstream` (default; column absent).

## Step 1.5 – External enrichment

MITRE / OSV not queried (external calls prohibited in eval). Treated as unavailable:
> External CVE databases unavailable — using Jira description data only. Fix threshold
> confidence is reduced.

Fix threshold used: **< 0.11.14** (fixed in 0.11.14).

## Step 1.7 – Embargo check

Skipped — no Embargo policy URL configured (CVSS 7.5 would otherwise trigger the gate).

## Step 2 – Version impact (simulated `git show <tag>:Cargo.lock`)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | out of issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | out of issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |

Development stream: no unreleased Jira version data available in the eval inputs; not
assessed (would be checked at branch HEAD in a live run).

Dependency chain: quinn-proto is a transitive dependency of the backend (via the QUIC
stack, e.g. quinn); exact chain not available from mock data.

Upstream fix status: `release/0.4.z` (2.2.x) — released tags v0.4.11/v0.4.12 already ship
0.11.14, so the fix is present on the branch lineage; `release/0.3.z` (2.1.x) — branch HEAD
not available in the mock data (unverified).

## Step 3 – Affects Versions correction (proposed)

Current: RHTPA 2.0.0 (incorrect — no 2.0.x stream exists and not in issue scope).
Proposed for scoped stream 2.2.x: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
(remove RHTPA 2.0.0). Not executed — requires engineer confirmation.

## Steps 4–6

- Step 4 (siblings/duplicates, cross-CVE overlap via customfield_10632): not simulated by
  eval data; no sibling results assumed. 2.1.x is also affected (cross-stream).
- Step 5 (lifecycle): lifecycle page not fetched; versions assumed supported.
- Step 6 (already fixed): no resolved siblings assumed.
