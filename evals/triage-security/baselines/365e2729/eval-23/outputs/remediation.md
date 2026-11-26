# TC-8001 Triage — Remediation (Step 8)

## Decision

- The issue is scoped to **2.2.x** and has affected versions in that stream (2.2.0, 2.2.1, 2.2.2), so **Case B** applies: create remediation tasks for 2.2.x.
- Stream **2.1.x** (2.1.0, 2.1.1) is also affected and is outside the issue's scope, so **Case A** applies. Post a cross-stream impact comment. No sibling CVE Jira for 2.1.x was found in the provided data, so 2.1.x gets **preemptive** tasks (label `security-preemptive`, linked as "Related").
- Ecosystem: Cargo, a source dependency, so each stream gets 2 tasks.
- Deployment context for rhtpa-backend is **customer-shipped**. Every task's Implementation Notes includes the customer-shipped `### Coordination Guidance` subsection.
- Steps 4.3 and 7 are skipped because the Upstream Affected Component field is not configured. Step 7.5 release Jira: RHTPA 2.2.x release Epic and Task, then find or create, with confirmation required.
- Every task is created with the parent TC-8001 security level, labels `ai-generated-jira, Security, CVE-2026-31812`, and a description digest comment posted before any links.

---

## Task 1 — Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

Variant: dependency bump (the fix is available upstream on release/0.4.z).
Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
Links: TC-8001 → Depend → this task; this task Blocks Task 2; this task Blocks the RHTPA 2.2.x CVE triage release Task.

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), 2.2.1 (0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8 (2.2.2 is a retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: undetermined (dependency chain not available) — verify with `cargo tree -i quinn-proto`
- **Remediation action**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version still < 0.11.14, pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects quinn-proto >= 0.11.14 after the update
- Note: tags v0.4.11 and v0.4.12 (RHTPA 2.2.3/2.2.4) already ship 0.11.14; confirm branch HEAD and close as already satisfied if no change is required
- If the vulnerable dependency is dev-only or build-only, priority is Normal and add the `dev-dependency` label

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

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

## Task 2 — Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
Links: TC-8001 → Depend → this task; Task 1 Blocks this task; this task Blocks the release Task.

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from {{Task 1 key}}.

The dependency bump ({{Task 1 key}}) bumps quinn-proto to 0.11.14 on
release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: undetermined — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly, verify the pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: {{Task 1 key}} (upstream change must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Task 3 (preemptive) — Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

Variant: upstream backport (release/0.3.z still at 0.11.9 as of v0.3.12).
Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
Links: TC-8001 → Related → this task; this task Blocks Task 4. Preemptive tasks are not linked to the release Jira.

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), 2.1.1 (0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: undetermined (dependency chain not available) — verify with `cargo tree -i quinn-proto`
- If the vulnerable dependency is dev-only or build-only, priority is Normal and add the `dev-dependency` label

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess a code-level workaround (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency** (e.g., quinn) to a version whose transitive
closure includes quinn-proto >= 0.11.14; verify no breaking API changes.

**Fallback: pin the transitive dependency directly**: `cargo add quinn-proto@0.11.14`;
document why the direct dep bump was not viable in the PR description.

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue, stream 2.2.x)
```

---

## Task 4 (preemptive) — Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
Links: TC-8001 → Related → this task; Task 3 Blocks this task.

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
CVE-2026-31812 fix from {{Task 3 key}}.

The upstream backport ({{Task 3 key}}) bumps quinn-proto to 0.11.14 on
release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: undetermined — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly, verify the pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: {{Task 3 key}} (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue)
```

---

## Cross-stream impact comment (Case A, on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
(RHTPA 2.1.0, 2.1.1 ship quinn-proto 0.11.9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: {{Task 3 key}}, {{Task 4 key}} (security-preemptive)

---
<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

## Pre-creation checklist

- [x] Task count per stream: 2 per stream (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks
- [x] Link types: Depend (2.2.x to TC-8001), Related (preemptive 2.1.x), Blocks (upstream to downstream)
- [x] Preemptive labels on the 2.1.x tasks
- [x] Coordination guidance: customer-shipped text in every task's Implementation Notes
- [x] Release Jira linking: the 2.2.x non-preemptive tasks Block the release Task; TC-8001 is Related to the release Task
- [x] Dedup consistency: not applicable (the Upstream Affected Component field is not configured)

Post-triage: add the `ai-cve-triaged` label, then post a summary comment with the impact table, the Affects Versions correction, task links, release Jira references, a reporter @mention, and the Comment Footnote. All of this requires engineer confirmation.
