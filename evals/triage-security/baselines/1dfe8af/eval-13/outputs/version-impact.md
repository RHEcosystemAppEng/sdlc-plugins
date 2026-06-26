# Step 2 - Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version |

## Source Data

Lock file versions extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`:

| Tag | Product Version | quinn-proto version |
|-----|-----------------|---------------------|
| v0.3.8 | 2.1.0 | 0.11.9 |
| v0.3.12 | 2.1.1 | 0.11.9 |
| v0.4.5 | 2.2.0 | 0.11.9 |
| v0.4.8 | 2.2.1 | 0.11.12 |
| v0.4.9 | 2.2.2 | (retag of v0.4.8) |
| v0.4.11 | 2.2.3 | 0.11.14 |
| v0.4.12 | 2.2.4 | 0.11.14 |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Source repository: rhtpa-backend

  quinn-proto present in all versions across both streams.
  Version bumped from 0.11.9 to 0.11.12 at v0.4.8 (2.2.1),
  then to 0.11.14 (fixed) at v0.4.11 (2.2.3).
  Stream 2.1.x remains at 0.11.9 across all versions.
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs check) | Unknown - requires git show |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (inferred from v0.4.11+) | YES |

Note: The fix was picked up in stream 2.2.x starting at build 0.4.11 (version 2.2.3).
Stream 2.1.x has not received the fix in any released version.

## Impact Summary

### Stream 2.2.x (in scope - issue scoped to rhtpa-2.2)

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Remediation needed**: YES - versions 2.2.0 through 2.2.2 ship quinn-proto < 0.11.14
- **Fix already present in stream**: YES - starting from 2.2.3 (build 0.4.11)

### Stream 2.1.x (out of scope - cross-stream impact)

- **Affected versions**: 2.1.0, 2.1.1 (all versions)
- **Not affected versions**: none
- **Cross-stream impact**: YES - all 2.1.x versions ship quinn-proto 0.11.9 which is vulnerable

## Triage Decision

- **Case A** applies for stream 2.2.x: affected versions exist within scope, create remediation tasks (upstream backport + downstream propagation)
- **Case B** also applies: stream 2.1.x is affected but outside issue scope, create preemptive remediation tasks or post cross-stream impact comment
