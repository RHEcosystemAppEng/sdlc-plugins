# Step 2 – Version Impact Analysis: CVE-2026-31812 (quinn-proto < 0.11.14)

## 2.1 – Supportability Matrix (aggregated)

Both matrices passed format validation: all required sections are present and the Ecosystem Mappings columns match the template.

| Stream | Version | Build | backend tag |
|--------|---------|-------|-------------|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 (backend retag of 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 |

## 2.2 – Development Stream

Unreleased Jira versions were not available, because this eval makes no Jira calls. No development-stream lock file data was provided, so no development stream (branch HEAD) row is included. This must be confirmed against Jira `getJiraIssueTypeMetaWithFields` before any real mutation.

## 2.3 – Lock File Extraction (Cargo, `Cargo.lock`)

The data comes from simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` output at the pinned backend tags.

## 2.4 – Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14):

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | In scope |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | In scope |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | Same as 2.2.1 (backend retag of 2.2.1, lock check skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Ships fixed version |

**Summary**
- In-scope (2.2.x) affected versions: **2.2.0, 2.2.1, 2.2.2**. The fix already shipped in 2.2.3 (backend v0.4.11) and is still present in 2.2.4.
- Out-of-scope affected stream: **2.1.x** (2.1.0 and 2.1.1, both quinn-proto 0.11.9). The fix has not shipped in any 2.1.x release.
- PSIRT's Affects Versions value (`RHTPA 2.0.0`) is wrong. There is no 2.0.x stream in the supportability matrix.

## 2.3.5 – Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn-proto
  Type: not determinable from provided evidence (the mock data includes only
        Cargo.lock version lines, not dependency graph / Cargo.toml). Most
        likely transitive (e.g., via quinn / an HTTP/3-capable client such as reqwest).
  Profile: assumed production (no evidence of dev-only/build-only scope)
  Present in: all supported versions (2.1.0 onward)
  Fixed in: backend v0.4.11 (2.2.3), quinn-proto 0.11.12 → 0.11.14
```

Remediation approach: bump the direct dependency that pulls in quinn-proto (or `cargo update -p quinn-proto --precise 0.11.14`) so that quinn-proto is at least 0.11.14. Before creating remediation tasks, verify the direct vs transitive classification with `cargo tree -i quinn-proto` at the pinned commit.

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not provided (latest tag v0.3.12 = 0.11.9) | NO (presumed, needs verification) |
| 2.2.x | Cargo | release/0.4.z | not provided (tags v0.4.11 and v0.4.12 = 0.11.14) | YES (fix tagged in v0.4.11 and released in 2.2.3) |

Remediation path:
- **2.2.x**: the fix is already upstream and already propagated downstream (2.2.3 and 2.2.4 ship quinn-proto 0.11.14). The stream needs no new code change. Affected versions 2.2.0 through 2.2.2 are remediated by upgrading to 2.2.3 or later.
- **2.1.x**: the fix is not upstream. This needs an upstream backport (bump quinn-proto to 0.11.14 or later on `release/0.3.z`), followed by downstream propagation in `rhtpa-release.0.3.z`.

The engineer should review and confirm this table before Step 3. Eval run: confirmed.
