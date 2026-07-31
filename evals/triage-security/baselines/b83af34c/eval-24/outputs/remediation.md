# Step 8 -- Remediation

## Triage Outcome: Case B (Affected) + Case A (Cross-Stream Impact)

The issue is scoped to stream **2.2.x**. In-scope versions 2.2.0, 2.2.1, and 2.2.2
are affected. Cross-stream analysis shows 2.1.x is also affected (Case A).

Ecosystem: **Cargo** (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation).

---

## Case A: Cross-Stream Impact

Stream 2.1.x (versions 2.1.0, 2.1.1) is also affected by CVE-2026-31812.
Cross-stream impact comment would be posted on TC-8001. Preemptive remediation
tasks would be created for stream 2.1.x with `security-preemptive` label and
"Related" link type.

---

## Case B: Remediation Tasks for Stream 2.2.x (In-Scope)

### Task 1: Upstream Backport (Stream 2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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

### Task 2: Downstream Propagation (Stream 2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Preemptive Tasks for Stream 2.1.x (Case A -- Cross-Stream)

### Preemptive Task 1: Upstream Backport (Stream 2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link type**: Related (to TC-8001, originating CVE)

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue, Related link)

---

### Preemptive Task 2: Downstream Propagation (Stream 2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link type**: Related (to TC-8001, originating CVE)

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the preemptive upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue, Related link)

---

## Deployment Context and Coordination Guidance -- ABSENT

**NOTE**: The Source Repositories table in the project CLAUDE.md does NOT include a
Deployment Context column. Per SKILL.md Step 0 backward compatibility rule, all
repositories default to deployment context `upstream`. However, per
remediation-templates.md Coordination Guidance section: "When the Deployment Context
column is absent from the Source Repositories table (backward compatibility), omit
the coordination guidance entirely -- do not add the subsection."

Therefore, **no Coordination Guidance subsection is included** in any of the
remediation task descriptions above. This is the correct behavior per the skill
specification -- the subsection is omitted entirely, not populated with upstream
defaults.

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation). Stream 2.2.x: 2 tasks. Stream 2.1.x: 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: Stream 2.1.x (outside issue scope) has preemptive tasks created (no existing sibling CVE Jira found).
- [x] **Link types**: "Depend" for tasks linked to TC-8001 (in-scope stream 2.2.x), "Related" for preemptive tasks (stream 2.1.x), "Blocks" for upstream-to-downstream within each stream.
- [x] **Preemptive labels**: Stream 2.1.x tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: OMITTED -- no Deployment Context column in Source Repositories table (backward compatibility).
