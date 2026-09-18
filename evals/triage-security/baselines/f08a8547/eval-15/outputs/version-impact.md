# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- both ship quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3+ ship the fixed version (0.11.14)

## Dependency Chain Context

quinn-proto is a Cargo (Rust) dependency in the backend repository. The lock file (`Cargo.lock`) at each pinned build tag was inspected to determine the shipped version.

- Affected versions ship quinn-proto 0.11.9 or 0.11.12, both below the fix threshold of 0.11.14
- Version 2.2.2 is a retag of 2.2.1 (backend tag `v0.4.9` is a retag of `v0.4.8`), so it inherits the same quinn-proto 0.11.12
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are not affected

## Cross-Stream Impact

This issue is scoped to 2.2.x (`[rhtpa-2.2]`), but the 2.1.x stream is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This will trigger Case A (cross-stream impact) in Step 8.
