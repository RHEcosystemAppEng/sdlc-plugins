# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Issue status | In Progress |
| Assignee | engineer-a@example.com |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in Security Configuration (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table in `security-matrix.md` lists **Cargo** as a supported ecosystem with:

- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem: **Cargo** (source dependency)

## Existing Comments on Issue

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` -- posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security
2. **Post-triage summary comment**: Documents version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), actions taken (Affects Versions corrected, ai-cve-triaged label added, remediation tasks TC-8100 and TC-8101 created, transitioned to In Progress) -- posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security

## Existing Issue Links

| Link Type | Linked Issue | Summary | Status |
|-----------|-------------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

TC-8101 is blocked by TC-8100 (upstream backport must merge first).

## Remote Links

| Title | URL |
|-------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Version Impact Table (from security-matrix mock data)

Based on the mock lock file data for quinn-proto across the 2.2.x stream:

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| RHTPA 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8, quinn-proto 0.11.12) |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

Cross-stream check (2.1.x stream, outside issue scope):

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
