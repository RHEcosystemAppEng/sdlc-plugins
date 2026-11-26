# TC-8050 — Step 2 Version Impact Analysis

The lock file data is simulated `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'` output, taken from the mock security matrix.

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

Issue stream scope: **2.2.x**

| Version | Stream | Pinned tag | criterion | Affected? | Notes |
|---------|--------|------------|-----------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.5.1 | YES | outside issue scope (cross-stream); dev-only |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.5.1 | YES | outside issue scope (cross-stream); dev-only |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.5.1 | YES | in scope; dev-only |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.5.1 | YES | in scope; dev-only |
| 2.2.2 | 2.2.x | `v0.4.8` | — | YES | same as 2.2.1 (backend retag of 2.2.1, lock file check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.5.1 | YES | in scope; dev-only |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.5.1 | YES | in scope; dev-only |
| dev stream | — | branch HEAD | not determined | — | No unreleased Jira version data was in the fixture (Step 2.2 needs `getJiraIssueTypeMetaWithFields`). No version is assumed. |

**In-scope result (2.2.x):** every released 2.2.x version (2.2.0 to 2.2.4) contains criterion 0.5.1, which is inside the affected range (< 0.5.2).
**Cross-stream:** every 2.1.x version (2.1.0, 2.1.1) is also affected.

## Dependency chain context (Step 2.3.5)

```
Dependency chain for criterion:
  backend (workspace) → criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds — used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in: all versions (2.1.0 – 2.2.4)

Manifest evidence (backend/Cargo.toml, all versions):
  [dev-dependencies]
  criterion = "0.5.1"

Remediation: bump criterion to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
(direct dependency, so no transitive pinning is needed)
```

### Dependency scope decision tree result

- Classification: **Cargo `[dev-dependencies]`**, which is dev-only and **not shipped** in the production binary or container image.
- Outcome: remediation tasks are **still created**, because a dev dependency is still a supply-chain risk. They are created with these changes:
  - Label **`dev-dependency`** added to every remediation task
  - Priority set to **Normal**, overriding the CVE severity instead of inheriting it
  - Description note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- This is not the feature-gated case, so the VEX "Vulnerable Code not in Execute Path" option does not apply. It also is not Case C: the package is present in the lock files within the affected range, so the issue is not closed as Not a Bug.

## Upstream fix status (Step 2.5)

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.2.x | Cargo | backend | `release/0.4.z` | not available in fixture | Not confirmed |
| 2.1.x | Cargo | backend | `release/0.3.z` | not available in fixture | Not confirmed |

The fixture has no branch-HEAD lock data, so the fix is not confirmed upstream. Remediation uses the **upstream backport + downstream propagation** pair rather than the dependency-bump variant.

## Steps 3–7.5 summary (as they bear on remediation)

- **Step 3 (Affects Versions):** the scoped issue currently has RHTPA 2.2.0. The proposed correction is RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4, all supported by the lock file evidence. The version IDs would come from dynamic version discovery, and the change needs engineer confirmation.
- **Step 4:** no sibling CVE-2026-99001 issues are in the fixture, so no 2.1.x companion CVE Jira is assumed to exist. Overlap check (4.3): skipped because the Upstream Affected Component field is not configured.
- **Step 5:** lifecycle status needs the product pages, which were not queried. All versions are treated as supported, per the matrix.
- **Step 6:** no resolved siblings, so the issue is not already fixed.
- **Step 7:** skipped because the Upstream Affected Component field is not configured.
- **Step 7.5:** release Epic/Task lookup ("RHTPA 2.2.x Release Tasks" / "CVE triage") needs Jira, which was not called. Linking is shown as conditional in remediation.md.
