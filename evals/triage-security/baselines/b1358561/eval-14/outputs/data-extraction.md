# Step 1 – Data Extraction: TC-8005

Source: mock Jira issue `vuln-issue-rpm.md` (no Jira MCP call made; simulated `jira.get_issue` / `jira.get_issue_remote_links`).

## Pre-flight (Steps 0 – 0.8)

| Check | Result |
|-------|--------|
| Step 0.6 Mode | Interactive (`FULLSEND_OUTPUT_DIR` absent) |
| Step 0 Configuration | PASS – Repository Registry, Jira Configuration (Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432), Code Intelligence, Security Configuration (Product Lifecycle, Version Streams, Source Repositories) all present |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Embargo policy URL | Not configured (Step 1.7 skipped) |
| Upstream Affected Component field | Not configured (Step 4.3 will be skipped) |
| Step 0.3 Matrix staleness | WARNING – `Last-Updated: 2026-06-28T10:00:00Z`, 152 days old (threshold 14 days). Matrix may not reflect recent 2.2.x releases. Options: Refresh now / Proceed anyway / Stop. For this eval: proceeding with the current matrix. |
| Step 0.8 Assign / transition | Would assign TC-8005 to current user and transition New → Assigned (not executed – no Jira calls in eval) |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` + summary |
| Affected component | `pscomponent:org/rhtpa-server` (org/rhtpa-server) | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → RHTPA 2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | openssl-libs | Description |
| Affected version range | versions before 3.0.7-28.el9_4 (< 3.0.7-28.el9_4) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS | 7.1 (High) | Description |
| Vulnerability summary | Buffer over-read in X.509 certificate chain verification (`X509_verify_cert()`, SAN extension length not validated) | Description |
| Upstream fix PR | None (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 (already past as of 2026-11-27) | `duedate` |
| Status | New (full triage path) | Issue |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Parsed stream | 2.2.x |
| Configured stream match | YES – `2.2.x` → `git.example.com/rhtpa/rhtpa-release.0.4.z` (local `/home/dev/repos/rhtpa-release.0.4.z`) |
| Issue stream scope | **Scoped – 2.2.x only** (2.1.x stream excluded from analysis) |

Note: the Jira Affects Versions value (RHTPA 2.0.0) is inconsistent with the stream suffix (2.2) and with the configured streams (no 2.0.x stream exists). This is a candidate for Step 3 correction.

## Ecosystem Detection

| Item | Value |
|------|-------|
| Ecosystem | RPM (system package in container image) |
| Listed in 2.2.x Ecosystem Mappings | YES – RPM, Lock File `rpms.lock.yaml`, Check Command `git show <tag>:rpms.lock.yaml`, Repository `—`, Upstream Branch `—` |
| Category | System package |
| Investigation method | Lock file (`rpms.lock.yaml`) + SBOM inspection |
| Remediation tasks per affected stream | 1 – Konflux release repo fix only |

## Deployment Context

Component `org/rhtpa-server` does not match a Source Repositories entry by name (only `rhtpa-backend` is listed; no Deployment Context column). Default deployment context: `upstream`.

## Step 1.5 – External CVE Data Enrichment

MITRE CVE API and OSV.dev were not queried (external calls prohibited in this eval) – treated as unavailable.

> "⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 3.0.7-28.el9_4 | 3.0.7-28.el9_4 |
| MITRE CVE API | unavailable | unavailable |
| OSV.dev | unavailable | unavailable |

**Fix threshold used for Step 2:** 3.0.7-28.el9_4 (Jira description).

## Step 1.7 – Embargo Check

Skipped – no Embargo policy URL configured in Security Configuration (CVSS 7.1 would otherwise meet the >= 7.0 threshold).
