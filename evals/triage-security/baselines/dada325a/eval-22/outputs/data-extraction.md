# Step 1 – Data Extraction: TC-8021

Skill: `/sdlc-workflow:triage-security` (interactive mode — `FULLSEND_OUTPUT_DIR` absent; eval simulation, no Jira/git calls made)

> Note: the mock issue file lists its key as `TC-8001`; the eval task names the issue `TC-8021`. All issue content below comes from the mock file and is treated as TC-8021.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key / Cloud ID | TC / 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | present, `mcp__<instance>__<tool>` convention | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification field | customfield_12345 | configured |
| Upstream Affected Component field | customfield_10632 | configured (per eval assumption) |
| PS Component field | — | not configured |
| Stream field | — | not configured |
| ProdSec contact / account ID | — | not configured (skip @mentions) |
| Embargo policy URL | — | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`) | OK |

## Step 0.3 – Matrix staleness check

- Matrix `Last-Updated`: 2026-06-28T10:00:00Z. Today: 2026-11-06. Age: **131 days**, which is over the 14-day threshold.
- **Warning to engineer:** "Security matrix for streams 2.1.x and 2.2.x was last updated on 2026-06-28 (131 days ago). It may not include recent releases. Options: 1) Refresh now, 2) Proceed anyway, 3) Stop."
- Eval assumption: **Proceed anyway** with the mock matrix. Any 2.2.x/2.1.x release after 2026-05-04 is not covered by this analysis.

## Step 0.8 – Assign and transition (simulated)

Status is `New`. In a live run: assign to the current user, then move the issue to `Assigned` via a dynamically discovered transition. Not executed here.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 | eval task |
| Issue type / Status | Vulnerability / New | issue |
| CVE ID | **CVE-2026-31812** | label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | label |
| Upstream Affected Component (customfield_10632) | **quinn-proto** | custom field |
| PSIRT-claimed product version | `[rhtpa-2.2]` → stream **2.2.x** | summary suffix |
| Affects Versions (Jira) | **RHTPA 2.0.0** (wrong: no 2.0.x stream exists) | versions field |
| Vulnerable library | **quinn-proto** (Rust crate) | description |
| Affected range | **< 0.11.14** | description |
| Fixed version | **0.11.14** | description |
| Severity | CVSS 7.5 (High), DoS (panic on excessive stream count) | description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | remote links |
| Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq ; RUSTSEC-2026-0042 | remote links / refs |
| CVE record | https://www.cve.org/CVERecord?id=CVE-2026-31812 | remote links |
| Due date | 2026-07-15 (already past) | duedate |
| Assignee | Unassigned | issue |
| Existing comments | none | issue |

All critical fields (CVE ID, library, affected range) were parsed, so triage can continue.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` matches configured stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to 2.2.x. Steps 3–4 and Case A/B apply in scoped mode.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (repo `backend`, `Cargo.lock`).
- Category: **source dependency**, so 2 remediation tasks per affected stream.
- Deployment context for rhtpa-backend: `upstream` (default; the Deployment Context column is absent).

## Step 1.5 – External CVE enrichment (simulated)

MITRE and OSV were not queried, per the eval constraints. Both are treated as unavailable:
> "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."

Fix threshold used: **quinn-proto < 0.11.14 affected; 0.11.14 fixed.**

## Step 1.7 – Embargo check

No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.5 would otherwise have triggered the gate.

## Step 2 – Version impact analysis (from mock lock-file data)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | backend retag of 2.2.1, result carried forward |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed |
| dev | — | — | — | UNKNOWN | no unreleased Jira version or branch-HEAD data in eval inputs |

- Dependency chain (2.3.5): the mock data cannot tell whether quinn-proto is a direct or transitive dependency of the backend (it is likely transitive via `quinn`). This must be confirmed with `cargo tree` or by inspecting the backend `Cargo.lock`.
- Upstream fix status (2.5): branch-HEAD lock data for `release/0.4.z` and `release/0.3.z` is not in the inputs, so it is **not verified**. The latest 2.2.x release (v0.4.12) ships 0.11.14, which strongly suggests `release/0.4.z` is fixed, but this was not confirmed with `git show`. No 2.1.x tag ships a fixed version.
