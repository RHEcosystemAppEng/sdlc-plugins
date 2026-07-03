# Step 8 -- Remediation: CVE-2026-48901 (h2 < 0.4.8)

## Triage Outcome

### Stream 2.2.x (scoped stream)

**Already fixed.** Only version 2.2.0 shipped the vulnerable h2 0.4.5. The fix was picked up in version 2.2.1 (h2 bumped to 0.4.8). All current versions (2.2.1--2.2.4) ship h2 >= 0.4.8 and are not affected.

- **Affects Versions correction**: RHTPA 2.2.0 is confirmed affected (matches PSIRT assignment). No additional versions to add or remove for the 2.2.x stream.
- **No remediation tasks needed** for the 2.2.x stream -- the fix is already present in current builds.

### Stream 2.1.x (cross-stream impact -- Case B)

**All versions affected.** Both 2.1.0 and 2.1.1 ship h2 0.4.5, which is within the affected range (< 0.4.8). No version in the 2.1.x stream includes the fix.

Since the issue TC-8030 is scoped to [rhtpa-2.2], the 2.1.x stream falls under **Case B: Cross-stream impact**. Preemptive remediation tasks are created for the 2.1.x stream with the `security-preemptive` label and "Related" link type to the originating CVE Jira.

## Cross-Stream Impact Comment

The following comment would be posted to TC-8030:

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis. Both 2.1.0 and 2.1.1 ship h2 0.4.5 (vulnerable). This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

## Remediation Task Descriptions

Since h2 is a **Cargo** (source dependency) ecosystem package, **two tasks** are created per affected stream: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport (2.1.x stream -- preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030 (originating CVE Jira, scoped to 2.2.x)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (v0.3.8, h2 0.4.5), 2.1.1 (v0.3.12, h2 0.4.5)
Source commits: v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

#### Repository

backend

#### Target Branch

release/0.3.z

#### Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

##### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

#### Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

#### Test Requirements

- [ ] Existing test suite passes with the updated dependency

#### Dependencies

- Related to: TC-8030 (originating CVE Jira)

---

### Task 2: Downstream Propagation (2.1.x stream -- preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030; Blocked by upstream backport task (Task 1)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

#### Repository

rhtpa-release.0.3.z

#### Target Branch

main

#### Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

#### Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

#### Test Requirements

- [ ] Container image builds successfully with the updated reference

#### Dependencies

- Blocked by: upstream backport task (Task 1, upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira)

---

## Post-Triage Summary

### Actions for TC-8030 (scoped to 2.2.x)

1. **Affects Versions**: Confirmed RHTPA 2.2.0 is correctly set (only 2.2.0 is affected in 2.2.x)
2. **2.2.x stream**: Already fixed in 2.2.1+ (h2 bumped to 0.4.8). No remediation tasks needed for this stream.
3. **Cross-stream impact**: 2.1.x stream is fully affected (h2 0.4.5 in all versions). Two preemptive remediation tasks created with `security-preemptive` label and "Related" link type.
4. **Label**: Add `ai-cve-triaged` to TC-8030

### Version Impact Table (summary)

| Stream | Affected Versions | Fix Status |
|--------|-------------------|------------|
| 2.2.x  | 2.2.0 only        | Fixed in 2.2.1+ |
| 2.1.x  | 2.1.0, 2.1.1 (all)| Not fixed -- preemptive remediation tasks created |
