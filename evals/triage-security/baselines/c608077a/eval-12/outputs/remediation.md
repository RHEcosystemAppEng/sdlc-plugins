# Step 8 – Remediation: TC-8030 (CVE-2026-48901, h2 < 0.4.8, scoped [rhtpa-2.2])

## Decision

| Question | Answer |
|---|---|
| Any supported versions affected? | Yes. 2.1.0 and 2.1.1 (stream 2.1.x) |
| Issue scoped to a single stream? | Yes. 2.2.x |
| Issue's own stream (2.2.x) affected? | **No.** All 2.2.x builds ship h2 0.4.8 or 0.4.9 (>= fixed 0.4.8) |
| Other streams affected? | Yes. 2.1.x, so **Case A applies (cross-stream impact, proactive remediation)** |
| 2.1.x has its own CVE Jira? | None known (no sibling data), so **preemptive tasks** are created |
| Ecosystem | Cargo, a source dependency. Upstream fix on `release/0.3.z` is unconfirmed, so 2 tasks: upstream backport + downstream propagation |
| Step 7.5 release Jira | Preemptive tasks are not linked to release Jira (only non-preemptive remediation is). No release Epic or Task is created for this issue |

**Outcome for TC-8030 itself:** no 2.2.x version is affected, so no Case B tasks are created for 2.2.x.
After the cross-stream actions, recommend closing TC-8030 as **Not a Bug** with VEX Justification
(customfield_12345) = **Component not Present**. The vulnerable h2 version (< 0.4.8) is not shipped in any
2.2.x release. Every Jira mutation below is a proposal only and was not executed.

## Proposed Jira actions (in order, each requiring engineer confirmation)

1. Assign TC-8030 to the current user and transition New → Assigned (Step 0.8).
2. Affects Versions: `[RHTPA 2.2.0] → []`, with a correction comment ("Scoped to stream 2.2.x per issue suffix"; lock file analysis shows 2.2.0 ships h2 0.4.8 = fixed version) and the Comment Footnote.
3. Cross-stream impact comment on TC-8030 (with Comment Footnote):
   > Cross-stream impact: h2 < 0.4.8 (CVE-2026-48901) also affects stream(s) 2.1.x (RHTPA 2.1.0, 2.1.1 ship h2 0.4.5)
   > based on lock file analysis. These streams are tracked by companion issues (see Related links)
   > or may require separate PSIRT triage.
4. Create the 2 preemptive tasks below for stream 2.1.x. After each task, post the description digest comment, then create links:
   - TC-8030 → Task 1: **Related** (preemptive)
   - TC-8030 → Task 2: **Related** (preemptive)
   - Task 1 **Blocks** Task 2
5. Comment on TC-8030 listing the preemptive tasks (with Comment Footnote):
   > Preemptive remediation tasks created for streams without CVE Jiras:
   > - 2.1.x: <task-1-key>, <task-2-key> (security-preemptive)
   >
   > These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates
   > stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.
6. Close TC-8030: transition to Closed, resolution **Not a Bug**, VEX Justification = **Component not Present**. Comment:
   > No versions in stream 2.2.x ship a vulnerable version of h2. Version impact analysis: 2.2.0 (h2 0.4.8), 2.2.1 (0.4.8),
   > 2.2.2 (same as 2.2.1), 2.2.3 (0.4.9), 2.2.4 (0.4.9). All ship h2 >= 0.4.8, which is outside the affected range (< 0.4.8,
   > per MITRE CVE API and OSV.dev RUSTSEC-2026-0089). Stream 2.1.x is affected and is covered by preemptive tasks.
7. Add the `ai-cve-triaged` label and post the summary comment: impact table, Affects Versions correction, outcome, preemptive task links, an @mention of the reporter, and the Comment Footnote.

---

## Task 1 – Upstream backport (preemptive, stream 2.1.x)

- **Summary:** Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)
- **Issue type:** Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Link:** Related to TC-8030; Blocks Task 2

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood. h2 does not limit the number of
CONTINUATION frames following a HEADERS frame, which allows excessive memory/CPU use (DoS, CVSS 7.5).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p (RUSTSEC-2026-0089)

## Implementation Notes

- Target branch: release/0.3.z
- Fix threshold: affected < 0.4.8, fixed 0.4.8. This was cross-validated from the MITRE CVE API (lessThan 0.4.8)
  and OSV.dev (fixed 0.4.8). The Jira description had no precise threshold.
- **Dependency type**: to be confirmed. Run `cargo tree -i h2` on release/0.3.z. h2 is typically
  transitive (e.g., via hyper/reqwest/tonic). If transitive, record the full chain in the PR.
- If the vulnerable dependency is dev-only or build-only, the remediation priority is Normal
  regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable
  (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (e.g., hyper/reqwest)
- Bump it to a version whose transitive closure includes h2 >= 0.4.8
  (within the 0.4.x line, `cargo update -p h2` may suffice since 0.4.5 → 0.4.8 is semver-compatible)
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add h2@0.4.8` to add as a direct dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE tracking issue, stream 2.2.x; preemptive)
```

---

## Task 2 – Downstream propagation (preemptive, stream 2.1.x)

- **Summary:** Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
- **Issue type:** Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Link:** Related to TC-8030; blocked by Task 1

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from <task-1-key>.

The upstream backport (<task-1-key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, currently `v0.3.12`)
- **Dependency type**: carried forward from <task-1-key> (direct or transitive, to be confirmed there)
- Update the backend reference to the merged commit or new release tag (e.g., a new v0.3.x tag)
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is reflected in
  the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <task-1-key> (upstream backport must merge first)
- Related to: TC-8030 (originating CVE tracking issue, stream 2.2.x; preemptive)
```

---

## Pre-creation checklist

- [x] Task count per stream: 2.1.x Cargo (source dependency) gets 2 tasks. 2.2.x is not affected and gets 0.
- [x] Cross-stream coverage: the only affected out-of-scope stream (2.1.x) has preemptive tasks.
- [x] Link types: Related (preemptive → originating CVE TC-8030), Blocks (upstream → downstream). No Depend links, because 2.1.x has no CVE Jira of its own.
- [x] Preemptive labels: `security-preemptive` on both tasks.
- [x] Coordination guidance: omitted, because the Source Repositories table has no Deployment Context column.
- [x] Release Jira linking: not applicable. Preemptive tasks are not linked to release Jira, and 2.2.x has no remediation.
- [x] Dedup consistency: Step 7.5.3 found no dedup (Upstream Affected Component field not configured).
