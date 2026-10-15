# Step 8 -- Remediation

## Step 7.5 -- Release Jira Orchestration (proposed)

Before creating remediation tasks, the release Jira structure would be resolved for each affected stream. This is described as a proposed procedure since the eval prohibits external calls.

**For stream 2.2.x:**
- Search for existing release Epic matching `"RHTPA 2.2.* Release Tasks"`.
- If found, reuse it; if not, propose creation after confirming the version with the engineer.
- Search for release Task `"RHTPA <version> CVE triage"` under the Epic.
- If found, reuse it; if not, propose creation after engineer confirmation.

**For stream 2.1.x (preemptive):**
- Preemptive tasks for streams without their own CVE Jira are also linked to the release Jira when available.

Release Jira orchestration confirmation and dedup decisions are pending -- they require interactive engineer confirmation for the exact release Epic version and separate child Task creation. Since release evidence and confirmation are unavailable in this eval, this is reported as pending work rather than claiming creation.

## Step 7.5.3 -- Cross-CVE Dedup Check

The Upstream Affected Component custom field is configured (customfield_10632). Dedup check is skipped because there is no existing release Task to inspect for covering remediation tasks. No prior remediation for tokio exists in the release scope. Proceed to standard remediation task creation.

---

## Case A: Cross-Stream Impact -- Standard Remediation for Current Stream (rhtpa-2.2)

Since the issue is scoped to stream [rhtpa-2.2] and versions 2.2.0, 2.2.1, and 2.2.2 are affected, standard remediation tasks are created for this stream.

Ecosystem: **Cargo** (source dependency) -- creates **two tasks** per stream.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Proposed Jira issue creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `['ai-generated-jira', 'Security', 'CVE-2026-55123']`

**Task description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update tokio dependency to >= 1.42.0 in Cargo.toml
- Run `cargo update -p tokio` to pull in the latest compatible version
- Verify Cargo.lock reflects tokio >= 1.42.0 after the update
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

**Post-creation linkage (proposed):**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: "<upstream-task-key>",
  type: "Depend"
)
```

**Description digest (proposed procedure):**

1. After `create_issue`, re-fetch the task description from Jira: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links (Depend, Blocks) or other comments

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Proposed Jira issue creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `['ai-generated-jira', 'Security', 'CVE-2026-55123']`

**Task description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Post-creation linkage (proposed):**

```
# Link downstream to CVE
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: "<downstream-task-key>",
  type: "Depend"
)

# Link upstream blocks downstream
jira.create_link(
  inwardIssue: "<upstream-task-key>",
  outwardIssue: "<downstream-task-key>",
  type: "Blocks"
)
```

**Description digest (proposed procedure):**

1. After `create_issue`, re-fetch the task description from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links (Depend, Blocks) or other comments

---

## Case B: Cross-Stream Proactive Remediation for Stream rhtpa-2.1

Stream rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira** -- no sibling Vulnerability issue exists for CVE-2026-55123 in that stream. Per Step 8 Case A, proactive preemptive remediation tasks are created for this stream.

Ecosystem: **Cargo** (source dependency) -- creates **two preemptive tasks**.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Proposed Jira issue creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `['ai-generated-jira', 'Security', 'CVE-2026-55123', 'security-preemptive']`

**Task description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update tokio dependency to >= 1.42.0 in Cargo.toml
- Run `cargo update -p tokio` to pull in the latest compatible version
- Verify Cargo.lock reflects tokio >= 1.42.0 after the update
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)
```

**Post-creation linkage (proposed):**

Preemptive tasks are linked with **Related** (not Depend) to the originating CVE because the originating CVE belongs to a different stream:

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: "<preemptive-upstream-task-key>",
  type: "Related"
)
```

**Description digest (proposed procedure):**

1. After `create_issue`, re-fetch the task description from Jira: `jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links or other comments

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Proposed Jira issue creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `['ai-generated-jira', 'Security', 'CVE-2026-55123', 'security-preemptive']`

**Task description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)
```

**Post-creation linkage (proposed):**

```
# Link downstream preemptive to originating CVE (Related, not Depend)
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: "<preemptive-downstream-task-key>",
  type: "Related"
)

# Link upstream blocks downstream (within preemptive pair)
jira.create_link(
  inwardIssue: "<preemptive-upstream-task-key>",
  outwardIssue: "<preemptive-downstream-task-key>",
  type: "Blocks"
)
```

**Description digest (proposed procedure):**

1. After `create_issue`, re-fetch the task description from Jira: `jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links or other comments

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -> 2 tasks per stream. 2.2.x gets 2 standard tasks, 2.1.x gets 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: Stream 2.1.x has no CVE Jira -> preemptive tasks created with `security-preemptive` label.
- [x] **Link types**: "Depend" for standard tasks linked to their own CVE Jira (TC-8020), "Related" for preemptive tasks linked to another stream's CVE Jira (TC-8020), "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: Tasks for stream 2.1.x (without its own CVE Jira) carry the `security-preemptive` label.
- [x] **Coordination guidance**: No Deployment Context column in Source Repositories table -- subsection omitted (backward compatibility).
- [x] **Release Jira linking**: Pending -- release Jira orchestration requires interactive confirmation.
- [x] **Dedup consistency**: No dedup detected -- no prior remediation for tokio in release scope.

## Post-Triage Summary (proposed)

After all remediation tasks are created, the following post-triage actions are proposed:

1. **Add `ai-cve-triaged` label** to TC-8020
2. **Transition TC-8020 to In Progress** (if not already)
3. **Post summary comment** to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (if any)
   - Remediation tasks created (standard for 2.2.x, preemptive for 2.1.x)
   - Cross-stream impact notice
   - @mention of the vulnerability issue's reporter using ADF mention node
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.10."
