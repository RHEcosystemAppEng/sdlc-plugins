# Step 2 -- Version Impact Analysis

## CVE-2026-99010 (h2 < 0.4.5)

### Stream scope: 2.2.x

Source: Konflux release repo `rhtpa-release.0.4.z`

### Version Impact Table

| Version | Build | Tag | h2 version | Affected? | Notes |
|---------|-------|-----|------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.4.4 | **YES** | h2 0.4.4 < 0.4.5 fix threshold |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.4.4 | **YES** | h2 0.4.4 < 0.4.5 fix threshold |
| 2.2.2 | 0.4.9 | `v0.4.8` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.5 | NO | ships fixed version (h2 0.4.5 >= 0.4.5) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.5 | NO | ships fixed version (h2 0.4.5 >= 0.4.5) |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

### Dependency Chain Context (Step 2.3.5)

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

### Remediation context

h2 is a **transitive dependency** -- it is NOT listed in `backend/Cargo.toml`
directly. The full dependency chain is:

```
backend (workspace) -> reqwest (0.12) -> hyper (1.4.1) -> h2 (0.4.4, vulnerable)
```

This means remediation requires a **two-tier approach**:
1. **Preferred**: bump `reqwest` (the direct dependency) to a version whose
   transitive closure includes h2 >= 0.4.5
2. **Fallback**: pin h2 directly via `cargo add h2@0.4.5` to override the
   transitive resolution

### Cross-Stream Impact Check (Case A)

Since the issue is scoped to 2.2.x, checking whether 2.1.x is also affected:

| Version | Tag | h2 version | Affected? | Notes |
|---------|-----|------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | NO | ships fixed version |
| 2.1.1 | `v0.3.12` | 0.4.5 | NO | ships fixed version |

**Result**: 2.1.x stream is NOT affected. No cross-stream impact notice is
required. All 2.1.x versions ship h2 0.4.5, which is at or above the fix
threshold.

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Status | Notes |
|--------|-----------|-----------------|--------|-------|
| 2.2.x | Cargo | `release/0.4.z` | **Fixed** | Versions 2.2.3+ already ship h2 0.4.5 |

Since the upstream branch already ships the fixed version (h2 0.4.5 in 2.2.3+),
remediation uses the **dependency bump** variant (not the upstream backport
variant). The remediation is a `cargo update -p h2` on the `release/0.4.z`
branch to update the lock file, followed by a downstream propagation to the
Konflux release repo.

### Affects Versions Correction (Step 3)

PSIRT-claimed Affects Versions: **RHTPA 2.2.0**

Lock file evidence shows versions 2.2.0, 2.2.1, and 2.2.2 are all affected.
The Affects Versions field should be corrected to include:
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2
