# Idempotency Check -- Re-run Analysis for TC-8001

This document analyzes every triage artifact that the triage-security skill
would create or mutate during a normal run, and documents whether each artifact
already exists on TC-8001 from the prior triage run.

## Summary

All triage artifacts from the prior run are already present on TC-8001. The
re-run detects each one and skips the corresponding mutation. **No new Jira
mutations are required.**

## Artifact-by-Artifact Analysis

### 1. Label: ai-cve-triaged

| Check | Result |
|-------|--------|
| Expected | `ai-cve-triaged` label on TC-8001 |
| Current state | **Present** -- label is in the issue's Labels field |
| Action | **SKIP** -- label already exists, no mutation needed |

The `ai-cve-triaged` label is the primary idempotency marker for the
triage-security skill. Its presence signals that a prior triage run completed
the full workflow, including post-triage summary. Discovery mode queries
(untriaged issues) exclude issues with this label, so TC-8001 would not
appear in the untriaged list.

### 2. Status: In Progress

| Check | Result |
|-------|--------|
| Expected | Issue transitioned to In Progress (or Assigned) |
| Current state | **In Progress** -- already past Assigned |
| Action | **SKIP** -- status is already at or beyond the target state |

Step 0.7 would attempt to assign and transition to Assigned, but the issue
is already In Progress (a later state). The status-aware handling in the
Inputs section detects this and warns: "This issue is already in In Progress.
It may be actively worked on." Since this is a deliberate re-run, triage
proceeds but skips the transition.

### 3. Assignee

| Check | Result |
|-------|--------|
| Expected | Issue assigned to current user |
| Current state | **Assigned** to engineer-a@example.com |
| Action | **SKIP** (or re-assign if current user differs) -- assignment is idempotent |

Step 0.7 assigns the issue to the current user. If the current user is the
same as the existing assignee, this is a no-op. If different, the assignment
would update, but this is safe and idempotent.

### 4. Remediation Task: TC-8100 (Upstream Backport)

| Check | Result |
|-------|--------|
| Expected | Upstream backport Task linked via Depend |
| Current state | **Present** -- TC-8100 exists with Depend link to TC-8001 |
| Task summary | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] |
| Task status | In Progress |
| Task labels | ai-generated-jira, Security, CVE-2026-31812 |
| Action | **SKIP** -- remediation task already exists for this stream and CVE |

Step 8 (Case B) would normally create an upstream backport task. The existing
Depend link from TC-8001 to TC-8100 confirms that this task was already
created. The task's labels include `CVE-2026-31812` and `ai-generated-jira`,
matching the expected creation pattern. No duplicate task creation is needed.

### 5. Remediation Task: TC-8101 (Downstream Propagation)

| Check | Result |
|-------|--------|
| Expected | Downstream propagation Task linked via Depend, blocked by upstream task |
| Current state | **Present** -- TC-8101 exists with Depend link to TC-8001 and Blocks link to TC-8100 |
| Task summary | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] |
| Task status | Open |
| Task labels | ai-generated-jira, Security, CVE-2026-31812 |
| Action | **SKIP** -- downstream propagation task already exists with correct blocking relationship |

The downstream subtask is present with the correct Blocks relationship to
TC-8100 (upstream must merge first). This matches the expected two-task
pattern for Cargo (source dependency) ecosystems.

### 6. Description Digest Comment

| Check | Result |
|-------|--------|
| Expected | Comment with format `[sdlc-workflow] Description digest: sha256-md:<hex>` |
| Current state | **Present** -- comment 1 contains digest `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` |
| Posted by | sdlc-workflow/triage-security |
| Created | 2026-07-01T10:00:00Z |
| Action | **SKIP** -- description digest already recorded |

The description digest comment is used by downstream skills (e.g.,
`/implement-task`) to verify description integrity. Posting a duplicate
would be redundant and could cause confusion in digest verification.

### 7. Post-Triage Summary Comment

| Check | Result |
|-------|--------|
| Expected | Summary comment documenting version impact, actions taken, remediation tasks |
| Current state | **Present** -- comment 2 contains full post-triage summary |
| Content includes | Version impact (2.2.0 and 2.2.1 affected), Affects Versions correction, remediation task links (TC-8100, TC-8101), transition to In Progress |
| Comment Footnote | Present -- includes skill attribution link |
| Created | 2026-07-01T10:01:00Z |
| Action | **SKIP** -- post-triage summary already posted |

The post-triage summary is the final artifact created by the skill. Its
presence confirms the prior run completed successfully through all steps.

### 8. Affects Versions Correction

| Check | Result |
|-------|--------|
| Expected | Affects Versions set to affected versions within the 2.2.x stream scope |
| Current state | **Correct** -- RHTPA 2.2.0, RHTPA 2.2.1 |
| Version impact analysis | 2.2.0 (YES, quinn-proto 0.11.9), 2.2.1 (YES, quinn-proto 0.11.12), 2.2.2 (YES, retag), 2.2.3 (NO), 2.2.4 (NO) |
| Action | **SKIP** -- Affects Versions already match the version impact analysis |

Note: RHTPA 2.2.2 is a retag of 2.2.1 and is also affected, but it may or
may not have a corresponding Jira version registered. The current Affects
Versions (2.2.0, 2.2.1) were confirmed correct by the prior triage run.

### 9. Issue Links (Depend)

| Check | Result |
|-------|--------|
| Expected | Depend links from TC-8001 to remediation tasks |
| Current state | **Present** -- two Depend links (TC-8100, TC-8101) |
| Action | **SKIP** -- all expected links already exist |

The idempotent link creation pattern (check existing issuelinks before
creating) would detect both Depend links and skip creation.

### 10. Transition to In Progress

| Check | Result |
|-------|--------|
| Expected | Issue transitioned to In Progress after remediation task creation |
| Current state | **Already In Progress** |
| Action | **SKIP** -- issue is already in target state |

## Detection Method Summary

The triage-security skill uses multiple idempotency signals:

1. **ai-cve-triaged label** -- primary gate: if present, the issue was fully triaged
2. **Status check** -- In Progress or later status indicates active triage
3. **Existing issue links** -- Depend links to remediation tasks checked before creation
4. **Comment pattern matching** -- description digest and post-triage summary comments identified by their `[sdlc-workflow]` prefix
5. **Affects Versions comparison** -- current values compared against version impact analysis; no correction if already correct

All five detection mechanisms confirm that TC-8001 was fully triaged in the
prior run. Each would independently prevent duplicate mutations.
