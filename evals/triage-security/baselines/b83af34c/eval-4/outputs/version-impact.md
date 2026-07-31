# Version Impact Analysis — TC-8004

## Step 2: Version Impact Table

CVE-2026-33501 affects h2 versions before 0.4.8 (fixed in 0.4.8).

Because the issue is **unscoped** (no stream suffix in summary), all versions across all configured streams are analyzed.

### Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | Source Tag | h2 version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | 2.2.x | `v0.4.9` | — | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 (above fix threshold) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 (above fix threshold) |

### Stream-level Summary

| Stream | Versions Checked | Affected? | h2 versions shipped |
|--------|-----------------|-----------|---------------------|
| 2.1.x | 2.1.0, 2.1.1 | **YES** — all versions affected | 0.4.5 (both versions) |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NO** — no versions affected | 0.4.8+ (at or above fix threshold) |

**Mixed impact across streams**: The 2.1.x stream ships h2 0.4.5 (vulnerable), while the 2.2.x stream ships h2 0.4.8+ (patched). Remediation is needed only for the 2.1.x stream.

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> h2
  Type: direct dependency (h2 is listed in Cargo.lock as a direct workspace dependency)
  Profile: production (h2 is a runtime HTTP/2 dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.lock on release/0.3.z branch
```

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 shipped | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 0.4.5 | **NO** — upstream backport needed |
| 2.2.x | Cargo | `release/0.4.z` | 0.4.8+ | **YES** — already ships patched version |

The 2.2.x stream's upstream branch already includes h2 >= 0.4.8. The 2.1.x stream's upstream branch (`release/0.3.z`) still ships h2 0.4.5 and requires a backport.
