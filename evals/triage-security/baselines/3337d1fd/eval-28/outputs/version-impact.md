# Step 2 -- Version Impact Analysis

## Version Impact Table

Issue stream scope: **2.2.x** (from suffix `[rhtpa-2.2]`)

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | Stream | backend Tag | h2 Version | Affected? | Notes |
|---------|--------|-------------|------------|-----------|-------|
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.4 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.4 | YES | |
| 2.2.2 | 2.2.x | `v0.4.8` | 0.4.4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.5 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.5 | NO | |

**Summary**: 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).
Versions 2.2.3 and 2.2.4 already ship h2 0.4.5, which is at or above the fix threshold.

## Cross-Stream Impact Check

Since this issue is scoped to the 2.2.x stream, other streams were checked for
cross-stream impact (Case B):

| Version | Stream | backend Tag | h2 Version | Affected? | Notes |
|---------|--------|-------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | NO | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | NO | |

The 2.1.x stream is **not affected** -- all versions ship h2 0.4.5 which is at or
above the fix threshold. No cross-stream remediation tasks are needed.

## Dependency Chain Context (Step 2.3.5)

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

**Lock file evidence (affected versions 2.2.0 through 2.2.2):**
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

**Lock file evidence (fixed versions 2.2.3+):**
```
[[package]]
name = "h2"
version = "0.4.5"
```

### Remediation Context

h2 is a **transitive** dependency (3 levels deep: reqwest -> hyper -> h2). This
means a straightforward `cargo add h2@0.4.5` in Cargo.toml is the fallback, not the
preferred approach. The two-tier remediation strategy applies:

1. **Preferred**: Bump the direct dependency `reqwest` to a version whose transitive
   closure includes h2 >= 0.4.5. This requires checking whether a newer reqwest release
   (or a hyper release that reqwest depends on) pulls in the fixed h2 version.

2. **Fallback**: If no reqwest/hyper release is available with the fixed h2, pin h2
   directly via `cargo add h2@0.4.5` to override the transitive resolution.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Fixed in versions 2.2.3+ (h2 0.4.5) |

The upstream fix is already present on the release/0.4.z branch for versions 2.2.3
onward. Versions 2.2.0 through 2.2.2 shipped before the fix was incorporated.
Since these are already-released versions, remediation consists of ensuring the fix
is available and propagated, but the affected versions (2.2.0-2.2.2) have already
been superseded by 2.2.3+ which include the fix.
