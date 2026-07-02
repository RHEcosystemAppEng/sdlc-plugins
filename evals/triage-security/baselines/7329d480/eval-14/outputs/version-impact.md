# Step 2 -- Version Impact Analysis: TC-8005

## CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4)

Stream scope: **2.2.x** only (from issue suffix [rhtpa-2.2])

### Version Impact Table

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | at fix version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | at fix version |

### Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix threshold**: 3.0.7-28.el9_4 (from CVE description, confirmed by rpms.lock.yaml analysis)

Versions 2.2.0 through 2.2.2 ship openssl-libs at versions older than the fix version 3.0.7-28.el9_4 and are vulnerable to CVE-2026-40215. Versions 2.2.3 and 2.2.4 ship the fixed version 3.0.7-28.el9_4 and are not affected.

Version 2.2.2 is a retag of 2.2.1 (backend tag v0.4.8 reused as v0.4.9), so it inherits the same openssl-libs version (3.0.7-27.el9_4) and the same affected status.

### Dependency Chain Context

See `sbom-verification.md` for the full dependency chain classification including SBOM verification results showing the disagreement between rpms.lock.yaml and SBOM signals.
