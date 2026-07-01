# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | (none) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| CVSS | 7.1 (High) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, mapping to the **2.2.x** stream in the Version Streams configuration. Triage is scoped to this stream only.

## Ecosystem Detection

The vulnerable library is **openssl-libs**, which is a system-level RPM package (not a Cargo crate or npm package). Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **RPM** ecosystem.

- Ecosystem: **RPM**
- Lock File: `rpms.lock.yaml`
- Check Command: `git show <tag>:rpms.lock.yaml`
- Upstream Branch: (none -- RPM packages have no upstream branch in the source repo)

The RPM ecosystem uses rpms.lock.yaml for version extraction. Since this is a system package ecosystem (not a source dependency), remediation will produce a single task (not the two-task upstream+downstream flow used for Cargo/npm).
