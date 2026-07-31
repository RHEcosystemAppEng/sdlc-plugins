# Version Impact Analysis — CVE-2026-31812 (quinn-proto < 0.11.14)

## Step 2 — Version Impact Table

The version impact analysis checks ALL versions from ALL streams in the
supportability matrix. Each version's quinn-proto dependency version is
extracted from the lock file at the pinned commit tag from the supportability
matrix (not branch HEAD).

### Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same backend tag `v0.4.8`) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | |

**Evidence source:** Dependency versions are extracted using
`git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at the pinned
commit tag from the supportability matrix for each version. Version 2.2.2 is
a retag of 2.2.1 (identical backend tag `v0.4.8`), so the lock file check is
skipped and the result is carried forward from 2.2.1 per Important Rule 5.

### Summary

- **Affected versions (within 2.2.x stream scope):** 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (within 2.2.x stream scope):** 2.2.3, 2.2.4
- **Cross-stream affected versions (outside scope):** 2.1.0, 2.1.1 (stream 2.1.x)

All versions shipping quinn-proto < 0.11.14 are affected. Versions 2.2.3 and
2.2.4 ship quinn-proto 0.11.14 (the fix version) and are not affected.

### Dependency chain context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock at workspace level)
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```
