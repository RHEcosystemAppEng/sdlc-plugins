# TC-8004 — Step 2: Version Impact Analysis

## 2.1 – Supportability Matrix (aggregated)

| Stream | Konflux Release Repo | Version | Build | backend tag (pinned) | Notes |
|---|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 | 0.3.8 | `v0.3.8` | |
| 2.1.x | rhtpa-release.0.3.z | 2.1.1 | 0.3.12 | `v0.3.12` | |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.x | rhtpa-release.0.4.z | 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.x | rhtpa-release.0.4.z | 2.2.2 | 0.4.9 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.x | rhtpa-release.0.4.z | 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.x | rhtpa-release.0.4.z | 2.2.4 | 0.4.12 | `v0.4.12` | |

Both matrices passed format validation: the Supportability Matrix, Ecosystem Mappings, Source Pinning Method and Forward Pointer sections are all present, and the Ecosystem Mappings columns match the template.

## 2.2 – Development Stream

The development stream comes from unreleased `RHTPA` Jira versions (`getJiraIssueTypeMetaWithFields`). That call is not available in this eval and the mock data has no branch-HEAD lock file. **The development stream was not evaluated.** In a live run, check `git show HEAD:Cargo.lock` on the dev stream's source branch and add a "(dev)" row.

## 2.3 – Dependency Versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`)

Ecosystem: **Cargo**. Lock file: `Cargo.lock` in `backend` (source of truth).

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-33501 (h2 < 0.4.8):
```

| Stream | Version | backend tag | h2 | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.4.8 | NO | ships the fixed version 0.4.8 |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.4.8 | NO | ships the fixed version 0.4.8 |
| 2.2.x | 2.2.2 | `v0.4.8` | — | NO | same as 2.2.1 (backend retag; lock check skipped) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| dev | — | branch HEAD | not evaluated | n/a | no dev-stream data available in eval |

### Impact Summary (mixed across streams)

| Stream | Versions affected | Versions not affected | Stream verdict |
|---|---|---|---|
| **2.1.x** | 2.1.0, 2.1.1 | — | **AFFECTED** (all released versions ship h2 0.4.5) |
| **2.2.x** | — | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NOT AFFECTED** (every version ships h2 >= 0.4.8) |

PSIRT got the scope partly wrong:
- **RHTPA 2.2.0 is a false positive.** Its backend tag `v0.4.5` already ships h2 0.4.8, the fixed version.
- **RHTPA 2.1.1 is missing.** It ships h2 0.4.5, which is vulnerable.

## 2.3.5 – Dependency Chain Context (affected 2.1.x versions)

```
Dependency chain for h2 (Cargo):
  backend (workspace) → ... → h2 0.4.5
  Type: not determined from available evidence (the eval mock gives only the
        resolved h2 version per tag, not the Cargo.lock dependents or Cargo.toml)
  Profile: assumed production pending verification (h2 is the HTTP/2 implementation
           normally pulled in at runtime through hyper/reqwest/tonic). Confirm with
           `git show v0.3.12:Cargo.lock` (the `dependencies` arrays that list "h2")
           and `git show v0.3.12:Cargo.toml`.
  Introduction point: h2 0.4.5 is present in 2.1.0 and 2.1.1; 2.2.0 (v0.4.5) moved to
           0.4.8, so the fix arrived in the 0.4.z line between v0.3.12 and v0.4.5.
```

h2 is usually a transitive dependency (via hyper). If it is transitive, remediation uses the two-tier approach: bump the direct dependency first, and fall back to pinning h2 directly if that bump is not possible. The remediation tasks call for this check.

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Repository | Upstream Branch | h2 at HEAD | Fixed? |
|---|---|---|---|---|---|
| 2.1.x | Cargo | backend | `release/0.3.z` | unknown (no data for `git show release/0.3.z:Cargo.lock` in eval) | **Not confirmed** |
| 2.2.x | Cargo | backend | `release/0.4.z` | n/a (stream not affected) | n/a |

The fix is not confirmed on `release/0.3.z`, so the 2.1.x remediation uses the **upstream backport + downstream propagation** path, not the dependency-bump variant. If a live check shows `release/0.3.z` already ships h2 >= 0.4.8, switch the first task to the dependency-bump variant. The task count (2) stays the same.

## Engineer Confirmation

Eval assumption: the engineer confirms the table above and proceeds to Step 3.
