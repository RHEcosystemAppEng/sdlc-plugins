# Step 2 – Version Impact Analysis: TC-8050 (CVE-2026-99001)

## 2.1 – Supportability matrix

Loaded from the fixture `security-matrix-mock.md` (Last-Updated 2026-06-28, 128 days old; see the staleness warning in data-extraction.md).

| Stream | Konflux repo | Versions | Cargo lock file | Upstream branch |
|--------|--------------|----------|-----------------|-----------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) | `Cargo.lock` | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (retag of `v0.4.8`), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) | `Cargo.lock` | `release/0.4.z` |

## 2.2 – Development stream

The fixture has no Jira unreleased-version metadata (`getJiraIssueTypeMetaWithFields` was not called), so I could not identify a development stream or check a branch HEAD. The table therefore has no development-stream row. In a live run, query Jira for unreleased `RHTPA` versions and check the development branch HEAD.

## 2.3 – Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`)

Fix threshold: criterion **< 0.5.2** is affected. Fixed in 0.5.2. Source: the Jira description; external APIs were unavailable.

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-99001 (criterion < 0.5.2):
```

| Version | Stream | Pinned tag | criterion | Affected? | Notes |
|---------|--------|------------|-----------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.5.1 | YES (dev-only) | Outside issue scope; cross-stream |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.5.1 | YES (dev-only) | Outside issue scope; cross-stream |
| **2.2.0** | **2.2.x** | `v0.4.5` | 0.5.1 | **YES (dev-only)** | In scope |
| **2.2.1** | **2.2.x** | `v0.4.8` | 0.5.1 | **YES (dev-only)** | In scope |
| **2.2.2** | **2.2.x** | `v0.4.8` | — | **YES (dev-only)** | In scope; retag of 2.2.1 (same as 2.2.1, lock file not re-checked) |
| **2.2.3** | **2.2.x** | `v0.4.11` | 0.5.1 | **YES (dev-only)** | In scope |
| **2.2.4** | **2.2.x** | `v0.4.12` | 0.5.1 | **YES (dev-only)** | In scope |

Every supported version has criterion 0.5.1 in `Cargo.lock`, which is inside the affected range (< 0.5.2). However, criterion is a **dev-dependency only** and is **not present in production builds** (see 2.3.5). The shipped `rhtpa-server` binary and container image do not contain the vulnerable code.

### 2.3.5 – Dependency chain context

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
(direct dependency, so a simple version bump; no transitive pinning needed)
```

**Result of the dependency scope decision tree: dev-only dependency (Cargo `[dev-dependencies]`).**

- Not shipped in production. It is used only for tests and benchmarks.
- It is still a supply chain risk: a vulnerable or compromised dev dependency can affect build and CI environments. Under the skill's rules, remediation tasks are **still created**, with these changes:
  - Add the `dev-dependency` label.
  - **Override priority to Normal**, regardless of CVE severity. Do not inherit the CVE's priority.
  - Add this note to each task description: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- This is not a feature-gated optional dependency, so the VEX "Vulnerable Code not in Execute Path" prompt does not apply.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | not provided in fixture (no evidence) | Not confirmed, treated as NOT fixed |
| 2.1.x | Cargo | `release/0.3.z` | not provided in fixture (no evidence) | Not confirmed, treated as NOT fixed (cross-stream) |

The fixture has no upstream branch HEAD data for criterion, and the newest pinned tag (`v0.4.12`) still ships 0.5.1. A fix on the upstream branch cannot be confirmed, so the remediation path is **upstream backport + downstream propagation**, not the dependency-bump variant.

## Summary for engineer confirmation

- **In-scope stream 2.2.x:** all versions 2.2.0–2.2.4 ship criterion 0.5.1, affected but **dev-only**.
- **Cross-stream 2.1.x:** 2.1.0 and 2.1.1 also ship criterion 0.5.1, affected but dev-only. This triggers Case A (cross-stream impact comment, plus preemptive tasks if 2.1.x has no CVE Jira of its own).
- **Proposed Affects Versions correction (Step 3, scoped to 2.2.x):** RHTPA 2.2.0 → RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4. Confirm against Jira versions discovered at runtime.
- **Outcome:** Case B. Create remediation tasks for 2.2.x with the `dev-dependency` label and Normal priority. See remediation.md.
