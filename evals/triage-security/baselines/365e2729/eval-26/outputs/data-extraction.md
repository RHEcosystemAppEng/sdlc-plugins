# TC-8050 — Step 1: Data Extraction

Skill: `/sdlc-workflow:triage-security` (eval mode; no Jira, git or external calls made)

## Step 0 — Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`; coordination guidance omitted for backward compatibility) |

All required sections are present. Proceeding.

## Step 0.3 — Matrix staleness check

The matrix's `Last-Updated` value is 2026-06-28T10:00:00Z, which is 151 days before today (2026-11-26). That exceeds the 14-day threshold.

> Warning: the security matrix for stream **2.2.x** (and 2.1.x) was last updated on 2026-06-28 (151 days ago), so it may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval assumption: **Proceed anyway** with the current matrix.

## Step 1 — Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8050 | Issue |
| Issue status | New (full triage path) | Issue |
| CVE ID | CVE-2026-99001 | Label `CVE-2026-99001` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | criterion (Rust crate) | Description |
| Affected version range | < 0.5.2 ("versions before 0.5.2") | Description |
| Fixed version | 0.5.2 | Description |
| CVSS / severity | 5.3 (Medium) | Description |
| Vulnerability summary | Path traversal in benchmark output: crafted benchmark names containing path separators can write output files to arbitrary paths | Description |
| Upstream fix PR | none provided | Remote links |
| Advisory URL | none provided (no GHSA link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 | Remote links |
| Due date | 2026-08-01 | `duedate` |
| Assignee | Unassigned (Step 0.8 would assign it to the current user and transition it to Assigned; no confirmation was given in this eval, so this is not executed) | Issue |
| Existing comments | none | Comments |

All critical fields (CVE ID, library, affected range) were parsed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream **2.2.x**, which matches the configured Version Stream `2.2.x` (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 2–8 are scoped to 2.2.x. Other streams are reported only as cross-stream impact.

### Ecosystem detection

- criterion is a Rust crate, so the ecosystem is **Cargo**, which is listed in the 2.2.x Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`, upstream branch `release/0.4.z`).
- Category: **source dependency**. That means 2 remediation tasks per affected stream.

### Deployment context

- Affected repository: backend / rhtpa-backend. The Source Repositories table has no Deployment Context column, so it defaults to `upstream`. Following the backward-compatibility rule, the Coordination Guidance subsection is omitted from task descriptions.

## Step 1.5 — External CVE enrichment

The eval forbids external calls, so MITRE and OSV.dev were not queried. This is treated as "both external APIs unavailable":

> Warning: external CVE databases are unavailable, so only the Jira description data is used. Confidence in the fix threshold is reduced.

Fix threshold used for Step 2: **criterion < 0.5.2 is affected; 0.5.2 is fixed.**

## Step 1.7 — Embargo check

Skipped. No Embargo policy URL is configured, and CVSS 5.3 (Medium) is below the 7.0 threshold anyway.
