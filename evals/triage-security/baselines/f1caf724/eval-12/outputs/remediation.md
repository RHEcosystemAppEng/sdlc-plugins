# Step 8 -- Remediation

## Triage Outcome

### Scoped Stream (2.2.x): Case C -- No Supported Versions Affected

The version impact table shows NO for all versions in the scoped stream (2.2.x). All five versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

**Proposed actions** (pending engineer confirmation):
1. Add comment: "No supported versions in the 2.2.x stream ship a vulnerable version of h2. Version impact analysis shows all versions ship h2 0.4.8 or 0.4.9, which is at or above the fix threshold (0.4.8). The affected range (< 0.4.8) does not apply to any 2.2.x release."
2. Transition TC-8030 to Closed with resolution "Not a Bug"
3. Set VEX Justification (customfield_12345) to **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not included in any 2.2.x release
4. Add label `ai-cve-triaged`

### Cross-Stream Impact (2.1.x): Case A -- Proactive Remediation

The cross-stream analysis reveals that the 2.1.x stream IS affected:
- 2.1.0 ships h2 0.4.5 (vulnerable)
- 2.1.1 ships h2 0.4.5 (vulnerable)

Since the 2.1.x stream does not have its own CVE Jira for CVE-2026-48901, create **preemptive remediation tasks** per Case A.

Ecosystem: Cargo (source dependency) -- 2 tasks required for the 2.1.x stream.

---

## Preemptive Remediation Task 1: Upstream Backport (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

**Link type**: Related (to TC-8030, since TC-8030 belongs to a different stream)

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (direct dependency)

The h2 crate is a direct dependency of the backend workspace. Update h2 to >= 0.4.8 in Cargo.toml and run `cargo update -p h2` to update Cargo.lock.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)

---

## Preemptive Remediation Task 2: Downstream Propagation (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

**Link type**: Related (to TC-8030), Blocks (blocked by upstream backport task above)

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)

---

## Post-Triage Summary

After all actions are confirmed and executed:

1. **Add label** `ai-cve-triaged` to TC-8030
2. **Post summary comment** to TC-8030 documenting:
   - Version impact table (all 2.2.x versions NOT affected, all 2.1.x versions affected)
   - Scoped stream (2.2.x): closed as Not a Bug -- VEX Justification: Component not Present
   - Cross-stream impact: 2.1.x stream affected, preemptive remediation tasks created
   - Links to preemptive remediation tasks created (upstream backport + downstream propagation for 2.1.x)
   - @mention of the issue reporter (PSIRT analyst)

### Pre-Creation Checklist

- [x] **Task count per stream**: Cargo is a source dependency ecosystem -- 2 tasks for 2.1.x stream (upstream backport + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x stream has preemptive tasks; no existing sibling CVE Jira for 2.1.x
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8030 (different stream); "Blocks" for upstream to downstream within 2.1.x stream
- [x] **Preemptive labels**: both tasks carry the `security-preemptive` label
- [x] **Coordination guidance**: deployment context not configured in Source Repositories table (no Deployment Context column present) -- coordination guidance subsection omitted
