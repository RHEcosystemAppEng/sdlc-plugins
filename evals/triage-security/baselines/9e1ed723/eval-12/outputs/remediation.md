# Steps 3–8 – Triage Decisions and Remediation: TC-8030 (CVE-2026-48901, h2)

All Jira mutations below are **proposals** (eval mode: no Jira calls made). In a live
run each requires explicit engineer confirmation, and every comment carries the
`triage-security` Comment Footnote.

## Step 3 – Affects Versions correction (scoped to 2.2.x)

- Current: `[RHTPA 2.2.0]`
- Stream-scoped impact table (2.2.x): 2.2.0 NO, 2.2.1 NO, 2.2.2 NO (retag), 2.2.3 NO, 2.2.4 NO
- Proposed: **remove RHTPA 2.2.0 — no 2.2.x version is affected** (2.2.0 ships h2 0.4.8, the fixed version per MITRE/OSV)
- 2.1.0 / 2.1.1 are affected but belong to the 2.1.x stream (sibling/cross-stream), not this issue
- Comment (proposed): "Affects Versions review: [RHTPA 2.2.0] → none in stream 2.2.x. Based on lock file analysis at pinned commits from security-matrix.md, using the cross-validated fix threshold h2 < 0.4.8 (MITRE CVE API + OSV.dev/RUSTSEC-2026-0089). RHTPA 2.2.0 ships h2 0.4.8 (fixed). Scoped to stream 2.2.x per issue suffix." (no ProdSec @mention — not configured)

## Step 4 – Duplicates / siblings / overlap / reconciliation

- Sibling JQL (`labels = CVE-2026-48901`, issuetype 10024): not executable in eval; fixture shows **no known siblings** and no comments. Assumed no `[rhtpa-2.1]` companion issue exists → 2.1.x has no CVE Jira of its own.
- Step 4.3 cross-CVE overlap: skipped (Upstream Affected Component field not configured).
- Step 4.4 preemptive reconciliation: no existing preemptive tasks known.

## Step 5 – Lifecycle

Product pages (`https://access.example.com/product-life-cycle/rhtpa`) not fetchable in eval. 2.1.x assumed in support (configured as an active stream); engineer should confirm before task creation.

## Step 6 – Already fixed

No resolved siblings. 2.2.x is already fixed by virtue of shipping h2 >= 0.4.8 in every release (not by a sibling fix).

## Step 7 – Concurrent triage

Skipped — Upstream Affected Component field not configured.

## Step 7.5 – Release Jira orchestration

Applies to non-preemptive remediation only. No standard (Case B) tasks are created for 2.2.x; the 2.1.x tasks are preemptive and are not linked to a release Task. No release Epic/Task proposed.

## Step 8 – Decision

```
Any supported version affected? YES (2.1.0, 2.1.1)
Issue scoped? YES (2.2.x)
Scoped stream affected? NO
Other streams affected? YES (2.1.x) → Case A (cross-stream, preemptive tasks)
```

### Outcome for TC-8030 (2.2.x) — Case C (within scope): Close as Not a Bug

1. Comment: "No supported versions in stream 2.2.x ship a vulnerable version of h2. Version impact analysis: [table from version-impact.md]. All 2.2.x versions ship h2 0.4.8 or 0.4.9, which is outside the affected range (< 0.4.8, per MITRE CVE API and OSV.dev RUSTSEC-2026-0089). Note: stream 2.1.x is affected — see cross-stream comment and preemptive tasks."
2. Transition to Closed, resolution **Not a Bug** (after the Case A actions below so the Related links exist).
3. VEX Justification (`customfield_12345`): **Component not Present** (the vulnerable h2 version range is not shipped in any 2.2.x build).

### Case A – Cross-stream impact comment on TC-8030

```
Cross-stream impact: h2 < 0.4.8 also affects stream(s) 2.1.x (RHTPA 2.1.0, 2.1.1 ship
h2 0.4.5) based on lock file analysis. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

### Case A – Preemptive remediation tasks for 2.1.x (no 2.1.x CVE Jira exists)

Ecosystem Cargo = source dependency → **2 tasks**. Upstream fix not confirmed on
`release/0.3.z` → **upstream backport + downstream propagation** variant.

Labels on both: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`.
Links: each task → TC-8030 **Related** (not Depend); Task 1 **Blocks** Task 2.
No release Task linkage (preemptive). Coordination Guidance omitted (no Deployment
Context column). Not dev-only → priority not overridden.

---

#### Task 1 — Upstream backport

**Summary:** Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood — h2 does not limit the number
of CONTINUATION frames following a HEADERS frame, allowing excessive memory/CPU use
(denial of service, CVSS 7.5).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p
Fix threshold source: MITRE CVE API (lessThan 0.4.8) and OSV.dev RUSTSEC-2026-0089
(fixed 0.4.8) — Jira description did not state a threshold.

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage — inspect Cargo.lock at
  release/0.3.z to see whether h2 is a direct workspace dependency or transitive
  (e.g., via hyper/reqwest), and apply the matching approach below.
- First check `git show release/0.3.z:Cargo.lock`; if it already ships h2 >= 0.4.8,
  record that and proceed directly to the downstream propagation task.
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if constrained)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2
- Bump it to a version whose transitive closure includes h2 >= 0.4.8
  (`cargo update -p h2` is sufficient if semver-compatible)
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add h2@0.4.8` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)
```

---

#### Task 2 — Downstream propagation

**Summary:** Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901
fix from [Task 1 key].

The upstream backport ([Task 1 key]) bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next 2.1.x build
ships the fix (current 2.1.1 pins backend v0.3.12 with h2 0.4.5).

## Implementation Notes

- Source pinning method: backend via `artifacts.lock.yaml` (download URL contains
  tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is
  reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [Task 1 key] (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)
```

---

### Proposed Jira operation order (after confirmation)

1. Create Task 1 → post description digest comment
2. Create Task 2 → post description digest comment
3. Link TC-8030 → Task 1 (Related); TC-8030 → Task 2 (Related); Task 1 → Task 2 (Blocks)
4. Comment on TC-8030: Affects Versions correction (Step 3)
5. Comment on TC-8030: cross-stream impact notice
6. Comment on TC-8030: "Preemptive remediation tasks created for streams without CVE Jiras: - 2.1.x: [Task 1 key], [Task 2 key] (security-preemptive). These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label."
7. Clear Affects Versions on TC-8030; set VEX Justification = Component not Present; transition to Closed / Not a Bug
8. Add label `ai-cve-triaged`; post post-triage summary comment (impact table, AV correction, outcome, preemptive task links, no release Jira, no dedup, @mention of the issue reporter)

### Pre-creation checklist

- [x] Task count per stream: Cargo → 2 tasks for 2.1.x; 0 for unaffected 2.2.x
- [x] Cross-stream coverage: 2.1.x covered by preemptive tasks
- [x] Link types: Related (preemptive → originating CVE), Blocks (upstream → downstream)
- [x] Preemptive labels: `security-preemptive` on both tasks
- [x] Coordination guidance: omitted (Deployment Context column absent)
- [x] Release Jira linking: N/A (preemptive only)
- [x] Dedup consistency: no Step 7.5.3 dedup (field not configured)

### Open items for the engineer

- Matrix is 148 days stale — consider refreshing before acting.
- Confirm no `[rhtpa-2.1]` sibling exists for CVE-2026-48901 (if one does, skip the preemptive tasks; that issue will own 2.1.x remediation).
- Confirm 2.1.x lifecycle status.
- Due date 2026-08-01 has already passed.
