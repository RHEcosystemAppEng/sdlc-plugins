# Step 2 -- Version Impact Analysis: TC-8005

## CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4)

Stream scope: **2.2.x** only (per issue suffix `[rhtpa-2.2]`)

## Version Impact Table

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable openssl-libs (before 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are NOT affected.

## Cross-Stream Impact

The issue is scoped to the 2.2.x stream. However, the 2.1.x stream also ships openssl-libs:

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 (out of scope) |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 (out of scope) |

The 2.1.x stream is outside this issue's scope but is also affected. This would trigger Case B (cross-stream impact comment) in Step 8.
