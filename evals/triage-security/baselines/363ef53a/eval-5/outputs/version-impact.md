# Step 2 -- Version Impact Analysis for CVE-2026-40215

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Stream | openssl-libs | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 3.0.7-24.el9 | YES | |
| 2.1.1 | 2.1.x | 3.0.7-24.el9 | YES | |
| 2.2.0 | 2.2.x | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 2.2.x | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1: 3.0.7-27.el9_4) |
| 2.2.3 | 2.2.x | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 3.0.7-28.el9_4 | NO | ships fixed version |

**Source data**: rpms.lock.yaml at each pinned tag from the supportability matrix.

**Fix threshold**: 3.0.7-28.el9_4 (from Jira description; advisory RHSA-2026:4021).

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT -- explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

### SBOM Verification Status

SBOM verification was **skipped** -- cosign is not available in the current
environment. The rpms.lock.yaml classification (explicit install) is used
as the sole determination of package origin. No SBOM cross-validation was
attempted.

## Cross-Stream Summary

- **2.2.x stream** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 are affected; 2.2.3 and 2.2.4 ship the fix
- **2.1.x stream** (out of scope): versions 2.1.0 and 2.1.1 are also affected (3.0.7-24.el9 < 3.0.7-28.el9_4)

The 2.1.x stream impact is noted for cross-stream awareness (Step 8, Case A)
but remediation tasks for this issue are scoped to 2.2.x only.

## Upstream Fix Status

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings
table (column value: --). Step 2.5 upstream fix check is not applicable
for system package ecosystems. The fix is delivered via Red Hat errata
(RHSA-2026:4021).
