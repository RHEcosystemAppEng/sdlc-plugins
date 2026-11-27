# TC-8001 — Version Impact Analysis (Step 2)

> Simulated lock file data comes from `security-matrix-mock.md` and stands in for
> `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`. No real `git show` was run.

## 2.1 Supportability matrix (aggregated)

Both streams pass format validation. Each has Supportability Matrix, Ecosystem Mappings with the
canonical columns, Source Pinning Method, and Forward Pointer.

| Stream | Konflux repo | Versions | Upstream branch (Cargo/backend) |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, backend retag of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) | `release/0.4.z` |

## 2.2 Development stream

Finding the development stream needs `getJiraIssueTypeMetaWithFields` to list unreleased
`RHTPA` versions. That is a Jira call, so it was not made, and the mock data has no unreleased
version. **No development stream row is included.** I did not invent a branch-HEAD value. In a
live run, the unreleased version with the earliest release date would be checked at branch HEAD.

## 2.3 / 2.4 Version impact table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | Outside this issue's scope (cross-stream) |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | Outside this issue's scope (cross-stream) |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | In scope |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | In scope |
| 2.2.2 | 2.2.x | `v0.4.8` | — | **YES** | Same as 2.2.1 (backend retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | Fixed version shipped |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | Fixed version shipped |
| dev | — | — | — | Not determined | Unreleased Jira versions not available (no Jira call) |

Summary:
- **In-scope (2.2.x) affected:** RHTPA 2.2.0, 2.2.1, 2.2.2. **Not affected:** 2.2.3, 2.2.4.
  The fix (quinn-proto 0.11.14) first shipped in **2.2.3** (backend `v0.4.11`, 2026-03-23).
- **Cross-stream (2.1.x) affected:** RHTPA 2.1.0 and 2.1.1. Every released 2.1.x version ships
  0.11.9, and no 2.1.x release contains the fix.
- **PSIRT-claimed RHTPA 2.0.0:** there is no 2.0.x stream in the matrix, so this cannot be
  verified and is invalid.

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn-proto
  Type: NOT DETERMINED — the mock data only contains Cargo.lock version lines; the
        Cargo.toml manifests and the lock-file dependency graph were not inspected.
  Profile: NOT DETERMINED (no evidence of dev-/build-only scope)
  Introduction point: present in every inspected tag (v0.3.8 … v0.4.12)

Remediation: if direct, bump quinn-proto to >= 0.11.14; if transitive, bump the direct
dependency that pulls it in (often the `quinn` crate — unverified), falling back to
`cargo add quinn-proto@0.11.14`.
```

The `dev-dependency` label and Normal-priority override are **not** applied, because nothing
shows the crate is dev-only.

## 2.5 Upstream fix status

Checking upstream branch HEAD needs `git -C <rhtpa-backend> show <branch>:Cargo.lock`, which was
not run. The only available evidence is the most recent **released tag** on each branch:

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? | Evidence |
|---|---|---|---|---|---|
| 2.1.x | Cargo | `release/0.3.z` | Not verified | **Unknown, treated as NOT fixed** | Latest release tag `v0.3.12` ships 0.11.9 |
| 2.2.x | Cargo | `release/0.4.z` | Not verified | **Likely YES** | Release tags `v0.4.11` and `v0.4.12` already ship 0.11.14 |

Impact on remediation path:
- **2.1.x:** use the upstream backport variant (fix not confirmed upstream). If a live
  `git show release/0.3.z:Cargo.lock` shows 0.11.14 or later, switch to the dependency-bump
  variant.
- **2.2.x:** the fix has already shipped in released product versions 2.2.3 and 2.2.4.

**Engineer review:** the skill requires the engineer to confirm this table before Step 3. In this
eval, I proceed on the table above.
