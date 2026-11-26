# Step 8 – Remediation: CVE-2026-31812 (TC-8001)

## Decision summary (Steps 3–7.5, simulated — no Jira calls made)

| Step | Result |
|---|---|
| 3 – Affects Versions correction | Proposed: remove `RHTPA 2.0.0`; set `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (scoped to 2.2.x). Requires confirmation. |
| 4 – Duplicate/sibling check | Not executed (JQL disallowed). Assumption: no sibling CVE-2026-31812 Vulnerability issue exists for 2.1.x. Step 4.3 is skipped because the Upstream Affected Component field is not configured. |
| 5 – Lifecycle check | Not executed (product pages not fetched). Assumed 2.1.x and 2.2.x are in support, because both are listed in the matrix. |
| 6 – Already fixed check | No resolved siblings known. Note: 2.2.3+ already ship the fixed quinn-proto 0.11.14. |
| 7 – Concurrent triage | Skipped (Upstream Affected Component field not configured). |
| 7.5 – Release Jira | Would find or create "RHTPA 2.2.5 Release Tasks" / "RHTPA 2.2.5 CVE triage" (next patch after 2.2.4), which needs individual confirmation. Not executed. 2.1.x preemptive tasks are not linked to release Jira. |

**Outcome:** a scoped issue (2.2.x) where another stream (2.1.x) is also affected, so the
**Case A** (cross-stream + preemptive tasks for 2.1.x) and **Case B** (remediation tasks for 2.2.x) paths both apply.
Ecosystem is Cargo (source dependency), so each stream gets **2 tasks**.

- 2.2.x: the fix is already on `release/0.4.z` (v0.4.11+) and shipped in 2.2.3. This uses the **dependency bump + downstream propagation** variant. Engineer note: the latest released 2.2.x (2.2.4) is already fixed, so these tasks mostly confirm and verify. The engineer may decide the bump task is already satisfied and only verify and close it.
- 2.1.x: not fixed. This uses the **upstream backport + downstream propagation** variant, **preemptive** (`security-preemptive`, linked "Related").

Coordination guidance is omitted: the Source Repositories table has no Deployment Context column (backward compatibility rule).
Security level: copy TC-8001's security level onto every task (`security: <parent-issue-security-level>`), and omit it only if the parent has none.

---

## Task 1 — 2.2.x dependency bump (Case B)

- **Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 → Task 1 (Depend); Task 1 → release Task "RHTPA 2.2.5 CVE triage" (Blocks)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (0.11.12), 2.2.2 (same as 2.2.1, retag)
Source commit(s): v0.4.5, v0.4.8 (2.2.2 retags v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: undetermined from triage data — confirm direct vs transitive
  (likely transitive via quinn) from Cargo.toml / cargo tree
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
- Tags v0.4.11 and v0.4.12 on this branch already ship quinn-proto 0.11.14; verify
  release/0.4.z HEAD still has >= 0.11.14 — if so, no code change is needed
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

## Task 2 — 2.2.x downstream propagation (Case B)

- **Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 → Task 2 (Depend); Task 1 → Task 2 (Blocks); Task 2 → release Task (Blocks)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <Task 1 key>.

The dependency bump (<Task 1 key>) ensures quinn-proto 0.11.14 on release/0.4.z.
Once that is confirmed/merged, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: undetermined (confirm direct vs transitive) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (current latest pin v0.4.12 already contains quinn-proto 0.11.14; ensure no
  regression to a pre-v0.4.11 tag)
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Case A — Cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x (2.1.0, 2.1.1 ship quinn-proto 0.11.9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

## Task 3 — 2.1.x upstream backport (preemptive)

- **Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 → Task 3 (Related). Not linked to release Jira (preemptive).

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic (DoS) on excessive stream counts in a
QUIC STREAMS frame. The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: undetermined from triage data — confirm direct vs transitive
  (likely transitive via quinn) from Cargo.toml / cargo tree
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g. quinn)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

## Task 4 — 2.1.x downstream propagation (preemptive)

- **Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 → Task 4 (Related); Task 3 → Task 4 (Blocks)

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <Task 3 key>.

The upstream backport (<Task 3 key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: undetermined (confirm direct vs transitive) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 3 key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Creation order (after engineer confirmation)

For each task: `create_issue` (with parent security level) → description digest comment
(`[sdlc-workflow] Description digest: <tagged-digest>`) → links → later comments.

1. Task 1, digest, Depend (TC-8001 → T1), Blocks (T1 → release Task)
2. Task 2, digest, Depend (TC-8001 → T2), Blocks (T1 → T2), Blocks (T2 → release Task)
3. Related (release Task → TC-8001)
4. Task 3, digest, Related (TC-8001 → T3)
5. Task 4, digest, Related (TC-8001 → T4), Blocks (T3 → T4)
6. Comment on TC-8001: "Remediation tasks created: <T1> (dependency bump), <T2> (downstream propagation, blocked by <T1>)"
7. Comment on TC-8001: "Preemptive remediation tasks created for streams without CVE Jiras: 2.1.x: <T3>, <T4> (security-preemptive) ..."
8. Transition TC-8001 to In Progress (skip if already Assigned or later); make sure it is assigned.

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo = source dependency) for both 2.2.x and 2.1.x
- [x] Cross-stream coverage: 2.1.x has preemptive tasks (assuming no sibling CVE Jira; Step 4 JQL not run)
- [x] Link types: Depend (2.2.x tasks → own CVE), Related (2.1.x preemptive), Blocks (upstream → downstream)
- [x] Preemptive labels on 2.1.x tasks
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: non-preemptive 2.2.x tasks Block the release Task; the CVE is Related to it
- [x] Dedup consistency: no dedup (Step 7.5.3 not applicable, field not configured)

## Post-triage summary (to post on TC-8001 after confirmation)

- Add label `ai-cve-triaged`.
- The summary comment includes: the version impact table, the Affects Versions correction (RHTPA 2.0.0 → RHTPA 2.2.0/2.2.1/2.2.2),
  the outcome (remediation created; 2.2.3+ already fixed), task links T1–T4, release Epic/Task keys,
  no dedup, an ADF @mention of the TC-8001 reporter (PSIRT analyst), and the Comment Footnote (skill `triage-security`).
