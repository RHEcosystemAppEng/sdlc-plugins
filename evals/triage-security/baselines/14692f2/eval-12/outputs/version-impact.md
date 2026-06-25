# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5: **h2 < 0.4.8 is affected**.

## 2.1 -- Supportability Matrix

### Stream 2.2.x (issue-scoped stream)

Source: `security-matrix.md` for rhtpa-release.0.4.z

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

### Stream 2.1.x (cross-stream check)

Source: `security-matrix.md` for rhtpa-release.0.3.z

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |

## 2.3 -- Dependency Version Extraction

Using mock lock file data for h2 versions by tag, compared against the
enriched fix threshold of **0.4.8** from Step 1.5.

### Stream 2.2.x (issue-scoped)

| Version | backend tag | h2 version | Affected? (< 0.4.8) | Notes |
|---------|-------------|------------|----------------------|-------|
| 2.2.0 | v0.4.5 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | v0.4.8 | -- | NO | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Stream 2.1.x (cross-stream)

| Version | backend tag | h2 version | Affected? (< 0.4.8) | Notes |
|---------|-------------|------------|----------------------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

## Version Impact Summary Table

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | **YES** | cross-stream |
| 2.1.1 | 2.1.x | 0.4.5 | **YES** | cross-stream |
| 2.2.0 | 2.2.x | 0.4.5 | **YES** | in-scope |
| 2.2.1 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

## 2.3.5 -- Dependency Chain Context

Dependency chain for h2 (Cargo):
- h2 is a transitive dependency via the HTTP stack
- backend (workspace) -> reqwest/hyper -> h2
- Profile: production (h2 is a runtime HTTP/2 dependency)
- Present in all versions (2.1.0 through 2.2.4)
- Fixed starting at version 2.2.1 (backend tag v0.4.8, h2 bumped to 0.4.8)

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.9 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.4.5 | NO |

- **2.2.x**: Upstream branch `release/0.4.z` already has h2 0.4.9 (>= 0.4.8).
  The fix was picked up in v0.4.8 and later.
- **2.1.x**: Upstream branch `release/0.3.z` still has h2 0.4.5 (< 0.4.8).
  Upstream backport is needed before downstream propagation.

## Triage Conclusion

**In-scope stream (2.2.x)**: Only version 2.2.0 is affected. Versions 2.2.1+
already ship h2 >= 0.4.8 and are not vulnerable.

**Cross-stream (2.1.x)**: All versions (2.1.0, 2.1.1) are affected -- h2 0.4.5
is below the fix threshold of 0.4.8.
