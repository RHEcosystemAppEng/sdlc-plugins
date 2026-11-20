# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Data source: simulated `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` output from
the "openssl-libs versions by tag (rpms.lock.yaml)" section of `security-matrix-mock.md`.
No real git commands were run.

## 2.1 – Matrix load

Both streams loaded from the mock matrix (2.1.x: rhtpa-release.0.3.z, 2.2.x: rhtpa-release.0.4.z).
Format check: required sections (Supportability Matrix, Ecosystem Mappings, Source Pinning Method,
Forward Pointer) present; Ecosystem Mappings columns match the template — Pass.
Staleness warning from Step 0.3 applies (Last-Updated 2026-06-28, 145 days old).

## 2.2 – Development stream

Not determined: unreleased Jira versions could not be queried (no Jira access in eval).
2.2.x is the latest stream (no forward pointer); no dev-stream/branch-HEAD row is included.
The engineer should confirm whether an unreleased RHTPA 2.2.x / 2.3 version exists and check it at HEAD.

## 2.4 – Version impact table

Comparison: RPM version-release compared against fix threshold `3.0.7-28.el9_4`
(same upstream version 3.0.7; release 24/25/27 < 28 → affected; 28 → fixed).

### In-scope stream: 2.2.x (issue scope `[rhtpa-2.2]`)

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | retag of 2.2.1 — same as 2.2.1 (lock check skipped, result carried forward) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | ships fixed version |

### Out-of-scope stream: 2.1.x (cross-stream context only — Case A)

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | YES | outside issue scope |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | YES | outside issue scope |

Summary: within 2.2.x, **2.2.0, 2.2.1, 2.2.2 are affected**; 2.2.3 and 2.2.4 already ship
3.0.7-28.el9_4. The fix entered the 2.2.x stream between 2.2.2 (0.4.9) and 2.2.3 (0.4.11).
Stream 2.1.x (2.1.0, 2.1.1) is also affected → cross-stream impact (Case A in Step 8).

## 2.3.5 – Dependency chain context

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present → explicit install
    2.2.0 (v0.4.5):  openssl-libs-3.0.7-25.el9_3
    2.2.1 (v0.4.8):  openssl-libs-3.0.7-27.el9_4
    2.2.2:           same as 2.2.1 (retag)
  SBOM verification: ⚠️ skipped — cosign not available in this eval run (external tools prohibited;
                     the matrix also has no Container Images section with image reference/digest
                     to download SBOMs from). Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs resolved in rpms.lock.yaml / rpms.in.yaml of
          the Konflux release repo rhtpa-release.0.4.z)
  Dockerfile: not inspected (git show not permitted in eval); FROM reference unknown
  Introduction point: openssl-libs present in rpms.lock.yaml in every inspected tag of both
          streams (no origin change between 2.1.x and 2.2.x); fixed release
          3.0.7-28.el9_4 first appears at v0.4.11 (2.2.3)

Remediation: ensure openssl-libs >= 3.0.7-28.el9_4 in rpms.lock.yaml on
rhtpa-release.0.4.z main (regenerate lock file); already satisfied by builds 0.4.11+.
```

> ⚠️ SBOM verification skipped — cosign not available / SBOM download not attempted.
> Using rpms.lock.yaml classification only. If cosign becomes available, compare the final
> image SBOM against the base image SBOM to confirm openssl-libs is an explicit install
> rather than inherited from the base image (openssl-libs is commonly present in UBI base
> images, so a discrepancy is plausible and worth checking).

Scope: production (system library in the shipped container image) — no dev-dependency handling.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (none configured) | n/a | n/a — RPM fixes happen directly in the Konflux release repo |

Latest released 2.2.x build (2.2.4 / v0.4.12) already ships 3.0.7-28.el9_4.

Engineer confirmation of this table is required before Step 3.
