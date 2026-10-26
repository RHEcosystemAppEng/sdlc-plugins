# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 external CVE data enrichment:
- **Affected range**: h2 < 0.4.8
- **First fixed version**: h2 0.4.8
- **Source**: MITRE CVE API + OSV.dev (cross-validated, high confidence)

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Backend Tag | h2 version | Affected? | Notes |
|--------|---------|-------------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Impact Summary by Stream

| Stream | Versions Affected | Versions Not Affected | Assessment |
|--------|-------------------|----------------------|------------|
| 2.1.x | 2.1.0, 2.1.1 (all) | -- | **All versions affected** |
| 2.2.x | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 (all) | **No versions affected** |

## Issue Stream Scope: 2.2.x

The issue TC-8030 is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).

**Within the scoped stream (2.2.x)**: No versions are affected. All versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Cross-stream impact**: Stream **2.1.x** is affected (both versions 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8).

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock

For 2.1.x (affected): h2 0.4.5 is present in Cargo.lock at tags v0.3.8 and v0.3.12
For 2.2.x (not affected): h2 0.4.8+ is present in Cargo.lock at all tags
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Affected -- h2 0.4.5 at pinned tags |
| 2.2.x | Cargo | release/0.4.z | Not affected -- h2 >= 0.4.8 at all pinned tags |
