# Step 2 -- Version Impact Analysis: TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |

## Stream Impact Summary

| Stream | Versions Checked | Affected Versions | Status |
|--------|------------------|-------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | 2.1.0, 2.1.1 | ALL AFFECTED -- ships h2 0.4.5 |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | _(none)_ | NOT AFFECTED -- ships h2 >= 0.4.8 |

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (h2 is present directly in Cargo.lock)
  Profile: production (h2 is a runtime HTTP/2 library)
  Ecosystem: Cargo

Present in: 2.1.x stream (v0.3.8 and v0.3.12 both ship h2 0.4.5)
Also present in: 2.2.x stream (v0.4.5+ ships h2 >= 0.4.8, already fixed)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml on the release/0.3.z upstream branch
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Upstream Repo | Fix Status |
|--------|-----------|-----------------|---------------|------------|
| 2.1.x | Cargo | release/0.3.z | backend | NEEDS FIX -- ships h2 0.4.5, must bump to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | backend | ALREADY FIXED -- ships h2 >= 0.4.8 |

## Conclusion

Only the **2.1.x stream** is affected. All versions in the 2.2.x stream ship h2 >= 0.4.8, which includes the fix for CVE-2026-33501. Remediation is required only for the 2.1.x stream.
