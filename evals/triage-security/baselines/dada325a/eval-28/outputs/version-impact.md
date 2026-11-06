# Step 2 – Version Impact Analysis: TC-8060 (CVE-2026-99010, h2 < 0.4.5)

_Simulated `git show <tag>:Cargo.lock` output comes from the fixtures. No git commands were run._

## 2.1 – Supportability Matrix (loaded from `security-matrix-mock.md`)

Matrix format validation passed. All required sections are present, and the Ecosystem Mappings columns are `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`.

| Stream | Konflux Release Repo | Cargo lock file | Check command | Upstream branch |
|--------|----------------------|-----------------|---------------|-----------------|
| 2.1.x | rhtpa-release.0.3.z | `Cargo.lock` (backend) | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| 2.2.x (**in scope**) | rhtpa-release.0.4.z | `Cargo.lock` (backend) | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Source pinning method for backend: `artifacts.lock.yaml`. The download URL contains the tag.

## 2.2 – Development Stream

Jira was not queried for unreleased versions because of the eval constraint. The matrix marks 2.2.x as the latest stream with no forward pointer, so no separate development stream (e.g. 3.0.x) was identified. The upstream-branch HEAD check (2.5) covers the in-progress state of `release/0.4.z`.

## 2.3 – Extracted Dependency Versions (h2)

**Evidence source note:** The two fixtures disagree for 2.2.x:
- The issue fixture's lock-file evidence (Step 2.3.5 mock) gives h2 **0.4.4** for 2.2.0–2.2.2 and **0.4.5** for 2.2.3+.
- The matrix fixture's generic "h2 versions by tag" table gives 0.4.8 for `v0.4.5`/`v0.4.8` and 0.4.9 for `v0.4.11`/`v0.4.12`.

This triage uses the **issue fixture's Cargo.lock evidence**. That evidence is specific to TC-8060 and is the simulated lock-file output the eval designates for this scenario. **The engineer must re-verify with real `git show v0.4.5:Cargo.lock | grep -A2 'name = "h2"'` before any Jira mutation.** With the other table, every 2.2.x version would be NOT affected (Case C).

### Version Impact for CVE-2026-99010 (h2 < 0.4.5), stream 2.2.x (issue scope)

| Version | Build | backend tag (pinned) | h2 | Affected? | Notes |
|---------|-------|----------------------|----|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.4.4 | **YES** | transitive via reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.4.4 | **YES** | transitive via reqwest → hyper → h2 |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag of 2.2.1; lock check skipped and result carried forward) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.5 | NO | at fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.5 | NO | at fixed version |

### Other streams (Case A cross-stream check only, outside issue scope)

| Version | backend tag (pinned) | h2 | Affected? | Notes |
|---------|----------------------|----|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | NO | from the matrix fixture h2 table. The issue fixture says h2 is present in all versions but gives no 2.1.x lock version |
| 2.1.1 | `v0.3.12` | 0.4.5 | NO | same as above |

Result: **Stream 2.2.x is affected at 2.2.0, 2.2.1 and 2.2.2.** The 2.1.x stream is not affected, so no Case A cross-stream notice or preemptive tasks are needed.

## 2.3.5 – Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime [dependencies] entry; not dev/build-only, not feature-gated)

Resolved versions (Cargo.lock, 2.2.0–2.2.2):
  reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4   (vulnerable)
Resolved versions (Cargo.lock, 2.2.3+):
  h2 0.4.5                                   (fixed)

First appeared: 2.1.0 (initial project setup; reqwest has always depended on hyper/h2)
Present in: all versions (2.1.x and 2.2.x)
Introduction point: not applicable (h2 was always present). The fix arrived through a lock-file
  refresh between backend v0.4.8 (2.2.1/2.2.2) and v0.4.11 (2.2.3).

Manifest evidence (backend/Cargo.toml, all versions):
  [dependencies]
  reqwest = { version = "0.12", features = ["json"] }
  # h2 is NOT a direct dependency

Remediation: preferred tier is to bump the direct dependency reqwest (and with it hyper) to a
release whose resolved closure includes h2 >= 0.4.5. Fallback tier is to pin h2 directly
(`cargo add h2@0.4.5`, or `cargo update -p h2 --precise 0.4.5`, which hyper's semver range
`h2 = "0.4"` allows). Coordination with hyper/reqwest maintainers is only needed if an
intermediate crate pins h2 < 0.4.5 (not indicated by the evidence).
```

**Dependency scope decision:** production dependency. There is no `dev-dependency` label and no priority override. It is not feature-gated, so no VEX "Vulnerable Code not in Execute Path" option applies.

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | not read (eval: no `git show`) | **Likely YES**, because the later tags `v0.4.11`/`v0.4.12` cut from this branch already resolve h2 0.4.5 |

Implication: the fix is probably already on `release/0.4.z` and has shipped in 2.2.3/2.2.4. Before choosing the remediation variant, the engineer should confirm with `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "h2"'`.
- If the fix is confirmed on HEAD, use the dependency-bump variant. The upstream task reduces to verifying, or locking in with an explicit floor, h2 >= 0.4.5. The downstream task makes sure the Konflux pin is at or after `v0.4.11`.
- If it is not confirmed, use the upstream backport variant with the two-tier approach below.

## Step 3 preview – Affects Versions Correction (proposed, not executed)

| | Versions |
|---|---|
| PSIRT-assigned | RHTPA 2.2.0 |
| Evidence-based (2.2.x scope) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Proposed change | **Add** RHTPA 2.2.1 and RHTPA 2.2.2. Keep RHTPA 2.2.0 |

Version IDs must be discovered dynamically with `getJiraIssueTypeMetaWithFields`. The correction comment must include the Comment Footnote.

## Steps 4–7 notes (not executable in eval)

- Step 4: Run sibling JQL for label `CVE-2026-99010` to find same-stream duplicates and the 2.1.x companion. Step 4.3 (overlap) is skipped because the Upstream Affected Component field is not configured.
- Step 5: Check the lifecycle of 2.2.0–2.2.2 at the Product pages URL. Not performed.
- Step 6: Already-fixed check. Shipped release 2.2.3 already contains h2 0.4.5. Customers on 2.2.0–2.2.2 can be remediated by upgrading to 2.2.3 or later, so the engineer should weigh this when deciding whether new remediation work is needed versus documenting "fixed in 2.2.3".
- Step 7: Skipped because the Upstream Affected Component field is not configured.

**Engineer confirmation of this table is required before proceeding to Step 3.**
