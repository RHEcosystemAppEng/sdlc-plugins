# Version Impact Analysis — TC-8002

## Step 2.1 — Supportability Matrix

Loaded from two streams configured in Version Streams table:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Step 2.3 — Dependency Version Extraction

Ecosystem: Cargo
Lock file: `Cargo.lock`
Vulnerable library: serde_json
Fix threshold: >= 1.0.135 (versions before 1.0.135 are affected)

Simulated `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'` results:

| Tag | Version (pinned commit) | serde_json version found |
|-----|-------------------------|--------------------------|
| `v0.3.8` | 2.1.0 | 1.0.137 |
| `v0.3.12` | 2.1.1 | 1.0.137 |
| `v0.4.5` | 2.2.0 | 1.0.138 |
| `v0.4.8` | 2.2.1 | 1.0.138 |
| `v0.4.9` | 2.2.2 | _(retag of v0.4.8 = 1.0.138)_ |
| `v0.4.11` | 2.2.3 | 1.0.139 |
| `v0.4.12` | 2.2.4 | 1.0.139 |

## Step 2.4 — Version Impact Table

Version Impact for CVE-2026-28940 (serde_json versions before 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | 1.0.137 >= 1.0.135 (fix threshold) |
| 2.1.1 | 2.1.x | 1.0.137 | NO | 1.0.137 >= 1.0.135 (fix threshold) |
| 2.2.0 | 2.2.x | 1.0.138 | NO | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.1 | 2.2.x | 1.0.138 | NO | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.2 | 2.2.x | 1.0.138 | NO | retag of 2.2.1; same as 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | NO | 1.0.139 >= 1.0.135 (fix threshold) |
| 2.2.4 | 2.2.x | 1.0.139 | NO | 1.0.139 >= 1.0.135 (fix threshold) |

**Result: NO supported versions are affected.** All versions across all streams ship serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerable version range (before 1.0.135) is not present in any supported version.

## Step 2.5 — Upstream Fix Check

Since no versions are affected, upstream fix checking is informational only. All streams already ship the fixed version.

| Stream | Ecosystem | Upstream Branch | Earliest shipped version | Fixed? |
|--------|-----------|-----------------|--------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 1.0.137 | YES (already ships fixed version) |
| 2.2.x | Cargo | release/0.4.z | 1.0.138 | YES (already ships fixed version) |

**Conclusion**: The vulnerability in serde_json (versions before 1.0.135) does not affect any supported product version. Every version in the supportability matrix ships serde_json 1.0.137 or later, which is above the fix threshold of 1.0.135.
