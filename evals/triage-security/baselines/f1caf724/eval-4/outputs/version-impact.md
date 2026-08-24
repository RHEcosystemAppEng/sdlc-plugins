# Version Impact Analysis -- CVE-2026-33501

## Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | Build Tag | h2 Version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Versions Affected | Versions Not Affected | Stream Status |
|--------|-------------------|-----------------------|---------------|
| 2.1.x | 2.1.0, 2.1.1 (all versions) | -- | **AFFECTED** -- all versions ship h2 0.4.5 |
| 2.2.x | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 (all versions) | **NOT AFFECTED** -- all versions ship h2 >= 0.4.8 |

## Mixed Impact Analysis

This is a **mixed impact** scenario across streams:

- **2.1.x stream**: All versions ship h2 0.4.5, which is vulnerable (< 0.4.8). The fix was never picked up on the `release/0.3.z` upstream branch. Remediation is required for this stream.
- **2.2.x stream**: The first version (2.2.0) already ships h2 0.4.8 (the exact fix version). All subsequent versions ship 0.4.8 or later. No remediation needed for this stream.

The vulnerability was effectively fixed in the 2.2.x stream from the beginning (v0.4.5 build tag ships h2 0.4.8), but the 2.1.x stream never received the fix because its upstream branch (`release/0.3.z`) pins an older version of h2.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock

  Stream 2.1.x: h2 0.4.5 shipped in all versions (v0.3.8, v0.3.12)
  Stream 2.2.x: h2 0.4.8+ shipped in all versions (v0.4.5 onward)

Remediation for 2.1.x: bump h2 to >= 0.4.8 on release/0.3.z branch
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 Version (from lock data) | Fixed? |
|--------|-----------|-----------------|----------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | **NO** -- upstream branch still ships vulnerable version |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | **YES** -- upstream branch ships fixed version |

The 2.1.x upstream branch (`release/0.3.z`) has NOT been fixed upstream. Remediation requires an upstream PR to bump h2 on `release/0.3.z`, followed by a downstream Konflux release repo update.
