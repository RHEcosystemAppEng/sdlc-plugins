# Step 7.5 / Step 8 – Remediation: TC-8004 (CVE-2026-33501, h2 < 0.4.8)

## Decision

| Check | Result |
|---|---|
| Any supported versions affected? | Yes: 2.1.0, 2.1.1 (stream 2.1.x) |
| Issue scope | **Unscoped**, so **Case A is skipped** (no cross-stream comment, no preemptive tasks) |
| Case | **Case B**: create remediation tasks for the affected streams only |
| 2.1.x | AFFECTED → 2 tasks (Cargo = source dependency) |
| 2.2.x | **NOT affected** (all versions ship h2 >= 0.4.8) → **no tasks** |
| Cross-CVE dedup (7.5.3) | Skipped (Upstream Affected Component field not configured) |
| Concurrent triage (7) | Skipped (same reason) |
| Upstream fix on `release/0.3.z` | Not confirmed → **upstream backport** variant (not dependency bump) |
| Dependency type | Not determined from the available evidence. Both direct and transitive approaches are included. |
| dev-dependency label | No (production runtime dependency) |
| Coordination Guidance | Left out (no Deployment Context column in Source Repositories) |
| Security level | Copy TC-8004's `security` level onto every created issue. The mock data does not show one; if TC-8004 has a level, pass it. |

Total tasks: **2** (2.1.x only). None for 2.2.x.

## Step 7.5 – Release Jira orchestration (stream 2.1.x only)

- 7.5.1: Search `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.1' AND summary ~ 'Release Tasks' ORDER BY created DESC`.
  - If found, reuse it.
  - If not found, the proposed default is the next patch after the latest 2.1.x release in the matrix (2.1.1), which is **"RHTPA 2.1.2 Release Tasks"**. Options: Accept / Specify different version / Skip. Requires individual engineer confirmation. The matrix is 151 days stale, so check that 2.1.2 has not already shipped.
- 7.5.2: Find or create **"RHTPA 2.1.2 CVE triage"** (Task, child of the Epic, labels `ai-generated-jira`). Requires individual confirmation.
- No release Jira is needed for 2.2.x because it is not affected.

---

## Task 1 – Upstream backport (2.1.x)

**Summary:** `Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)`
**Type:** Task  **Project:** TC
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`
**Security:** `<TC-8004 security level>`

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames. The h2
library accumulates CONTINUATION frame data without enforcing a size limit on the
accumulated header block, allowing a peer to consume unbounded server memory.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1 (both ship h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed (`cargo tree -i h2` on release/0.3.z). h2 is
  typically transitive (e.g. backend → hyper/reqwest/tonic → h2).
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.
- Reference: the 2.2.x line (backend v0.4.5 and later) already ships h2 0.4.8+;
  its Cargo.toml/Cargo.lock changes can guide the backport.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if constrained)
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (see dependency chain above)
- Bump the direct dependency to a version whose transitive closure
  includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add h2@0.4.8` to add as a direct dependency, overriding the
  transitive resolution (or `cargo update -p h2 --precise 0.4.8` if semver-compatible)
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

## Task 2 – Downstream propagation (2.1.x)

**Summary:** `Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)`
**Type:** Task  **Project:** TC
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`
**Security:** `<TC-8004 security level>`

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from {{upstream-task-key}}.

The upstream backport ({{upstream-task-key}}) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: backend via `artifacts.lock.yaml` (download URL contains
  tag, e.g., `v0.3.12`). Update it to the new release tag that contains the fix.
- **Dependency type**: carried forward from upstream task
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

- Depends on: {{upstream-task-key}} (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## No tasks for 2.2.x

Stream 2.2.x (rhtpa-release.0.4.z / `release/0.4.z`) is **not affected**. Every
released version (2.2.0 through 2.2.4) ships h2 0.4.8 or 0.4.9, which is at or above
the fixed version 0.4.8. No upstream, downstream, or preemptive task is created for it.

---

## Creation and linkage sequence (each step requires confirmation, none executed)

1. Create Task 1 → post description digest comment (`[sdlc-workflow] Description digest: <sha256-...>`) before any links.
2. Create Task 2 → post description digest comment.
3. Links:
   - TC-8004 → Task 1 (**Depend**)
   - TC-8004 → Task 2 (**Depend**)
   - Task 1 → Task 2 (**Blocks**: the upstream task blocks downstream)
   - Task 1 → release Task "RHTPA 2.1.2 CVE triage" (**Blocks**)
   - Task 2 → release Task (**Blocks**)
   - release Task → TC-8004 (**Related**)
4. TC-8004 is already moved to Assigned (an indeterminate-category status) in Step 0.8, so skip the In Progress transition. Assignment was handled in Step 0.8.
5. Comment on TC-8004: "Remediation tasks created: {{task1}} (upstream backport), {{task2}} (downstream propagation, blocked by {{task1}})" plus footnote.

## Pre-creation checklist

- [x] Task count per stream: 2.1.x → 2 (Cargo = source dependency); 2.2.x → 0 (not affected)
- [x] Cross-stream coverage: N/A (unscoped issue, so Case A is skipped)
- [x] Link types: Depend (own CVE), Blocks (upstream → downstream, remediation → release Task), Related (release Task → CVE)
- [x] Preemptive labels: none (TC-8004 covers 2.1.x directly)
- [x] Coordination guidance: left out (no Deployment Context column)
- [x] Release Jira linking: both 2.1.x tasks → release Task (Blocks); CVE → release Task (Related)
- [x] Dedup consistency: dedup skipped (field not configured)

## Post-triage summary (proposed)

- Add label `ai-cve-triaged` to TC-8004.
- Summary comment on TC-8004 containing:
  - the version impact table
  - the Affects Versions correction ([RHTPA 2.1.0, RHTPA 2.2.0] → [RHTPA 2.1.0, RHTPA 2.1.1])
  - the outcome: remediation created for 2.1.x only, and 2.2.x not affected
  - the two task keys
  - the release Epic/Task keys
  - dedup: none
  - an ADF @mention of the TC-8004 reporter (PSIRT analyst; account ID from the issue `reporter` field)
  - the comment footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.14.0."
