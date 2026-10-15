# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

All supported versions from the supportability matrix are included, using pinned commit tags for released versions.

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

### Evidence

- **Fix threshold**: quinn-proto >= 0.11.14 (from Jira description: "fixed in 0.11.14")
- **Method**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` per Ecosystem Mappings Check Command
- **Retag handling**: Version 2.2.2 (tag `v0.4.9`) is a retag of 2.2.1 (tag `v0.4.8`); the backend source commit is identical, so the quinn-proto version is carried forward as 0.11.12 (affected)
- **Pinned commits**: All version impact evidence uses the exact pinned commit tags from the supportability matrix, not branch HEAD

### Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Cross-stream impact**: Both 2.1.x and 2.2.x streams contain affected versions. The issue is scoped to `[rhtpa-2.2]`, so remediation tasks are created for the 2.2.x stream. The 2.1.x stream impact is noted for Case A cross-stream handling.

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)
```

quinn-proto is a direct dependency of the backend workspace. Remediation is a straightforward version bump in Cargo.toml/Cargo.lock.
