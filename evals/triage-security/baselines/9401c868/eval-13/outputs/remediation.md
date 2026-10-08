# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

- **Case A** applies: the issue is scoped to 2.2.x, but 2.1.x is also affected (cross-stream impact).
- **Case B** applies: affected versions exist within the scoped 2.2.x stream -- create remediation tasks.
- Ecosystem: **Cargo** (source dependency). Fix is available upstream on `release/0.4.z`. Remediation uses the **dependency bump** variant (2 tasks per stream).
- For the out-of-scope 2.1.x stream, fix is **not** available upstream on `release/0.3.z`. Preemptive remediation uses the **upstream backport** variant (2 tasks).

---

## In-Scope Remediation Tasks (2.2.x stream)

### Task 1: Dependency Bump -- quinn-proto (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct dependency of the backend workspace)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range, pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira link:**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <bump-task-key>,
  type: "Depend"
)
```

#### Description Digest Comment (Task 1)

After creating the dependency bump task, perform the following steps to post the description digest comment:

1. **Fetch the created task's description** from Jira:
   ```
   bump_desc = jira.get_issue(<bump-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the digest** using the sha256-digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

4. **Post the digest comment** on the created task (before creating issue links or other comments):
   ```
   jira.add_comment(<bump-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 3 (e.g., `sha256-md:a1b2c3...64 hex chars`).

---

### Task 2: Downstream Propagation -- rhtpa-release.0.4.z (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <bump-task-key>.

The dependency bump (<bump-task-key>) updates quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira links:**
```
# Link downstream to CVE
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream blocked by upstream bump task
jira.create_link(
  inwardIssue: <bump-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

#### Description Digest Comment (Task 2)

After creating the downstream propagation task, perform the following steps:

1. **Fetch the created task's description** from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the digest** using the sha256-digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment** on the created task (before creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Case A: Cross-Stream Impact -- Preemptive Tasks (2.1.x stream)

The version impact analysis shows that stream 2.1.x (versions 2.1.0 and 2.1.1) is also affected by CVE-2026-31812. Since the current issue TC-8001 is scoped to stream 2.2.x only, the 2.1.x stream is out-of-scope.

**Cross-stream impact comment** to post on TC-8001:
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

Before creating preemptive tasks, search for existing CVE Jiras for stream 2.1.x:
```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001"
)
```

If no sibling CVE Jira exists for stream 2.1.x, create the following preemptive tasks.

Note: For 2.1.x, the upstream branch `release/0.3.z` does NOT ship the fix (latest tag v0.3.12 has quinn-proto 0.11.9). Therefore the **upstream backport** variant is used (not dependency bump).

### Preemptive Task 3: Upstream Backport -- quinn-proto (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct dependency of the backend workspace)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira link (Related, not Depend -- preemptive task):**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

#### Description Digest Comment (Preemptive Task 3)

After creating the preemptive upstream backport task, perform the following steps:

1. **Fetch the created task's description** from Jira:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the digest** using the sha256-digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment** on the created task (before creating issue links or other comments):
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Preemptive Task 4: Downstream Propagation -- rhtpa-release.0.3.z (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira links:**
```
# Link preemptive downstream to originating CVE (Related, not Depend)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link preemptive downstream blocked by preemptive upstream
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

#### Description Digest Comment (Preemptive Task 4)

After creating the preemptive downstream propagation task, perform the following steps:

1. **Fetch the created task's description** from Jira:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the digest** using the sha256-digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment** on the created task (before creating issue links or other comments):
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Preemptive Tasks Comment on TC-8001

After creating the preemptive tasks, post a comment on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <preemptive-downstream-task-key> (downstream propagation, security-preemptive, blocked by <preemptive-upstream-task-key>)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump + downstream propagation); 2.1.x has 2 preemptive tasks (upstream backport + downstream propagation). Matches the ecosystem classification table (Cargo = source dependency = 2 tasks).
- [x] **Cross-stream coverage**: 2.1.x (out-of-scope) covered by preemptive tasks (no existing sibling CVE Jira found).
- [x] **Link types**: "Depend" for in-scope tasks linked to TC-8001; "Related" for preemptive tasks linked to TC-8001; "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes upstream deployment context guidance.
- [x] **Release Jira linking**: Would be performed after Step 7.5 (not shown here as release Jira orchestration depends on Jira API calls).
- [x] **Dedup consistency**: No dedup detected (Step 7.5.3 not applicable without Jira access).

## Post-Triage Summary

After all triage actions complete:

1. Add the `ai-cve-triaged` label to TC-8001.
2. Post a summary comment on TC-8001 documenting:
   - Version impact table
   - Affects Versions correction: `[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: Remediation tasks created for 2.2.x (dependency bump + downstream); preemptive tasks created for 2.1.x (upstream backport + downstream)
   - Links to all remediation tasks
   - @mention of the vulnerability issue reporter
