# Step 8 -- Remediation for CVE-2026-31812

## Case A: Affected versions in scoped stream (2.2.x)

Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Since the ecosystem is **Cargo** (source dependency), two tasks are created: an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml/Cargo.lock

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

### Description Digest Protocol for Upstream Task

After `create_issue` returns the new task key (e.g., TC-XXXX), perform the following steps **before** creating any issue links or other comments:

1. **Re-fetch the task description from Jira** -- the description must be re-fetched from the Jira API after creation because Jira normalizes content during storage. Do NOT compute the digest from the description string passed to `create_issue`.

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute SHA-256 digest** using `scripts/sha256-digest.py`:

   ```
   # Write the re-fetched description to a temp file
   # (content comes from the Jira API response, not the original input string)
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

   The script auto-detects the input format (ADF JSON vs markdown) and outputs a format-tagged digest.

3. **Post the digest comment on the upstream task** with the exact marker prefix `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

4. **Only after the digest comment is posted**, proceed to create issue links:

   ```
   # Link upstream task to CVE Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Task 2: Downstream Propagation Subtask

### Proposed Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
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
- **Dependency type**: direct -- carried forward from upstream task
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

### Description Digest Protocol for Downstream Task

After `create_issue` returns the new downstream task key (e.g., TC-YYYY), perform the following steps **before** creating any issue links or other comments:

1. **Re-fetch the task description from Jira** -- the description must be re-fetched from the Jira API after creation because Jira normalizes content during storage. Do NOT compute the digest from the description string passed to `create_issue`.

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute SHA-256 digest** using `scripts/sha256-digest.py`:

   ```
   # Write the re-fetched description to a temp file
   # (content comes from the Jira API response, not the original input string)
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment on the downstream task** with the exact marker prefix `[sdlc-workflow] Description digest:`:

   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-adf:e4f5a6...64chars`).

4. **Only after the digest comment is posted**, proceed to create issue links:

   ```
   # Link downstream task to CVE Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )

   # Link downstream task as blocked by upstream task
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Sequence Summary

The full procedure for both tasks follows this exact order:

1. Create upstream backport task via `jira.create_issue`
2. Re-fetch upstream task description via `jira.get_issue` (from Jira API, not the input string)
3. Compute upstream digest via `scripts/sha256-digest.py`
4. Post upstream digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
5. Create downstream propagation task via `jira.create_issue`
6. Re-fetch downstream task description via `jira.get_issue` (from Jira API, not the input string)
7. Compute downstream digest via `scripts/sha256-digest.py`
8. Post downstream digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
9. Create Depend link: TC-8001 -> upstream task
10. Create Depend link: TC-8001 -> downstream task
11. Create Blocks link: upstream task -> downstream task
12. Transition TC-8001 to In Progress
13. Add `ai-cve-triaged` label to TC-8001
14. Post summary comment on TC-8001

Digest comments are posted **before** issue links (Depend, Blocks) or other comments on each task. This is mandatory per `shared/description-digest-protocol.md` Rules.

---

## Post-Triage Summary

**Proposed** summary comment on TC-8001 (includes Comment Footnote):

> Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14).
>
> Version impact: 2.2.0 (YES), 2.2.1 (YES), 2.2.2 (YES, retag), 2.2.3 (NO), 2.2.4 (NO)
>
> Affects Versions corrected: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
>
> Remediation tasks created:
> - <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14)
> - <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
>
> @reporter-mention (ADF mention node with reporter account ID)
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.12.3.
