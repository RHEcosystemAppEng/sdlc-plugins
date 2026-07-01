# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-28940 (serde_json < 1.0.135)

The issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`). Per Important Rule 4, ALL versions from the 2.2.x stream supportability matrix are checked.

| Version | Tag | serde_json | Affected? | Notes |
|---------|-----|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | NO | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.1 | v0.4.8 | 1.0.138 | NO | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 -- same as 2.2.1 (1.0.138) |
| 2.2.3 | v0.4.11 | 1.0.139 | NO | 1.0.139 >= 1.0.135 (fix threshold) |
| 2.2.4 | v0.4.12 | 1.0.139 | NO | 1.0.139 >= 1.0.135 (fix threshold) |

### Evidence Summary

Every supported version in the 2.2.x stream ships serde_json >= 1.0.135 (the fix threshold). The earliest version (2.2.0, tag v0.4.5) already ships serde_json 1.0.138, which is well above the fix threshold of 1.0.135.

**Conclusion: No supported versions are affected by CVE-2026-28940.**

All supported versions ship serde_json at version 1.0.138 or 1.0.139, both of which are outside the affected range (< 1.0.135). The vulnerable version was never shipped in any 2.2.x release.

### Dependency Chain Context

Since no versions are affected (all ship a patched serde_json version), dependency chain tracing is not required. The package is present in the lock file but at a version that is already fixed.
