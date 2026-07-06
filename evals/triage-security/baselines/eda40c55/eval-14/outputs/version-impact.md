# Step 2 -- Version Impact Analysis: TC-8005

## Supportability Matrix (2.2.x stream)

Source: rhtpa-release.0.4.z security-matrix.md

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Version Impact Table

CVE-2026-40215 (openssl-libs, affected versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | matches fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | matches fixed version |

## Dependency Chain

See `sbom-verification.md` for the full dependency chain analysis including rpms.lock.yaml and SBOM verification results.

## Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix already present from**: 2.2.3 onwards (openssl-libs 3.0.7-28.el9_4)
- **Remediation scope**: versions 2.2.0 through 2.2.2 require openssl-libs update to >= 3.0.7-28.el9_4
