# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Vulnerability Summary

- **Library**: serde_json
- **Affected range**: < 1.0.135
- **Fixed version**: 1.0.135

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | Tag | serde_json | Affected? | Notes |
|---------|--------|-----|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | NO | >= 1.0.135 |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | NO | >= 1.0.135 |
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | NO | >= 1.0.135 |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | NO | >= 1.0.135 |
| 2.2.2 | 2.2.x | v0.4.9 | 1.0.138 | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | NO | >= 1.0.135 |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | NO | >= 1.0.135 |

**Result: NO supported versions are affected.** All supported versions ship serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerable version range (< 1.0.135) is not present in any supported release.

## Dependency Chain Context

Not applicable -- no versions are affected. serde_json is a direct Cargo dependency of the backend workspace, but since all shipped versions are already patched (>= 1.0.135), no remediation path analysis is needed.

## Upstream Fix Status

Not applicable -- the vulnerability does not affect any supported version. All versions already ship a fixed serde_json version.
