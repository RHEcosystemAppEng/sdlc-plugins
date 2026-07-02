# Version Impact Analysis -- TC-8002

## CVE-2026-28940: serde_json (affected: versions before 1.0.135, fixed: 1.0.135)

## Step 2.1 -- Supportability Matrix

Loaded from security-matrix-mock.md. Both streams aggregated:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 |

## Step 2.3 -- Dependency Version Extraction

Ecosystem: Cargo
Lock file: Cargo.lock
Fix threshold: serde_json >= 1.0.135

Simulated `git show <tag>:Cargo.lock` results for serde_json:

| Tag | serde_json version | Comparison to fix (1.0.135) |
|-----|--------------------|-----------------------------|
| v0.3.8 | 1.0.137 | 1.0.137 >= 1.0.135 -- PATCHED |
| v0.3.12 | 1.0.137 | 1.0.137 >= 1.0.135 -- PATCHED |
| v0.4.5 | 1.0.138 | 1.0.138 >= 1.0.135 -- PATCHED |
| v0.4.8 | 1.0.138 | 1.0.138 >= 1.0.135 -- PATCHED |
| v0.4.9 | _(retag of v0.4.8)_ | same as v0.4.8 -- PATCHED |
| v0.4.11 | 1.0.139 | 1.0.139 >= 1.0.135 -- PATCHED |
| v0.4.12 | 1.0.139 | 1.0.139 >= 1.0.135 -- PATCHED |

## Step 2.4 -- Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | ships patched version |
| 2.1.1 | 2.1.x | 1.0.137 | NO | ships patched version |
| 2.2.0 | 2.2.x | 1.0.138 | NO | ships patched version |
| 2.2.1 | 2.2.x | 1.0.138 | NO | ships patched version |
| 2.2.2 | 2.2.x | 1.0.138 | NO | retag of 2.2.1; ships patched version |
| 2.2.3 | 2.2.x | 1.0.139 | NO | ships patched version |
| 2.2.4 | 2.2.x | 1.0.139 | NO | ships patched version |

**Result: NO supported versions are affected.** All versions across all streams ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerable version of serde_json was never shipped in any supported product release.

## Step 2.3.5 -- Dependency Chain Context

Not applicable -- no versions are affected. Dependency chain tracing is only performed for affected versions to inform remediation planning.

## Step 2.5 -- Upstream Fix Status

Not applicable -- since no versions are affected, upstream fix status does not change the triage outcome. For completeness, all versions already ship the fix.
