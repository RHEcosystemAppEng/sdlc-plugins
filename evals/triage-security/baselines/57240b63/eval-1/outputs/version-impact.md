# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

All supported version streams are analyzed, even though TC-8001 is scoped to
stream 2.2.x. Cross-stream results inform Case B (proactive remediation).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Combined Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed |

## Upstream Fix Status

The upstream fix is already merged (quinn-rs/quinn#2048). Checking upstream
branch HEAD versions from the Ecosystem Mappings:

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs verification) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (per v0.4.11+) | YES |

For stream 2.2.x, the latest released versions (2.2.3 and 2.2.4) already ship
the fix. The fix was picked up between v0.4.8 (0.11.12) and v0.4.11 (0.11.14).

For stream 2.1.x, both released versions ship 0.11.9. The upstream branch
release/0.3.z needs verification to determine if a fix has been merged.

## Cross-Stream Impact Summary

- **Stream 2.2.x** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 are affected;
  versions 2.2.3, 2.2.4 are fixed.
- **Stream 2.1.x** (outside issue scope): ALL versions (2.1.0, 2.1.1) are
  affected. This triggers Case B (cross-stream proactive remediation) in Step 8.
