# TC-8050 — Step 2: Version Impact Analysis

CVE-2026-99001: criterion < 0.5.2, fixed in 0.5.2. Issue scope is **2.2.x**.

## 2.1 – Supportability matrix

Both streams from the Version Streams table were loaded (mock `security-matrix-mock.md`). Format check: every required section is present (Supportability Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer), and the Ecosystem Mappings columns match the template. Result: **Pass**.

## 2.2 – Development stream

No Jira version metadata (unreleased RHTPA versions) was available in the eval, and no dev-branch HEAD lock data was supplied. The development stream could not be determined, so it is **not assessed**. I have not assumed any value for it. In a live triage this would come from `getJiraIssueTypeMetaWithFields` plus `git show HEAD:Cargo.lock`.

## 2.3 – Extracted dependency versions

Method: Cargo uses `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'` at the pinned backend tag from the matrix. Results are the simulated output from the mock lock-file data.

## 2.4 – Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

### In-scope stream: 2.2.x (rhtpa-release.0.4.z)

| Version | Backend tag (pinned) | criterion | Affected? | Notes |
|---------|----------------------|-----------|-----------|-------|
| 2.2.0 | `v0.4.5`  | 0.5.1 | YES | dev-dependency only — not shipped |
| 2.2.1 | `v0.4.8`  | 0.5.1 | YES | dev-dependency only — not shipped |
| 2.2.2 | `v0.4.8`  | —     | YES | same as 2.2.1 (backend retag of 2.2.1; lock check skipped) |
| 2.2.3 | `v0.4.11` | 0.5.1 | YES | dev-dependency only — not shipped |
| 2.2.4 | `v0.4.12` | 0.5.1 | YES | dev-dependency only — not shipped |
| dev   | branch HEAD | not available | not assessed | no development-stream data in the eval |

### Out-of-scope stream (for Case A cross-stream impact): 2.1.x (rhtpa-release.0.3.z)

| Version | Backend tag (pinned) | criterion | Affected? | Notes |
|---------|----------------------|-----------|-----------|-------|
| 2.1.0 | `v0.3.8`  | 0.5.1 | YES | dev-dependency only — not shipped |
| 2.1.1 | `v0.3.12` | 0.5.1 | YES | dev-dependency only — not shipped |

Summary: every supported version ships a lock file with criterion 0.5.1, which is inside the affected range (< 0.5.2). **Strictly by lock-file evidence**, all versions are affected. However, criterion is a **dev-only dependency** and does not reach production artifacts (see 2.3.5).

## 2.3.5 – Dependency chain context

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
and refresh Cargo.lock
```

### Dependency scope decision tree result

- Classification: **Dev-only dependency** (Cargo `[dev-dependencies]`, used for tests and benchmarks, NOT shipped in the production binary or container image).
- Effect on risk: the shipped product cannot be exploited through this path. A residual **supply-chain / build-environment risk** remains, because the path traversal can occur when benchmarks run in CI or on developer machines.
- Handling, per decision tree:
  - Remediation tasks **are still created**.
  - Each remediation task gets the **`dev-dependency`** label.
  - Priority is overridden to **Normal**, regardless of CVE severity (CVSS 5.3 Medium). The CVE's priority is not inherited.
  - Each task description carries this note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- This is **not** a feature-gated optional dependency, so the VEX "Vulnerable Code not in Execute Path" prompt does not apply. Case C (close as Not a Bug) is also not chosen, because the decision tree calls for remediation of dev-only dependencies.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.2.x | Cargo | backend (rhtpa-backend) | `release/0.4.z` | not available in eval data | NOT CONFIRMED |
| 2.1.x | Cargo | backend (rhtpa-backend) | `release/0.3.z` | not available in eval data | NOT CONFIRMED |

The eval data does not show the fix on the upstream branch, so I used the **upstream backport + downstream propagation** pair rather than the dependency-bump variant. In practice the remediation is a direct `[dev-dependencies]` bump either way.

## Steps 3–7 summary (proposed, no Jira mutations performed)

- **Step 3 – Affects Versions correction (scoped to 2.2.x):** the current value is RHTPA 2.2.0. By lock-file evidence it should be **RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4**, with version IDs discovered at runtime. The correction comment should note that criterion is dev-only and not shipped.
- **Step 4 – Duplicates/siblings:** JQL was not run in the eval. Sibling CVE-2026-99001 issues, such as a `[rhtpa-2.1]` companion, are unknown.
- **Step 5 – Lifecycle:** the product pages were not queried. No EOL status is assumed.
- **Step 6 – Already fixed:** no resolved siblings are known, so nothing is detected.
- **Step 7 – Concurrent triage:** skipped because the Upstream Affected Component field is not configured.
- **Step 7.5 – Release Jira:** would find or create "RHTPA 2.2.5 Release Tasks" and "RHTPA 2.2.5 CVE triage". The next version needs engineer confirmation and was not confirmed in the eval.
