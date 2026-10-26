# Version Impact Analysis -- TC-8002

## CVE-2026-28940: serde_json (affected versions before 1.0.135)

### Step 2.1 -- Supportability Matrix

Two streams loaded from the security matrix:

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Step 2.3 -- Dependency Version Extraction

Using the mock lock file data for serde_json at each pinned commit:

| Tag | serde_json version | Source |
|-----|--------------------|--------|
| `v0.3.8` | 1.0.137 | Cargo.lock |
| `v0.3.12` | 1.0.137 | Cargo.lock |
| `v0.4.5` | 1.0.138 | Cargo.lock |
| `v0.4.8` | 1.0.138 | Cargo.lock |
| `v0.4.9` | _(retag of v0.4.8)_ | Retag carry-forward |
| `v0.4.11` | 1.0.139 | Cargo.lock |
| `v0.4.12` | 1.0.139 | Cargo.lock |

### Step 2.4 -- Version Impact Table

Fix threshold: serde_json >= 1.0.135 (from CVE description, used as authoritative
since external enrichment was not performed in this eval).

**Version Impact for CVE-2026-28940 (serde_json < 1.0.135):**

| Version | Stream | serde_json version | Affected? | Notes |
|---------|--------|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | >= 1.0.135 (fixed) |
| 2.1.1 | 2.1.x | 1.0.137 | NO | >= 1.0.135 (fixed) |
| 2.2.0 | 2.2.x | 1.0.138 | NO | >= 1.0.135 (fixed) |
| 2.2.1 | 2.2.x | 1.0.138 | NO | >= 1.0.135 (fixed) |
| 2.2.2 | 2.2.x | 1.0.138 | NO | retag of 2.2.1; same as 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | NO | >= 1.0.135 (fixed) |
| 2.2.4 | 2.2.x | 1.0.139 | NO | >= 1.0.135 (fixed) |

**Result: NO supported versions are affected.**

Every version across both streams ships serde_json >= 1.0.137, which is well
above the fix threshold of 1.0.135. The vulnerable range (versions before
1.0.135) does not apply to any shipped version.

### Step 2.5 -- Upstream Fix Check

Since no versions are affected, the upstream fix check is informational only.
All pinned commits and both upstream branches already ship a serde_json version
above the fix threshold:

| Stream | Ecosystem | Upstream Branch | Version at Pinned Commits | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 1.0.137 | YES |
| 2.2.x | Cargo | release/0.4.z | 1.0.138 -- 1.0.139 | YES |

### Dependency Chain Context (Step 2.3.5)

Since no versions are affected (all ship serde_json >= 1.0.135), detailed
dependency chain analysis is not required for remediation purposes. For
reference, serde_json is a core Rust serialization library typically included
as a direct dependency in Cargo.toml.
