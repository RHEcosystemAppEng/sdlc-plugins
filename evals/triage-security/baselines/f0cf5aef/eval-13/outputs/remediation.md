# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

### Stream 2.2.x (issue scope)

The fix is already present in versions 2.2.3 and 2.2.4 (quinn-proto 0.11.14).
No remediation tasks needed for this stream. The upstream branch `release/0.4.z`
already contains the fix. Affects Versions correction captures the historical
impact (2.2.0, 2.2.1, 2.2.2).

### Stream 2.1.x (cross-stream impact -- Case A)

All versions in stream 2.1.x (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is
within the vulnerable range (< 0.11.14). The upstream branch `release/0.3.z` does
NOT contain the fix. No stream-specific CVE Jira exists for 2.1.x.

**Action**: Create preemptive remediation tasks for stream 2.1.x using the
security-preemptive variant. Since quinn-proto is a Cargo (source dependency)
ecosystem, create 2 tasks: upstream backport + downstream propagation.

---

## Remediation Task 1: Upstream Backport (2.1.x)

### Jira Creation Call

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or transitive -- to be confirmed via dependency chain analysis)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

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

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol -- Upstream Task

After creating the upstream task, perform the following steps to post the
description digest comment. This MUST be done BEFORE creating issue links
or any other comments on the task.

**Step 1: Re-fetch the description from Jira.**

The description passed to `create_issue` may be normalized by Jira during storage.
Always re-fetch to get the canonical form:

```
upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
```

**Step 2: Write the description to a temp file.**

Write the returned description content (markdown or ADF JSON, depending on the
API access method) to a temporary file:

```
# Write the re-fetched description to a temp file
# (the content from jira.get_issue response's description field)
write /tmp/task-desc.md <re-fetched description content>
```

**Step 3: Compute the SHA-256 digest using the script.**

```bash
python3 scripts/sha256-digest.py /tmp/task-desc.md
```

The script auto-detects the input format:
- ADF JSON input produces: `sha256-adf:<64-char-hex-digest>`
- Markdown text input produces: `sha256-md:<64-char-hex-digest>`

Check exit code -- non-zero means an error (e.g., empty input).

**Step 4: Post the digest comment on the upstream task.**

Post a comment with the exact marker prefix `[sdlc-workflow] Description digest:`
followed by the tagged digest output from the script:

```
jira.add_comment(<upstream-task-key>,
  "[sdlc-workflow] Description digest: <tagged-digest>")
```

For example:
```
jira.add_comment(<upstream-task-key>,
  "[sdlc-workflow] Description digest: sha256-md:a3f7b2c1d4e5...64 hex chars total")
```

The comment must be exactly one line containing the marker and full tagged digest.
Do not append explanations, timestamps, or metadata. Do not abbreviate the hash.
Do not use placeholder text.

**Step 5: ONLY AFTER the digest comment is posted, create issue links.**

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)
```

Note: Link type is "Related" (not "Depend") because this is a preemptive task
linked to another stream's CVE Jira.

---

## Remediation Task 2: Downstream Propagation (2.1.x)

### Jira Creation Call

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description below>,
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
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct or transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
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
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol -- Downstream Task

After creating the downstream task, perform the following steps to post the
description digest comment. This MUST be done BEFORE creating issue links
or any other comments on the task.

**Step 1: Re-fetch the description from Jira.**

```
downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
```

**Step 2: Write the description to a temp file.**

```
write /tmp/task-desc.md <re-fetched description content>
```

**Step 3: Compute the SHA-256 digest using the script.**

```bash
python3 scripts/sha256-digest.py /tmp/task-desc.md
```

The script auto-detects the input format and outputs a format-tagged digest
(e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

**Step 4: Post the digest comment on the downstream task.**

```
jira.add_comment(<downstream-task-key>,
  "[sdlc-workflow] Description digest: <tagged-digest>")
```

The comment must be exactly one line: the marker prefix followed by the full
tagged digest from the script output. Do not use placeholder text, abbreviated
hashes, or example hashes.

**Step 5: ONLY AFTER the digest comment is posted, create issue links.**

```
# Link downstream task to the originating CVE (Related, preemptive)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Related"
)

# Link downstream task as blocked by the upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Post-Task-Creation Actions

After both tasks are created with their digest comments and links:

### 1. Post preemptive tasks comment on TC-8001

```
jira.add_comment("TC-8001",
  "Preemptive remediation tasks created for streams without CVE Jiras:
  - 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
  - 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive, blocked by <upstream-task-key>)

  These tasks use the \"Related\" link type and carry the security-preemptive
  label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
  reconciliation will link them and remove the label.")
```

### 2. Add ai-cve-triaged label to TC-8001

```
jira.edit_issue("TC-8001", labels=["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"])
```

### 3. Post triage summary comment on TC-8001

Post a summary comment documenting:
1. The version impact table (all versions across both streams)
2. The Affects Versions correction (removed RHTPA 2.0.0, added RHTPA 2.2.0/2.2.1/2.2.2)
3. Triage outcome: stream 2.2.x already fixed in 2.2.3+; stream 2.1.x requires preemptive remediation
4. Links to preemptive remediation tasks created for 2.1.x
5. @mention of the Vulnerability issue reporter

This comment MUST include the Comment Footnote per `shared/comment-footnote.md`
with skill name `triage-security`.

## Summary of Digest Protocol for Both Tasks

For BOTH the upstream and downstream remediation tasks, the description digest
protocol follows this exact sequence:

1. **Create the task** via `jira.create_issue(...)`
2. **Re-fetch the description** via `jira.get_issue(<task-key>, fields=["description"])`
   -- do NOT hash the description string passed to `create_issue`, because Jira
   normalizes content during storage
3. **Write the re-fetched description** to a temp file (e.g., `/tmp/task-desc.md`)
4. **Compute the digest** via `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   -- produces a format-tagged digest like `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`
5. **Post the digest comment** via `jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
   -- marker prefix is exactly `[sdlc-workflow] Description digest:`
   -- the tagged digest includes the format tag (do not strip it)
   -- the comment is a standalone single-line comment
6. **THEN create issue links** via `jira.create_link(...)` -- links must come AFTER the digest comment
7. **THEN post any other comments** -- the digest comment must be the first comment on the task
