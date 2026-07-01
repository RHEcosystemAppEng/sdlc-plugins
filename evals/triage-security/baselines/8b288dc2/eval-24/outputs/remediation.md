# Step 8 -- Remediation: TC-8001

## Triage Outcome: Case A -- Affected (with Case B cross-stream impact)

Stream 2.2.x has affected versions (2.2.0, 2.2.1, 2.2.2). Ecosystem is Cargo (source dependency), so two remediation tasks are created: an upstream backport task and a downstream propagation subtask.

Stream 2.1.x is also affected (cross-stream, Case B) but is outside this issue's scope. A cross-stream impact comment would be posted, and if no sibling CVE Jira exists for 2.1.x, preemptive remediation tasks would be created for that stream.

---

## Remediation Task 1: Upstream Backport (stream 2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (stream 2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage (proposed)

1. Link upstream backport task to TC-8001 with type "Depend"
2. Link downstream propagation task to TC-8001 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"
4. Transition TC-8001 to In Progress
5. Assign TC-8001 to current user
6. Add ai-cve-triaged label to TC-8001

## Cross-Stream Impact Comment (Case B)

Post to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. All versions in stream 2.1.x (2.1.0, 2.1.1) ship quinn-proto 0.11.9. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks would be created with the `security-preemptive` label and "Related" link type to TC-8001.
