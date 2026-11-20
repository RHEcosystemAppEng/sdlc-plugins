# Step 1 – Data Extraction: TC-8001

Source: mock Jira issue (`vuln-issue-standard.md`). In a live run this comes from
`jira.get_issue(TC-8001)` and `jira.get_issue_remote_links(TC-8001)`; no external
calls were made here.

## Step 0 – Configuration check (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column → default `upstream`, Coordination Guidance omitted per backward-compat rule) |
| Optional fields not configured | Upstream Affected Component (Step 4.3 and Step 7 skipped), PS Component, Stream field, ProdSec email/account ID (no @mention), Embargo policy URL (Step 1.7 skipped) |

All required sections are present, so triage can go ahead.

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` (org/rhtpa-server) | Labels |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High), DoS (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Status / Assignee | New / Unassigned | Issue |
| Existing comments | None | Comment history |

## Derived context

| Item | Value |
|------|-------|
| Stream scope | **Scoped to 2.2.x**. The suffix `[rhtpa-2.2]` matches the configured 2.2.x stream (rhtpa-release.0.4.z) |
| Ecosystem | **Cargo** (Rust crate). Source dependency category: 2 remediation tasks per stream |
| Lock file / check command | `Cargo.lock` via `git show <tag>:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| Source repository | backend (rhtpa-backend) |
| Deployment context | `upstream` (default, because the Deployment Context column is absent) |
| Affects Versions sanity | **Mismatch**: `RHTPA 2.0.0` does not belong to any configured stream (2.1.x, 2.2.x). Step 3 corrects it |

## Step 1.5 – External enrichment

MITRE / OSV were not queried because this eval forbids external calls. In a live run
both would be fetched and cross-validated. For this run the fix threshold comes from
the Jira description only (< 0.11.14, fixed 0.11.14), so confidence is reduced:

> External CVE databases unavailable: using Jira description data only. Fix threshold confidence is reduced.

## Step 1.7 – Embargo check

No Embargo policy URL is configured, so the step is skipped silently (CVSS 7.5 would otherwise trigger the gate).
