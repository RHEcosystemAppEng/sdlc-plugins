# Step 2 — Version Impact Analysis: CVE-2026-40215 (openssl-libs)

## Version Impact Table

Affected range: versions before 3.0.7-28.el9_4
Fixed version: 3.0.7-28.el9_4
Data source: `rpms.lock.yaml` at each pinned build tag

### Stream 2.2.x (issue scope)

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

### Stream 2.1.x (cross-stream analysis)

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

**Summary:** Within the 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are
affected. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs
(3.0.7-28.el9_4). Cross-stream: all 2.1.x versions are also affected.

## Dependency Chain (Step 2.3.5)

### RPM origin classification

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3 at v0.4.5, 3.0.7-27.el9_4 at v0.4.8)
  Origin: explicit install (openssl-libs found in rpms.lock.yaml)
  SBOM verification: skipped -- cosign not available in this environment.
    Using rpms.lock.yaml classification only.

Remediation: update the package spec in rpms.lock.yaml (and rpms.in.yaml
if present) to require openssl-libs >= 3.0.7-28.el9_4. Regenerate the
lock file to pick up the patched version from RHSA-2026:4021.
```

The package `openssl-libs` is present in `rpms.lock.yaml` for all checked tags
in the 2.2.x stream, confirming it is an **explicitly installed** RPM package
(not inherited from the base image). SBOM cross-validation via cosign was not
performed because cosign is not available in this environment; the
rpms.lock.yaml classification stands as the sole evidence source.

### Introduction point

openssl-libs is present across all versions in both the 2.1.x and 2.2.x
streams — it was not introduced by a specific version change. The package
version was incrementally updated across builds:
- 2.1.x: consistently at 3.0.7-24.el9
- 2.2.0: bumped to 3.0.7-25.el9_3
- 2.2.1-2.2.2: bumped to 3.0.7-27.el9_4
- 2.2.3-2.2.4: bumped to 3.0.7-28.el9_4 (the fixed version)

## Upstream Fix Status

Not applicable for RPM ecosystem — RPM packages do not have an upstream branch
in the Ecosystem Mappings table. The fix is delivered via Red Hat errata
(RHSA-2026:4021) and is already present in versions 2.2.3+ of the 2.2.x stream.

## Cross-Stream Impact

The issue is scoped to the 2.2.x stream via the `[rhtpa-2.2]` suffix. However,
the 2.1.x stream is also affected (all versions ship openssl-libs < 3.0.7-28.el9_4).
This triggers Case A (cross-stream impact) — a cross-stream notice should be
posted, and preemptive remediation tasks should be created for 2.1.x if no
sibling CVE Jira exists for that stream.
