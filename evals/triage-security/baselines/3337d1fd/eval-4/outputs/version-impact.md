# Version Impact Analysis -- TC-8004

## CVE-2026-33501: h2 (versions before 0.4.8)

Fixed version: 0.4.8

### Version Impact Table

| Version | Stream | Source Tag | h2 Version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | `v0.4.8` | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | >= 0.4.8 (fixed) |

### Stream-Level Summary

| Stream | Affected Versions | Not Affected Versions | Impact |
|--------|-------------------|-----------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **ALL versions affected** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NO versions affected** |

### Mixed Impact Across Streams

This CVE exhibits **mixed impact**: the 2.1.x stream ships h2 0.4.5 (vulnerable), while the 2.2.x stream ships h2 0.4.8 or later (patched). The fix was picked up in the 2.2.x stream starting from version 2.2.0 (source tag v0.4.5, which ships h2 0.4.8).

### Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> h2
  Type: direct dependency (present in Cargo.lock for backend workspace)
  Profile: production (h2 is a runtime HTTP/2 dependency)
  Ecosystem: Cargo

  Stream 2.1.x: h2 0.4.5 at all versions (v0.3.8, v0.3.12)
  Stream 2.2.x: h2 0.4.8+ at all versions (v0.4.5 onward)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml on release/0.3.z branch
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | Needs upstream backport -- h2 0.4.5 shipped, fix requires bump to >= 0.4.8 |
| 2.2.x | Cargo | `release/0.4.z` | Already fixed -- h2 0.4.8+ shipped since 2.2.0 |
