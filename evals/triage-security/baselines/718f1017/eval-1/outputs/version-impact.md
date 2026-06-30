# Step 2 — Version Impact Analysis for CVE-2026-31812

## 2.1 — Supportability Matrix

Loaded from two configured Version Streams:

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

## 2.2 — Development Stream Detection

Not performed in this eval (requires live Jira API call to discover unreleased versions).

## 2.3 — Dependency Version Extraction

Ecosystem: Cargo. Lock file: `Cargo.lock`. Library: quinn-proto.
Fix threshold: 0.11.14 (from Jira description; external CVE data enrichment skipped per eval constraints).

Extracted quinn-proto versions from `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`:

| Version | Tag | quinn-proto | Affected? (< 0.11.14) | Notes |
|---------|-----|-------------|------------------------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | **YES** | |
| 2.1.1 | `v0.3.12` | 0.11.9 | **YES** | |
| 2.2.0 | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.1 | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.2 | `v0.4.9` | — | **YES** | retag of 2.2.1 (same as 2.2.1: quinn-proto 0.11.12) |
| 2.2.3 | `v0.4.11` | 0.11.14 | **NO** | ships fixed version |
| 2.2.4 | `v0.4.12` | 0.11.14 | **NO** | ships fixed version |

## 2.3.5 — Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → quinn → quinn-proto
  Ecosystem: Cargo (source dependency — Rust crate)
  Profile: production (quinn is a runtime dependency)

  Present in all versions checked (2.1.0 through 2.2.4).
  Fix was applied between v0.4.8 (0.11.12) and v0.4.11 (0.11.14).
```

Since this is a source dependency (Cargo ecosystem), remediation requires two tasks:
1. Upstream backport task (fix in rhtpa-backend source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

## 2.4 — Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | — | **YES** | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | **NO** | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | **NO** | ships fixed version |

**Summary**: Versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are NOT affected.

## 2.5 — Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | Upstream fix check requires live git access (skipped in eval) |
| 2.2.x | Cargo | `release/0.4.z` | Versions 2.2.3+ already ship 0.11.14 — fix was already picked up on this branch |

Based on the supportability matrix, the fix (quinn-proto 0.11.14) was incorporated starting with tag `v0.4.11` (version 2.2.3), indicating the upstream branch `release/0.4.z` already has the fix.

## Cross-Stream Impact

This issue is scoped to stream 2.2.x, but the version impact analysis shows that stream 2.1.x (versions 2.1.0, 2.1.1) is also affected. This triggers Case B (cross-stream impact) in Step 7.
