# Step 1 -- Data Extraction

## TC-8005 -- Parsed CVE Data

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
| Upstream fix PR | N/A |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x
stream only.

## Ecosystem Detection

The vulnerable library is **openssl-libs**, a system-level RPM package. Based on
the library name and the component context (pscomponent:org/rhtpa-server), the
ecosystem is identified as **RPM** -- not Cargo or npm.

The Ecosystem Mappings table for the 2.2.x stream confirms that RPM is a
configured ecosystem with lock file `rpms.lock.yaml` and check command
`git show <tag>:rpms.lock.yaml`.

Per the ecosystem classification table:
- **RPM** is a **system package** ecosystem
- Remediation produces **1 task** per stream (Konflux release repo fix only)
- No upstream backport task is created for system packages

## Deployment Context Lookup

The Source Repositories table does not include a Deployment Context column.
Per backward compatibility rules, all repositories default to `upstream`.
The affected repository (rhtpa-backend / rhtpa-server) defaults to `upstream`.
