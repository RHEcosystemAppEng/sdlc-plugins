# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Scoped stream: 2.2.x

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Cross-stream impact: 2.1.x

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

Both 2.1.x versions ship openssl-libs below the fix threshold and are
affected. This is cross-stream impact (Case B) -- the 2.1.x stream is
outside the scope of this issue ([rhtpa-2.2]).

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (versions 3.0.7-25.el9_3 through 3.0.7-28.el9_4) --> explicit install
  SBOM verification: skipped -- cosign not available in this environment.
    Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation path: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The package `openssl-libs` is present in `rpms.lock.yaml` at each pinned
tag, classifying it as an **explicit install** (not inherited from the base
image). SBOM cross-validation via cosign was not performed because cosign
is not available in the current environment. The rpms.lock.yaml
classification is used as the sole source of truth for package origin.

## Upstream Fix Status

RPM ecosystem has no upstream branch configured (the Upstream Branch column
is empty in the Ecosystem Mappings table for RPM). Upstream fix status
check is not applicable -- RPM remediation happens directly in the Konflux
release repo.

The fix (3.0.7-28.el9_4) is already present in the 2.2.x stream as of
version 2.2.3 (build tag v0.4.11, released 2026-03-23). No new upstream
backport is required for the 2.2.x stream.
