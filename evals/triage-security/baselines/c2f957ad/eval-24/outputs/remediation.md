# TC-8001 — Step 8 Remediation

## Decision

- Supported versions affected: **YES**. In 2.2.x: 2.2.0, 2.2.1, 2.2.2. In 2.1.x: 2.1.0 and 2.1.1.
- Issue scope: **scoped** to 2.2.x (`[rhtpa-2.2]`).
- Other streams affected: **YES** (2.1.x). This is **Case A**: post a cross-stream comment and create preemptive tasks for 2.1.x, because it has no CVE Jira of its own (assumed). Then apply **Case B** to 2.2.x.
- Ecosystem: **Cargo** (source dependency), so each stream gets 2 tasks.
  - 2.2.x: released tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14, so the fix is probably already on `release/0.4.z`. That makes this the **dependency bump + downstream propagation** variant. The engineer must confirm this, because branch HEAD was not inspected.
  - 2.1.x: there is no evidence of a fix on `release/0.3.z`, so this is the **upstream backport + downstream propagation** variant (preemptive).
- Deployment context: rhtpa-backend defaults to `upstream` because the Source Repositories table has no Deployment Context column. Under the backward-compatibility rule, **no Coordination Guidance subsection is added** to any task.
- Labels on standard tasks: `ai-generated-jira`, `Security`, `CVE-2026-31812`. Preemptive tasks also get `security-preemptive`.
- Security level: copied from the parent TC-8001. The mock does not include it; omit it only if the parent has none.
- No dev-dependency label, so priority follows the CVE (High).

---

## Task 1 — 2.2.x dependency bump (standard)

**Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812
**Links:** TC-8001 → Depend → this task. This task Blocks Task 2. This task Blocks the 2.2.x release Task (Step 7.5, if active).

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8 (2.2.2 is a backend retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage (no manifest data available) — verify whether quinn-proto is a direct dependency of a workspace member or transitive (e.g., via quinn)
- Released tags v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14; verify that release/0.4.z HEAD is >= 0.11.14. If it is, no source change is needed and this task can be closed once verified.
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update
- If the vulnerable dependency is dev-only or build-only, the remediation
  priority is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

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

---

## Task 2 — 2.2.x downstream propagation (standard)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812
**Links:** TC-8001 → Depend → this task. Task 1 Blocks this task. This task Blocks the 2.2.x release Task (if active).

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from {{Task 1 key}}.

The dependency bump ({{Task 1 key}}) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend — `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: not determined — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Current latest reference v0.4.12 already ships quinn-proto 0.11.14; confirm the next build continues to reference a tag >= v0.4.11
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

- Depends on: {{Task 1 key}} (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Task 3 — 2.1.x upstream backport (preemptive)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Links:** TC-8001 → Related → this task. This task Blocks Task 4. Not linked to a release Task, because the task is preemptive.

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS via
excessive STREAMS frame). The vulnerable dependency (quinn-proto < 0.11.14) must be
updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (no manifest data available) — verify direct vs transitive before choosing the approach below
- If the vulnerable dependency is dev-only or build-only, the remediation
  priority is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn)
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

---

## Task 4 — 2.1.x downstream propagation (preemptive)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Links:** TC-8001 → Related → this task. Task 3 Blocks this task.

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
CVE-2026-31812 fix from {{Task 3 key}}.

The upstream backport ({{Task 3 key}}) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend — `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: not determined — carried forward from upstream task
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

- Depends on: {{Task 3 key}} (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Proposed Jira comments on TC-8001 (each comment ends with the triage-security Comment Footnote)

1. **Affects Versions correction:** RHTPA 2.0.0 → RHTPA 2.2.0, 2.2.1, 2.2.2 (based on lock file evidence; 2.2.3 and 2.2.4 ship quinn-proto 0.11.14).
2. **Cross-stream impact:** quinn-proto < 0.11.14 also affects stream 2.1.x (2.1.0 and 2.1.1 ship 0.11.9) according to lock file analysis. This stream is tracked by companion issues (see Related links) or may need separate PSIRT triage.
3. **Preemptive tasks:** 2.1.x: {{Task 3 key}}, {{Task 4 key}} (security-preemptive, Related link).
4. **Remediation tasks created:** {{Task 1 key}} (dependency bump), {{Task 2 key}} (downstream propagation, blocked by {{Task 1 key}}).
5. **Post-triage summary:** version impact table, AV correction, outcome (remediation created), task links, release Jira references (pending Step 7.5), and an @mention of the TC-8001 reporter. Add the `ai-cve-triaged` label.

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo source dependency) for 2.2.x and 2.1.x
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks
- [x] Link types: Depend (2.2.x to TC-8001), Related (2.1.x preemptive), Blocks (upstream to downstream)
- [x] Preemptive labels on the 2.1.x tasks
- [x] Coordination guidance: **intentionally omitted**, because the Source Repositories table has no Deployment Context column (backward compatibility; the context defaults to `upstream`, but no subsection is added)
- [ ] Release Jira linking: pending Step 7.5 (no Jira access in eval)
- [x] Dedup consistency: no dedup found (Step 7.5.3 not run, and Upstream Affected Component field not configured)
