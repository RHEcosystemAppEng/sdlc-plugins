<!-- SYNTHETIC TEST DATA — mock security-matrix.md files for two version streams for triage-security eval testing -->

# Stream 1: rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

## Forward Pointer

Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`

---

# Stream 2: rhtpa-release.0.4.z (2.2.x stream)

## Version Stream

This Konflux release repo covers the **2.2.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

## Forward Pointer

This is the latest stream — no forward pointer.

---

# Mock Lock File Data

The following sections provide the dependency versions that would be extracted
by running `git show <tag>:Cargo.lock | grep -A2 'name = "<library>"'` for
each pinned commit. In a real triage, the skill runs these commands; in this
eval, use this data as the simulated output.

## quinn-proto versions by tag

| Tag | quinn-proto version |
|-----|---------------------|
| `v0.3.8` | 0.11.9 |
| `v0.3.12` | 0.11.9 |
| `v0.4.5` | 0.11.9 |
| `v0.4.8` | 0.11.12 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 0.11.14 |
| `v0.4.12` | 0.11.14 |

## serde_json versions by tag

| Tag | serde_json version |
|-----|--------------------|
| `v0.3.8` | 1.0.137 |
| `v0.3.12` | 1.0.137 |
| `v0.4.5` | 1.0.138 |
| `v0.4.8` | 1.0.138 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 1.0.139 |
| `v0.4.12` | 1.0.139 |

## h2 versions by tag

| Tag | h2 version |
|-----|------------|
| `v0.3.8` | 0.4.5 |
| `v0.3.12` | 0.4.5 |
| `v0.4.5` | 0.4.8 |
| `v0.4.8` | 0.4.8 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 0.4.9 |
| `v0.4.12` | 0.4.9 |
