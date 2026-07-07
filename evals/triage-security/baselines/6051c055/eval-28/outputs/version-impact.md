# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99010 (h2 < 0.4.5)

### 2.2.x Stream (scoped)

| Version | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.4.4 | YES | |
| 2.2.1 | `v0.4.8` | 0.4.4 | YES | |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.4.5 | NO | |
| 2.2.4 | `v0.4.12` | 0.4.5 | NO | |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

### 2.1.x Stream (out of scope -- checked for cross-stream impact)

| Version | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | NO | |
| 2.1.1 | `v0.3.12` | 0.4.5 | NO | |

The 2.1.x stream is **not affected** -- all versions ship h2 >= 0.4.5.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Lock file evidence (affected versions -- 2.2.0 through 2.2.2):**
```
[[package]]
name = "h2"
version = "0.4.4"

[[package]]
name = "hyper"
version = "1.4.1"
dependencies = ["h2"]

[[package]]
name = "reqwest"
version = "0.12.5"
dependencies = ["hyper"]
```

**Lock file evidence (fixed versions -- 2.2.3+):**
```
[[package]]
name = "h2"
version = "0.4.5"
```

### Dependency Classification

- **Dependency type**: transitive (not direct)
- **Dependency chain**: backend -> reqwest -> hyper -> h2
- **Depth**: 3 levels
- **Direct dependency that pulls in h2**: reqwest
- **Intermediate dependency**: hyper (between reqwest and h2)
- **Profile**: production -- reqwest is a `[dependencies]` entry (runtime)
- **Remediation complexity**: moderate -- requires bumping reqwest to a version whose transitive closure includes h2 >= 0.4.5, or pinning h2 directly as a fallback

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Fixed at branch HEAD (versions 2.2.3+ already ship h2 0.4.5) |

The upstream source repository already has the fix on the release/0.4.z branch -- versions 2.2.3 and later ship h2 0.4.5 (the fixed version). Remediation for 2.2.0-2.2.2 requires backporting or ensuring customers upgrade to 2.2.3+.

## Cross-Stream Impact

No cross-stream impact detected. The 2.1.x stream ships h2 0.4.5 in all versions and is not affected. Case B (cross-stream proactive remediation) does not apply.
