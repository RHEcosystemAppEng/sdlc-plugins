# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

- **Case B** (2.2.x stream -- in scope): Affected versions 2.2.0, 2.2.1, 2.2.2 require remediation. Upstream fix is available on `release/0.4.z` (v0.4.11+ ships quinn-proto 0.11.14), so the **dependency bump** variant applies.
- **Case A** (2.1.x stream -- cross-stream impact): All 2.1.x versions are affected. No sibling CVE Jira exists for 2.1.x. Preemptive remediation tasks are created with the `security-preemptive` label. Upstream fix is NOT available on `release/0.3.z`, so the **upstream backport** variant applies.

---

## Task 1: Dependency Bump -- quinn-proto (2.2.x stream)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link to CVE**: TC-8001 (Depend)

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) is already fixed
upstream -- a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of v0.4.8)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

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

### Description Digest Comment (Task 1)

After creating the task, perform the following steps to post the description digest:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<task-1-key>, fields=["description"])
   ```

2. Write the description to a temp file and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

3. Post the digest as a standalone comment on the task (before creating any links or other comments):
   ```
   jira.add_comment(<task-1-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `sha256-digest.py`.

4. After the digest comment is posted, create the issue link:
   ```
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: <task-1-key>,
     type: "Depend"
   )
   ```

---

## Task 2: Downstream Propagation -- rhtpa-release.0.4.z (2.2.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link to CVE**: TC-8001 (Depend)
**Blocked by**: Task 1 (Blocks)

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812
fix from <task-1-key>.

The dependency bump (<task-1-key>) updates quinn-proto to 0.11.14 on
release/0.4.z. Once that PR merges, update the source pinning in this Konflux
release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <task-1-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (Task 2)

After creating the task, perform the following steps to post the description digest:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<task-2-key>, fields=["description"])
   ```

2. Write the description to a temp file and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. Post the digest as a standalone comment on the task (before creating any links or other comments):
   ```
   jira.add_comment(<task-2-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. After the digest comment is posted, create the issue links:
   ```
   # Link downstream task to CVE
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: <task-2-key>,
     type: "Depend"
   )

   # Link downstream task as blocked by upstream bump task
   jira.create_link(
     inwardIssue: <task-1-key>,
     outwardIssue: <task-2-key>,
     type: "Blocks"
   )
   ```

---

## Task 3 (Preemptive): Upstream Backport -- quinn-proto (2.1.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link to CVE**: TC-8001 (Related -- preemptive, different stream)

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- The upstream branch release/0.3.z does NOT yet ship the fix (latest tag
  v0.3.12 ships quinn-proto 0.11.9) -- an upstream backport is required
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (Task 3)

After creating the task, perform the following steps to post the description digest:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<task-3-key>, fields=["description"])
   ```

2. Write the description to a temp file and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. Post the digest as a standalone comment on the task (before creating any links or other comments):
   ```
   jira.add_comment(<task-3-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. After the digest comment is posted, create the issue link (Related, not Depend, because this is a preemptive task linked to a different stream's CVE):
   ```
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: <task-3-key>,
     type: "Related"
   )
   ```

---

## Task 4 (Preemptive): Downstream Propagation -- rhtpa-release.0.3.z (2.1.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link to CVE**: TC-8001 (Related -- preemptive, different stream)
**Blocked by**: Task 3 (Blocks)

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812
fix from <task-3-key>.

The upstream backport (<task-3-key>) bumps quinn-proto to 0.11.14 on
release/0.3.z. Once that PR merges, update the source pinning in this Konflux
release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <task-3-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (Task 4)

After creating the task, perform the following steps to post the description digest:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<task-4-key>, fields=["description"])
   ```

2. Write the description to a temp file and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. Post the digest as a standalone comment on the task (before creating any links or other comments):
   ```
   jira.add_comment(<task-4-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. After the digest comment is posted, create the issue links:
   ```
   # Link preemptive downstream task to CVE (Related, not Depend)
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: <task-4-key>,
     type: "Related"
   )

   # Link downstream task as blocked by upstream backport task
   jira.create_link(
     inwardIssue: <task-3-key>,
     outwardIssue: <task-4-key>,
     type: "Blocks"
   )
   ```

---

## Cross-Stream Impact Comment (posted to TC-8001)

After creating the preemptive tasks, a cross-stream impact comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <task-3-key> (upstream backport, security-preemptive), <task-4-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates a stream-specific CVE Jira for 2.1.x, Step 4.4 reconciliation
will link them and remove the label.
```

## Post-Triage Summary Comment (posted to TC-8001)

After all triage actions are complete, a summary comment would be posted:

```
## Triage Summary: CVE-2026-31812 (quinn-proto)

### Version Impact

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | 0.11.14 | NO | |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Corrected: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

### Triage Outcome

Remediation required. Created tasks:

**2.2.x stream (in scope):**
- <task-1-key>: dependency bump -- update quinn-proto to 0.11.14 (release/0.4.z)
- <task-2-key>: downstream propagation -- update backend ref in rhtpa-release.0.4.z (blocked by <task-1-key>)

**2.1.x stream (preemptive -- no CVE Jira for this stream):**
- <task-3-key>: upstream backport -- bump quinn-proto to 0.11.14 (release/0.3.z, security-preemptive)
- <task-4-key>: downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by <task-3-key>, security-preemptive)

@<reporter-account-id> (reporter mention)

---
This comment was AI-generated by sdlc-workflow/triage-security v<version>.
```

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8001
2. Transition TC-8001 to In Progress
