# Step 7.5 / Step 8 – Remediation: TC-8004

## Decision

- Supported versions affected: **yes** (2.1.0, 2.1.1) -> not Case C.
- Issue is **unscoped** -> Case A skipped (no "other streams" outside scope) -> **Case B** for affected streams.
- Affected streams: **2.1.x only**. Stream 2.2.x is NOT affected (h2 0.4.8/0.4.9 in all versions) -> **no remediation tasks for 2.2.x**.
- Ecosystem: Cargo (source dependency) -> **2 tasks** for 2.1.x.
- Upstream fix on `release/0.3.z`: unknown (no data) -> **upstream backport + downstream propagation** (not dependency-bump variant).
- Step 7 concurrent triage / Step 7.5.3 dedup: skipped (Upstream Affected Component field not configured).
- Preemptive tasks: none (unscoped issue owns all streams; Depend links, no `security-preemptive` label).

## Step 7.5 – Release Jira orchestration (2.1.x only)

1. Search: `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.1' AND summary ~ 'Release Tasks' ORDER BY created DESC` (not executed in eval).
2. If none found -> propose default `RHTPA 2.1.2 Release Tasks` (next patch after latest released 2.1.1); engineer options: Accept / Specify / Skip. Individual confirmation required.
3. Find/create child Task `RHTPA 2.1.2 CVE triage` under the Epic (individual confirmation). Labels `ai-generated-jira`; post description digest after each creation.

No release Jira for 2.2.x (stream not affected).

---

## Task 1 — Upstream backport (2.1.x)

**Summary**: `Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)`
**Issue type**: Task | **Project**: TC
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`
**Priority**: prompt engineer (CLAUDE.md: Prompt for priority) — CVSS 7.5 High
**fixVersion**: prompt engineer (e.g. RHTPA 2.1.2 if confirmed in 7.5)

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames — h2
accumulates CONTINUATION frame data without a size limit on the header block,
allowing a peer to consume unbounded server memory.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (only Cargo.lock package
  version was inspected). Run `cargo tree -i h2` to determine whether h2 is
  direct or transitive and record the chain in the PR.
- Not identified as dev-only/build-only; production priority applies.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if pinned)
- If the bump introduces breaking changes, assess a code-level workaround
  (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (e.g. hyper/reqwest/tonic)
- Bump it to a version whose transitive closure includes h2 >= 0.4.8
  (within h2 0.4.x, `cargo update -p h2 --precise 0.4.8` may suffice)
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add h2@0.4.8` to override transitive resolution
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

---

## Task 2 — Downstream propagation (2.1.x)

**Summary**: `Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)`
**Issue type**: Task | **Project**: TC
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag,
  currently `v0.3.12`)
- **Dependency type**: carried forward from upstream task (to be determined there)
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the
  pinning is reflected in the downstream build's Cargo.lock after the update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

Coordination Guidance subsection omitted: Source Repositories table has no Deployment Context column (backward-compat rule).

---

## Creation order and linkage (after confirmation)

1. Create Task 1 -> post description digest comment (`[sdlc-workflow] Description digest: <sha256-md:...>`).
2. Create Task 2 -> post description digest comment.
3. Links:
   - TC-8004 -> Task 1 (`Depend`)
   - TC-8004 -> Task 2 (`Depend`)
   - Task 1 -> Task 2 (`Blocks`; downstream blocked by upstream)
   - Task 1 -> release Task `RHTPA 2.1.2 CVE triage` (`Blocks`) [if 7.5 active]
   - Task 2 -> release Task (`Blocks`) [if 7.5 active]
   - release Task -> TC-8004 (`Related`) [if 7.5 active]
4. TC-8004 already Assigned from Step 0.8 (indeterminate category) -> skip "In Progress" transition.
5. Comment on TC-8004: "Remediation tasks created: <Task 1> (upstream backport), <Task 2> (downstream propagation, blocked by <Task 1>)" + footnote.

## No tasks for 2.2.x

| Stream | Reason |
|---|---|
| 2.2.x | Not affected — 2.2.0/2.2.1/2.2.2 ship h2 0.4.8, 2.2.3/2.2.4 ship h2 0.4.9 (>= fix 0.4.8). No remediation, no preemptive task. |

## Pre-creation checklist

- [x] Task count per stream: 2.1.x -> 2 (Cargo source dependency); 2.2.x -> 0 (not affected)
- [x] Cross-stream coverage: N/A (unscoped issue)
- [x] Link types: Depend (task <-> own CVE), Blocks (upstream -> downstream, remediation -> release Task), Related (release Task -> CVE)
- [x] Preemptive labels: none required
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: planned for 2.1.x if release Task confirmed
- [x] Dedup consistency: dedup skipped (field not configured)

## Post-triage summary (after all actions)

- Add label `ai-cve-triaged` to TC-8004.
- Summary comment: version impact table (2.1.x YES, 2.2.x NO), Affects Versions correction ([2.1.0, 2.2.0] -> [2.1.0, 2.1.1]), outcome "remediation created for 2.1.x only", task keys, release Epic/Task keys, no dedup, @mention of TC-8004 reporter (ADF mention node with reporter account ID), and footnote "This comment was AI-generated by sdlc-workflow/triage-security v0.14.0."
