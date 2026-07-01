# Step 2 -- Version Impact Analysis

## 2.1 -- Load the Supportability Matrix

Loaded security-matrix.md for both configured version streams:

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

All versions across both streams are included in the aggregated matrix (Important Rule 4: check ALL supported versions).

## 2.2 -- Detect the Development Stream

(Simulated -- in a real triage, this would query Jira for unreleased versions filtered by the RHTPA prefix.)

## 2.3 -- Extract Dependency Versions

For each version, the h2 dependency version is extracted from `Cargo.lock` at the pinned commit tag from the supportability matrix. The fix threshold is **h2 0.4.8** (versions before 0.4.8 are affected).

**Stream 2.1.x:**

- **Version 2.1.0** (tag `v0.3.8`):
  `git show v0.3.8:Cargo.lock | grep -A2 'name = "h2"'` -> h2 version **0.4.5**
  Comparison: 0.4.5 < 0.4.8 -> **AFFECTED**

- **Version 2.1.1** (tag `v0.3.12`):
  `git show v0.3.12:Cargo.lock | grep -A2 'name = "h2"'` -> h2 version **0.4.5**
  Comparison: 0.4.5 < 0.4.8 -> **AFFECTED**

**Stream 2.2.x:**

- **Version 2.2.0** (tag `v0.4.5`):
  `git show v0.4.5:Cargo.lock | grep -A2 'name = "h2"'` -> h2 version **0.4.8**
  Comparison: 0.4.8 >= 0.4.8 -> **NOT AFFECTED**

- **Version 2.2.1** (tag `v0.4.8`):
  `git show v0.4.8:Cargo.lock | grep -A2 'name = "h2"'` -> h2 version **0.4.8**
  Comparison: 0.4.8 >= 0.4.8 -> **NOT AFFECTED**

- **Version 2.2.2** (tag `v0.4.9`):
  Retag of 2.2.1 (identical source commits). Carrying forward result from 2.2.1 -> **NOT AFFECTED** (same as 2.2.1)

- **Version 2.2.3** (tag `v0.4.11`):
  `git show v0.4.11:Cargo.lock | grep -A2 'name = "h2"'` -> h2 version **0.4.9**
  Comparison: 0.4.9 >= 0.4.8 -> **NOT AFFECTED**

- **Version 2.2.4** (tag `v0.4.12`):
  `git show v0.4.12:Cargo.lock | grep -A2 'name = "h2"'` -> h2 version **0.4.9**
  Comparison: 0.4.9 >= 0.4.8 -> **NOT AFFECTED**

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | pinned at v0.3.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | pinned at v0.3.12 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fix version |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fix version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | ships post-fix version |
| 2.2.4 | 2.2.x | 0.4.9 | NO | ships post-fix version |

**Summary**: Stream 2.1.x is AFFECTED (all versions ship h2 0.4.5 which is < 0.4.8). Stream 2.2.x is NOT AFFECTED (all versions ship h2 >= 0.4.8).

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime dependency)

  Stream 2.1.x: h2 0.4.5 (affected) -- present in all versions
  Stream 2.2.x: h2 0.4.8+ (not affected) -- updated in v0.4.5 build
```

h2 is a transitive dependency pulled in through hyper (the HTTP library). Since hyper is a production runtime dependency, the vulnerable h2 code is in the execute path.

## 2.5 -- Upstream Fix Check

For the affected stream (2.1.x), check whether the upstream source repository has already fixed the vulnerability on the `release/0.3.z` branch:

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (would need git show) | TBD |
| 2.2.x | Cargo | release/0.4.z | 0.4.8+ | YES (already ships fix) |

For stream 2.1.x, the upstream branch `release/0.3.z` would need to be checked at HEAD to determine whether the fix has already been applied upstream. In a real triage, this would run:
```
git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock | grep -A2 'name = "h2"'
```

This determines whether the remediation task is an upstream-first backport or a downstream-only reference update.

**Proposed action**: Present this version impact table to the engineer for confirmation before proceeding to Step 3.
