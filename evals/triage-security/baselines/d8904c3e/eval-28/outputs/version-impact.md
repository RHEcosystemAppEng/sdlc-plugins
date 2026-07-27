# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99010 (h2 < 0.4.5)

### Scoped stream: 2.2.x (rhtpa-release.0.4.z)

| Version | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.2.0   | `v0.4.5`    | 0.4.4      | YES       |       |
| 2.2.1   | `v0.4.8`    | 0.4.4      | YES       |       |
| 2.2.2   | `v0.4.9`    | --         | YES       | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | `v0.4.11`   | 0.4.5      | NO        | fixed version |
| 2.2.4   | `v0.4.12`   | 0.4.5      | NO        | fixed version |

**Affected versions**: 2.2.0, 2.2.1, 2.2.2
**Not affected versions**: 2.2.3, 2.2.4

### Cross-stream check: 2.1.x (rhtpa-release.0.3.z)

| Version | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.1.0   | `v0.3.8`    | 0.4.5      | NO        | already at fixed version |
| 2.1.1   | `v0.3.12`   | 0.4.5      | NO        | already at fixed version |

The 2.1.x stream is **not affected** -- all versions ship h2 0.4.5 which is at or above the fix threshold. No cross-stream remediation is needed.

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

### Remediation complexity assessment

h2 is a **transitive** dependency (3 levels deep: reqwest -> hyper -> h2). This means:
- A direct `cargo add h2` pin is possible but a workaround, not a root fix
- The preferred approach is to bump `reqwest` to a version whose transitive closure includes h2 >= 0.4.5
- If no such reqwest version exists, fall back to pinning h2 directly

Since versions 2.2.3+ already ship h2 0.4.5, the fix is already present in the upstream source at the tags used by those versions. The remediation for affected versions (2.2.0-2.2.2) involves updating the Cargo.lock to resolve h2 >= 0.4.5 on the upstream branch `release/0.4.z`, then propagating that fix downstream to the Konflux release repo.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at Branch HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x  | Cargo     | release/0.4.z   | 0.4.5             | YES    |

The upstream branch `release/0.4.z` already ships h2 0.4.5 (as evidenced by versions 2.2.3 and 2.2.4 being unaffected). Remediation is a Konflux release repo change: bump the source tag/commit reference to pick up the fix that is already present in newer backend tags.
