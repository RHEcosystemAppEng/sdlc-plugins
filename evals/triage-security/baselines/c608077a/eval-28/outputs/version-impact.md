# TC-8060 — Step 2 Version Impact Analysis

CVE-2026-99010: h2 < 0.4.5 is affected and 0.4.5 is the fix. The ecosystem is Cargo and the lock file is `Cargo.lock` in `backend`.
Issue scope: **2.2.x** (`rhtpa-release.0.4.z`, upstream branch `release/0.4.z`).

## 2.1 – Supportability matrix (loaded from security-matrix-mock.md)

| Stream | Konflux repo | Versions | Format check |
|--------|--------------|----------|--------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) | Pass |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, retag of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) | Pass |

Pinning method: `artifacts.lock.yaml`. The download URL contains the backend tag.

## 2.2 – Development stream

Not determined. The unreleased RHTPA versions come from `getJiraIssueTypeMetaWithFields`, and Jira was not called in this eval. Neither stream has a forward pointer to a 3.x dev stream, so no dev-HEAD row is included. **The engineer needs to confirm whether a development stream exists.**

## ⚠ Evidence conflict (engineer must resolve)

The two fixture sources disagree about the h2 versions in the 2.2.x lock files:

| Tag (version) | `security-matrix-mock.md`, "h2 versions by tag" | TC-8060 fixture, Step 2.3.5 Cargo.lock evidence |
|---------------|------------------------------------------------|------------------------------------------------|
| `v0.4.5` (2.2.0) | 0.4.8 | 0.4.4 |
| `v0.4.8` (2.2.1 / 2.2.2) | 0.4.8 | 0.4.4 |
| `v0.4.11` (2.2.3) | 0.4.9 | 0.4.5 |
| `v0.4.12` (2.2.4) | 0.4.9 | 0.4.5 |

- With the matrix-mock values, **no** 2.2.x version is affected (all ≥ 0.4.5), which would lead to Case C, closing as Not a Bug.
- With the TC-8060 Cargo.lock evidence, 2.2.0 through 2.2.2 ship h2 **0.4.4**, which is affected.

This triage uses the **TC-8060 Cargo.lock evidence**. It is the scenario-specific simulated `git show <tag>:Cargo.lock` output for this CVE, and it includes the full `[[package]]` blocks (h2, hyper, reqwest) that show the dependency chain. The matrix-mock h2 table is generic data shared across scenarios. In a real run, the engineer must re-run `git show v0.4.5:Cargo.lock | grep -A2 'name = "h2"'` (and the same for `v0.4.8`, `v0.4.11`, `v0.4.12`) before any Jira mutation. If the matrix-mock values turn out to be correct, the outcome changes to Case C.

## 2.3 / 2.4 – Version impact table

```
Version Impact for CVE-2026-99010 (h2 < 0.4.5):
```

| Version | Stream | Pinned backend tag | h2 | Affected? | Notes |
|---------|--------|--------------------|----|-----------|-------|
| 2.2.0 | 2.2.x (in scope) | `v0.4.5` | 0.4.4 | **YES** | |
| 2.2.1 | 2.2.x (in scope) | `v0.4.8` | 0.4.4 | **YES** | |
| 2.2.2 | 2.2.x (in scope) | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag of 2.2.1, lock check skipped) |
| 2.2.3 | 2.2.x (in scope) | `v0.4.11` | 0.4.5 | NO | first fixed version in the stream |
| 2.2.4 | 2.2.x (in scope) | `v0.4.12` | 0.4.5 | NO | |
| 2.1.0 | 2.1.x (out of scope) | `v0.3.8` | 0.4.5 | NO | matrix-mock lock data only, cross-stream check |
| 2.1.1 | 2.1.x (out of scope) | `v0.3.12` | 0.4.5 | NO | matrix-mock lock data only, cross-stream check |
| dev | — | branch HEAD | not checked | unknown | no dev stream identified (Jira not queried) |

Summary: in the scoped stream, **2.2.0, 2.2.1, and 2.2.2 are affected**, and 2.2.3 and 2.2.4 are already fixed. No other stream is affected, so **Case A (cross-stream) does not apply**.

### Dependency chain context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime [dependencies] entry, not dev/build-only)

First appeared: 2.1.0 (initial project setup — reqwest has always depended on hyper/h2)
Present in all versions (2.1.x and 2.2.x)

Manifest evidence (backend/Cargo.toml, all versions):
  [dependencies]
  reqwest = { version = "0.12", features = ["json"] }
  # h2 is NOT a direct dependency

Lock evidence (Cargo.lock, 2.2.0–2.2.2):
  reqwest 0.12.5  → depends on hyper
  hyper   1.4.1   → depends on h2
  h2      0.4.4   (vulnerable, < 0.4.5)

Lock evidence (Cargo.lock, 2.2.3+):
  h2      0.4.5   (fixed)

Remediation: two-tier, because h2 is transitive.
  1. Preferred: bump the direct dependency (reqwest, or hyper as the intermediate)
     so that the resolved transitive closure includes h2 >= 0.4.5. Since
     reqwest 0.12 → hyper 1.x → h2 0.4.x is semver-compatible, a
     `cargo update -p reqwest` / `cargo update -p h2` within the existing
     constraints is expected to be enough (2.2.3+ already resolves h2 0.4.5).
  2. Fallback: pin h2 directly (`cargo add h2@0.4.5`) if reqwest/hyper
     constraints prevent resolving 0.4.5.
```

Dependency scope decision: **production** runtime dependency. No `dev-dependency` label is needed, no priority override applies, and there is no feature-gate VEX option.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | not read (git disallowed in eval) | **Likely YES.** The released tags `v0.4.11` and `v0.4.12` from this branch already ship h2 0.4.5. HEAD still needs to be confirmed with `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock \| grep -A2 'name = "h2"'` |

Because HEAD could not be verified, the remediation tasks use the upstream-backport template with the two-tier transitive approach. Its first action is to verify `release/0.4.z`. If HEAD already has h2 ≥ 0.4.5, the upstream task closes as already satisfied. The downstream task then only needs to confirm that the Konflux reference points at `v0.4.11` or later, which 2.2.3 and 2.2.4 already do.

## Step 3 – Affects Versions correction (proposed, not executed)

| | Versions |
|--|----------|
| Current (PSIRT) | RHTPA 2.2.0 |
| Proposed | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Rationale | Cargo.lock at `v0.4.5` and `v0.4.8` resolves h2 0.4.4 (< 0.4.5). 2.2.2 is a retag of 2.2.1. 2.2.3 and 2.2.4 ship 0.4.5. |

Version IDs must be discovered dynamically through `getJiraIssueTypeMetaWithFields`. The change needs engineer confirmation and a comment with the Comment Footnote.

## Steps 4–7 – Notes (not executed, Jira unavailable)

- Step 4: JQL sibling search (`labels = CVE-2026-99010`) not run. Step 4.3 is skipped because the Upstream Affected Component field is not configured.
- Step 5: lifecycle check of 2.2.0–2.2.2 at the Product pages URL not run. Any EOL z-stream would be dropped from remediation.
- Step 6: already-fixed check against resolved siblings not run. Note that 2.2.3+ already ship the fixed h2.
- Step 7: skipped because the Upstream Affected Component field is not configured.
- Step 7.5: the release Epic and release Task (RHTPA <next 2.2.z> Release Tasks / CVE triage) still need to be found or created. This is not executed and uses placeholders.
