# Step 2 -- Version Impact Analysis

## Supportability Matrix

Loaded from two streams configured in Security Configuration Version Streams table:

- **2.1.x** stream: `security-matrix.md` at rhtpa-release.0.3.z
- **2.2.x** stream: `security-matrix.md` at rhtpa-release.0.4.z

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8: 0.11.12) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo ecosystem):

- quinn-proto is a transitive dependency via the QUIC networking stack
- Typical chain: backend (workspace) -> reqwest or quinn -> quinn-proto
- Profile: production (quinn-proto is a runtime dependency for QUIC transport)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | Would need to check `git show release/0.3.z:Cargo.lock` |
| 2.2.x | Cargo | `release/0.4.z` | v0.4.11+ already ships 0.11.14 (fixed); upstream branch likely fixed |

## Cross-Stream Impact

This issue is scoped to stream **2.2.x** (from suffix `[rhtpa-2.2]`), but the version impact analysis shows that stream **2.1.x** is also affected:

- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This cross-stream impact would trigger Case B in Step 7, posting a cross-stream impact comment and checking for sibling CVE Jiras for the 2.1.x stream.
