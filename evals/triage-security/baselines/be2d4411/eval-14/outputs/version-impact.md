# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Stream scope: **2.2.x** (per issue suffix [rhtpa-2.2])

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|--------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

## Summary

- Affected versions: 2.2.0, 2.2.1, 2.2.2
- Not affected versions: 2.2.3, 2.2.4
- Fix was picked up in version 2.2.3 (tag v0.4.11) which ships openssl-libs 3.0.7-28.el9_4
