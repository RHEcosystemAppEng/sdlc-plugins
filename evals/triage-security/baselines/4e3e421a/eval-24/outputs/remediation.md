# TC-8001 — Remediation Plan (Step 8)

**CVE:** CVE-2026-31812, quinn-proto < 0.11.14 (fixed in 0.11.14). Ecosystem is Cargo, a source dependency, so each affected stream gets **2 tasks**.
**Issue scope:** 2.2.x (from `[rhtpa-2.2]`).
**Outcome:** Case B for 2.2.x and Case A (preemptive) for 2.1.x.
**Deployment context:** `upstream` (default). The Source Repositories table has **no Deployment Context column**, so each task **leaves out the Coordination Guidance subsection** under Implementation Notes, as remediation-templates.md requires.

Nothing below was executed. Each Jira mutation would need explicit engineer confirmation first.

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks for 2.2.x and 2 tasks for 2.1.x
- [x] Cross-stream coverage: 2.1.x (outside scope) gets preemptive tasks, assuming no sibling CVE Jira exists (Step 4 JQL not run in eval)
- [x] Link types: Depend (TC-8001 → 2.2.x tasks), Related (TC-8001 → 2.1.x preemptive tasks), Blocks (upstream/bump → downstream in each stream)
- [x] Preemptive labels: `security-preemptive` on both 2.1.x tasks
- [x] Coordination guidance: left out, because the Deployment Context column is absent
- [x] Release Jira linking: the non-preemptive 2.2.x tasks would Block the RHTPA 2.2.x release Task, and TC-8001 would be Related to it (if Step 7.5 is active)
- [x] Dedup consistency: no dedup (Upstream Affected Component field not configured)

**Note for the engineer on 2.2.x:** 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14, and release/0.4.z carries the fix. So the 2.2.x tasks use the **dependency bump** variant, and their main job is to confirm that the current branch and next build still ship 0.11.14 or later. The engineer may decline them as already satisfied.

---

## Task 1 — 2.2.x dependency bump (Case B)

- **Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 → Task 1 (Depend); Task 1 → Task 2 (Blocks); Task 1 → RHTPA 2.2.x release Task (Blocks)

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1, v0.4.8)
Source commit(s): v0.4.5, v0.4.8 (fixed in v0.4.11 and v0.4.12, which ship quinn-proto 0.11.14)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage (no Cargo.toml / cargo tree evidence); quinn-proto is commonly transitive via quinn — verify with `cargo tree -i quinn-proto`
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update (tags v0.4.11/v0.4.12 already ship 0.11.14; confirm branch HEAD has not regressed)
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

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

- **Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Links:** TC-8001 → Task 2 (Depend); blocked by Task 1 (Blocks); Task 2 → RHTPA 2.2.x release Task (Blocks)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from [Task 1 key].

The dependency bump ([Task 1 key]) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: not determined (see [Task 1 key]) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [Task 1 key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Case A — Cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x based on lock file analysis (2.1.0 / v0.3.8 and 2.1.1 / v0.3.12 ship quinn-proto 0.11.9).
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

## Task 3 — 2.1.x upstream backport (preemptive)

- **Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 → Task 3 (Related); Task 3 → Task 4 (Blocks). Not linked to the release Task because it is preemptive.
- **Variant:** upstream backport. No HEAD evidence shows release/0.3.z has the fix (the last tag, v0.3.12, ships 0.11.9).

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS via crafted QUIC STREAMS frame).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (no Cargo.toml / cargo tree evidence); quinn-proto is commonly transitive via quinn — verify with `cargo tree -i quinn-proto`
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (likely quinn)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
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

- **Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Links:** TC-8001 → Task 4 (Related); blocked by Task 3 (Blocks)

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

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from [Task 3 key].

The upstream backport ([Task 3 key]) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: not determined (see [Task 3 key]) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [Task 3 key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Follow-up Jira operations (proposed, not executed)

1. After each task is created, post a description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`) before any links.
2. Add the links listed above.
3. Post a preemptive task-list comment on TC-8001 listing Tasks 3 and 4 (2.1.x, `security-preemptive`), with the footnote.
4. Correct Affects Versions from RHTPA 2.0.0 to RHTPA 2.2.0, 2.2.1, 2.2.2.
5. Assign TC-8001 and transition it to Assigned, then to In Progress.
6. Add the `ai-cve-triaged` label to TC-8001.
7. Post a summary comment on TC-8001 with the version impact table, the Affects Versions correction, outcome (remediation created), task keys, release Jira keys, no dedup, an @mention of the reporter, and the Comment Footnote.
