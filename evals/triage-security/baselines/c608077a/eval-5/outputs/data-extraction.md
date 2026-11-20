# Step 1 – Data Extraction: TC-8005

Source: mock Jira issue `vuln-issue-rpm.md` (no live Jira call made — eval mode).

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | not configured (Step 4.3 cross-CVE overlap and Step 7 concurrent triage will be skipped) |
| ProdSec Jira account ID | not configured (no @mention in correction comment) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`; coordination guidance omitted per backward-compat rule) |

Result: all required sections present — proceed.

## Step 0.3 – Matrix staleness check

> WARNING: Security matrix was last updated on 2026-06-28 (145 days ago, threshold 14 days). The matrix may not reflect recent releases (e.g., a 2.2.5 build released after 2026-05-04 would be missing).
> Options: 1. Refresh now / 2. Proceed anyway / 3. Stop.

Eval mode: proceeding with the current matrix (option 2). The engineer should refresh before acting on the results.

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8005 |
| CVE ID | CVE-2026-40215 (label + summary) |
| Summary | CVE-2026-40215 openssl-libs - Buffer over-read in X.509 certificate verification [rhtpa-2.2] |
| Status | New (full triage path) |
| Affected component | `pscomponent:org/rhtpa-server` → org/rhtpa-server |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs (RPM, openssl) |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Vulnerable code path | `X509_verify_cert()` — SAN extension length field not validated |
| Upstream fix PR | none (no GitHub PR remote link) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 (already past as of 2026-11-20) |
| Assignee | Unassigned |
| Existing comments | none |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z) |
| Scope | Scoped — Steps 3–8 limited to the 2.2.x stream; other streams handled via Case A cross-stream notice |

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | **RPM** (system package in container image) |
| Category | System package → **1 remediation task per stream** (Konflux release repo fix) |
| Lock file configured | Yes — `rpms.lock.yaml` (Ecosystem Mappings, both streams) |
| Investigation method | Lock file (`git show <tag>:rpms.lock.yaml \| grep 'openssl-libs'`) + optional SBOM verification |
| Deployment context | `upstream` (default — Deployment Context column absent) |

## Step 1.5 – External CVE data enrichment

Not performed: the eval forbids external calls (MITRE CVE API / OSV.dev WebFetch).
> WARNING: External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **3.0.7-28.el9_4** (Jira description).

## Step 1.7 – Embargo check

Skipped — no Embargo policy URL configured (CVSS 7.1 would otherwise trigger the gate).
