# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs, affected: versions before 3.0.7-28.el9_4)

The issue is scoped to stream **2.2.x**. All versions from the 2.2.x supportability matrix are checked using `rpms.lock.yaml` data.

| Version | Build Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8)_ | **YES** | retag of 2.2.1 — same as 2.2.1 (3.0.7-27.el9_4) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** | = 3.0.7-28.el9_4 (fixed version) |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship the vulnerable openssl-libs version. Versions 2.2.3 and 2.2.4 ship the patched version (3.0.7-28.el9_4).

## Step 2.3.5 — Dependency Chain Context

### Package origin classification

**Investigation method**: rpms.lock.yaml (RPM lock file configured for the 2.2.x stream)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present → explicit install
  Origin: explicit install (openssl-libs listed in rpms.lock.yaml)
  
  SBOM verification: skipped — external tools are prohibited in this eval.
  Using rpms.lock.yaml classification only.
```

The rpms.lock.yaml for the 2.2.x stream lists openssl-libs, confirming it is an **explicit install** (not inherited from the base image). The rpms.lock.yaml presence is the primary classification signal.

### SBOM Verification Status

SBOM verification via cosign was **skipped** because external tools (cosign, registry access) are prohibited in this eval context. The rpms.lock.yaml classification alone is used:

> SBOM verification skipped — cosign not available / external tools prohibited. Using rpms.lock.yaml classification only.

The rpms.lock.yaml classification remains the primary signal. SBOM comparison would supplement but not override it.

### Remediation path

Since openssl-libs is an **explicit install** (present in rpms.lock.yaml), remediation is:
- Update the package version spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if needed
- Trigger a Konflux rebuild
