# Step 2 -- Version Impact Analysis: CVE-2026-28940

## CVE Details

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Version Impact Table

This issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`). All versions in the 2.2.x stream are evaluated.

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0   | 1.0.138    | NO        | 1.0.138 >= 1.0.135; outside affected range |
| 2.2.1   | 1.0.138    | NO        | 1.0.138 >= 1.0.135; outside affected range |
| 2.2.2   | --         | NO        | retag of 2.2.1 (same source commit v0.4.8, serde_json 1.0.138) |
| 2.2.3   | 1.0.139    | NO        | 1.0.139 >= 1.0.135; outside affected range |
| 2.2.4   | 1.0.139    | NO        | 1.0.139 >= 1.0.135; outside affected range |

## Lock File Evidence

Dependency versions extracted from mock lock file data (simulating `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`):

| Tag (source commit) | serde_json version | Comparison to fix threshold (1.0.135) |
|----------------------|--------------------|---------------------------------------|
| v0.4.5 (2.2.0)      | 1.0.138            | >= 1.0.135 -- NOT affected            |
| v0.4.8 (2.2.1)      | 1.0.138            | >= 1.0.135 -- NOT affected            |
| v0.4.9 (2.2.2)      | retag of v0.4.8    | same as 2.2.1 -- NOT affected         |
| v0.4.11 (2.2.3)     | 1.0.139            | >= 1.0.135 -- NOT affected            |
| v0.4.12 (2.2.4)     | 1.0.139            | >= 1.0.135 -- NOT affected            |

## Summary

**No versions in the 2.2.x stream are affected.** Every version ships serde_json >= 1.0.137, which is well above the fix threshold of 1.0.135. The vulnerable code (present in serde_json < 1.0.135) is not present in any shipped version.
