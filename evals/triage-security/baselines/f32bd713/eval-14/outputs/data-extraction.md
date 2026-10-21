# Step 1 -- Data Extraction: TC-8005

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
| Upstream fix PR | None |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched Version Stream: **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only** (scoped issue)

Triage is scoped to the 2.2.x stream. Other streams (2.1.x) will be checked for cross-stream impact in Step 2 but remediation is scoped to 2.2.x.

## Ecosystem Detection

- Library: openssl-libs
- Ecosystem: **RPM** (system package in container images)
- Classification: **System package** -- produces 1 remediation task per affected stream (Konflux release repo fix only)
- Lock file: `rpms.lock.yaml` (configured in 2.2.x stream Ecosystem Mappings)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Deployment Context Lookup

- Affected repository from component label: org/rhtpa-server
- Source Repositories match: rhtpa-backend
- Deployment context: upstream (default, no Deployment Context column present)

## Affects Versions Mismatch (Preliminary)

PSIRT assigned **RHTPA 2.0.0** as Affects Versions, but there is no 2.0.x stream configured in the Version Streams table. The issue is scoped to the 2.2.x stream via its summary suffix. This will be corrected in Step 3 after version impact analysis confirms which 2.2.x versions are actually affected.
