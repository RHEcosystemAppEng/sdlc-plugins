# Step 8 -- Remediation for CVE-2026-31812

## Triage Outcome Summary

- **Issue scope**: 2.2.x stream (`[rhtpa-2.2]`)
- **2.2.x stream**: Versions 2.2.0, 2.2.1, 2.2.2 are affected. Fix already shipped in 2.2.3+ (quinn-proto 0.11.14). Upstream branch `release/0.4.z` already has the fix. **No new remediation tasks needed.**
- **2.1.x stream**: All versions affected (2.1.0, 2.1.1). Fix NOT on upstream branch `release/0.3.z`. **Preemptive remediation tasks needed** (Case A -- cross-stream impact).

## Case A: Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

Since no existing CVE Jira was found for CVE-2026-31812 in the 2.1.x stream, preemptive remediation tasks are created below.

---

## Preemptive Remediation Tasks for 2.1.x Stream

Ecosystem: Cargo (source dependency) -- 2 tasks required per stream.

### Task 1: Upstream Backport (Preemptive)

**Jira creation call:**

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment for Task 1

After creating the upstream backport task, the following steps are performed to post the description digest comment:

1. **Re-fetch the description** from Jira (do not hash the input string -- Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file**:
   ```
   # Write the fetched description content to /tmp/task-desc.md
   ```

3. **Compute the digest** using the script:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the format of the fetched description.

4. **Post the digest comment** on the upstream task (before creating any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from the script (e.g., `sha256-md:a1b2c3...64 hex chars`).

5. **Link the task** to the originating CVE Jira with "Related" (preemptive link type):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Related"
   )
   ```

---

### Task 2: Downstream Propagation (Preemptive)

**Jira creation call:**

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment for Task 2

After creating the downstream propagation task, the following steps are performed to post the description digest comment:

1. **Re-fetch the description** from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file**:
   ```
   # Write the fetched description content to /tmp/task-desc.md
   ```

3. **Compute the digest** using the script:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

4. **Post the digest comment** on the downstream task (before creating any links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from the script (e.g., `sha256-adf:e4f5a6...64 hex chars`).

5. **Link the downstream task** to the originating CVE Jira with "Related" (preemptive link type):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Related"
   )
   ```

6. **Link the downstream task as blocked by the upstream task**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Preemptive Task Summary Comment on TC-8001

After creating both preemptive tasks, post a comment on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive, blocked by <upstream-task-key>)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## 2.2.x Stream -- No Remediation Tasks Needed

The 2.2.x stream (in-scope for TC-8001) does not require new remediation tasks because:

1. The fix (quinn-proto 0.11.14) is already present on the upstream branch `release/0.4.z` since build tag v0.4.11
2. Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship the fixed version
3. Affects Versions are corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 to reflect which released versions were affected

The Vulnerability issue TC-8001 remains open with corrected Affects Versions. The `ai-cve-triaged` label is added to mark it as triaged.

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.1.x gets 2 tasks (source dependency -- upstream backport + downstream propagation). 2.2.x gets 0 tasks (fix already shipped).
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks. No existing sibling CVE Jira for 2.1.x.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001 (originating CVE from a different stream). "Blocks" for upstream -> downstream within the 2.1.x stream.
- [x] **Preemptive labels**: Both tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes upstream deployment context guidance (default -- no Deployment Context column present in Source Repositories table).
- [x] **Description digest**: Each task gets a description digest comment posted immediately after creation, before any links or other comments.

## Post-Triage Actions

1. **Add `ai-cve-triaged` label** to TC-8001
2. **Post summary comment** to TC-8001 documenting:
   - Version impact table (all streams)
   - Affects Versions correction (RHTPA 2.0.0 removed, RHTPA 2.2.0/2.2.1/2.2.2 added)
   - Triage outcome: 2.2.x already fixed in 2.2.3+, preemptive remediation created for 2.1.x
   - Links to preemptive tasks created
   - @mention of the vulnerability issue's reporter
