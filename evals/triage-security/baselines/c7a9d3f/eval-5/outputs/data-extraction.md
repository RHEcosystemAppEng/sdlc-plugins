# Step 1 — Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | — |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`).

Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

Vulnerable library: **openssl-libs** — this is an RPM system package (not a Cargo/npm source dependency).

Ecosystem: **RPM**
Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
