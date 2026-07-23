# Step 2 -- Version Impact Analysis: CVE-2026-99001

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | Stream | Tag | criterion | Affected? | Notes |
|---------|--------|-----|-----------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.5.1 | YES | outside issue scope (2.1.x) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.5.1 | YES | outside issue scope (2.1.x) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.5.1 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.5.1 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.5.1 | YES | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.5.1 | YES | |

All versions in the 2.2.x stream ship criterion 0.5.1, which is below the fix threshold of 0.5.2.

The 2.1.x stream is also affected but is outside this issue's scope (scoped to 2.2.x per `[rhtpa-2.2]` suffix). Cross-stream impact is noted for Case B handling.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency Scope Assessment

criterion is declared in `[dev-dependencies]` in `backend/Cargo.toml`. Dev-dependencies in Cargo are used for tests and benchmarks only and are **NOT** shipped in production builds. The production binary and container image do not include criterion.

Per the dependency scope decision tree:
- **Dev-only dependency**: not shipped in production
- **Supply chain risk only**: compromised dev deps could inject malicious code during builds, but the library itself is not present in the runtime artifact
- **Remediation handling**:
  - Add `dev-dependency` label to remediation tasks
  - Override priority to **Normal** regardless of CVE severity
  - Include note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | criterion at HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 | NO |
| 2.1.x | Cargo | release/0.3.z | 0.5.1 | NO |

The upstream source repository has not yet bumped criterion to the fixed version (0.5.2) on either release branch. Remediation requires an upstream PR first.
