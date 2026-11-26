# TC-8050 — Step 2: Version Impact Analysis

Source data: security-matrix-mock.md (supportability matrix plus mock `Cargo.lock` data) and the mock dependency chain data in vuln-issue-dev-dependency.md. This stands in for the output of `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'` and the manifest inspection.

Issue scope: **2.2.x** (from the `[rhtpa-2.2]` suffix). 2.1.x was also checked, as Rule 4 requires, to detect cross-stream impact.

## 2.1 — Supportability matrix (2.2.x stream, rhtpa-release.0.4.z)

| Version | Build | backend tag | Notes |
|---------|-------|-------------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | `v0.4.12` | |

Matrix format validation passed: Supportability Matrix, Ecosystem Mappings, Source Pinning Method and Forward Pointer are all present, and the Ecosystem Mappings columns match the template.

## 2.2 — Development stream

The fixture provides no unreleased RHTPA Jira versions and no development-branch HEAD lock file data. No development stream was identified, so no dev row is added. In a live run, this comes from `getJiraIssueTypeMetaWithFields`.

## 2.4 — Version impact table

```
Version Impact for CVE-2026-99001 (criterion < 0.5.2):
```

**Issue stream: 2.2.x (in scope)**

| Version | backend tag | criterion | Affected? | Notes |
|---------|-------------|-----------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.5.1 | YES (dev-only) | dev-dependency, not in production build |
| 2.2.1 | `v0.4.8` | 0.5.1 | YES (dev-only) | dev-dependency, not in production build |
| 2.2.2 | `v0.4.8` | — | YES (dev-only) | retag of 2.2.1, so the 2.2.1 result is carried forward |
| 2.2.3 | `v0.4.11` | 0.5.1 | YES (dev-only) | dev-dependency, not in production build |
| 2.2.4 | `v0.4.12` | 0.5.1 | YES (dev-only) | dev-dependency, not in production build |

**Other stream: 2.1.x (out of scope; cross-stream impact only)**

| Version | backend tag | criterion | Affected? | Notes |
|---------|-------------|-----------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.5.1 | YES (dev-only) | dev-dependency, not in production build |
| 2.1.1 | `v0.3.12` | 0.5.1 | YES (dev-only) | dev-dependency, not in production build |

Every inspected version pins criterion 0.5.1, which is below the 0.5.2 fix threshold. The package appears in `Cargo.lock` at every pinned commit, so by lock-file analysis every version is in the affected range. The dependency chain below qualifies this: criterion is a dev-only dependency.

## 2.3.5 — Dependency chain context

```
Dependency chain for criterion:
  backend (workspace) → criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds — used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions (2.1.0 through 2.2.4)

Remediation: bump criterion to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
```

Manifest evidence (all versions):

```toml
# backend/Cargo.toml
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency scope decision

The profile is **Cargo `[dev-dependencies]`**, so it falls under **dev-only / build-only (not shipped in production)** in the decision tree.

- The production binary and container image do not include criterion, so the runtime exploit risk to shipped RHTPA is nil.
- It is still a supply chain risk (a compromised dev dependency can inject code during builds or benchmarks), so **remediation tasks are still created**, with these changes:
  - Add the `dev-dependency` label to each remediation task.
  - Set priority to **Normal** regardless of CVE severity. The CVE's priority is not inherited.
  - Add this note to each task description: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- It is not a feature-gated optional dependency, so the VEX-skip prompt does not apply.

## 2.5 — Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.2.x | Cargo | backend | `release/0.4.z` | no HEAD data in fixture; latest pinned tag `v0.4.12` has 0.5.1 | NO (not confirmed fixed) |

The upstream fix is not confirmed, so the 2.2.x remediation uses the **upstream backport + downstream propagation** pair. Before starting, the engineer should check `git -C <rhtpa-backend> show release/0.4.z:Cargo.lock`. If HEAD already has criterion >= 0.5.2, switch the first task to the dependency-bump variant.

## Steps 3–7 summary (as relevant to the outputs)

- **Step 3, Affects Versions:** The Jira field is `RHTPA 2.2.0`. The lock-file evidence shows 2.2.0, 2.2.1, 2.2.2, 2.2.3 and 2.2.4 all ship criterion 0.5.1, but only as a dev dependency. Proposed correction, scoped to 2.2.x: add RHTPA 2.2.1, 2.2.2, 2.2.3 and 2.2.4. Version IDs would be found at runtime and the change needs engineer confirmation. Not executed in the eval.
- **Step 4, Siblings:** Not queried (no Jira). In a live run, the JQL for `CVE-2026-99001` would find any 2.1.x companion issue.
- **Step 5, Lifecycle:** Not queried (no external calls).
- **Step 6, Already fixed:** No resolved sibling data, so not already fixed.
- **Step 7, Concurrent triage:** Skipped because the Upstream Affected Component field is not configured.
- **Case A, cross-stream:** 2.1.x is also affected (criterion 0.5.1, dev-only). For a scoped issue, a cross-stream impact comment is proposed: "Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x based on lock file analysis (dev-dependency only, not shipped in production). These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage." If Step 4 finds no 2.1.x CVE Jira, preemptive tasks labeled `security-preemptive` and `dev-dependency` would be created for 2.1.x. Those preemptive tasks are listed in remediation.md.
