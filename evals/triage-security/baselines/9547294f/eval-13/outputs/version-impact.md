# Step 2 -- Version Impact Analysis

## Supportability Matrix

Loaded from security-matrix.md for both streams (2.1.x and 2.2.x). Although the issue is scoped to 2.2.x, version impact is checked across ALL supported versions per Important Rule 4.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):
- backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
- Profile: production (reqwest is a runtime dependency)
- First appeared: present in all checked versions

## Notes

- Version 2.2.2 is a retag of 2.2.1 (identical backend source commit v0.4.8), so the lock file check was skipped and the result carried forward (Important Rule 5).
- Pinned commit tags from the supportability matrix were used for each version, not branch HEAD (Important Rule 13).
- The 2.1.x stream is also affected but is outside this issue's scope (stream suffix [rhtpa-2.2]).
