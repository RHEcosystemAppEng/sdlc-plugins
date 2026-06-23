# Step 1 -- Data Extraction

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | N/A (RPM system package -- no upstream PR) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x only. Steps 3-4 will be scoped to this stream.

## Ecosystem Detection

**Ecosystem: RPM**

The vulnerable library `openssl-libs` is a system RPM package (not a Cargo crate, npm package, or Go module). This is confirmed by:

1. The package name follows RPM naming conventions (`openssl-libs` with version format `3.0.7-28.el9_4`)
2. The version format includes RPM release/dist tags (`.el9_4`)
3. The advisory is an RHSA (Red Hat Security Advisory), indicating a system-level RPM fix
4. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md lists RPM as a configured ecosystem with `rpms.lock.yaml` as the lock file

The RPM ecosystem means:
- Lock file: `rpms.lock.yaml`
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Remediation: **1 task** (Konflux release repo only -- no upstream backport needed since this is a system package)
