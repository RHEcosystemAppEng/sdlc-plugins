# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (vulnerable) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (vulnerable) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (patched) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (patched) |

## Stream Impact Summary

| Stream | Affected? | Affected Versions | Shipped h2 Version |
|--------|-----------|-------------------|--------------------|
| 2.1.x | YES | 2.1.0, 2.1.1 | 0.4.5 (all versions) |
| 2.2.x | NO | _(none)_ | 0.4.8+ (fixed from first release) |

**Mixed impact**: The 2.1.x stream ships h2 0.4.5, which is vulnerable (below the 0.4.8 fix threshold). The 2.2.x stream ships h2 0.4.8 or later in all versions, meaning it was never affected -- the patched h2 version was adopted before 2.2.0 was built.

## Dependency Chain

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo
  Lock file: Cargo.lock

  2.1.x stream: h2 0.4.5 shipped in all versions (v0.3.8, v0.3.12)
  2.2.x stream: h2 0.4.8 shipped from first version (v0.4.5 tag onward)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.1.x | Cargo | release/0.3.z | h2 >= 0.4.8 | Needs upstream backport |
| 2.2.x | Cargo | release/0.4.z | h2 >= 0.4.8 | Already fixed (ships 0.4.8+) |

The 2.2.x stream already includes the fix in all released versions. Remediation is needed only for the 2.1.x stream.
