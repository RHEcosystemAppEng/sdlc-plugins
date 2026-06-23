# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | (none -- no GitHub PR in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (Red Hat Security Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| CVSS | 7.1 (High) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches the 2.2.x row in the Version Streams table)
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

Triage is **scoped to the 2.2.x stream only**. Steps 3-7 will only operate on versions within this stream.

## Ecosystem Detection

- Vulnerable library: **openssl-libs** -- this is an RPM system package (not a Cargo/npm/Go source dependency)
- Ecosystem: **RPM**
- Lock file: `rpms.lock.yaml` (configured in the 2.2.x stream's Ecosystem Mappings table)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Upstream Branch: (none -- RPM ecosystem has no upstream branch configured)

Since openssl-libs is an RPM system package, remediation will follow the **single-task** pattern (Konflux repo fix only, no upstream backport needed).
