# TC-8004 — Step 7.5 / Step 8 Remediation

## Decision

- Supported versions affected: **yes** (2.1.0, 2.1.1).
- Issue scope: **unscoped** → Case A (cross-stream preemptive) is **skipped**; go to **Case B**.
- Affected streams: **2.1.x only**. The 2.2.x stream is not affected → **no tasks for 2.2.x**.
- Ecosystem: Cargo (source dependency) → **2 tasks** for 2.1.x.
- Upstream fix on `release/0.3.z` not confirmed (Step 2.5) → upstream backport variant
  (not the dependency-bump variant).
- Dedup (7.5.3), cross-CVE overlap (4.3), concurrent triage (7): skipped — Upstream
  Affected Component field not configured.
- No siblings, no preemptive tasks to reconcile → standard (non-preemptive) tasks,
  linked to TC-8004 with `Depend`.

## Step 7.5 – Release Jira Orchestration (2.1.x)

- Search: `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.1' AND summary ~ 'Release Tasks' ORDER BY created DESC`
- If none found, proposed default (next patch after latest released 2.1.1):
  **"RHTPA 2.1.2 Release Tasks"** (Epic) with child Task **"RHTPA 2.1.2 CVE triage"**.
  Each requires individual engineer confirmation (Accept / specify version / Skip).
- No release Jira for 2.2.x (stream not affected).

---

## Task 1 — Upstream backport (2.1.x)

**Summary:** Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`
**Issue type:** Task — Project TC

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames. The h2
library accumulates CONTINUATION frame data without enforcing a size limit on the
accumulated header block, allowing a peer to consume unbounded server memory.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed — run `cargo tree -i h2` on release/0.3.z
  (direct vs transitive could not be determined from triage evidence)
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (e.g. via `cargo tree -i h2`)
- Bump it to a version whose transitive closure includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo update -p h2 --precise 0.4.8` (or `cargo add h2@0.4.8`) to override the
  transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

## Task 2 — Downstream propagation (2.1.x)

**Summary:** Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`
**Issue type:** Task — Project TC

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix
from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is
  reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

(Coordination Guidance subsection omitted: Source Repositories table has no Deployment
Context column.)

---

## Proposed Jira operations (in order; each requires confirmation — NOT executed)

1. Create Task 1 → post description digest comment on it.
2. Create Task 2 → post description digest comment on it.
3. Link TC-8004 → Task 1 (`Depend`); TC-8004 → Task 2 (`Depend`).
4. Link Task 1 → Task 2 (`Blocks`; downstream blocked by upstream).
5. If release Jira active: Task 1 → release Task (`Blocks`), Task 2 → release Task
   (`Blocks`); release Task → TC-8004 (`Related`).
6. TC-8004 already transitioned to Assigned in Step 0.8 → skip "In Progress" transition.
7. Comment on TC-8004: "Remediation tasks created: <task-1> (upstream backport),
   <task-2> (downstream propagation, blocked by <task-1>)" + Comment Footnote.
8. Add label `ai-cve-triaged` to TC-8004.
9. Post-triage summary comment on TC-8004 with version impact table, Affects Versions
   correction (2.1.0, 2.2.0 → 2.1.0, 2.1.1), outcome (remediation for 2.1.x only;
   2.2.x not affected), task links, release Jira refs, no dedup, @mention of the
   reporter, and the Comment Footnote.

## Not created

- **No 2.2.x tasks** — all 2.2.x versions (2.2.0–2.2.4) already ship h2 >= 0.4.8.
- No preemptive tasks (issue is unscoped; Case A not applicable).
- No new Vulnerability issues (PSIRT owns those).
- No Not-a-Bug closure / VEX value (2.1.x is affected).

## Pre-creation checklist

- [x] Task count per stream: 2.1.x → 2 (Cargo source dependency); 2.2.x → 0 (not affected)
- [x] Cross-stream coverage: N/A (unscoped issue)
- [x] Link types: Depend (CVE → tasks), Blocks (upstream → downstream)
- [x] Preemptive labels: none required
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: planned for RHTPA 2.1.x release Task, pending confirmation
- [x] Dedup consistency: dedup skipped (field not configured)

## Open items for the engineer

- Matrix is 131 days stale — refresh to confirm no newer 2.1.x release exists.
- Confirm 2.1.x is within support lifecycle (product pages not checked).
- Confirm h2 dependency chain (`cargo tree -i h2`) and whether `release/0.3.z` HEAD already ships h2 >= 0.4.8 (would switch Task 1 to the dependency-bump variant).
- Due date 2026-08-01 has already passed.
