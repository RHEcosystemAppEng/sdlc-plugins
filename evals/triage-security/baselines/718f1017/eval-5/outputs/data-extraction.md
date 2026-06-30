# Step 1 -- Data Extraction for TC-8005

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-40215 | Labels, summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (Component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | openssl-libs | Description text |
| Affected version range | versions before 3.0.7-28.el9_4 | Description text |
| Fixed version | 3.0.7-28.el9_4 | Description text |
| CVSS | 7.1 (High) | Description text |
| Upstream fix PR | (none) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 | Remote links (RHSA) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links (cve.org) |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | (no comments) | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `[rhtpa-2.2]` -> stream `2.2.x`
2. Matched to Version Streams table: `2.2.x` stream at `git.example.com/rhtpa/rhtpa-release.0.4.z`
3. Issue stream scope: **2.2.x** (scoped -- Steps 2-7 apply only to this stream)

## Ecosystem Detection

The vulnerable library is **openssl-libs**, which is a system-level RPM package (not a Cargo crate, npm package, or Go module). The ecosystem mappings in the 2.2.x stream's `security-matrix.md` include an RPM ecosystem entry with:
- Lock File: `rpms.lock.yaml`
- Check Command: `git show <tag>:rpms.lock.yaml`
- Upstream Branch: (none -- RPM packages have no upstream branch)

**Ecosystem: RPM** (system package). Remediation will produce a single task (Konflux release repo fix). No upstream backport step is needed.
