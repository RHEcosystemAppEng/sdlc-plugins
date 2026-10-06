# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Assignee | engineer-a@example.com | Issue `assignee` field |
| Status | In Progress | Issue `status` field |
| Existing comments | 2 (description digest + post-triage summary) | Issue comments |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Remediation task count per stream: **2** (upstream backport + downstream propagation)

## Existing Issue Links

| Link Type | Linked Issue | Summary | Status |
|-----------|-------------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Comments

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z)
2. **Post-triage summary**: Documents version impact, Affects Versions correction, remediation tasks TC-8100/TC-8101, and transition to In Progress (posted 2026-07-01T10:01:00Z)

## Version Impact (from security-matrix mock data)

| Product Version | Build Tag | quinn-proto Version | Affected? |
|----------------|-----------|---------------------|-----------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 (retag of v0.4.8) | YES (< 0.11.14) |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO (>= 0.11.14) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO (>= 0.11.14) |

The issue is scoped to the 2.2.x stream. Cross-stream analysis of the 2.1.x stream shows:

| Product Version | Build Tag | quinn-proto Version | Affected? |
|----------------|-----------|---------------------|-----------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |
