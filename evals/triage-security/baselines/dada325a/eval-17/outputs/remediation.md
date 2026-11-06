# Step 8 – Remediation: CVE-2026-31812 (TC-8001)

## Decision

- Supported versions affected: **yes** (2.2.0, 2.2.1, 2.2.2 in scope; 2.1.0, 2.1.1 cross-stream).
- Issue scoped to 2.2.x (`[rhtpa-2.2]`) and another stream (2.1.x) is affected →
  **Case A** (cross-stream comment + preemptive tasks for 2.1.x) **plus Case B**
  (remediation tasks for 2.2.x).
- Ecosystem: Cargo → source dependency → **2 tasks per stream**.
  - 2.2.x: fix already on `release/0.4.z` (shipped since `v0.4.11` / 2.2.3) →
    dependency bump + downstream propagation.
  - 2.1.x: fix not confirmed on `release/0.3.z` → upstream backport + downstream
    propagation, preemptive variant.
- Coordination Guidance: omitted (no Deployment Context column in Source Repositories).
- Embargo: High severity — gate passed (engineer confirmed). Upstream PRs must still
  respect https://example.com/security/embargo-policy if the CVE is not yet public.

> Engineer note: 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14, so the next 2.2.x
> build from `release/0.4.z` already contains the fix. Task 1 is primarily a
> verification; if confirmed, Task 2 can be closed once the Konflux repo is confirmed
> to reference `v0.4.11` or later.

---

## Task 1 (2.2.x) — Dependency bump

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Links**: TC-8001 → Depend → this task; this task → Blocks → Task 2

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient. quinn-proto before 0.11.14 panics when
a remote peer sends a QUIC STREAMS frame requesting an excessive number of
streams (denial of service, CVSS 7.5).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): backend v0.4.5, v0.4.8 (v0.4.9 build is a retag of v0.4.8)
Already fixed in: backend v0.4.11 / v0.4.12 (quinn-proto 0.11.14; RHTPA 2.2.3, 2.2.4)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (expected chain: backend → ... → quinn → quinn-proto);
  confirm with `cargo tree -i quinn-proto`
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects quinn-proto >= 0.11.14 after the update (release/0.4.z
  is expected to already be at 0.11.14 as of v0.4.11 — if so, record that no change
  is needed)
- The vulnerable dependency is a production (runtime) dependency, not dev-only;
  priority follows the CVE severity.

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

## Task 2 (2.2.x) — Downstream propagation

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Links**: TC-8001 → Depend → this task; Task 1 → Blocks → this task

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <Task 1 key>.

The dependency bump (<Task 1 key>) ensures quinn-proto is 0.11.14 on
release/0.4.z. Once that is merged/verified, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  (must be `v0.4.11` or later; `v0.4.12` is the current latest and already ships 0.11.14)
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

- Depends on: <Task 1 key> (upstream dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Case A – Cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x (RHTPA 2.1.0, 2.1.1 — quinn-proto 0.11.9) based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

No sibling CVE Jira for 2.1.x is known → create preemptive tasks (Tasks 3 and 4).

---

## Task 3 (2.1.x, preemptive) — Upstream backport

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Links**: TC-8001 → Related → this task; this task → Blocks → Task 4

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of
service via crafted QUIC STREAMS frame, CVSS 7.5).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): backend v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: transitive (expected chain: backend → ... → quinn → quinn-proto);
  confirm with `cargo tree -i quinn-proto`
- Production (runtime) dependency — not dev-only; priority follows CVE severity.
- Upstream fix status on release/0.3.z was not confirmed (last release tag v0.3.12
  ships 0.11.9).

### Remediation approach (direct dependency)

If quinn-proto turns out to be a direct dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn or the
  HTTP/3 client stack)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14 (a semver-compatible `cargo update -p quinn-proto`
  within 0.11.x may be sufficient)
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
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

## Task 4 (2.1.x, preemptive) — Downstream propagation

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Links**: TC-8001 → Related → this task; Task 3 → Blocks → this task

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: transitive — carried forward from upstream task
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

## Jira operations (proposed — each requires engineer confirmation; NOT executed)

1. Step 0.8: assign TC-8001 to current user; transition New → Assigned.
2. Step 3: Affects Versions RHTPA 2.0.0 → RHTPA 2.2.0, 2.2.1, 2.2.2 (+ correction comment with footnote).
3. Create Tasks 1–4; post description digest comment on each before any links.
4. Links: TC-8001 Depend → Tasks 1, 2; TC-8001 Related → Tasks 3, 4;
   Task 1 Blocks Task 2; Task 3 Blocks Task 4; (if Step 7.5 release Task exists)
   Tasks 1, 2 Blocks release Task, release Task Related TC-8001.
5. Cross-stream impact comment (Case A) and preemptive-task list comment on TC-8001.
6. Remediation-task list comment: "Remediation tasks created: <T1> (dependency bump),
   <T2> (downstream propagation, blocked by <T1>)".
7. Add label `ai-cve-triaged`; post post-triage summary comment (impact table,
   Affects Versions correction, tasks, @mention of reporter, Comment Footnote).

## Pre-creation checklist

- [x] Task count per stream: Cargo → 2 tasks for 2.2.x, 2 tasks for 2.1.x
- [x] Cross-stream coverage: 2.1.x covered by preemptive Tasks 3–4
- [x] Link types: Depend (own CVE), Related (preemptive), Blocks (upstream → downstream)
- [x] Preemptive labels on 2.1.x tasks
- [x] Coordination guidance: omitted (no Deployment Context column)
- [ ] Release Jira linking: pending Step 7.5 (not resolvable in eval)
- [x] Dedup consistency: no Step 7.5.3 dedup (Upstream Affected Component not configured)
