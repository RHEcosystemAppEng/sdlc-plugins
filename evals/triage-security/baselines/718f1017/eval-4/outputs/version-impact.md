# Step 2 -- Version Impact Analysis: TC-8004

## 2.1 -- Supportability Matrix

Loaded from two configured Version Streams:

- **2.1.x stream**: `security-matrix.md` at rhtpa-release.0.3.z (Local Path: /home/dev/repos/rhtpa-release.0.3.z)
- **2.2.x stream**: `security-matrix.md` at rhtpa-release.0.4.z (Local Path: /home/dev/repos/rhtpa-release.0.4.z)

## 2.3 -- Dependency Version Extraction

Ecosystem: **Cargo** (h2 is a Rust crate)
Lock file: `Cargo.lock`
Fix threshold (enriched from Step 1.5): **0.4.8**

Extracted h2 versions from lock files at pinned commits:

| Stream | Version | Tag | h2 version | Command |
|--------|---------|-----|------------|---------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | `git show v0.3.8:Cargo.lock \| grep -A2 'name = "h2"'` |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | `git show v0.3.12:Cargo.lock \| grep -A2 'name = "h2"'` |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | `git show v0.4.5:Cargo.lock \| grep -A2 'name = "h2"'` |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | `git show v0.4.8:Cargo.lock \| grep -A2 'name = "h2"'` |
| 2.2.x | 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | skipped -- retag of 2.2.1 |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | `git show v0.4.11:Cargo.lock \| grep -A2 'name = "h2"'` |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | `git show v0.4.12:Cargo.lock \| grep -A2 'name = "h2"'` |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Stream | Version | h2 version | Affected? | Notes |
|--------|---------|------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.2 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

**Summary**: The 2.1.x stream is **affected** -- all versions (2.1.0, 2.1.1) ship h2 0.4.5 which is below the fix threshold of 0.4.8. The 2.2.x stream is **NOT affected** -- all versions ship h2 >= 0.4.8 (the fixed version).

This is a **mixed impact across streams**: 2.1.x versions ship the vulnerable dependency while 2.2.x versions ship a patched version.

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime dependency used for HTTP/2 support)

  Present in: all versions across both streams
  Affected in: 2.1.x only (ships h2 0.4.5)
  Already fixed in: 2.2.x (ships h2 >= 0.4.8)
```

h2 is a transitive dependency pulled in through hyper (HTTP library). It is a production dependency -- not dev-only.

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | h2 at branch HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | needs inspection | Unknown -- requires `git show release/0.3.z:Cargo.lock` |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (per latest tag v0.4.12) | YES (already ships fixed version) |

For the 2.1.x stream, the upstream branch `release/0.3.z` needs to be checked at HEAD to determine if the fix has already been backported. The remediation task for 2.1.x will cover bumping h2 to >= 0.4.8 on the `release/0.3.z` branch.

For the 2.2.x stream, no remediation is needed -- all released versions already ship h2 >= 0.4.8.
