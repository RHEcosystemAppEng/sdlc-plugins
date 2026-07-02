# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none) |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to
the **2.2.x** stream in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `openssl-libs` is a system RPM package (not a Cargo crate
or npm package). The Ecosystem Mappings table for the 2.2.x stream confirms RPM
is a configured ecosystem with lock file `rpms.lock.yaml` and check command
`git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

Ecosystem: **RPM**
