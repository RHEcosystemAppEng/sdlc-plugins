# TC-8050 — Step 2: Version Impact Analysis

CVE-2026-99001: **criterion < 0.5.2** (fixed in 0.5.2). Ecosystem: Cargo. Issue scope: **2.2.x**.

Lock file data comes from the simulated output of `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`, as supplied in security-matrix-mock.md. Manifest and chain data come from the simulated Step 2.3.5 output in vuln-issue-dev-dependency.md.

## 2.1: Matrix load and format validation

| Stream | Konflux repo | Sections (Supportability Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer) | Ecosystem Mappings columns | Result |
|--------|--------------|------|------|--------|
| 2.1.x | rhtpa-release.0.3.z | present | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | Pass |
| 2.2.x | rhtpa-release.0.4.z | present | same | Pass |

Matrix staleness: both matrices were last updated 2026-06-28, which is 145 days old. The engineer chose to proceed (see data-extraction.md).

## 2.2: Development stream

No Jira version metadata is available in this eval, because `getJiraIssueTypeMetaWithFields` was not called. 2.2.x is the latest configured stream and has no forward pointer. Its upstream branch `release/0.4.z` stands in for the development head. That branch HEAD was not checked because the fixture has no data for it (see 2.5).

## 2.4: Version Impact Table (scoped stream: 2.2.x)

```
Version Impact for CVE-2026-99001 (criterion < 0.5.2):
```

| Version | Build | backend tag | criterion | Affected? | Notes |
|---------|-------|-------------|-----------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | YES | same as 2.2.1 (backend retag of 2.2.1); lock check skipped |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.5.1 | YES | dev-dependency only (not shipped) |

### Cross-stream impact (outside issue scope)

| Version | Build | backend tag | criterion | Affected? | Notes |
|---------|-------|-------------|-----------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.5.1 | YES | dev-dependency only (not shipped) |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.5.1 | YES | dev-dependency only (not shipped) |

All supported versions in both streams pin criterion **0.5.1**, which is below the 0.5.2 fix. Per the lock file, every version is in the affected range. The dependency is dev-only, so the vulnerable code does **not** ship in any production artifact.

## 2.3.5: Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) → criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds — used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions (2.1.0 – 2.2.4)

Remediation: bump criterion to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
(direct dependency, so no transitive two-tier approach is needed)
```

Manifest evidence:

```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency scope decision

The dependency scope decision tree classifies this as **Cargo `[dev-dependencies]`: dev/build-only, NOT shipped**. The resulting handling:

- Remediation tasks are **still created**, because a compromised or vulnerable dev dependency is a supply-chain and build-environment risk.
- Each remediation task gets the **`dev-dependency`** label.
- Task priority is set to **Normal**, overriding the CVE severity (CVSS 5.3 Medium). The CVE's priority is not inherited.
- Each task description includes this note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- It is not a feature-gated optional dependency, so the VEX "Vulnerable Code not in Execute Path" prompt does not apply.

## 2.5: Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not available (no fixture data; `git show` not run) | UNKNOWN, treated as not fixed |
| 2.1.x | Cargo | release/0.3.z | not available (no fixture data; `git show` not run) | UNKNOWN, treated as not fixed |

No evidence shows the fix already on the upstream branch, so Step 8 uses the **upstream backport + downstream propagation** task pair, not the dependency-bump variant. If the engineer confirms that `release/0.4.z` already has criterion >= 0.5.2, switch the first task to the dependency-bump template.

## Downstream Step 3–7 summary (for context)

- **Step 3 (Affects Versions):** the Jira field shows RHTPA 2.2.0, but the lock file evidence shows every 2.2.x version is affected. Proposed correction: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4. Version IDs must be discovered dynamically, so this is not executed.
- **Step 4 (Duplicates/siblings):** JQL was not run. The search for sibling CVE-2026-99001 issues, especially a `[rhtpa-2.1]` companion, still needs to be done.
- **Step 5 (Lifecycle):** product pages were not queried, so lifecycle status for 2.1.x and 2.2.x is not verified.
- **Step 6 (Already fixed):** no resolved siblings are known, and no lock file shows criterion >= 0.5.2.
- **Step 7 (Concurrent triage):** skipped because the Upstream Affected Component field is not configured.
- **Step 8 outcome:** **Case B** (2.2.x affected), plus **Case A** (2.1.x is also affected outside scope).
