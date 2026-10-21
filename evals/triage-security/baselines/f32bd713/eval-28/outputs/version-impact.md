# Step 2 -- Version Impact Analysis for TC-8060

## CVE-2026-99010 (h2 < 0.4.5)

### Stream Scope

This issue is scoped to the **2.2.x** stream (`[rhtpa-2.2]`). The 2.1.x stream is checked for cross-stream impact only.

## Version Impact Table (2.2.x stream -- scoped)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.4 | YES | h2 0.4.4 < 0.4.5 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.4 | YES | h2 0.4.4 < 0.4.5 (fix threshold) |
| 2.2.2 | v0.4.9 | -- | YES | backend retag of 2.2.1; same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 (at fix threshold) |
| 2.2.4 | v0.4.12 | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 (at fix threshold) |

**Affected versions (2.2.x)**: 2.2.0, 2.2.1, 2.2.2

## Version Impact Table (2.1.x stream -- cross-stream check)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 (at fix threshold) |
| 2.1.1 | v0.3.12 | 0.4.5 | NO | h2 0.4.5 >= 0.4.5 (at fix threshold) |

**Cross-stream result**: The 2.1.x stream is **not affected**. No cross-stream impact (Case A does not apply).

## Dependency Chain Context (Step 2.3.5)

### h2 dependency chain for backend

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**Dependency type**: transitive

**Chain**: `backend (workspace root) -> reqwest 0.12.5 -> hyper 1.4.1 -> h2 0.4.4`

The vulnerable package `h2` is **not** a direct dependency of the backend workspace. It is pulled in transitively through the following chain:

1. `backend` declares `reqwest = { version = "0.12", features = ["json"] }` as a direct runtime dependency
2. `reqwest 0.12.5` depends on `hyper 1.4.1`
3. `hyper 1.4.1` depends on `h2 0.4.4`

**Manifest evidence** (from `backend/Cargo.toml`):
```toml
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Profile**: Production -- `reqwest` is listed under `[dependencies]` (not `[dev-dependencies]` or `[build-dependencies]`), so `h2` is shipped in the production binary.

**Remediation implications**:
Since h2 is a transitive dependency (3 levels deep), a direct version bump of h2 in `Cargo.toml` is not the default approach. The two-tier remediation strategy applies:
1. **Preferred**: Bump `reqwest` to a version whose transitive closure includes `h2 >= 0.4.5`
2. **Fallback**: Pin `h2` directly via `cargo add h2@0.4.5` to override transitive resolution

## Upstream Fix Status (Step 2.5)

The fix is already present in later 2.2.x versions (2.2.3+ ship h2 0.4.5), indicating the upstream branch `release/0.4.z` already carries the fix. The remediation approach is therefore the **dependency bump** variant (not the upstream backport variant), since the upstream branch already ships the fixed version.

| Stream | Ecosystem | Upstream Branch | Version at HEAD (inferred) | Fixed? |
|--------|-----------|-----------------|----------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.5 (per 2.2.3+ evidence) | YES |

**Remediation path**: Dependency bump (cargo update) + downstream propagation. Two tasks required for the 2.2.x stream.
