# Step 8 — Remediation

## Case A: Cross-Stream Impact

The issue is scoped to `[rhtpa-2.2]` but the 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9 < 0.11.14). A cross-stream impact comment would be posted:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks would be created with the `security-preemptive` label.

## Case B: Remediation Tasks for 2.2.x stream

Since this is a Cargo (source dependency) ecosystem, two tasks are created per affected stream.

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 1a: Description Digest Protocol

After creating the upstream backport task:

1. **Re-fetch the description** from Jira: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. **Compute SHA-256 digest** from the re-fetched description (not the description string passed to `create_issue`): `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. **Post digest comment** with the marker `[sdlc-workflow] Description digest: <tagged-digest>` — this comment MUST be posted BEFORE creating issue links (Depend, Blocks) or other comments

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct — carried forward from upstream task
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

### Task 2a: Description Digest Protocol

After creating the downstream propagation subtask:

1. **Re-fetch the description** from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. **Compute SHA-256 digest** from the re-fetched description: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. **Post digest comment** with the marker `[sdlc-workflow] Description digest: <tagged-digest>` — posted BEFORE creating issue links

---

## Jira Linkage

After creating both tasks:

1. Link upstream task to Vulnerability: `jira.create_link(inwardIssue: TC-8001, outwardIssue: <upstream-task-key>, type: "Depend")`
2. Link downstream task to Vulnerability: `jira.create_link(inwardIssue: TC-8001, outwardIssue: <downstream-task-key>, type: "Depend")`
3. Link downstream blocked by upstream: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`
4. Transition TC-8001 to In Progress
5. Add `ai-cve-triaged` label to TC-8001

## Step 7.5 — Release Jira Orchestration

Release orchestration confirmations would be required before creating remediation tasks:

1. **Resolve stream-to-version mapping**: Search for existing release Epic matching `"RHTPA 2.2.* Release Tasks"`. If found, use it. If not, propose the next patch version (e.g., RHTPA 2.2.5) and require explicit engineer confirmation.
2. **Find or create release Task**: Search for `"RHTPA <version> CVE triage"` under the release Epic. Individual confirmation required for creation.
3. **Cross-CVE dedup**: Check if an existing remediation Task linked to the release Task already covers quinn-proto. If so, skip task creation and link the CVE to the existing task instead.

Since this eval prohibits actual Jira calls, the release orchestration confirmations are described as planned procedures. The engineer must interactively confirm the exact release Epic version and child Task creation before proceeding.

## Release Dedup Decision

The Upstream Affected Component custom field is not explicitly configured in this eval's CLAUDE.md (claude-md-security-config-embargo.md does not include `Upstream Affected Component custom field`). When the Upstream Affected Component configuration is absent, Step 7.5.3 cross-CVE dedup is skipped entirely — consistent with Step 4.3's conditional behavior.
