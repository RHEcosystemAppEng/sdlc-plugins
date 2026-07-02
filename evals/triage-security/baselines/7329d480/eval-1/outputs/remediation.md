# Step 8 -- Remediation

## Triage Outcome

- **Case A** applies: the 2.2.x stream (issue scope) has affected versions (2.2.0, 2.2.1, 2.2.2). Create remediation tasks.
- **Case B** also applies: the 2.1.x stream (outside issue scope) is also affected. Create preemptive remediation tasks for the 2.1.x stream.

Ecosystem: **Cargo** (source dependency) -- two tasks per stream: upstream backport + downstream propagation.

---

## Case A: Remediation Tasks for 2.2.x Stream (Issue Scope)

### Task 1: Upstream Backport (2.2.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812

**Description:**

> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
> The vulnerable dependency (quinn-proto < 0.11.14) must be updated
> to the fixed version (0.11.14+).
>
> Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
> Source commit(s): v0.4.5, v0.4.8
>
> Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
> Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
>
> ## Implementation Notes
>
> - Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
> - Target branch: release/0.4.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ### Coordination Guidance
>
> This component is public upstream. Coordinate fix with upstream maintainers
> if the vulnerability is not yet public. Follow your organization's embargo
> policy before discussing in public channels or PRs.
>
> ## Acceptance Criteria
>
> - [ ] quinn-proto dependency is >= 0.11.14
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8001 (parent tracking issue)

**Linkage:**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
```

---

### Task 2: Downstream Propagation (2.2.x)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812

**Description:**

> ## Repository
>
> rhtpa-release.0.4.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-31812 fix from <upstream-task-key>.
>
> The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
> on release/0.4.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: <upstream-task-key> (upstream backport must merge first)
> - Depends on: TC-8001 (parent tracking issue)

**Linkage:**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

---

## Case B: Preemptive Remediation Tasks for 2.1.x Stream (Cross-Stream Impact)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9) but has no stream-specific CVE Jira. Creating preemptive remediation tasks with the `security-preemptive` label.

### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
> The vulnerable dependency (quinn-proto < 0.11.14) must be updated
> to the fixed version (0.11.14+).
>
> Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
> Source commit(s): v0.3.8, v0.3.12
>
> Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
> Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
>
> ## Implementation Notes
>
> - Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
> - Target branch: release/0.3.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
> - NOTE: The upstream branch release/0.3.z does NOT yet have the fix
>   (latest tag v0.3.12 ships quinn-proto 0.11.9). An upstream PR is required first.
>
> ### Coordination Guidance
>
> This component is public upstream. Coordinate fix with upstream maintainers
> if the vulnerability is not yet public. Follow your organization's embargo
> policy before discussing in public channels or PRs.
>
> ## Acceptance Criteria
>
> - [ ] quinn-proto dependency is >= 0.11.14
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8001 (parent tracking issue)

**Linkage** (Related, not Depend -- preemptive task for a different stream):
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-upstream-task-key>, type: "Related")
```

---

### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-release.0.3.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-31812 fix from <preemptive-upstream-task-key>.
>
> The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
> on release/0.3.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
> - Depends on: TC-8001 (parent tracking issue)

**Linkage** (Related, not Depend -- preemptive task for a different stream):
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-downstream-task-key>, type: "Related")
jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")
```

---

## Cross-Stream Impact Comment (proposed for TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. The 2.1.x stream ships quinn-proto 0.11.9
in all supported versions (2.1.0, 2.1.1).

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```
