# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

- **Case A (2.2.x stream)**: Affected versions exist (2.2.0, 2.2.1, 2.2.2), but the fix is already present in the latest releases (2.2.3, 2.2.4) and upstream branch `release/0.4.z`. Create remediation tasks to formally track the fix.
- **Case B (2.1.x cross-stream)**: The 2.1.x stream is also affected (2.1.0, 2.1.1) and does NOT have the fix upstream. Since no stream-specific CVE Jira exists for 2.1.x, create preemptive remediation tasks.

---

## Case A -- 2.2.x Stream Remediation Tasks

Since the fix is already present upstream on `release/0.4.z` (v0.4.11+) and in the latest downstream releases (2.2.3, 2.2.4), the upstream backport task documents the existing fix. The downstream propagation subtask confirms the fix is already propagated.

### Task 1: Upstream Backport Task (2.2.x)

**Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
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
- Note: upstream branch release/0.4.z already has quinn-proto 0.11.14
  as of tag v0.4.11. Verify the fix is present at branch HEAD.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment Steps (Task 1):

1. Re-fetch the created task's description from Jira:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file:
   ```
   # Write description to /tmp/task-desc.md
   ```
3. Compute the SHA-256 digest using the digest script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a tagged digest, e.g. `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
4. Post the digest comment to the task (before creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. Link the upstream task to the Vulnerability issue:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Jira API call:**
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
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment Steps (Task 2):

1. Re-fetch the created task's description from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file:
   ```
   # Write description to /tmp/task-desc.md
   ```
3. Compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest comment to the task (before creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. Link the downstream task to the upstream task (Blocks):
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```
6. Link the downstream task to the Vulnerability issue (Depend):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

---

## Case B -- 2.1.x Cross-Stream Preemptive Remediation Tasks

The version impact analysis reveals that the 2.1.x stream (versions 2.1.0, 2.1.1) is also affected. No stream-specific CVE Jira exists for 2.1.x (no sibling issue with suffix `[rhtpa-2.1]` found). Therefore, preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

### Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. The 2.1.x stream ships quinn-proto 0.11.9
in versions 2.1.0 and 2.1.1. This stream does not have a companion CVE
Jira -- preemptive remediation tasks have been created.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.12.1.
```

### Task 3: Preemptive Upstream Backport Task (2.1.x)

**Jira API call:**
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

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: upstream branch release/0.3.z currently has quinn-proto 0.11.9.
  An upstream PR is required to bump the dependency before downstream
  propagation.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment Steps (Task 3):

1. Re-fetch the created task's description from Jira:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file:
   ```
   # Write description to /tmp/task-desc.md
   ```
3. Compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest comment to the task (before creating issue links or other comments):
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. Link the preemptive task to the originating CVE with "Related" (not "Depend"):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <preemptive-upstream-task-key>,
     type: "Related"
   )
   ```

---

### Task 4: Preemptive Downstream Propagation Subtask (2.1.x)

**Jira API call:**
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
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment Steps (Task 4):

1. Re-fetch the created task's description from Jira:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file:
   ```
   # Write description to /tmp/task-desc.md
   ```
3. Compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest comment to the task (before creating issue links or other comments):
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. Link the preemptive downstream task to the preemptive upstream task (Blocks):
   ```
   jira.create_link(
     inwardIssue: <preemptive-upstream-task-key>,
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Blocks"
   )
   ```
6. Link the preemptive downstream task to the originating CVE with "Related":
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Related"
   )
   ```

---

## Preemptive Tasks Summary Comment

The following comment would be posted to TC-8001 after preemptive task creation:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <preemptive-downstream-task-key> (downstream propagation, security-preemptive, blocked by <preemptive-upstream-task-key>)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
This comment was AI-generated by sdlc-workflow/triage-security v0.12.1.
```

---

## Post-Triage Summary

After all triage actions are complete, the following would be performed:

1. **Add `ai-cve-triaged` label** to TC-8001.

2. **Post summary comment** to TC-8001:

```
## CVE-2026-31812 Triage Summary

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= fix version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= fix version |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

### Triage Outcome

**Case A (2.2.x)**: Remediation tasks created:
- <upstream-task-key> (upstream backport on release/0.4.z)
- <downstream-task-key> (downstream propagation in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

**Case B (2.1.x cross-stream)**: Preemptive remediation tasks created:
- <preemptive-upstream-task-key> (upstream backport on release/0.3.z, security-preemptive)
- <preemptive-downstream-task-key> (downstream propagation in rhtpa-release.0.3.z, security-preemptive)

@<reporter-name> (reporter @mention via ADF mention node)

---
This comment was AI-generated by sdlc-workflow/triage-security v0.12.1.
```
