# Step 8 -- Remediation for TC-8001 (CVE-2026-31812)

## Triage Decision Summary

### Stream 2.2.x (in scope)

The issue is scoped to stream 2.2.x. Versions 2.2.0, 2.2.1, and 2.2.2 are affected (ship quinn-proto < 0.11.14). However, versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version). The upstream branch `release/0.4.z` also ships the fix at HEAD. **No new remediation tasks are needed for the 2.2.x stream** -- the fix is already incorporated.

Affects Versions are corrected to: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

### Stream 2.1.x (Case A -- cross-stream preemptive remediation)

All versions in stream 2.1.x (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the vulnerable range. The upstream branch `release/0.3.z` does NOT have the fix. Since no CVE Jira exists for stream 2.1.x, preemptive remediation tasks are created.

Ecosystem: Cargo (source dependency) -- 2 tasks per stream:
1. Upstream backport task (fix in rhtpa-backend on release/0.3.z)
2. Downstream propagation task (update rhtpa-backend ref in rhtpa-release.0.3.z)

Both tasks carry the `security-preemptive` label and use the "Related" link type to the originating CVE TC-8001.

---

## Preemptive Remediation Task 1: Upstream Backport (Stream 2.1.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

```
## Repository

rhtpa-backend (backend)

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be determined via Cargo.lock inspection (likely direct or transitive via a QUIC-related crate)
- Run `cargo update -p quinn-proto` to pull in quinn-proto >= 0.11.14
- If the update does not resolve to >= 0.11.14 due to semver constraints,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects quinn-proto >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Vulnerability issue, stream 2.2.x)
```

### Description Digest Comment

After creating the upstream backport task, perform the following steps to post the description digest:

1. **Re-fetch the description** from Jira (to get the normalized content after Jira storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   # Write the fetched description to a temp file
   cat > /tmp/task-desc.md << 'EOF'
   <the description content returned by Jira>
   EOF

   # Compute the SHA-256 digest with format tag
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> (or sha256-adf:<64-char-hex> if ADF)
   ```

3. **Post the digest comment** on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<64-char-hex>")
   ```

   The comment is posted using ADF contentFormat:
   ```json
   {
     "type": "doc",
     "version": 1,
     "content": [
       {
         "type": "paragraph",
         "content": [
           {
             "type": "text",
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>"
           }
         ]
       }
     ]
   }
   ```

### Jira Links (after digest comment)

```
# Link preemptive task to originating CVE with "Related" (not "Depend")
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)
```

---

## Preemptive Remediation Task 2: Downstream Propagation (Stream 2.1.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

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
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
  that includes quinn-proto >= 0.11.14
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Vulnerability issue, stream 2.2.x)
```

### Description Digest Comment

After creating the downstream propagation task, perform the following steps:

1. **Re-fetch the description** from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   cat > /tmp/task-desc.md << 'EOF'
   <the description content returned by Jira>
   EOF

   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> (or sha256-adf:<64-char-hex>)
   ```

3. **Post the digest comment** on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<64-char-hex>")
   ```

   ADF format:
   ```json
   {
     "type": "doc",
     "version": 1,
     "content": [
       {
         "type": "paragraph",
         "content": [
           {
             "type": "text",
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>"
           }
         ]
       }
     ]
   }
   ```

### Jira Links (after digest comment)

```
# Link preemptive downstream task to originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Related"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Post-Creation Comment on TC-8001

After creating both preemptive tasks, post a comment on the originating CVE Jira (TC-8001):

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive),
         <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary Comment on TC-8001

After all triage actions are complete, add the `ai-cve-triaged` label and post a summary comment:

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

Summary comment on TC-8001:

```
## CVE-2026-31812 Triage Summary

### Version Impact Table

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.11.14 | NO | fix introduced here |
| 2.2.x | 2.2.4 | 0.11.14 | NO | |

### Affects Versions Correction

RHTPA 2.0.0 (incorrect) -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
(scoped to stream 2.2.x per issue suffix [rhtpa-2.2])

### Triage Outcome

**Stream 2.2.x (in scope)**: Fix already incorporated in versions 2.2.3+
(build 0.4.11 onward ships quinn-proto 0.11.14). No new remediation tasks needed.

**Stream 2.1.x (cross-stream preemptive)**: All versions affected. Preemptive
remediation tasks created:
- <upstream-task-key>: upstream backport -- bump quinn-proto to >= 0.11.14 on
  release/0.3.z (security-preemptive)
- <downstream-task-key>: downstream propagation -- update rhtpa-backend ref in
  rhtpa-release.0.3.z (security-preemptive, blocked by <upstream-task-key>)

---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.
```

The summary comment includes an @mention of the vulnerability issue's reporter (using the reporter's account ID from the Jira issue data) via an ADF mention node. The comment MUST include the Comment Footnote (shown above).
