# TC-8050 — Step 2 Version Impact Analysis

Version impact for CVE-2026-99001 (criterion < 0.5.2). Issue scope: **2.2.x**.

Evidence comes from the mock `Cargo.lock` data in `security-matrix-mock.md` (simulating `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`) and the mock manifest data in `vuln-issue-dev-dependency.md` (simulating `git show <tag>:backend/Cargo.toml`).

## 2.1 Supportability matrix

Both streams were loaded from the matrix fixture, and both pass format validation: the required sections are present and the Ecosystem Mappings columns match.

## 2.2 Development stream

No unreleased Jira version data is available because Jira was not queried. 2.2.x is the latest stream (it has no forward pointer). There is no development-HEAD lock data in the fixtures, so no development-stream row could be checked. **The dev-stream row is marked "not determined" rather than assumed.**

## 2.4 Version impact table — stream 2.2.x (in scope)

| Version | Build | backend tag | criterion | Affected? | Notes |
|---------|-------|-------------|-----------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.5.1 | YES (dev-only) | `[dev-dependencies]`; not shipped |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.5.1 | YES (dev-only) | `[dev-dependencies]`; not shipped |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | YES (dev-only) | same as 2.2.1 (backend retag of 2.2.1); lock check skipped |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.5.1 | YES (dev-only) | `[dev-dependencies]`; not shipped |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.5.1 | YES (dev-only) | `[dev-dependencies]`; not shipped |
| dev (branch HEAD) | — | — | not determined | — | no HEAD lock data available in eval |

## Cross-stream context — stream 2.1.x (outside issue scope)

| Version | Build | backend tag | criterion | Affected? | Notes |
|---------|-------|-------------|-----------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.5.1 | YES (dev-only) | `[dev-dependencies]`; not shipped |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.5.1 | YES (dev-only) | `[dev-dependencies]`; not shipped |

Every version ships criterion 0.5.1, which is below the fixed version 0.5.2, so all are in the affected range. However, criterion is in the lock file only as a dev-dependency and is **not present in production builds or container images**.

## 2.3.5 Dependency chain context

```
Dependency chain for criterion:
  backend (workspace) → criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds — used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions (2.1.0 – 2.2.4)

Manifest evidence (backend/Cargo.toml, all versions):
  [dev-dependencies]
  criterion = "0.5.1"

Remediation: bump criterion to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
(direct dependency — simple version bump; no transitive two-tier approach needed)
```

### Dependency scope decision tree result

- Classification: **Dev-only dependency** (Cargo `[dev-dependencies]`, test and benchmark only, NOT shipped).
- Risk assessment: there is no production exposure. The remaining risk is to the supply chain and to developer/CI environments. For example, a crafted benchmark name could write files to arbitrary paths during `cargo bench`.
- Handling: **still create remediation tasks**, with these modifications:
  - Add the `dev-dependency` label.
  - **Override priority to Normal**, regardless of CVE severity. The CVE's priority is not inherited.
  - Add this note to each task description: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- The VEX "Component not Present" close (Case C) is **not** applied. The skill's decision tree routes dev-only dependencies to remediation at Normal priority, not to closure.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not determined (no HEAD data in eval) | Not confirmed |
| 2.1.x | Cargo | release/0.3.z | not determined (no HEAD data in eval) | Not confirmed |

The upstream fix is not confirmed, so the remediation path for the 2.2.x stream is **upstream backport + downstream propagation**, not the dependency-bump variant.

## Steps 3–7 summary (simulated, no Jira calls)

- **Step 3 – Affects Versions correction (scoped to 2.2.x):** the current value is RHTPA 2.2.0. Lock evidence shows 2.2.0 through 2.2.4 all contain criterion 0.5.1. Proposed correction: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4, with version IDs discovered dynamically. This needs engineer confirmation and must not touch 2.1.x versions. Note that all of these are affected only through a dev-only dependency.
- **Step 4 – Duplicates and siblings:** JQL for label `CVE-2026-99001` was not run. Any 2.1.x sibling would be a cross-stream companion, linked as Related. Step 4.3 overlap is skipped because Upstream Affected Component is not configured.
- **Step 5 – Lifecycle:** the product pages lookup was not run. All matrix versions are assumed supported for this analysis and need verification.
- **Step 6 – Already fixed:** no resolved siblings are known.
- **Step 7 – Concurrent triage:** skipped because Upstream Affected Component is not configured.
- **Step 7.5 – Release Jira:** find or create "RHTPA 2.2.5 Release Tasks" (Epic) and "RHTPA 2.2.5 CVE triage" (Task). This is the proposed next 2.2.x version and needs individual engineer confirmation.
