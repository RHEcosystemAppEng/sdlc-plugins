# Step 8 -- Remediation

## Cross-Stream Impact (Case A) -- Not Applicable

Case A is **skipped** for this issue. The guard condition states: "Case A applies
exclusively to stream-scoped issues (those whose summary contains a stream suffix).
Unscoped issues cover all streams by definition -- there are no 'other streams
outside this issue's scope,' so the cross-stream impact check is not applicable."

Since TC-8004 has no stream suffix (unscoped), Case A does not apply. No
cross-stream impact notice is generated. Proceed directly to Case B task creation
for affected streams.

## Case B -- Remediation Tasks (Affected Streams Only)

The version impact table shows:

- **Stream 2.1.x**: AFFECTED (all versions ship h2 0.4.5 < 0.4.8) -- remediation required
- **Stream 2.2.x**: NOT AFFECTED (all versions ship h2 >= 0.4.8) -- no remediation needed

Remediation tasks are created **only for stream 2.1.x**. Stream 2.2.x already
ships the patched version and requires no action.

### Ecosystem Classification

h2 is a **Cargo** dependency (source dependency ecosystem). Per the classification
table, this produces **two tasks** for the affected stream:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

## Task 1: Upstream Backport (Stream 2.1.x)

**Proposed Jira create_issue:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version
(0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (direct dependency)

The vulnerable package h2 is a direct dependency of the backend workspace:

```
backend (workspace) -> h2
```

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update the lock file
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Description Digest (Task 1)

After creating the upstream backport task, perform the description digest protocol:

1. **Re-fetch** the task description from Jira after create_issue:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. **Write** the re-fetched description to a temp file and **compute digest** using
   `scripts/sha256-digest.py`:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a format-tagged digest: `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
3. **Post the digest comment** on the upstream task (BEFORE creating issue links or
   other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Task 2: Downstream Propagation (Stream 2.1.x)

**Proposed Jira create_issue:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Description Digest (Task 2)

After creating the downstream propagation task, perform the description digest protocol:

1. **Re-fetch** the task description from Jira after create_issue:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. **Write** the re-fetched description to a temp file and **compute digest**:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. **Post the digest comment** on the downstream task (BEFORE creating issue links
   or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Jira Linkage (after digest comments)

After creating both tasks and posting digest comments:

1. **Link upstream task to the Vulnerability issue:**
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream task to the Vulnerability issue:**
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream task as blocked by upstream task:**
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Transition** TC-8004 to In Progress (if not already).

5. **Add ai-cve-triaged label** to TC-8004.

## Post-Triage Summary Comment

Post a summary comment on TC-8004:

```
## CVE-2026-33501 Triage Summary

### Version Impact

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.4.5      | YES       | 0.4.5 < 0.4.8 |
| 2.1.1   | 2.1.x  | 0.4.5      | YES       | 0.4.5 < 0.4.8 |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        | fixed version |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        | fixed version |
| 2.2.2   | 2.2.x  | --         | NO        | retag of 2.2.1 |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        | >= 0.4.8 |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        | >= 0.4.8 |

### Affects Versions Correction

[RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

### Triage Outcome

Remediation tasks created for stream 2.1.x (affected).
Stream 2.2.x ships h2 >= 0.4.8 and is not affected -- no remediation needed.

- <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

@<reporter-name> (ADF mention node with reporter account ID from the Jira issue)

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.7.
```

The post-triage summary comment includes an @mention of the vulnerability issue's
reporter using an ADF mention node:
```json
{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
```
This @mention is mandatory and uses the reporter field from the Jira issue data
extracted in Step 1.
