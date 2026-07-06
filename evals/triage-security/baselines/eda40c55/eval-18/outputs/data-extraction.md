# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote link: https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote link: https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | CVE-2026-31812 | Remote link: https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 | Jira `duedate` field |
| Assignee | engineer-a@example.com | Jira `assignee` field |
| Issue status | In Progress | Jira `status` field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: 2.2.x -> rhtpa-release.0.4.z)
- Issue is **stream-scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Source repository: rhtpa-backend

## Existing Comments

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. **Post-triage summary comment**: Documents triage completion, version impact, actions taken including Affects Versions correction, label addition, remediation task creation, and status transition (posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security)

## Existing Issue Links

| Link Type | Target | Summary | Status |
|-----------|--------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

TC-8101 blocks TC-8100 (downstream propagation depends on upstream backport).

## Version Impact (from security-matrix mock data, stream 2.2.x)

| Version | Build Tag | quinn-proto version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | v0.4.9 | (retag of v0.4.8 = 0.11.12) | YES (< 0.11.14) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (= 0.11.14, fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (= 0.11.14, fixed) |

Conclusion: RHTPA 2.2.0 and 2.2.1 are affected. RHTPA 2.2.2 ships the same source as 2.2.1 (retag) so is also affected. RHTPA 2.2.3 and 2.2.4 ship the fixed version.
