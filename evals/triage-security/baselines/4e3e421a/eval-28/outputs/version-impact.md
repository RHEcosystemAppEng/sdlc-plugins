# TC-8060 — Step 2 Version Impact Analysis

CVE-2026-99010: h2 < 0.4.5 (fixed in 0.4.5). Issue scope: **2.2.x** (`[rhtpa-2.2]`).

## 2.1 — Matrix loaded

| Stream | Konflux repo | Versions | Retags |
|--------|--------------|----------|--------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) | none |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, retag of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) | 2.2.2 is a backend retag of 2.2.1 |

Matrix format check: Supportability Matrix, Ecosystem Mappings, Source Pinning Method, and Forward Pointer are all present. The Ecosystem Mappings columns match the template. **Pass.**

## 2.2 — Development stream

This step needs `getJiraIssueTypeMetaWithFields` to find unreleased RHTPA versions. It was **not run** because Jira calls are not allowed in this eval. No development stream evidence exists, so no dev row is shown. In a live run, add the unreleased version's branch-HEAD `Cargo.lock` result before Step 3.

## 2.3 — Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`)

**Evidence source note (data conflict):** the two fixtures disagree for the 2.2.x tags:

- The issue fixture's lock file evidence (vuln-issue-transitive.md, "Mock Dependency Chain Data") gives h2 **0.4.4** for 2.2.0–2.2.2 and **0.4.5** for 2.2.3 and later.
- The matrix fixture's generic "h2 versions by tag" table gives h2 0.4.8 at `v0.4.5`/`v0.4.8` and 0.4.9 at `v0.4.11`/`v0.4.12`. That would make every 2.2.x version NOT affected.

This triage uses the **issue-specific lock file evidence** for 2.2.x, because it is the simulated `git show` output written for this scenario and it agrees with PSIRT's Affects Versions. Under Important Rule 2, the engineer must settle this conflict against the real `Cargo.lock` at `v0.4.5`, `v0.4.8`, `v0.4.11`, and `v0.4.12` before any Jira mutation. The issue fixture gives no per-version h2 data for 2.1.x, so 2.1.x uses the matrix table.

## 2.4 — Version impact table

```
Version Impact for CVE-2026-99010 (h2 < 0.4.5):
```

| Stream | Version | Backend tag | h2 | Affected? | Notes |
|--------|---------|-------------|----|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | NO | Out of scope (matrix data) |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | NO | Out of scope (matrix data) |
| **2.2.x** | **2.2.0** | `v0.4.5` | 0.4.4 | **YES** | transitive: reqwest → hyper → h2 |
| **2.2.x** | **2.2.1** | `v0.4.8` | 0.4.4 | **YES** | transitive: reqwest → hyper → h2 |
| **2.2.x** | **2.2.2** | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag; lock file check skipped, result carried forward) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.5 | NO | Fixed version shipped |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.5 | NO | Fixed version shipped |
| dev | — | branch HEAD | not checked | — | Needs Jira unreleased-version lookup (Step 2.2) |

**In-scope affected versions (2.2.x): 2.2.0, 2.2.1, 2.2.2.**
**Out-of-scope streams affected: none.** 2.1.x ships h2 0.4.5, so Case A (cross-stream) does not apply.

## 2.3.5 — Dependency chain context

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency in [dependencies])

First appeared: 2.1.0 (initial project setup — reqwest has always depended on hyper/h2)
Present in all versions

Resolved versions in affected lock files (2.2.0–2.2.2):
  reqwest 0.12.5  → hyper 1.4.1 → h2 0.4.4   (vulnerable, < 0.4.5)
Resolved in fixed lock files (2.2.3+):
  h2 0.4.5                                    (fixed)

Manifest evidence (backend/Cargo.toml, all versions):
  [dependencies]
  reqwest = { version = "0.12", features = ["json"] }
  # h2 is NOT a direct dependency

Remediation: two-tier
  1. Preferred: bump the direct dependency (reqwest, and hyper with it if needed)
     to a release whose resolved dependency tree has h2 >= 0.4.5. Because h2 0.4.5
     is semver-compatible with the existing 0.4.x requirement chain, a
     `cargo update -p h2` (lock-only refresh within reqwest 0.12 / hyper 1.x) is
     likely enough. 2.2.3 already resolves h2 0.4.5 with the same manifest.
  2. Fallback: pin the transitive dep directly with `cargo add h2@0.4.5` in the
     backend workspace if the reqwest/hyper bump is not viable (breaking API
     change, or an intermediate crate pins h2 < 0.4.5). That case may need
     coordination with the reqwest/hyper maintainers.
```

### Dependency scope decision

| Check | Result |
|-------|--------|
| `[dev-dependencies]` / `[build-dependencies]`? | No. reqwest is in `[dependencies]` |
| Feature-gated optional? | No. Not `optional = true`, and h2 comes in through reqwest's default HTTP/2 support via hyper |
| Classification | **Production runtime dependency.** No `dev-dependency` label, no priority override, and no VEX "Vulnerable Code not in Execute Path" option |

## 2.5 — Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | not read (would need `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock`). Latest released tags `v0.4.11`/`v0.4.12` from this branch ship h2 0.4.5 | **Likely YES. Inferred from tags, not verified at HEAD** |

Effect on remediation: the fixed h2 appears to be on `release/0.4.z` already. That makes this the **dependency bump** path, not an upstream backport. The task still keeps the two-tier transitive approach in case HEAD regressed or the engineer must re-pin. The current 2.2.x release (2.2.4) already ships the fix. The affected versions are earlier z-stream builds (2.2.0–2.2.2). See remediation.md for how this affects the outcome.

## Step 3 preview — Affects Versions correction (proposed, not executed)

| | Value |
|--|--|
| Current (PSIRT) | RHTPA 2.2.0 |
| Proposed (lock file evidence, 2.2.x scope only) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Rationale | 2.2.1 (`v0.4.8`) resolves h2 0.4.4. 2.2.2 is a retag of 2.2.1. 2.2.3/2.2.4 ship h2 0.4.5 and stay excluded. Version IDs would come from `getJiraIssueTypeMetaWithFields` at runtime |
