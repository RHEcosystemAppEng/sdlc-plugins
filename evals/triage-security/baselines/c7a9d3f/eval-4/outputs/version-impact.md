# Step 2 -- Version Impact Analysis: TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

### Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | `v0.4.9` | _(retag)_ | NO | same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | >= 0.4.8 (fixed) |

### Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Status |
|--------|-------------------|---------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **All versions affected** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **No versions affected** |

### Mixed Impact Across Streams

This CVE exhibits **mixed impact** across version streams:

- **2.1.x stream**: All versions ship h2 0.4.5, which is below the fix threshold (0.4.8). Both 2.1.0 and 2.1.1 are **affected**.
- **2.2.x stream**: All versions ship h2 >= 0.4.8 (the fixed version). The earliest 2.2.x version (2.2.0) already ships h2 0.4.8. No 2.2.x versions are affected.

The 2.2.x stream was never vulnerable because the backend source tag `v0.4.5` (used for 2.2.0) already included h2 0.4.8 in its Cargo.lock.

### Dependency Chain Context

```
Dependency chain for h2 (Cargo ecosystem):
  backend (workspace) -> hyper -> h2
  Lock file: Cargo.lock
  Ecosystem: Cargo (source dependency)

  2.1.x stream: h2 0.4.5 pinned across all versions (v0.3.8, v0.3.12)
  2.2.x stream: h2 0.4.8+ pinned from first version (v0.4.5 onward)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | h2 >= 0.4.8 | Needs upstream backport |
| 2.2.x | Cargo | `release/0.4.z` | h2 >= 0.4.8 | Already fixed (ships 0.4.8+) |

The 2.2.x stream's upstream branch `release/0.4.z` already ships h2 >= 0.4.8. The 2.1.x stream's upstream branch `release/0.3.z` needs h2 bumped from 0.4.5 to >= 0.4.8.
