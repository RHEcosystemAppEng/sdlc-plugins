# TC-8020 — Version Impact Analysis (Step 2) and Affects Versions (Step 3)

## Step 2.1 – Supportability matrix

Both streams were loaded from `security-matrix-mock.md`. The Version Streams table lists two streams:

| Stream | Konflux repo | Versions (backend tag) | Cargo upstream branch |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, retag of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) | `release/0.4.z` |

## Step 2.2 – Development stream

Jira unreleased versions were not queried (no external calls). 2.2.x is the latest stream and has no forward pointer. No development-stream evidence was supplied, so the branch-HEAD row is marked *not evaluated* and is not guessed.

## Step 2.3 – tokio versions

Source: the cross-stream version impact data supplied with the task, which stands in for `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`. Fix threshold: **1.42.0**.

## Step 2.4 – Version impact table

```
Version Impact for CVE-2026-55123 (tokio < 1.42.0):
```

| Version | Stream | backend tag | tokio | Affected? | In TC-8020 scope? | Notes |
|---|---|---|---|---|---|---|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | `v0.3.8` | 1.40.0 | **YES** | No (other stream) | Cross-stream impact; no CVE Jira for this stream |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | `v0.3.12` | 1.40.0 | **YES** | No (other stream) | Cross-stream impact; no CVE Jira for this stream |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | `v0.4.5` | 1.41.1 | **YES** | Yes | |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | `v0.4.8` | 1.41.1 | **YES** | Yes | |
| RHTPA 2.2.2 | rhtpa-2.2 (2.2.x) | `v0.4.8` | — | **YES** | Yes | Same as 2.2.1 (backend retag of `v0.4.8`); result carried forward |
| RHTPA 2.2.3 | rhtpa-2.2 (2.2.x) | `v0.4.11` | *not provided* | **UNVERIFIED** | Yes | No tokio lock-file evidence supplied. Run `git show v0.4.11:Cargo.lock` before closing out scope |
| RHTPA 2.2.4 | rhtpa-2.2 (2.2.x) | `v0.4.12` | *not provided* | **UNVERIFIED** | Yes | No tokio lock-file evidence supplied. Run `git show v0.4.12:Cargo.lock` |
| dev (branch HEAD) | — | — | *not evaluated* | — | — | No development-stream evidence |

No dependency versions were invented. 2.2.3 and 2.2.4 are in the matrix, but the supplied evidence (the four-row cross-stream table) does not cover them. The engineer must confirm them.

### Cross-stream summary

| Stream | Affected versions | tokio | Own CVE Jira? | Handling |
|---|---|---|---|---|
| rhtpa-2.2 (current scope) | 2.2.0, 2.2.1, 2.2.2 (retag); 2.2.3/2.2.4 unverified | 1.41.1 | Yes (TC-8020) | **Case B**: standard remediation tasks |
| rhtpa-2.1 (other stream) | 2.1.0, 2.1.1 | 1.40.0 | **No** (Step 4 JQL returned no results) | **Case A**: cross-stream comment and **preemptive** remediation tasks |

## Step 2.3.5 – Dependency chain context

No Cargo.lock dependency-graph evidence was supplied, so the direct/transitive classification is **undetermined**. tokio is normally a direct dependency of Rust async services, but that is not assumed here. The remediation tasks include both the direct and transitive approaches, and the engineer or `/implement-task` confirms the chain. tokio is a runtime dependency (not dev-only or build-only), so the `dev-dependency` label and Normal-priority override do not apply.

## Step 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | tokio at HEAD | Fixed? |
|---|---|---|---|---|---|
| 2.1.x | Cargo | rhtpa-backend | `release/0.3.z` | *not checked (no git access in eval)* | Unknown, treated as **not fixed** |
| 2.2.x | Cargo | rhtpa-backend | `release/0.4.z` | *not checked (no git access in eval)* | Unknown, treated as **not fixed** |

Remediation path: **upstream backport + downstream propagation** for each stream. If a later `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock` (or `release/0.3.z`) shows tokio >= 1.42.0, switch that stream's first task to the dependency-bump variant.

---

## Step 3 – Affects Versions correction (scoped to 2.2.x)

TC-8020 is scoped to `[rhtpa-2.2]`, so only 2.2.x versions are considered. The 2.1.x versions are **not** added to TC-8020; they belong to a future rhtpa-2.1 CVE Jira and are covered meanwhile by preemptive tasks.

| | Versions |
|---|---|
| Current (PSIRT) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Evidence-confirmed affected in scope | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (retag of 2.2.1) |
| **Proposed** | `[RHTPA 2.2.0, RHTPA 2.2.1]` → `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` |
| Pending engineer verification | RHTPA 2.2.3, RHTPA 2.2.4 (add if their lock files show tokio < 1.42.0) |

The PSIRT versions are correct but incomplete, so the proposal adds 2.2.2. Version IDs are discovered at runtime with `getJiraIssueTypeMetaWithFields`, not hardcoded. If a matrix version has no Jira version, flag it to the project admin.

Proposed mutation (requires confirmation; not executed):

```
jira.edit_issue("TC-8020", fields={"versions": [{"id": "<RHTPA 2.2.0 id>"}, {"id": "<RHTPA 2.2.1 id>"}, {"id": "<RHTPA 2.2.2 id>"}]})
```

Proposed correction comment:

```
Corrected Affects Versions: [RHTPA 2.2.0, RHTPA 2.2.1] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md
(RHTPA 2.2.2 is a backend retag of 2.2.1, v0.4.8, tokio 1.41.1).
Scoped to stream rhtpa-2.2 per issue suffix.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.
```

(ProdSec @mention omitted because no ProdSec Jira account ID is configured.)

## Steps 4–7 summary

| Step | Result |
|---|---|
| 4 / 4.1 Same-stream duplicates | None (no siblings found) |
| 4.2 Cross-stream siblings | **None**. JQL `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020` returned no rhtpa-2.1 issue, so there are no Related links to create |
| 4.3 Cross-CVE overlap | Skipped (Upstream Affected Component field not configured in Security Configuration) |
| 4.4 Preemptive reconciliation | No existing `security-preemptive` task for CVE-2026-55123 (rhtpa-2.2) is assumed, so new tasks are created |
| 5 Lifecycle | Not fetched (no external calls). All affected versions are assumed supported. The engineer should check the product pages, especially 2.1.x |
| 6 Already fixed | No resolved siblings, so this is not an already-fixed case |
| 7 Concurrent triage | Skipped (Upstream Affected Component field not configured) |
