# Step 1 – Data Extraction: TC-8005

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Step 0 configuration validated from
`claude-md-security-config.md` (Repository Registry, Jira Configuration, Code Intelligence,
Security Configuration with Product Lifecycle, Version Streams, Source Repositories all present).

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8005 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-40215 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` (summary suffix) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) |
| Fixed version | 3.0.7-28.el9_4 |
| Severity | CVSS 7.1 (High) |
| Vulnerable code path | `X509_verify_cert()` – SAN extension length not bounds-checked (buffer over-read) |
| Upstream fix PR | None in remote links (RPM vendor errata only) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x**
  (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue is **scoped** to stream 2.2.x for Steps 2–8.

## Ecosystem Detection

- Library `openssl-libs` is a system package -> ecosystem **RPM**.
- RPM is listed in the 2.2.x Ecosystem Mappings with Lock File `rpms.lock.yaml`
  (Check Command `git show <tag>:rpms.lock.yaml`).
- Classification: **System package** -> **1 remediation task per stream** (Konflux release repo fix).
- Investigation method: lock file (`rpms.lock.yaml`) + optional SBOM verification.

## Deployment Context

- Source Repositories table has no Deployment Context column (backward compatibility):
  default `upstream`, and coordination guidance is omitted from remediation tasks
  per `remediation-templates.md`.

## Pre-analysis checks

- **Step 0.3 Matrix staleness**: matrix `Last-Updated: 2026-06-28T10:00:00Z`, which is
  151 days before today (2026-11-26) and over the 14-day threshold. Warning: the matrix may not
  reflect recent 2.2.x releases (anything after 2.2.4). For this eval, proceeding with the
  current matrix ("Proceed anyway").
- **Step 1.5 External enrichment**: MITRE/OSV were not queried because external calls are
  prohibited in this eval. "External CVE databases unavailable — using Jira description data
  only. Fix threshold confidence is reduced." Fix threshold used: `3.0.7-28.el9_4`.
- **Step 1.7 Embargo check**: no Embargo policy URL is configured, so the step was skipped
  even though CVSS 7.1 is at or above the threshold.
