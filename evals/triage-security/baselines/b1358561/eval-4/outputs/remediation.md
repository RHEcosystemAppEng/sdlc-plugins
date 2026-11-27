# TC-8004 — Steps 7.5 / 8 Remediation

## Decision

| Check | Result |
|---|---|
| Any supported version affected? | Yes: 2.1.0 and 2.1.1 (2.1.x stream) |
| Issue scope | **Unscoped**, so **Case A is skipped** (it applies to scoped issues only) |
| Case | **Case B: create remediation tasks for affected streams only** |
| Affected streams | **2.1.x only** |
| Unaffected streams | **2.2.x: no tasks** (every 2.2.x version ships h2 >= 0.4.8) |
| Ecosystem | Cargo (source dependency), so **2 tasks** for 2.1.x |
| Upstream fix on `release/0.3.z` | Unknown (not confirmed), so use **upstream backport + downstream propagation** |
| Step 7 concurrent triage | skipped (Upstream Affected Component field not configured) |
| Step 7.5.3 cross-CVE dedup | skipped (same reason). 2.1.x is not deduplicated. |
| Coordination Guidance | omitted. The Source Repositories table has no Deployment Context column, and the template says to omit it in that case. |
| Total new Tasks | **2** (none for 2.2.x) |

The existing Vulnerability TC-8004 stays as it is, with Affects Versions corrected to
[RHTPA 2.1.0, RHTPA 2.1.1]. No Vulnerability issues are created.

## Step 7.5 — Release Jira orchestration (2.1.x only)

Not executed. These proposals need individual engineer confirmation:

1. **7.5.1 Epic search:** `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.1' AND summary ~ 'Release Tasks' ORDER BY created DESC`
   - If an Epic exists, reuse it.
   - If none exists, the proposed default is **"RHTPA 2.1.2 Release Tasks"**: a patch bump from the latest released 2.1.x version (2.1.1) in the matrix. The options are Accept, Specify a different version, or Skip.
2. **7.5.2 Release Task:** find or create **"RHTPA 2.1.2 CVE triage"** as a child of that Epic (separate confirmation).
3. No release Jira for 2.2.x, because that stream is not affected.

## Task 1: Upstream backport (2.1.x)

- **Summary:** `Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)`
- **Project / Type:** TC / Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`
- **Security level:** copy TC-8004's `security` level (`{id, name}`) from the live issue
- **Priority / fixVersion:** prompt the engineer (per Jira Field Defaults)

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames. A peer can
send an unbounded number of CONTINUATION frames after a HEADERS frame and h2
accumulates the header block without a size limit, allowing unbounded memory
consumption on the server (CVSS 7.5).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed. Triage did not have manifest/dependency-graph
  evidence. Inspect Cargo.lock reverse dependencies (e.g. `cargo tree -i h2`) to
  determine whether h2 is direct or transitive (commonly via hyper / reqwest / tonic).
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if constrained)
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency, use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (`cargo tree -i h2`)
- Bump the direct dependency to a version whose transitive closure
  includes h2 >= 0.4.8 (h2 0.4.x is semver-compatible, so `cargo update -p h2`
  may suffice)
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add h2@0.4.8` to add as a direct dependency, overriding the
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

## Task 2: Downstream propagation (2.1.x), blocked by Task 1

- **Summary:** `Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)`
- **Project / Type:** TC / Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`
- **Security level:** copy TC-8004's `security` level

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <TASK-1-KEY>.

The upstream backport (<TASK-1-KEY>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next 2.1.x build ships the fix.

## Implementation Notes

- Source pinning method: backend is pinned via `artifacts.lock.yaml` (download URL
  contains the tag, currently `v0.3.12`)
- **Dependency type**: carried forward from <TASK-1-KEY>
- Update the rhtpa-backend reference to the merged commit or new release tag
  (e.g. a new v0.3.x tag cut from release/0.3.z)
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

- Depends on: <TASK-1-KEY> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira operations sequence (proposed, needs confirmation, none executed)

1. Create Task 1. Post a description digest comment
   (`[sdlc-workflow] Description digest: sha256-...`) before any links.
2. Create Task 2. Post its description digest comment.
3. Links:
   - TC-8004 → Task 1 (**Depend**)
   - TC-8004 → Task 2 (**Depend**)
   - Task 1 → Task 2 (**Blocks**: upstream blocks downstream)
   - Task 1 → RHTPA 2.1.x release Task (**Blocks**), if Step 7.5 is accepted
   - Task 2 → RHTPA 2.1.x release Task (**Blocks**), if Step 7.5 is accepted
   - release Task → TC-8004 (**Related**), if Step 7.5 is accepted
4. Transition TC-8004 to In Progress. Skip this if it is already in an
   indeterminate-category status such as ASSIGNED from Step 0.8.
5. Comment on TC-8004: "Remediation tasks created: <TASK-1-KEY> (upstream backport),
   <TASK-2-KEY> (downstream propagation, blocked by <TASK-1-KEY>)" + footnote.
6. Add the `ai-cve-triaged` label to TC-8004.
7. Post-triage summary comment, which includes: the version impact table; the Affects
   Versions correction [2.1.0, 2.2.0] → [2.1.0, 2.1.1]; outcome "remediation created
   for 2.1.x; 2.2.x not affected (h2 >= 0.4.8)"; task keys; release Epic/Task keys;
   "dedup: skipped (field not configured)"; an ADF @mention of the TC-8004 reporter; and
   the Comment Footnote ("This comment was AI-generated by sdlc-workflow/triage-security
   v0.14.0.").

## Pre-creation checklist

- [x] Task count per stream: 2.1.x has 2 (Cargo source dependency). 2.2.x has 0 (not affected).
- [x] Cross-stream coverage: N/A because the issue is unscoped (Case A skipped)
- [x] Link types: Depend (task to own CVE), Blocks (upstream to downstream, task to release Task); no preemptive Related links
- [x] Preemptive labels: none (no preemptive tasks; TC-8004 covers 2.1.x itself)
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: planned for both tasks, if the 2.1.x release Task is accepted
- [x] Dedup consistency: dedup skipped, no streams marked as deduplicated

## Open items for a live run

- Matrix is 152 days stale. Refresh it and re-check for any new 2.1.x or 2.2.x releases.
- Confirm the upstream h2 version on `release/0.3.z`. If it is already >= 0.4.8, use the
  dependency-bump variant for Task 1.
- Determine the development stream through Jira unreleased versions and check its HEAD.
- Verify that 2.1.x is still in support on the product lifecycle page.
- Resolve Jira version IDs, the TC-8004 reporter, and its security level.
