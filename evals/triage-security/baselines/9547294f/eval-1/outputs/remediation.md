# Step 8 -- Remediation Task Descriptions for TC-8001

## Triage Outcome: Case A -- Affected, Create Remediation Tasks

The version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream are affected. Remediation tasks are proposed below.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, **two tasks** are created per Important Rule 8:
1. An **upstream backport task** to fix the dependency in the source repository
2. A **downstream propagation subtask** to update the reference in the Konflux release repository, blocked by the upstream task

Additionally, cross-stream impact is noted: the 2.1.x stream (versions 2.1.0, 2.1.1) is also affected. This is documented via a cross-stream impact comment on TC-8001 (Case B), but remediation tasks for 2.1.x are outside this issue's scope and would be handled by a companion CVE issue for that stream.

---

## Task 1: Upstream Backport Task

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z (from Ecosystem Mappings)
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

### Description Digest Protocol for Upstream Task

After creating the upstream backport task, the following digest procedure would be performed:

1. **Re-fetch the description** from Jira after `create_issue` returns:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
   The digest is computed from the **re-fetched** description (as returned by the Jira API after storage), not from the description string passed to `create_issue`. This is critical because Jira normalizes content during storage.

2. **Write the description to a temp file** and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF JSON or markdown) and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** on the newly created upstream task **before** creating any issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

4. **Only after** the digest comment is posted, create the issue links:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira Issue Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Description Digest Protocol for Downstream Task

After creating the downstream propagation subtask, the following digest procedure would be performed:

1. **Re-fetch the description** from Jira after `create_issue` returns:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
   The digest is computed from the **re-fetched** description (as returned by the Jira API after storage), not from the description string passed to `create_issue`.

2. **Write the description to a temp file** and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format and outputs a format-tagged digest.

3. **Post the digest comment** on the downstream task **before** creating any issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Only after** the digest comment is posted, create the issue links:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

## Linkage Summary

After both tasks and their digest comments are created, the following links are established:

1. **Depend**: TC-8001 (Vulnerability) -> <upstream-task-key> (upstream backport)
2. **Depend**: TC-8001 (Vulnerability) -> <downstream-task-key> (downstream propagation)
3. **Blocks**: <upstream-task-key> -> <downstream-task-key> (downstream is blocked by upstream)

The Blocks link ensures the downstream propagation task cannot proceed until the upstream backport merges.

## Cross-Stream Impact Notice (Case B)

The version impact analysis reveals that the **2.1.x stream** (versions 2.1.0 and 2.1.1) is also affected by CVE-2026-31812, but this stream is outside the current issue's scope ([rhtpa-2.2]).

**Proposed comment on TC-8001:**

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis.
> - 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- affected
> - 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- affected
>
> These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

## Post-Triage Summary

**Proposed actions** (all require engineer confirmation before execution):

1. Add label `ai-cve-triaged` to TC-8001
2. Transition TC-8001 to In Progress
3. Assign TC-8001 to current user
4. Post summary comment to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Remediation tasks created: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   - Cross-stream impact notice for 2.1.x stream

All Affects Versions changes, label additions, status transitions, and task creation are presented as **proposals** for engineer review and confirmation. No Jira mutations are executed without explicit approval.
