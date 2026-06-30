# Step 7 -- Remediation for TC-8001

## Triage Outcome

**Case A + Case B**: The 2.2.x stream (in scope) has affected versions (2.2.0, 2.2.1, 2.2.2), so remediation tasks are needed. The 2.1.x stream (out of scope) is also affected, triggering cross-stream impact handling.

quinn-proto is a **Cargo** (source dependency) ecosystem, so each affected stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A: Remediation Tasks for 2.2.x Stream (In Scope)

### Task 1: Upstream Backport Task (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
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
- Note: tags v0.4.11 and v0.4.12 on release/0.4.z already ship quinn-proto 0.11.14, so the fix is already present at branch HEAD. This task may only require a downstream propagation to cut a new release for 2.2.0/2.2.1/2.2.2.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

#### Description Digest Comment for Task 1

After creating the upstream backport task, the following steps would be performed to post the description digest comment:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file (`/tmp/task-desc.md`).
3. Compute the digest using the script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
4. Post the digest as a standalone Jira comment on the upstream task (before creating any issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `sha256-digest.py`.

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
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

---

#### Description Digest Comment for Task 2

After creating the downstream propagation subtask, the following steps would be performed:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file (`/tmp/task-desc.md`).
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone Jira comment on the downstream task (before creating any issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Jira Linkage for 2.2.x Tasks

After both tasks are created and their digest comments posted:

1. Link upstream task to the Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```
2. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```
3. Link downstream task to the Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

---

## Case B: Cross-Stream Impact -- Preemptive Remediation for 2.1.x Stream

The version impact analysis reveals that the **2.1.x stream** (outside the scope of TC-8001) is also affected: all versions (2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which is within the vulnerable range (< 0.11.14).

### Cross-Stream Impact Comment

The following comment would be posted on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.
```

### Preemptive Task 1: Upstream Backport Task (2.1.x -- preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

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

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
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
- Note: the upstream branch release/0.3.z does NOT yet carry the fix (quinn-proto is still at 0.11.9 at the latest tag v0.3.12). An upstream PR is required to bump the dependency on this branch before downstream propagation.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

#### Description Digest Comment for Preemptive Task 1

After creating the preemptive upstream backport task:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file (`/tmp/task-desc.md`).
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone Jira comment (before creating any issue links or other comments):
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Preemptive Task 2: Downstream Propagation Subtask (2.1.x -- preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

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
CVE-2026-31812 fix from the preemptive upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
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

---

#### Description Digest Comment for Preemptive Task 2

After creating the preemptive downstream propagation subtask:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```
2. Write the description content to a temporary file (`/tmp/task-desc.md`).
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone Jira comment (before creating any issue links or other comments):
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Preemptive Task Linkage for 2.1.x

After both preemptive tasks are created and their digest comments posted:

1. Link preemptive upstream task to the originating CVE Jira with "Related" (not "Depend"):
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-upstream-task-key>, type: "Related")
   ```
2. Link preemptive downstream subtask as blocked by the preemptive upstream task:
   ```
   jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")
   ```
3. Link preemptive downstream task to the originating CVE Jira with "Related":
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-downstream-task-key>, type: "Related")
   ```

### Preemptive Tasks Comment on TC-8001

The following comment would be posted on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (security-preemptive), <preemptive-downstream-task-key> (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

After all triage actions are complete:

1. **Add `ai-cve-triaged` label** to TC-8001.
2. **Post a summary comment** on TC-8001 documenting:
   - The version impact table (all versions across all streams)
   - The Affects Versions correction: `[RHTPA 2.0.0]` changed to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: remediation tasks created for 2.2.x (upstream + downstream); preemptive remediation tasks created for 2.1.x (upstream + downstream)
   - Links to all remediation tasks
   - @mention of the Vulnerability issue's reporter (using their account ID from the Jira issue data)
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.11.0."
3. **Transition** TC-8001 to In Progress.
4. **Assign** TC-8001 to the current user.
