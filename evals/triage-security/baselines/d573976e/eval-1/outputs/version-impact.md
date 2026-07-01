# Step 2 -- Version Impact Analysis

## 2.1 -- Load the Supportability Matrix

Loaded from local security-matrix.md files for both configured streams.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.2 -- Detect the Development Stream

(Simulated -- in a real triage, the skill would call `getJiraIssueTypeMetaWithFields`
to discover unreleased Jira versions matching prefix RHTPA and identify the
development stream. For this eval, development stream detection is noted but not
executed against live Jira.)

## 2.3 -- Extract Dependency Versions

Extracting quinn-proto versions from Cargo.lock at each pinned commit tag.
Using enriched fix threshold from Step 1.5: **0.11.14** (versions < 0.11.14 are affected).

### Lock file inspection results (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`):

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | `v0.3.12` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.0 | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1: 0.11.12) |
| 2.2.3 | `v0.4.11` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (at fix threshold) |
| 2.2.4 | `v0.4.12` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (at fix threshold) |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

### Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1)
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are NOT affected (ship quinn-proto 0.11.14 which meets the fix threshold)

## 2.3.5 -- Dependency Chain Context

Dependency chain for quinn-proto:

The quinn-proto crate is a Cargo (Rust) source dependency. Based on the Ecosystem
Mappings, it is tracked via `Cargo.lock` in the `backend` repository (rhtpa-backend).

```
Dependency chain for quinn-proto (Cargo):
  rhtpa-backend (workspace) -> quinn -> quinn-proto
  Profile: production (quinn is a runtime dependency for QUIC transport)

  Present in: all versions from 2.1.0 onward
  Updated from 0.11.9 -> 0.11.12 between v0.4.5 and v0.4.8
  Updated from 0.11.12 -> 0.11.14 between v0.4.8 and v0.4.11
```

## 2.5 -- Upstream Fix Check

Upstream fix status (simulated -- in a real triage, the skill would run
`git show <upstream-branch>:Cargo.lock` to check current upstream state):

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | (would check HEAD of release/0.3.z for quinn-proto version) |
| 2.2.x | Cargo | release/0.4.z | versions 2.2.3+ already ship 0.11.14 -- fix is in upstream |

The upstream fix PR is https://github.com/quinn-rs/quinn/pull/2048.

Since versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14, the fix has been
incorporated in the release/0.4.z branch. However, versions 2.2.0, 2.2.1, and 2.2.2
were released before the fix was available, so the affected product releases shipped
the vulnerable version.

**Proposed action**: Present this version impact table to the engineer for review
and confirmation before proceeding to Step 3.
