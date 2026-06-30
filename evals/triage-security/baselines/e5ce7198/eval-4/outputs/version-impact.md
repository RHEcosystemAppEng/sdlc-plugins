# Version Impact Analysis -- TC-8004

## Step 2 -- Version Impact for CVE-2026-33501 (h2 < 0.4.8)

### 2.1 -- Supportability Matrix

Two version streams loaded from Security Configuration:

- **2.1.x** stream: rhtpa-release.0.3.z (2 versions)
- **2.2.x** stream: rhtpa-release.0.4.z (5 versions)

### 2.3 -- Dependency Version Extraction

Lock file data extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` for each pinned commit:

| Stream | Version | Tag | h2 version | Affected? | Notes |
|--------|---------|-----|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Stream Impact Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | **YES** | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is below the fix threshold 0.4.8 |
| 2.2.x | NO | All versions ship h2 >= 0.4.8 (fix threshold). 2.2.0 and 2.2.1 ship exactly 0.4.8; 2.2.3+ ship 0.4.9 |

### 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  Ecosystem: Cargo (source dependency)
  h2 is a Rust crate for HTTP/2 protocol handling.
  Likely dependency path: backend (workspace) -> hyper / reqwest -> h2
  Profile: production (h2 is a runtime HTTP/2 dependency)

  Present in: 2.1.x stream (h2 0.4.5, vulnerable)
  Present in: 2.2.x stream (h2 >= 0.4.8, already patched)
```

### 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs investigation -- 2.1.x ships h2 0.4.5, upstream branch may not yet have the bump to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- all 2.2.x versions ship h2 >= 0.4.8 |

The 2.1.x stream (release/0.3.z branch) requires remediation. The upstream backport task should bump h2 to >= 0.4.8 on the release/0.3.z branch of the backend repository.
