# Version Impact Analysis — TC-8002 (CVE-2026-28940)

## Step 2.1 — Supportability Matrix

Loaded matrix data from two version streams.

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

Fix threshold: serde_json < 1.0.135 (versions before 1.0.135 are vulnerable).

### serde_json versions by pinned commit

| Tag | serde_json version | Compared to fix threshold (< 1.0.135) |
|-----|--------------------|----------------------------------------|
| `v0.3.8` (2.1.0) | 1.0.137 | >= 1.0.135 — NOT vulnerable |
| `v0.3.12` (2.1.1) | 1.0.137 | >= 1.0.135 — NOT vulnerable |
| `v0.4.5` (2.2.0) | 1.0.138 | >= 1.0.135 — NOT vulnerable |
| `v0.4.8` (2.2.1) | 1.0.138 | >= 1.0.135 — NOT vulnerable |
| `v0.4.9` (2.2.2) | _(retag of v0.4.8)_ | same as 2.2.1 — NOT vulnerable |
| `v0.4.11` (2.2.3) | 1.0.139 | >= 1.0.135 — NOT vulnerable |
| `v0.4.12` (2.2.4) | 1.0.139 | >= 1.0.135 — NOT vulnerable |

## Step 2.4 — Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | **NO** | Ships patched version |
| 2.1.1 | 2.1.x | 1.0.137 | **NO** | Ships patched version |
| 2.2.0 | 2.2.x | 1.0.138 | **NO** | Ships patched version |
| 2.2.1 | 2.2.x | 1.0.138 | **NO** | Ships patched version |
| 2.2.2 | 2.2.x | -- | **NO** | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | **NO** | Ships patched version |
| 2.2.4 | 2.2.x | 1.0.139 | **NO** | Ships patched version |

**Result: NO supported versions are affected.**

All supported versions ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerable version range (< 1.0.135) is not present in any supported product version.

## Step 2.5 — Upstream Fix Check

Not applicable. Since no supported versions are affected (all ship the fixed version already), upstream fix status is moot. No remediation tasks will be created.
