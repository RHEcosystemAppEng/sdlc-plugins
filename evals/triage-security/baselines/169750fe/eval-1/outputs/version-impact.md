# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed at >= 0.11.14 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed at >= 0.11.14 |

## Evidence

- **Fix threshold**: quinn-proto >= 0.11.14 (from Jira description: "fixed in 0.11.14")
- **Comparison method**: Each version's quinn-proto dependency extracted via
  `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at the pinned
  source commit from the supportability matrix
- **Retag handling**: Version 2.2.2 uses build tag v0.4.9, which is a retag of
  v0.4.8 (same source). Result carried forward from 2.2.1.

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- quinn-proto 0.11.9
- **2.2.x stream**: 3 of 5 versions affected (2.2.0, 2.2.1, 2.2.2) -- fix
  shipped starting from 2.2.3 (quinn-proto 0.11.14)

## Dependency Chain Context (Step 2.3.5)

quinn-proto is a Cargo (Rust) crate present in `Cargo.lock` for the backend
repository. It is the protocol implementation crate for the quinn QUIC
transport library.

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn -> quinn-proto
  Type: transitive dependency (via quinn crate)
  Profile: production (quinn is a runtime dependency)

  Present in: all versions across both streams (2.1.x and 2.2.x)
```

The transitive nature means remediation should prefer bumping the direct
dependency (quinn) to a version whose transitive closure includes
quinn-proto >= 0.11.14. Fallback: pin quinn-proto directly via
`cargo add quinn-proto@0.11.14`.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? | Notes |
|--------|-----------|-----------------|-------------------|--------|-------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO | Latest pinned tag still ships vulnerable version |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES | Fix present since v0.4.11 |

### Remediation path implications

- **2.1.x (release/0.3.z)**: Fix NOT available upstream. Remediation requires
  an upstream backport (bump quinn-proto to >= 0.11.14 on release/0.3.z),
  followed by downstream propagation to the Konflux release repo.
- **2.2.x (release/0.4.z)**: Fix already available upstream (since v0.4.11).
  The fix was already shipped in product version 2.2.3. No new remediation
  work is needed for the 2.2.x stream.
