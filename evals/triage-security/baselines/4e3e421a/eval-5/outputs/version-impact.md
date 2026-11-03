# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scope: issue stream **2.2.x** (rhtpa-release.0.4.z). The 2.1.x stream was also checked (Rule 4: check all supported versions) to find cross-stream impact.

Evidence: simulated output of `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` at pinned tags from security-matrix.md (mock data). Ecosystem mapping: RPM -> `rpms.lock.yaml`.

Comparison uses RPM EVR ordering (version 3.0.7 is the same everywhere; release number compared: 24 < 25 < 27 < 28).

## Version Impact Table (2.2.x, in scope)

| Version | Build | Pinned tag | openssl-libs | Affected? | Notes |
|---------|-------|------------|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | retag of 2.2.1, same as 2.2.1 (lock file check skipped) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | ships fixed version |

## Cross-stream check (2.1.x, out of scope for this issue)

| Version | Build | Pinned tag | openssl-libs | Affected? | Notes |
|---------|-------|------------|--------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | **YES** | outside TC-8005 scope |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | **YES** | outside TC-8005 scope |

## Development stream (Step 2.2)

2.2.x is the latest stream (no forward pointer). Unreleased Jira versions could not be queried (no Jira calls), so no separate development stream was identified. The latest 2.2.x build (2.2.4 / `v0.4.12`) already ships 3.0.7-28.el9_4. The Konflux repo HEAD check (`git show HEAD:rpms.lock.yaml`) still needs to be run to confirm.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM), stream 2.2.x:
  rpms.lock.yaml: present at v0.4.5 (3.0.7-25.el9_3) and v0.4.8 (3.0.7-27.el9_4) → explicit install
  SBOM verification: ⚠️ skipped — cosign not available (eval: external tools / `which cosign` / `cosign download sbom` not run). Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs is pinned in rpms.lock.yaml, resolved from rpms.in.yaml)
  Introduction point: present in every 2.2.x build. Upgraded to 3.0.7-28.el9_4 at v0.4.11 (2.2.3), which fixes it.

Remediation: update the openssl-libs package spec in rpms.in.yaml / regenerate rpms.lock.yaml
in rhtpa-release.0.4.z so it resolves to >= 3.0.7-28.el9_4. The current release line
(2.2.3+) already does this, so the next 2.2.x build from main inherits the fix.
```

```
Dependency chain for openssl-libs (RPM), stream 2.1.x (cross-stream):
  rpms.lock.yaml: present at v0.3.8 / v0.3.12 (3.0.7-24.el9) → explicit install
  SBOM verification: ⚠️ skipped — cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install
```

SBOM cross-check note: a base image vs final image SBOM comparison (Step 2.3.5 sub-step 3) was **not performed**. The explicit-install classification comes from rpms.lock.yaml alone. It has not been cross-checked against the image SBOM.

## Upstream fix status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (none; fixed in Konflux repo directly) | n/a | Fix present in the latest released build (v0.4.11+) |
| 2.1.x | RPM | — | n/a | Not fixed in any released 2.1.x build |

RPM has no upstream source branch, so the remediation is a Konflux release repo change only.

## Summary

- 2.2.x affected: **2.2.0, 2.2.1, 2.2.2**. Not affected: 2.2.3, 2.2.4.
- 2.1.x is also affected (2.1.0, 2.1.1). This is cross-stream impact (Case A) and must not be added to TC-8005's Affects Versions.
