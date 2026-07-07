# Step 8 -- Remediation

## Triage Outcome

### Scoped stream (2.2.x)

The issue is scoped to stream 2.2.x via the summary suffix `[rhtpa-2.2]`. Within this stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected (quinn-proto < 0.11.14), but versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version). The upstream branch `release/0.4.z` already includes the fix. No remediation task is needed for the 2.2.x stream -- the fix was picked up organically.

Affects Versions correction: Remove `RHTPA 2.0.0` (invalid), add `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`.

### Cross-stream impact (Case B)

Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9). The issue is scoped to 2.2.x, so this triggers Case B: cross-stream impact with preemptive remediation. No sibling CVE Jira exists for stream 2.1.x, so preemptive remediation tasks are created.

#### Cross-stream impact comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x ships quinn-proto 0.11.9
in all versions (2.1.0, 2.1.1). This stream may require separate
PSIRT triage or is covered by the preemptive remediation tasks below.
```

---

## Preemptive Remediation Tasks for Stream 2.1.x

Since quinn-proto is a Cargo (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask. Both carry the `security-preemptive` label.

---

### Task 1: Upstream Backport Task (2.1.x, preemptive)

#### Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Task Description

```markdown
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
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
- Run `cargo update -p quinn-proto` to update Cargo.lock
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
```

#### Description Digest Comment Steps

After creating the upstream backport task (assume it receives key `TC-XXXX`):

1. **Re-fetch the task description from Jira** (do NOT use the description string passed to `create_issue` -- Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue("TC-XXXX", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute SHA-256 digest**:
   ```bash
   # Write re-fetched description to temp file
   # (the description text from the Jira API response)
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> or sha256-adf:<64-char-hex-digest>
   ```

3. **Post the digest comment** (BEFORE any issue links or other comments):
   ```
   jira.add_comment("TC-XXXX", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars...`).

4. **THEN create issue links** (sequenced AFTER the digest comment):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-XXXX",
     type: "Related"
   )
   ```
   Note: Link type is "Related" (not "Depend") because this is a preemptive task linked to a CVE from a different stream.

---

### Task 2: Downstream Propagation Subtask (2.1.x, preemptive)

#### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Task Description

```markdown
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from TC-XXXX.

The upstream backport (TC-XXXX) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: TC-XXXX (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment Steps

After creating the downstream propagation subtask (assume it receives key `TC-YYYY`):

1. **Re-fetch the task description from Jira** (do NOT use the description string passed to `create_issue` -- Jira normalizes content during storage):
   ```
   downstream_desc = jira.get_issue("TC-YYYY", fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute SHA-256 digest**:
   ```bash
   # Write re-fetched description to temp file
   # (the description text from the Jira API response)
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> or sha256-adf:<64-char-hex-digest>
   ```

3. **Post the digest comment** (BEFORE any issue links or other comments):
   ```
   jira.add_comment("TC-YYYY", "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:e5f6a7...64chars...`).

4. **THEN create issue links** (sequenced AFTER the digest comment):
   ```
   # Link downstream subtask as blocked by the upstream task
   jira.create_link(
     inwardIssue: "TC-XXXX",
     outwardIssue: "TC-YYYY",
     type: "Blocks"
   )

   # Link downstream subtask to originating CVE (Related, since preemptive)
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-YYYY",
     type: "Related"
   )
   ```

---

## Complete Sequencing of Jira Mutations

The full sequence of Jira operations after engineer confirmation:

### Phase 1: Create upstream backport task
1. `jira.create_issue(...)` -- creates TC-XXXX (upstream backport task for 2.1.x)
2. `jira.get_issue("TC-XXXX", fields=["description"])` -- re-fetch description
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest
4. `jira.add_comment("TC-XXXX", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex>")` -- post digest comment
5. `jira.create_link(inward: "TC-8001", outward: "TC-XXXX", type: "Related")` -- link to CVE (Related, preemptive)

### Phase 2: Create downstream propagation subtask
6. `jira.create_issue(...)` -- creates TC-YYYY (downstream propagation subtask for 2.1.x)
7. `jira.get_issue("TC-YYYY", fields=["description"])` -- re-fetch description
8. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest
9. `jira.add_comment("TC-YYYY", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex>")` -- post digest comment
10. `jira.create_link(inward: "TC-XXXX", outward: "TC-YYYY", type: "Blocks")` -- blocked by upstream task
11. `jira.create_link(inward: "TC-8001", outward: "TC-YYYY", type: "Related")` -- link to CVE (Related, preemptive)

### Phase 3: Post-creation comments on originating CVE
12. `jira.add_comment("TC-8001", <cross-stream impact comment>)` -- cross-stream notice
13. `jira.add_comment("TC-8001", <preemptive tasks comment>)` -- list preemptive tasks created

Preemptive tasks comment on TC-8001:
```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-XXXX (upstream backport, security-preemptive), TC-YYYY (downstream propagation, security-preemptive, blocked by TC-XXXX)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

### Phase 4: Post-triage summary
14. `jira.edit_issue("TC-8001", labels: [add "ai-cve-triaged"])` -- mark as triaged
15. `jira.add_comment("TC-8001", <post-triage summary with version impact table, Affects Versions correction, triage outcome, links to remediation tasks, @mention of reporter, and Comment Footnote>)`

All Jira comments include the Comment Footnote (sdlc-workflow/triage-security v0.12.2).

---

## Digest Protocol Key Rules

1. **Always re-fetch** the description from Jira after `create_issue`. Do NOT hash the description string passed to `create_issue` -- Jira normalizes content during storage and the stored version may differ.

2. **Use `scripts/sha256-digest.py`** to compute the digest. Do NOT compute SHA-256 manually. The script auto-detects input format (ADF JSON vs markdown) and outputs a format-tagged digest (`sha256-adf:<hex>` or `sha256-md:<hex>`).

3. **Post digest comment BEFORE issue links or other comments.** The sequencing is: create_issue -> get_issue (re-fetch) -> sha256-digest.py -> add_comment (digest) -> create_link.

4. **Digest comment is a standalone comment.** It is not appended to other comments or the post-triage summary. It is exactly one line: `[sdlc-workflow] Description digest: <tagged-digest>`.

5. **Full 64-character hex digest.** Never use abbreviated hashes, placeholder text, or example hashes.
